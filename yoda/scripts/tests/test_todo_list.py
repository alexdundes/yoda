from __future__ import annotations

import json

from conftest import REPO_ROOT, TEST_DEV, TEST_TODO, TodoFactory, cleanup_test_files, run_script, write_yaml


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def _issue_md_path(issue: dict) -> str:
    return str(
        REPO_ROOT
        / "yoda"
        / "project"
        / "issues"
        / f"{issue['id']}-{issue['slug']}.md"
    )


def _write_issue_md(issue: dict, content: str) -> None:
    path = REPO_ROOT / "yoda" / "project" / "issues" / f"{issue['id']}-{issue['slug']}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_todo_list_default_order_and_pending_in_json() -> None:
    factory = TodoFactory(TEST_DEV)
    issue_a = factory.issue(title="A", status="to-do", priority=5)
    issue_b = factory.issue(title="B", status="to-do", priority=7)
    issue_pending = factory.issue(title="P", status="pending", pending_reason="Wait", priority=5)
    issue_done = factory.issue(title="D", status="done", priority=9)
    issue_dep = factory.issue(title="E", status="to-do", priority=6, depends_on=[issue_a["id"]])
    issues = [issue_a, issue_b, issue_pending, issue_done, issue_dep]
    write_yaml(TEST_TODO, factory.todo(issues))

    result = run_script(
        "todo_list.py",
        ["--dev", TEST_DEV, "--format", "json"],
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    ids = [item["id"] for item in payload["issues"]]
    assert issue_done["id"] not in ids
    assert ids == [issue_b["id"], issue_a["id"], issue_dep["id"], issue_pending["id"]]
    assert "pending_reason" in payload["issues"][0]
    assert "origin" in payload["issues"][0]


def test_todo_list_rejects_removed_tags_flag() -> None:
    factory = TodoFactory(TEST_DEV)
    issue_a = factory.issue(title="A")
    write_yaml(TEST_TODO, factory.todo([issue_a]))

    result = run_script(
        "todo_list.py",
        ["--dev", TEST_DEV, "--tags", "alpha"],
    )
    assert result.returncode == 2
    assert "unrecognized arguments: --tags alpha" in result.stderr


def test_todo_list_rejects_removed_agent_flag() -> None:
    factory = TodoFactory(TEST_DEV)
    issue_a = factory.issue(title="A")
    write_yaml(TEST_TODO, factory.todo([issue_a]))

    result = run_script(
        "todo_list.py",
        ["--dev", TEST_DEV, "--agent", "Codex"],
    )
    assert result.returncode == 2
    assert "unrecognized arguments: --agent Codex" in result.stderr


def test_todo_list_order_by_created_desc() -> None:
    factory = TodoFactory(TEST_DEV)
    issue_a = factory.issue(title="A", created_at="2026-01-01T00:00:00+00:00")
    issue_b = factory.issue(title="B", created_at="2026-02-01T00:00:00+00:00")
    issues = [issue_a, issue_b]
    write_yaml(TEST_TODO, factory.todo(issues))

    result = run_script(
        "todo_list.py",
        ["--dev", TEST_DEV, "--format", "json", "--order", "created-desc"],
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    ids = [item["id"] for item in payload["issues"]]
    assert ids == [issue_b["id"], issue_a["id"]]


def test_todo_list_grep_output_in_md() -> None:
    factory = TodoFactory(TEST_DEV)
    issue_a = factory.issue(title="A", slug="a")
    issue_b = factory.issue(title="B", slug="b")
    issues = [issue_a, issue_b]
    write_yaml(TEST_TODO, factory.todo(issues))

    _write_issue_md(issue_a, "Hello world\nNothing else")
    _write_issue_md(issue_b, "Another line\nHELLO again")

    result = run_script(
        "todo_list.py",
        ["--dev", TEST_DEV, "--grep", "hello"],
    )
    assert result.returncode == 0, result.stderr
    assert "##" in result.stdout
    assert "Hello world" in result.stdout
    assert "HELLO again" in result.stdout


def test_todo_list_pending_block_in_md() -> None:
    factory = TodoFactory(TEST_DEV)
    issue_pending = factory.issue(title="P", status="pending", pending_reason="Waiting")
    issue_todo = factory.issue(title="T", status="to-do")
    issues = [issue_pending, issue_todo]
    write_yaml(TEST_TODO, factory.todo(issues))

    result = run_script(
        "todo_list.py",
        ["--dev", TEST_DEV, "--status", "pending,to-do"],
    )
    assert result.returncode == 0, result.stderr
    assert "## Pending issues" in result.stdout
    assert issue_pending["id"] in result.stdout
    assert "Waiting" in result.stdout
    for line in result.stdout.splitlines():
        if line.strip().startswith("|"):
            assert issue_pending["id"] not in line


def test_todo_list_invalid_regex() -> None:
    factory = TodoFactory(TEST_DEV)
    issue_a = factory.issue(title="A")
    write_yaml(TEST_TODO, factory.todo([issue_a]))

    result = run_script(
        "todo_list.py",
        ["--dev", TEST_DEV, "--grep", "["],
    )
    assert result.returncode == 2
    assert "Invalid regex pattern" in result.stderr
