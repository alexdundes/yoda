from __future__ import annotations

import subprocess
import sys

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
    assert "agent" not in issue
    assert issue["id"].startswith(f"{TEST_DEV}-")
    issue_path = f"yoda/project/issues/{issue['id']}-{issue['slug']}.md"
    log_path = f"yoda/logs/{issue['id']}-{issue['slug']}.yaml"

    issue_file = REPO_ROOT / issue_path
    assert issue_file.exists()
    assert (REPO_ROOT / log_path).exists()
    assert "agent:" not in issue_file.read_text(encoding="utf-8")


def test_issue_add_conflict_when_issue_file_exists() -> None:
    issue_path = (
        REPO_ROOT / "yoda" / "project" / "issues" / "test-0001-test-issue.md"
    )
    issue_path.parent.mkdir(parents=True, exist_ok=True)
    issue_path.write_text("placeholder", encoding="utf-8")

    result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Test issue", "--description", "Desc"],
    )
    assert result.returncode == 4, result.stderr
    assert f"Issue file already exists: {issue_path}" in result.stderr


def test_issue_add_sets_origin_from_external_issue() -> None:
    result = run_script(
        "issue_add.py",
        [
            "--dev",
            TEST_DEV,
            "--title",
            "From external",
            "--description",
            "Desc",
            "--extern-issue",
            "123",
            "--origin-system",
            "github",
        ],
    )
    assert result.returncode == 0, result.stderr

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    issue = todo["issues"][0]
    assert issue["origin"]["system"] == "github"
    assert issue["origin"]["external_id"] == "123"


def test_issue_add_rejects_non_numeric_external_issue() -> None:
    result = run_script(
        "issue_add.py",
        [
            "--dev",
            TEST_DEV,
            "--title",
            "From external",
            "--description",
            "Desc",
            "--extern-issue",
            "abc",
        ],
    )
    assert result.returncode == 2
    assert "--extern-issue must be numeric" in result.stderr


def test_issue_add_parallel_creations_generate_unique_ids() -> None:
    script = REPO_ROOT / "yoda" / "scripts" / "issue_add.py"
    cmd_a = [
        sys.executable,
        str(script),
        "--dev",
        TEST_DEV,
        "--title",
        "Concurrent alpha",
        "--description",
        "Desc A",
    ]
    cmd_b = [
        sys.executable,
        str(script),
        "--dev",
        TEST_DEV,
        "--title",
        "Concurrent beta",
        "--description",
        "Desc B",
    ]

    proc_a = subprocess.Popen(cmd_a, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    proc_b = subprocess.Popen(cmd_b, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out_a, err_a = proc_a.communicate()
    out_b, err_b = proc_b.communicate()

    assert proc_a.returncode == 0, f"{err_a}\n{out_a}"
    assert proc_b.returncode == 0, f"{err_b}\n{out_b}"

    todo = yaml.safe_load(TEST_TODO.read_text(encoding="utf-8"))
    ids = [item["id"] for item in todo["issues"]]
    assert len(ids) == 2
    assert len(set(ids)) == 2

    for issue in todo["issues"]:
        issue_file = REPO_ROOT / "yoda" / "project" / "issues" / f"{issue['id']}-{issue['slug']}.md"
        log_file = REPO_ROOT / "yoda" / "logs" / f"{issue['id']}-{issue['slug']}.yaml"
        assert issue_file.exists()
        assert log_file.exists()

    lock_file = REPO_ROOT / "yoda" / "locks" / f"issue_add.{TEST_DEV}.lock"
    assert not lock_file.exists()


def test_issue_add_fails_when_lock_contention_exhausts_retries() -> None:
    lock_file = REPO_ROOT / "yoda" / "locks" / f"issue_add.{TEST_DEV}.lock"
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    lock_file.write_text("locked\n", encoding="utf-8")
    try:
        result = run_script(
            "issue_add.py",
            ["--dev", TEST_DEV, "--title", "Locked issue", "--description", "Desc"],
        )
    finally:
        lock_file.unlink(missing_ok=True)

    assert result.returncode == 4, result.stderr
    assert "Failed to acquire issue_add lock" in result.stderr
