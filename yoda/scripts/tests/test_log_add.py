from __future__ import annotations

import yaml

from conftest import REPO_ROOT, TEST_DEV, TEST_TODO, cleanup_test_files, run_script


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def test_log_add_appends_entry() -> None:
    add_result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Test issue", "--description", "Desc"],
    )
    assert add_result.returncode == 0, add_result.stderr

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    issue = todo["issues"][0]
    log_path = REPO_ROOT / "yoda" / "logs" / f"{issue['id']}-{issue['slug']}.yaml"

    before = yaml.safe_load(log_path.read_text(encoding="utf-8"))
    before_len = len(before.get("entries", []))

    result = run_script(
        "log_add.py",
        [
            "--dev",
            TEST_DEV,
            "--issue",
            issue["id"],
            "--message",
            f"[{issue['id']}] Ping",
        ],
    )
    assert result.returncode == 0, result.stderr

    after = yaml.safe_load(log_path.read_text(encoding="utf-8"))
    assert len(after.get("entries", [])) == before_len + 1
    assert after["entries"][-1]["message"] == f"[{issue['id']}] Ping"


def test_log_add_requires_issue_id_in_message() -> None:
    add_result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Test issue", "--description", "Desc"],
    )
    assert add_result.returncode == 0, add_result.stderr

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    issue = todo["issues"][0]

    result = run_script(
        "log_add.py",
        [
            "--dev",
            TEST_DEV,
            "--issue",
            issue["id"],
            "--message",
            "Ping",
        ],
    )
    assert result.returncode == 2
    assert "Log message must mention the issue id" in result.stderr


def test_log_add_errors_when_issue_file_missing() -> None:
    add_result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Test issue", "--description", "Desc"],
    )
    assert add_result.returncode == 0, add_result.stderr

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    issue = todo["issues"][0]
    issue_path = REPO_ROOT / "yoda" / "project" / "issues" / f"{issue['id']}-{issue['slug']}.md"
    if issue_path.exists():
        issue_path.unlink()

    result = run_script(
        "log_add.py",
        [
            "--dev",
            TEST_DEV,
            "--issue",
            issue["id"],
            "--message",
            f"[{issue['id']}] Ping",
        ],
    )
    assert result.returncode == 3
    assert f"Issue file not found: {issue_path}" in result.stderr
