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


def test_flow_next_resumes_doing_issue() -> None:
    _write_issue_file(
        "test-0001-doing.md",
        {
            "schema_version": "1.02",
            "status": "doing",
            "phase": "document",
            "title": "Doing",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Doing\n\n## Flow log\n- 2026-01-01T00:00:00+00:00 | seed | start\n",
    )
    _write_issue_file(
        "test-0002-todo.md",
        {
            "schema_version": "1.02",
            "status": "to-do",
            "title": "Todo",
            "description": "Desc",
            "priority": 10,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Todo\n\n## Flow log\n",
    )

    result = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["issue_id"] == "test-0001"
    assert payload["next_step"] == "document"
    assert payload["blocked_reason"] == ""


def test_flow_next_selects_selectable_issue_and_reports_pending() -> None:
    _write_issue_file(
        "test-0001-done.md",
        {
            "schema_version": "1.02",
            "status": "done",
            "title": "Done",
            "description": "Desc",
            "priority": 1,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Done\n\n## Flow log\n",
    )
    _write_issue_file(
        "test-0002-selectable.md",
        {
            "schema_version": "1.02",
            "status": "to-do",
            "depends_on": ["test-0001"],
            "title": "Selectable",
            "description": "Desc",
            "priority": 7,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Selectable\n\n## Flow log\n",
    )
    _write_issue_file(
        "test-0003-pending.md",
        {
            "schema_version": "1.02",
            "status": "pending",
            "title": "Pending",
            "description": "Desc",
            "priority": 9,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Pending\n\n## Flow log\n",
    )

    result = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["issue_id"] == "test-0002"
    assert payload["next_step"] == "study"
    assert payload["pending"]
    assert payload["pending"][0]["id"] == "test-0003"


def test_flow_next_returns_blocked_reason_dependency_blocked() -> None:
    _write_issue_file(
        "test-0001-pending-a.md",
        {
            "schema_version": "1.02",
            "status": "pending",
            "title": "A",
            "description": "Desc",
            "priority": 3,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# A\n\n## Flow log\n",
    )
    path_blocked = _write_issue_file(
        "test-0002-todo-b.md",
        {
            "schema_version": "1.02",
            "status": "to-do",
            "depends_on": ["test-0001"],
            "title": "B",
            "description": "Desc",
            "priority": 7,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# B\n\n## Flow log\n",
    )

    result = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 3, result.stderr
    payload = json.loads(result.stdout)
    assert payload["issue_id"] == ""
    assert payload["blocked_reason"] == "dependency_blocked"
    assert payload["next_step"] == "blocked"
    assert payload["blocked"][0]["id"] == "test-0002"

    # Only pending issues => only_pending_issues
    path_blocked.unlink()
    result_pending = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result_pending.returncode == 3
    payload_pending = json.loads(result_pending.stdout)
    assert payload_pending["blocked_reason"] == "only_pending_issues"
    assert payload_pending["next_step"] == "blocked"


def test_flow_next_output_md_contains_runbook_section() -> None:
    _write_issue_file(
        "test-0001-todo.md",
        {
            "schema_version": "1.02",
            "status": "to-do",
            "title": "Todo",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Todo\n\n## Flow log\n",
    )

    result = run_script("yoda_flow_next.py", ["--dev", TEST_DEV])
    assert result.returncode == 0, result.stderr
    assert "Runbook:" in result.stdout
    assert "- Run Study:" in result.stdout


def test_flow_next_does_not_mutate_when_flow_log_missing() -> None:
    path = _write_issue_file(
        "test-0001-todo-no-flow.md",
        {
            "schema_version": "1.02",
            "status": "to-do",
            "title": "Todo",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Todo without flow log\n",
    )
    before = path.read_text(encoding="utf-8")
    result = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 0, result.stderr
    after = path.read_text(encoding="utf-8")
    assert before == after
