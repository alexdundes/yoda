from __future__ import annotations

from pathlib import Path

from conftest import REPO_ROOT, TEST_DEV, cleanup_test_files, run_script


def _write_issue_file(name: str, include_flow_log: bool = True) -> Path:
    path = REPO_ROOT / "yoda" / "project" / "issues" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "# Test\n\n"
    if include_flow_log:
        body += "## Flow log\n"
    text = (
        "---\n"
        "schema_version: '2.00'\n"
        "id: test-0001\n"
        "status: to-do\n"
        "title: Test\n"
        "description: Desc\n"
        "priority: 5\n"
        "created_at: '2026-01-01T00:00:00+00:00'\n"
        "updated_at: '2026-01-01T00:00:00+00:00'\n"
        "---\n\n"
        f"{body}"
    )
    path.write_text(text, encoding="utf-8")
    return path


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def test_log_add_appends_flow_log_line() -> None:
    issue_path = _write_issue_file("test-0001-test.md", include_flow_log=True)
    result = run_script(
        "log_add.py",
        ["--dev", TEST_DEV, "--issue", "test-0001", "--message", "note"],
    )
    assert result.returncode == 0, result.stderr
    text = issue_path.read_text(encoding="utf-8")
    assert "note" in text
    assert "\n- " in text


def test_log_add_creates_flow_log_section_when_missing() -> None:
    issue_path = _write_issue_file("test-0001-test.md", include_flow_log=False)
    result = run_script(
        "log_add.py",
        ["--dev", TEST_DEV, "--issue", "test-0001", "--message", "created section"],
    )
    assert result.returncode == 0, result.stderr
    text = issue_path.read_text(encoding="utf-8")
    assert "## Flow log" in text
    assert "created section" in text
    assert "\n- " in text
