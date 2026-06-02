from __future__ import annotations

import json
import re
from pathlib import Path

import frontmatter

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


def _read_front_matter(path: Path) -> dict:
    return dict(frontmatter.load(path).metadata)


def _read_flow_log_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^## Flow log\s*$", text)
    assert match is not None
    section = text[match.end() :]
    next_header = re.search(r"(?m)^##\s+", section)
    if next_header:
        section = section[: next_header.start()]
    return [line for line in section.splitlines() if line.strip()]


def _last_log_line(path: Path) -> str:
    lines = _read_flow_log_lines(path)
    assert lines
    return lines[-1]


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def test_prep_flow_requires_explicit_dev_slug() -> None:
    result = run_script("yoda_prep_flow.py", ["--issue", "test-0001"])
    assert result.returncode == 2
    assert "--dev is required" in result.stderr


def test_prep_flow_help_contains_agent_guidance() -> None:
    result = run_script("yoda_prep_flow.py", ["--help"])
    assert result.returncode == 0
    assert "Agent guidance:" in result.stdout


def test_prep_flow_targets_explicit_issue_and_ignores_priority_order() -> None:
    _write_issue_file(
        "test-0001-high-priority.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "High",
            "description": "Desc",
            "priority": 10,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# High\n\n## Flow log\n",
    )
    target = _write_issue_file(
        "test-0002-target.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "Target",
            "description": "Desc",
            "priority": 1,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Target\n\n## Flow log\n",
    )

    result = run_script(
        "yoda_prep_flow.py",
        ["--dev", TEST_DEV, "--issue", "test-0002", "--format", "json"],
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["issue_id"] == "test-0002"
    assert payload["status"] == "to-do"
    assert payload["flow_prepared_until"] == "study"
    assert payload["next_step"] == "study"
    assert payload["runbook_line"].startswith("Run Prep Study:")

    meta = _read_front_matter(target)
    assert meta["status"] == "to-do"
    assert "phase" not in meta
    assert meta["flow_prepared_until"] == "study"
    assert _last_log_line(target).endswith("prep transition prepared_until=none->study")


def test_prep_flow_advances_to_document_and_keeps_issue_todo() -> None:
    target = _write_issue_file(
        "test-0001-target.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "flow_prepared_until": "study",
            "title": "Target",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Target\n\n## Flow log\n",
    )

    result = run_script(
        "yoda_prep_flow.py",
        ["--dev", TEST_DEV, "--issue", "test-0001", "--format", "json"],
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["flow_prepared_until"] == "document"
    assert payload["next_step"] == "document"
    assert payload["runbook_line"].startswith("Run Prep Document:")

    meta = _read_front_matter(target)
    assert meta["status"] == "to-do"
    assert "phase" not in meta
    assert meta["flow_prepared_until"] == "document"
    assert _last_log_line(target).endswith("prep transition prepared_until=study->document")


def test_prep_flow_dry_run_does_not_write() -> None:
    target = _write_issue_file(
        "test-0001-dry-run.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "Dry",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Dry\n\n## Flow log\n",
    )
    before = target.read_text(encoding="utf-8")

    result = run_script(
        "yoda_prep_flow.py",
        ["--dev", TEST_DEV, "--issue", "test-0001", "--dry-run", "--format", "json"],
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["flow_prepared_until"] == "study"
    assert target.read_text(encoding="utf-8") == before
    assert _read_flow_log_lines(target) == []


def test_prep_flow_rejects_done_issue() -> None:
    _write_issue_file(
        "test-0001-done.md",
        {
            "schema_version": "2.00",
            "status": "done",
            "title": "Done",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Done\n\n## Flow log\n",
    )

    result = run_script("yoda_prep_flow.py", ["--dev", TEST_DEV, "--issue", "test-0001"])
    assert result.returncode == 2
    assert "cannot run on done issues" in result.stderr
