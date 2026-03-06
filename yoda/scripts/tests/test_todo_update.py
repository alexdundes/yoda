from __future__ import annotations

import frontmatter
import yaml

from conftest import REPO_ROOT, TEST_DEV, TEST_TODO, cleanup_test_files, run_script


def _issue_file_for_id(issue_id: str):
    matches = list((REPO_ROOT / "yoda" / "project" / "issues").glob(f"{issue_id}-*.md"))
    assert len(matches) == 1
    return matches[0]


def _log_file_for_id(issue_id: str):
    matches = list((REPO_ROOT / "yoda" / "logs").glob(f"{issue_id}-*.yaml"))
    assert len(matches) == 1
    return matches[0]


def _front_matter_keys(path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    assert lines and lines[0] == "---"
    end = 1
    while end < len(lines) and lines[end] != "---":
        end += 1
    keys: list[str] = []
    for line in lines[1:end]:
        if not line or line.startswith(" "):
            continue
        if ":" in line:
            keys.append(line.split(":", 1)[0].strip())
    return keys


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

    issue_path = _issue_file_for_id(issue["id"])
    parsed = frontmatter.load(issue_path)
    assert parsed.metadata["status"] == "doing"
    assert parsed.metadata["priority"] == 7
    assert _front_matter_keys(issue_path) == [
        "schema_version",
        "id",
        "status",
        "title",
        "description",
        "priority",
        "created_at",
        "updated_at",
    ]


def test_todo_update_sets_phase_for_doing_and_omits_phase_for_done() -> None:
    add_result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Test issue", "--description", "Desc"],
    )
    assert add_result.returncode == 0, add_result.stderr

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    issue = todo["issues"][0]

    doing_result = run_script(
        "todo_update.py",
        [
            "--dev",
            TEST_DEV,
            "--issue",
            issue["id"],
            "--status",
            "doing",
            "--phase",
            "document",
        ],
    )
    assert doing_result.returncode == 0, doing_result.stderr

    updated_doing = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    updated_issue_doing = updated_doing["issues"][0]
    assert updated_issue_doing["status"] == "doing"
    assert updated_issue_doing["phase"] == "document"

    issue_path = _issue_file_for_id(issue["id"])
    parsed_doing = frontmatter.load(issue_path)
    assert parsed_doing.metadata["status"] == "doing"
    assert parsed_doing.metadata["phase"] == "document"

    done_result = run_script(
        "todo_update.py",
        [
            "--dev",
            TEST_DEV,
            "--issue",
            issue["id"],
            "--status",
            "done",
            "--phase",
            "implement",
        ],
    )
    assert done_result.returncode == 0, done_result.stderr

    updated_done = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    updated_issue_done = updated_done["issues"][0]
    assert updated_issue_done["status"] == "done"
    assert "phase" not in updated_issue_done

    parsed_done = frontmatter.load(issue_path)
    assert parsed_done.metadata["status"] == "done"
    assert "phase" not in parsed_done.metadata


def test_todo_update_rejects_missing_depends_on() -> None:
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
            "--depends-on",
            "test-9999",
        ],
    )
    assert update_result.returncode == 2, update_result.stderr
    assert "depends_on references missing ids" in update_result.stderr


def test_todo_update_updates_extern_issue_file_and_front_matter() -> None:
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
            "--extern-issue-file",
            "../extern_issues/github-2.json",
        ],
    )
    assert update_result.returncode == 0, update_result.stderr

    updated = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    updated_issue = updated["issues"][0]
    assert updated_issue["extern_issue_file"] == "../extern_issues/github-2.json"

    issue_path = _issue_file_for_id(issue["id"])
    parsed = frontmatter.load(issue_path)
    assert parsed.metadata["extern_issue_file"] == "../extern_issues/github-2.json"
    assert _front_matter_keys(issue_path) == [
        "schema_version",
        "id",
        "status",
        "title",
        "description",
        "priority",
        "extern_issue_file",
        "created_at",
        "updated_at",
    ]


def test_todo_update_clear_extern_issue_file_removes_key() -> None:
    add_result = run_script(
        "issue_add.py",
        [
            "--dev",
            TEST_DEV,
            "--title",
            "Test issue",
            "--description",
            "Desc",
            "--extern-issue",
            "2",
        ],
    )
    assert add_result.returncode == 0, add_result.stderr

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    issue = todo["issues"][0]
    assert issue["extern_issue_file"] == "../extern_issues/github-2.json"

    update_result = run_script(
        "todo_update.py",
        [
            "--dev",
            TEST_DEV,
            "--issue",
            issue["id"],
            "--clear-extern-issue-file",
        ],
    )
    assert update_result.returncode == 0, update_result.stderr

    updated = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    updated_issue = updated["issues"][0]
    assert "extern_issue_file" not in updated_issue

    issue_path = _issue_file_for_id(issue["id"])
    parsed = frontmatter.load(issue_path)
    assert "extern_issue_file" not in parsed.metadata


