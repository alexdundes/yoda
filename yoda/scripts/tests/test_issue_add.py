from __future__ import annotations

import yaml

from conftest import REPO_ROOT, TEST_DEV, TEST_TODO, cleanup_test_files, run_script


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def test_issue_add_creates_todo_issue_and_log() -> None:
    result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Test issue", "--description", "Desc"],
    )
    assert result.returncode == 0, result.stderr
    assert TEST_TODO.exists()

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    assert todo["developer_slug"] == TEST_DEV
    assert len(todo["issues"]) == 1

    issue = todo["issues"][0]
    assert issue["id"].startswith(f"{TEST_DEV}-")
    issue_path = f"yoda/project/issues/{issue['id']}-{issue['slug']}.md"
    log_path = f"yoda/logs/{issue['id']}-{issue['slug']}.yaml"

    assert (REPO_ROOT / issue_path).exists()
    assert (REPO_ROOT / log_path).exists()
