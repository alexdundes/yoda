from __future__ import annotations

import subprocess
import sys

import frontmatter

from conftest import REPO_ROOT, TEST_DEV, cleanup_test_files, run_script


def _issue_file(issue_id: str):
    matches = list((REPO_ROOT / "yoda" / "project" / "issues").glob(f"{issue_id}-*.md"))
    assert len(matches) == 1
    return matches[0]


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def test_issue_add_creates_markdown_issue_only() -> None:
    result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Test issue", "--description", "Desc"],
    )
    assert result.returncode == 0, result.stderr
    issue_path = _issue_file("test-0001")
    parsed = frontmatter.load(issue_path)
    assert parsed.metadata["schema_version"] == "2.00"
    assert parsed.metadata["id"] == "test-0001"
    assert parsed.metadata["status"] == "to-do"


def test_issue_add_skips_existing_number_and_creates_next_id() -> None:
    existing = REPO_ROOT / "yoda" / "project" / "issues" / "test-0001-test-issue.md"
    existing.parent.mkdir(parents=True, exist_ok=True)
    existing.write_text("placeholder", encoding="utf-8")

    result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Test issue", "--description", "Desc"],
    )
    assert result.returncode == 0, result.stderr
    _issue_file("test-0002")


def test_issue_add_sets_extern_issue_file_from_external_issue() -> None:
    result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "From external", "--description", "Desc", "--extern-issue", "123"],
    )
    assert result.returncode == 0, result.stderr
    parsed = frontmatter.load(_issue_file("test-0001"))
    assert parsed.metadata["extern_issue_file"].endswith("-123.json")


def test_issue_add_parallel_creations_generate_unique_ids() -> None:
    script = REPO_ROOT / "yoda" / "scripts" / "issue_add.py"
    cmd_a = [sys.executable, str(script), "--dev", TEST_DEV, "--title", "Concurrent alpha", "--description", "A"]
    cmd_b = [sys.executable, str(script), "--dev", TEST_DEV, "--title", "Concurrent beta", "--description", "B"]
    proc_a = subprocess.Popen(cmd_a, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    proc_b = subprocess.Popen(cmd_b, cwd=REPO_ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    out_a, err_a = proc_a.communicate()
    out_b, err_b = proc_b.communicate()
    assert proc_a.returncode == 0, f"{err_a}\n{out_a}"
    assert proc_b.returncode == 0, f"{err_b}\n{out_b}"

    files = sorted((REPO_ROOT / "yoda" / "project" / "issues").glob("test-*.md"))
    ids = [path.stem.split("-")[0] + "-" + path.stem.split("-")[1] for path in files]
    assert ids == ["test-0001", "test-0002"]
