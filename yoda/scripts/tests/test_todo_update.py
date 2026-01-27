from __future__ import annotations

import frontmatter
import yaml

from .conftest import TEST_DEV, TEST_TODO, cleanup_test_files, run_script


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def test_todo_update_changes_status_and_front_matter() -> None:
    add_result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Test issue", "--description", "Desc"],
    )
    assert add_result.returncode == 0, add_result.stderr

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    issue = todo["issues"][0]

    update_result = run_script(
        "todo_update.py",
        [
            "--dev",
            TEST_DEV,
            "--issue",
            issue["id"],
            "--status",
            "doing",
            "--priority",
            "7",
        ],
    )
    assert update_result.returncode == 0, update_result.stderr

    updated = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    updated_issue = updated["issues"][0]
    assert updated_issue["status"] == "doing"
    assert updated_issue["priority"] == 7

    issue_path = TEST_TODO.parents[1] / "yoda" / "project" / "issues" / f"{issue['id']}-{issue['slug']}.md"
    parsed = frontmatter.load(issue_path)
    assert parsed.metadata["status"] == "doing"
    assert parsed.metadata["priority"] == 7
