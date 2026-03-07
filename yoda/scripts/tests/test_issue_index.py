from __future__ import annotations

import sys
from pathlib import Path

import pytest

from conftest import REPO_ROOT, cleanup_test_files

sys.path.insert(0, str(REPO_ROOT / "yoda" / "scripts"))
from lib.errors import YodaError
from lib.issue_index import load_issue_index


def _write_issue_file(name: str, front_matter: dict[str, object], body: str = "# Test\n") -> Path:
    path = REPO_ROOT / "yoda" / "project" / "issues" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    for key, value in front_matter.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"- {item}")
        elif isinstance(value, int):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: '{value}'")
    lines.extend(["---", "", body.rstrip("\n"), ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def test_load_issue_index_filters_by_dev_and_derives_id_from_filename() -> None:
    _write_issue_file(
        "test-0001-alpha.md",
        {
            "schema_version": "2.00",
            "id": "WRONG-9999",
            "status": "to-do",
            "title": "Alpha",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )
    _write_issue_file(
        "other-0001-beta.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "Beta",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    index = load_issue_index("test")
    assert len(index["issues"]) == 1
    issue = index["issues"][0]
    assert issue["id"] == "test-0001"
    assert issue["dev"] == "test"
    assert issue["slug"] == "alpha"


def test_load_issue_index_fail_fast_on_invalid_required_field() -> None:
    _write_issue_file(
        "test-0001-invalid.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "Invalid",
            # description missing
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )
    _write_issue_file(
        "test-0002-valid.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "Valid",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    with pytest.raises(YodaError) as exc_info:
        load_issue_index("test")
    assert "invalid or missing 'description'" in str(exc_info.value)


def test_load_issue_index_appends_flow_log_section_when_missing() -> None:
    issue_path = _write_issue_file(
        "test-0001-no-flow-log.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "No flow",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Test\n\n## Entry points\n- x\n",
    )

    index = load_issue_index("test")
    assert index["issues"][0]["flow_log_exists"] is True
    updated = issue_path.read_text(encoding="utf-8")
    assert "## Flow log" in updated


def test_load_issue_index_ignores_phase_when_status_is_not_doing() -> None:
    _write_issue_file(
        "test-0001-phase.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "phase": "implement",
            "title": "Phase",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    index = load_issue_index("test")
    assert index["issues"][0]["phase"] is None


def test_load_issue_index_dependency_rules_and_selectability() -> None:
    _write_issue_file(
        "test-0001-base.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "Base",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )
    _write_issue_file(
        "test-0002-missing-dep.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "depends_on": ["test-9999"],
            "title": "Missing dep",
            "description": "Desc",
            "priority": 6,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )
    _write_issue_file(
        "test-0003-existing-not-done.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "depends_on": ["test-0001"],
            "title": "Blocked dep",
            "description": "Desc",
            "priority": 7,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    index = load_issue_index("test")
    by_id = index["by_id"]
    assert by_id["test-0002"]["selectable"] is True
    assert by_id["test-0003"]["selectable"] is False
    assert by_id["test-0003"]["blocked_by"] == ["test-0001"]


def test_load_issue_index_uses_priority_then_source_order() -> None:
    _write_issue_file(
        "test-0001-low.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "Low",
            "description": "Desc",
            "priority": 1,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )
    _write_issue_file(
        "test-0002-high.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "High",
            "description": "Desc",
            "priority": 9,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    index = load_issue_index("test")
    ordered_ids = [item["id"] for item in index["issues"]]
    assert ordered_ids == ["test-0002", "test-0001"]