def test_todo_update_updates_extern_issue_file_from_extern_issue(monkeypatch) -> None:
    monkeypatch.setenv("YODA_ORIGIN_URL", "https://github.com/acme/proj.git")
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
            "--extern-issue",
            "2",
        ],
    )
    assert update_result.returncode == 0, update_result.stderr

    updated = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    updated_issue = updated["issues"][0]
    assert updated_issue["extern_issue_file"] == "../extern_issues/github-2.json"

    issue_path = _issue_file_for_id(issue["id"])
    parsed = frontmatter.load(issue_path)
    assert parsed.metadata["extern_issue_file"] == "../extern_issues/github-2.json"


def test_todo_update_rejects_conflicting_extern_issue_file_flags() -> None:
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
            "--extern-issue-file",
            "../extern_issues/github-2.json",
            "--clear-extern-issue-file",
        ],
    )
    assert update_result.returncode == 2
    assert "Use either --extern-issue-file or --clear-extern-issue-file" in update_result.stderr


def test_todo_update_rejects_conflicting_extern_issue_flags() -> None:
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
            "--extern-issue",
            "2",
            "--extern-issue-file",
            "../extern_issues/github-2.json",
        ],
    )
    assert update_result.returncode == 2
    assert "Use either --extern-issue or --extern-issue-file" in update_result.stderr


def test_todo_update_rejects_removed_tags_flags() -> None:
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
            "--tags",
            "alpha",
        ],
    )
    assert update_result.returncode == 2
    assert "unrecognized arguments: --tags alpha" in update_result.stderr

    clear_result = run_script(
        "todo_update.py",
        [
            "--dev",
            TEST_DEV,
            "--issue",
            issue["id"],
            "--clear-tags",
        ],
    )
    assert clear_result.returncode == 2
    assert "unrecognized arguments: --clear-tags" in clear_result.stderr


def test_todo_update_rejects_removed_agent_flag() -> None:
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
            "--agent",
            "Codex",
        ],
    )
    assert update_result.returncode == 2
    assert "unrecognized arguments: --agent Codex" in update_result.stderr


def test_todo_update_preserves_status_pending_reason_depends_order() -> None:
    first = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "First issue", "--description", "Desc"],
    )
    second = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Second issue", "--description", "Desc"],
    )
    assert first.returncode == 0, first.stderr
    assert second.returncode == 0, second.stderr

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    issue = todo["issues"][1]
    blocker = todo["issues"][0]

    update_result = run_script(
        "todo_update.py",
        [
            "--dev",
            TEST_DEV,
            "--issue",
            issue["id"],
            "--status",
            "pending",
            "--pending-reason",
            "Waiting",
            "--depends-on",
            blocker["id"],
        ],
    )
    assert update_result.returncode == 0, update_result.stderr

    issue_path = _issue_file_for_id(issue["id"])
    keys = _front_matter_keys(issue_path)
    assert keys == [
        "schema_version",
        "id",
        "status",
        "pending_reason",
        "depends_on",
        "title",
        "description",
        "priority",
        "created_at",
        "updated_at",
    ]


def test_todo_update_title_change_recalculates_slug_and_renames_files() -> None:
    add_result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Initial title", "--description", "Desc"],
    )
    assert add_result.returncode == 0, add_result.stderr

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    issue = todo["issues"][0]
    old_issue_path = _issue_file_for_id(issue["id"])
    old_log_path = _log_file_for_id(issue["id"])

    update_result = run_script(
        "todo_update.py",
        [
            "--dev",
            TEST_DEV,
            "--issue",
            issue["id"],
            "--title",
            "Renamed title",
        ],
    )
    assert update_result.returncode == 0, update_result.stderr

    new_issue_path = _issue_file_for_id(issue["id"])
    new_log_path = _log_file_for_id(issue["id"])
    assert old_issue_path != new_issue_path
    assert old_log_path != new_log_path
    assert not old_issue_path.exists()
    assert not old_log_path.exists()
    assert new_issue_path.name.endswith("-renamed-title.md")
    assert new_log_path.name.endswith("-renamed-title.yaml")

    updated = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    assert "slug" not in updated["issues"][0]
    assert updated["issues"][0]["title"] == "Renamed title"


def test_todo_update_title_and_slug_override_uses_explicit_slug() -> None:
    add_result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Initial title", "--description", "Desc"],
    )
    assert add_result.returncode == 0, add_result.stderr

    issue_id = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))["issues"][0]["id"]
    update_result = run_script(
        "todo_update.py",
        [
            "--dev",
            TEST_DEV,
            "--issue",
            issue_id,
            "--title",
            "Other title",
            "--slug",
            "manual-slug",
        ],
    )
    assert update_result.returncode == 0, update_result.stderr

    assert _issue_file_for_id(issue_id).name.endswith("-manual-slug.md")
    assert _log_file_for_id(issue_id).name.endswith("-manual-slug.yaml")
