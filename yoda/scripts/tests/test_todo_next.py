from __future__ import annotations

import json
from pathlib import Path

from conftest import REPO_ROOT, TEST_DEV, cleanup_test_files, run_script


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


def test_todo_next_returns_doing_issue_when_exists() -> None:
    _write_issue_file(
        "test-0001-doing.md",
        {
            "schema_version": "2.00",
            "status": "doing",
            "phase": "document",
            "title": "Doing",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )
    _write_issue_file(
        "test-0002-todo.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "Todo",
            "description": "Desc",
            "priority": 9,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    result = run_script("todo_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["issue_id"] == "test-0001"


def test_todo_next_selects_selectable_and_reports_pending_blocked() -> None:
    _write_issue_file(
        "test-0001-done.md",
        {
            "schema_version": "2.00",
            "status": "done",
            "title": "Done",
            "description": "Desc",
            "priority": 1,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )
    _write_issue_file(
        "test-0002-selectable.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "depends_on": ["test-0001"],
            "title": "Selectable",
            "description": "Desc",
            "priority": 7,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )
    _write_issue_file(
        "test-0003-pending.md",
        {
            "schema_version": "2.00",
            "status": "pending",
            "title": "Pending",
            "description": "Desc",
            "priority": 9,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )
    _write_issue_file(
        "test-0004-blocked.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "depends_on": ["test-0003"],
            "title": "Blocked",
            "description": "Desc",
            "priority": 8,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    result = run_script("todo_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["issue_id"] == "test-0002"
    assert payload["pending"][0]["id"] == "test-0003"
    assert payload["blocked"][0]["id"] == "test-0004"


def test_todo_next_not_found_when_no_selectable() -> None:
    _write_issue_file(
        "test-0001-pending.md",
        {
            "schema_version": "2.00",
            "status": "pending",
            "title": "Pending",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    result = run_script("todo_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 3
    payload = json.loads(result.stdout)
    assert payload["issue_id"] == ""
