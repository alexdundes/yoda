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
    assert not (tmp_path / "AGENTS.md").exists()
    assert not (tmp_path / "GEMINI.md").exists()
    assert not (tmp_path / "CLAUDE.md").exists()
    assert not (tmp_path / "REPO_INTENT.md").exists()
    assert not (tmp_path / "repo.intent.yaml").exists()
    assert (tmp_path / "yoda" / "project" / "issues").exists()
    assert not (tmp_path / "yoda" / "todos" / f"TODO.{TEST_DEV}.yaml").exists()


def test_init_does_not_modify_existing_host_agent_or_intent_files(tmp_path: Path) -> None:
    _seed_manual(tmp_path)
    existing_files = {
        "AGENTS.md": "# Host agents\n",
        "GEMINI.md": "# Host gemini\n",
        "CLAUDE.md": "# Host claude\n",
        "REPO_INTENT.md": "# Host intent\n",
        "repo.intent.yaml": "project: host\n",
    }
    for name, content in existing_files.items():
        (tmp_path / name).write_text(content, encoding="utf-8")

    result = run_script("init.py", ["--dev", TEST_DEV, "--root", str(tmp_path)])
    assert result.returncode == 0, result.stderr

    for name, content in existing_files.items():
        assert (tmp_path / name).read_text(encoding="utf-8") == content


def test_init_dry_run_does_not_report_host_agent_or_intent_writes(tmp_path: Path) -> None:
    _seed_manual(tmp_path)
    result = run_script("init.py", ["--dev", TEST_DEV, "--root", str(tmp_path), "--dry-run"])
    assert result.returncode == 0, result.stderr
    assert "AGENTS.md" not in result.stdout
    assert "GEMINI.md" not in result.stdout
    assert "CLAUDE.md" not in result.stdout
    assert "REPO_INTENT.md" not in result.stdout
    assert "repo.intent.yaml" not in result.stdout


def test_init_sanitizes_existing_issue_front_matter_id_without_legacy_todo(tmp_path: Path) -> None:
    _seed_manual(tmp_path)
    issue_path = tmp_path / "yoda" / "project" / "issues" / "test-0001-existing.md"
    issue_path.parent.mkdir(parents=True, exist_ok=True)
    issue_path.write_text(
        "---\n"
        "schema_version: '2.00'\n"
        "id: test-0001\n"
        "status: to-do\n"
        "title: Existing\n"
        "description: Existing\n"
        "priority: 5\n"
        "created_at: '2026-01-01T00:00:00+00:00'\n"
        "updated_at: '2026-01-01T00:00:00+00:00'\n"
        "---\n\n# Existing\n\n## Flow log\n",
        encoding="utf-8",
    )

    result = run_script("init.py", ["--dev", TEST_DEV, "--root", str(tmp_path)])
    assert result.returncode == 0, result.stderr
    parsed = frontmatter.load(issue_path)
    assert "id" not in parsed.metadata


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
    assert "id" not in parsed.metadata
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
    parsed = frontmatter.load(issue_path)
    assert "id" not in parsed.metadata
    text = issue_path.read_text(encoding="utf-8")
    assert "should not migrate" not in text
