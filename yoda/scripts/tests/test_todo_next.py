from __future__ import annotations

import json

from .conftest import TEST_DEV, TEST_TODO, TodoFactory, cleanup_test_files, run_script, write_yaml


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def test_todo_next_conflict_when_doing_exists() -> None:
    factory = TodoFactory(TEST_DEV)
    issues = [
        factory.issue(title="Doing issue", status="doing"),
        factory.issue(title="Todo issue", status="to-do"),
    ]
    write_yaml(TEST_TODO, factory.todo(issues))

    result = run_script(
        "todo_next.py",
        ["--dev", TEST_DEV, "--todo", "yoda/todos/TODO.test.yaml", "--format", "json"],
    )
    assert result.returncode == 4
    payload = json.loads(result.stdout)
    assert payload["doing"]


def test_todo_next_selects_highest_priority_and_hints_pending() -> None:
    factory = TodoFactory(TEST_DEV)
    done_issue = factory.issue(title="Done", status="done", priority=1)
    todo_second = factory.issue(title="Second", status="to-do", priority=7)
    todo_first = factory.issue(title="First", status="to-do", priority=5)
    pending_issue = factory.issue(title="Pending", status="pending", pending_reason="Waiting")

    issues = [done_issue, todo_second, todo_first, pending_issue]
    write_yaml(TEST_TODO, factory.todo(issues))

    result = run_script(
        "todo_next.py",
        ["--dev", TEST_DEV, "--todo", "yoda/todos/TODO.test.yaml", "--format", "json"],
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["issue_id"] == todo_second["id"]
    assert payload["pending"]


def test_todo_next_not_found_when_blocked() -> None:
    factory = TodoFactory(TEST_DEV)
    blocker = factory.issue(title="Blocker", status="to-do")
    blocked = factory.issue(
        title="Blocked",
        status="to-do",
        depends_on=[blocker["id"]],
    )
    issues = [blocker, blocked]
    write_yaml(TEST_TODO, factory.todo(issues))

    result = run_script(
        "todo_next.py",
        ["--dev", TEST_DEV, "--todo", "yoda/todos/TODO.test.yaml", "--format", "json"],
    )
    assert result.returncode == 3
    payload = json.loads(result.stdout)
    assert payload["blocked"]
