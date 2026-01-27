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
        ["--dev", TEST_DEV, "--issue", issue["id"], "--message", "Ping"],
    )
    assert result.returncode == 0, result.stderr

    after = yaml.safe_load(log_path.read_text(encoding="utf-8"))
    assert len(after.get("entries", [])) == before_len + 1
    assert after["entries"][-1]["message"] == "Ping"
