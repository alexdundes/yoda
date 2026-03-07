from __future__ import annotations

from pathlib import Path

import frontmatter

from conftest import run_script


TEST_DEV = "test"


def _seed_manual(root: Path) -> None:
    manual = root / "yoda" / "yoda.md"
    manual.parent.mkdir(parents=True, exist_ok=True)
    manual.write_text("# Manual\n", encoding="utf-8")


def test_init_creates_structure_without_todo_file(tmp_path: Path) -> None:
    _seed_manual(tmp_path)
    result = run_script("init.py", ["--dev", TEST_DEV, "--root", str(tmp_path)])
    assert result.returncode == 0, result.stderr
    assert (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / "yoda" / "project" / "issues").exists()
    assert not (tmp_path / "yoda" / "todos" / f"TODO.{TEST_DEV}.yaml").exists()


def test_init_migrates_legacy_todo_and_logs_then_removes_legacy_files(tmp_path: Path) -> None:
    _seed_manual(tmp_path)
    todo_path = tmp_path / "yoda" / "todos" / f"TODO.{TEST_DEV}.yaml"
    issue_path = tmp_path / "yoda" / "project" / "issues" / "test-0001-legacy.md"
    log_path = tmp_path / "yoda" / "logs" / "test-0001-legacy.yaml"
    issue_path.parent.mkdir(parents=True, exist_ok=True)
    todo_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    issue_path.write_text(
        "---\n"
        "schema_version: '1.02'\n"
        "id: test-0001\n"
        "status: to-do\n"
        "title: Legacy\n"
        "description: Legacy\n"
        "priority: 5\n"
        "created_at: '2026-01-01T00:00:00+00:00'\n"
        "updated_at: '2026-01-01T00:00:00+00:00'\n"
        "---\n\n# Legacy\n",
        encoding="utf-8",
    )
    todo_path.write_text(
        "schema_version: '1.02'\n"
        "developer_name: Test\n"
        "developer_slug: test\n"
        "timezone: UTC\n"
        "updated_at: '2026-01-01T00:00:00+00:00'\n"
        "issues:\n"
        "- schema_version: '1.02'\n"
        "  id: test-0001\n"
        "  title: Legacy\n"
        "  description: Legacy\n"
        "  status: to-do\n"
        "  priority: 5\n"
        "  depends_on: []\n"
        "  pending_reason: ''\n"
        "  created_at: '2026-01-01T00:00:00+00:00'\n"
        "  updated_at: '2026-01-01T00:00:00+00:00'\n"
        "  extern_issue_file: ''\n",
        encoding="utf-8",
    )
    log_path.write_text(
        "schema_version: '1.0'\n"
        "issue_id: test-0001\n"
        "issue_path: yoda/project/issues/test-0001-legacy.md\n"
        "todo_id: test-0001\n"
        "status: to-do\n"
        "entries:\n"
        "  - timestamp: '2026-01-01T00:00:00+00:00'\n"
        "    message: \"line 1\\nline 2\"\n",
        encoding="utf-8",
    )

    result = run_script("init.py", ["--dev", TEST_DEV, "--root", str(tmp_path)])
    assert result.returncode == 0, result.stderr

    parsed = frontmatter.load(issue_path)
    assert parsed.metadata["schema_version"] == "2.00"
    text = issue_path.read_text(encoding="utf-8")
    assert "## Flow log" in text
    assert "line 1 | line 2" in text
    assert not todo_path.exists()
    assert not log_path.exists()


def test_init_skips_legacy_log_migration_when_flow_log_exists(tmp_path: Path) -> None:
    _seed_manual(tmp_path)
    todo_path = tmp_path / "yoda" / "todos" / f"TODO.{TEST_DEV}.yaml"
    issue_path = tmp_path / "yoda" / "project" / "issues" / "test-0001-legacy.md"
    log_path = tmp_path / "yoda" / "logs" / "test-0001-legacy.yaml"
    issue_path.parent.mkdir(parents=True, exist_ok=True)
    todo_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    issue_path.write_text(
        "---\n"
        "schema_version: '1.02'\n"
        "id: test-0001\n"
        "status: to-do\n"
        "title: Legacy\n"
        "description: Legacy\n"
        "priority: 5\n"
        "created_at: '2026-01-01T00:00:00+00:00'\n"
        "updated_at: '2026-01-01T00:00:00+00:00'\n"
        "---\n\n# Legacy\n\n## Flow log\n2026-01-01T00:00:00+00:00 keep\n",
        encoding="utf-8",
    )
    todo_path.write_text(
        "schema_version: '1.02'\n"
        "developer_name: Test\n"
        "developer_slug: test\n"
        "timezone: UTC\n"
        "updated_at: '2026-01-01T00:00:00+00:00'\n"
        "issues:\n"
        "- schema_version: '1.02'\n"
        "  id: test-0001\n"
        "  title: Legacy\n"
        "  description: Legacy\n"
        "  status: to-do\n"
        "  priority: 5\n"
        "  depends_on: []\n"
        "  pending_reason: ''\n"
        "  created_at: '2026-01-01T00:00:00+00:00'\n"
        "  updated_at: '2026-01-01T00:00:00+00:00'\n"
        "  extern_issue_file: ''\n",
        encoding="utf-8",
    )
    log_path.write_text(
        "schema_version: '1.0'\n"
        "issue_id: test-0001\n"
        "issue_path: yoda/project/issues/test-0001-legacy.md\n"
        "todo_id: test-0001\n"
        "status: to-do\n"
        "entries:\n"
        "  - timestamp: '2026-01-01T00:00:00+00:00'\n"
        "    message: \"should not migrate\"\n",
        encoding="utf-8",
    )

    result = run_script("init.py", ["--dev", TEST_DEV, "--root", str(tmp_path)])
    assert result.returncode == 0, result.stderr
    text = issue_path.read_text(encoding="utf-8")
    assert "should not migrate" not in text
