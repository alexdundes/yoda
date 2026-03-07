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


def test_todo_list_default_excludes_done_and_orders_by_priority() -> None:
    _write_issue_file(
        "test-0001-low.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "Low",
            "description": "Desc",
            "priority": 2,
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
    _write_issue_file(
        "test-0003-done.md",
        {
            "schema_version": "2.00",
            "status": "done",
            "title": "Done",
            "description": "Desc",
            "priority": 10,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    result = run_script("todo_list.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    ids = [item["id"] for item in payload["issues"]]
    assert ids == ["test-0002", "test-0001"]


def test_todo_list_filters_status_and_depends_on() -> None:
    _write_issue_file(
        "test-0001-base.md",
        {
            "schema_version": "2.00",
            "status": "done",
            "title": "Base",
            "description": "Desc",
            "priority": 1,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )
    _write_issue_file(
        "test-0002-child.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "depends_on": ["test-0001"],
            "title": "Child",
            "description": "Desc",
            "priority": 5,
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
            "priority": 7,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    result = run_script(
        "todo_list.py",
        ["--dev", TEST_DEV, "--format", "json", "--status", "to-do", "--depends-on", "test-0001"],
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert [item["id"] for item in payload["issues"]] == ["test-0002"]


def test_todo_list_grep_searches_issue_files() -> None:
    _write_issue_file(
        "test-0001-a.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "A",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# A\n\nhello world\n",
    )
    _write_issue_file(
        "test-0002-b.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "B",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# B\n\nanother line\n",
    )

    result = run_script("todo_list.py", ["--dev", TEST_DEV, "--grep", "hello"])
    assert result.returncode == 0, result.stderr
    assert "test-0001" in result.stdout
    assert "hello world" in result.stdout


def test_todo_list_dependency_order_moves_blocked_after_unblocked() -> None:
    _write_issue_file(
        "test-0001-blocked.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "depends_on": ["test-0002"],
            "title": "Blocked",
            "description": "Desc",
            "priority": 9,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )
    _write_issue_file(
        "test-0002-unblocked.md",
        {
            "schema_version": "2.00",
            "status": "to-do",
            "title": "Unblocked",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
    )

    result = run_script("todo_list.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    ids = [item["id"] for item in payload["issues"]]
    assert ids[0] == "test-0002"
    assert ids[1] == "test-0001"


def test_todo_list_empty_backlog_outputs_expected_message() -> None:
    result = run_script("todo_list.py", ["--dev", TEST_DEV])
    assert result.returncode == 0, result.stderr
    assert "No issues to execute. Nothing needs to be done." in result.stdout
