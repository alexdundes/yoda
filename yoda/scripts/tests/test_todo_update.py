from __future__ import annotations

import frontmatter

from conftest import REPO_ROOT, TEST_DEV, cleanup_test_files, run_script


def _issue_file_for_id(issue_id: str):
    matches = list((REPO_ROOT / "yoda" / "project" / "issues").glob(f"{issue_id}-*.md"))
    assert len(matches) == 1
    return matches[0]


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def _create_issue() -> str:
    add_result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Test issue", "--description", "Desc"],
    )
    assert add_result.returncode == 0, add_result.stderr
    return "test-0001"


def test_todo_update_changes_status_and_priority() -> None:
    issue_id = _create_issue()
    update_result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", issue_id, "--status", "doing", "--priority", "7"],
    )
    assert update_result.returncode == 0, update_result.stderr
    parsed = frontmatter.load(_issue_file_for_id(issue_id))
    assert parsed.metadata["status"] == "doing"
    assert parsed.metadata["priority"] == 7


def test_todo_update_sets_phase_for_doing_and_omits_for_done() -> None:
    issue_id = _create_issue()
    doing_result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", issue_id, "--status", "doing", "--phase", "document"],
    )
    assert doing_result.returncode == 0, doing_result.stderr
    parsed_doing = frontmatter.load(_issue_file_for_id(issue_id))
    assert parsed_doing.metadata["phase"] == "document"

    done_result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", issue_id, "--status", "done", "--phase", "implement"],
    )
    assert done_result.returncode == 0, done_result.stderr
    parsed_done = frontmatter.load(_issue_file_for_id(issue_id))
    assert parsed_done.metadata["status"] == "done"
    assert "phase" not in parsed_done.metadata


def test_todo_update_title_change_renames_issue_file() -> None:
    issue_id = _create_issue()
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", issue_id, "--title", "Renamed issue"],
    )
    assert result.returncode == 0, result.stderr
    new_path = _issue_file_for_id(issue_id)
    assert "renamed-issue" in new_path.name


def test_todo_update_rejects_invalid_schema_version() -> None:
    issue_id = _create_issue()
    issue_path = _issue_file_for_id(issue_id)
    parsed = frontmatter.load(issue_path)
    parsed.metadata["schema_version"] = "1.02"
    issue_path.write_text(frontmatter.dumps(parsed), encoding="utf-8")

    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", issue_id, "--status", "doing"],
    )
    assert result.returncode == 2
    assert "Run init.py migration first" in result.stderr


def test_todo_update_flow_log_entry_has_no_issue_id_prefix() -> None:
    issue_id = _create_issue()
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", issue_id, "--status", "doing", "--phase", "study"],
    )
    assert result.returncode == 0, result.stderr
    text = _issue_file_for_id(issue_id).read_text(encoding="utf-8")
    assert "todo_update status:" in text
    assert f"{issue_id}: todo_update" not in text
