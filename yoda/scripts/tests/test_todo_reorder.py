from __future__ import annotations

import json

import yaml

from conftest import TEST_DEV, TEST_TODO, TodoFactory, cleanup_test_files, run_script, write_yaml


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def _load_ids() -> list[str]:
    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    return [item["id"] for item in todo["issues"]]


def test_todo_reorder_default_order() -> None:
    factory = TodoFactory(TEST_DEV)
    pending_old = factory.issue(
        title="P1",
        status="pending",
        pending_reason="x",
        updated_at="2026-01-01T00:00:00+00:00",
    )
    pending_new = factory.issue(
        title="P2",
        status="pending",
        pending_reason="y",
        updated_at="2026-02-01T00:00:00+00:00",
    )
    active_a = factory.issue(title="A", status="to-do", priority=5)
    active_b = factory.issue(title="B", status="to-do", priority=7)
    active_dep = factory.issue(title="C", status="to-do", priority=6, depends_on=[active_a["id"]])
    done_old = factory.issue(
        title="D1",
        status="done",
        updated_at="2026-01-01T00:00:00+00:00",
    )
    done_new = factory.issue(
        title="D2",
        status="done",
        updated_at="2026-03-01T00:00:00+00:00",
    )

    issues = [active_a, done_old, pending_new, active_b, pending_old, active_dep, done_new]
    write_yaml(TEST_TODO, factory.todo(issues))

    result = run_script("todo_reorder.py", ["--dev", TEST_DEV])
    assert result.returncode == 0, result.stderr

    ordered = _load_ids()
    assert ordered[:2] == [pending_old["id"], pending_new["id"]]
    assert ordered[-2:] == [done_new["id"], done_old["id"]]
    assert ordered[2:5] == [active_b["id"], active_a["id"], active_dep["id"]]


def test_todo_reorder_prefer_updates_priority() -> None:
    factory = TodoFactory(TEST_DEV)
    issue_a = factory.issue(title="A", status="to-do", priority=4)
    issue_b = factory.issue(title="B", status="to-do", priority=7)
    issues = [issue_a, issue_b]
    write_yaml(TEST_TODO, factory.todo(issues))

    result = run_script(
        "todo_reorder.py",
        ["--dev", TEST_DEV, "--prefer", issue_a["id"], "--over", issue_b["id"], "--format", "json"],
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["priority_updated"] is True

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    updated = {item["id"]: item for item in todo["issues"]}
    assert updated[issue_a["id"]]["priority"] == issue_b["priority"]


def test_todo_reorder_prefer_requires_to_do() -> None:
    factory = TodoFactory(TEST_DEV)
    issue_a = factory.issue(title="A", status="done", priority=4)
    issue_b = factory.issue(title="B", status="to-do", priority=7)
    write_yaml(TEST_TODO, factory.todo([issue_a, issue_b]))

    result = run_script(
        "todo_reorder.py",
        ["--dev", TEST_DEV, "--prefer", issue_a["id"], "--over", issue_b["id"]],
    )
    assert result.returncode == 2


def test_todo_reorder_prefer_rejects_dependency() -> None:
    factory = TodoFactory(TEST_DEV)
    issue_b = factory.issue(title="B", status="to-do", priority=7)
    issue_a = factory.issue(title="A", status="to-do", priority=4, depends_on=[issue_b["id"]])
    write_yaml(TEST_TODO, factory.todo([issue_a, issue_b]))

    result = run_script(
        "todo_reorder.py",
        ["--dev", TEST_DEV, "--prefer", issue_a["id"], "--over", issue_b["id"]],
    )
    assert result.returncode == 2


def test_todo_reorder_dry_run_does_not_write() -> None:
    factory = TodoFactory(TEST_DEV)
    issue_a = factory.issue(title="A", status="to-do", priority=4)
    issue_b = factory.issue(title="B", status="to-do", priority=7)
    write_yaml(TEST_TODO, factory.todo([issue_a, issue_b]))
    before = _load_ids()

    result = run_script(
        "todo_reorder.py",
        ["--dev", TEST_DEV, "--dry-run"],
    )
    assert result.returncode == 0, result.stderr
    after = _load_ids()
    assert before == after
