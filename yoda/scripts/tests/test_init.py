from __future__ import annotations

from pathlib import Path

import yaml

from conftest import TEST_DEV, run_script


def _seed_manual(root: Path) -> None:
    yoda_dir = root / "yoda"
    yoda_dir.mkdir(parents=True, exist_ok=True)
    (yoda_dir / "yoda.md").write_text("# Manual\n", encoding="utf-8")


AGENT_FILES = ["AGENTS.md", "GEMINI.md", "CLAUDE.md", "agent.md"]


def test_init_creates_structure_and_is_idempotent(tmp_path: Path) -> None:
    _seed_manual(tmp_path)

    result = run_script(
        "init.py",
        ["--dev", TEST_DEV, "--root", str(tmp_path)],
    )
    assert result.returncode == 0, result.stderr

    agents_path = tmp_path / "AGENTS.md"
    todo_path = tmp_path / "yoda" / "todos" / f"TODO.{TEST_DEV}.yaml"
    issues_dir = tmp_path / "yoda" / "project" / "issues"

    assert agents_path.exists()
    assert todo_path.exists()
    assert issues_dir.exists()

    todo = yaml.safe_load(todo_path.read_text(encoding="utf-8"))
    assert todo["schema_version"] == "1.01"
    assert todo["developer_slug"] == TEST_DEV
    assert todo["issues"] == []

    for name in AGENT_FILES:
        path = tmp_path / name
        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "<!-- YODA:BEGIN -->" in content
        assert "<!-- YODA:END -->" in content
        assert "yoda/yoda.md" in content

    second = run_script(
        "init.py",
        ["--dev", TEST_DEV, "--root", str(tmp_path)],
    )
    assert second.returncode == 0, second.stderr

    for name in AGENT_FILES:
        path = tmp_path / name
        content = path.read_text(encoding="utf-8")
        assert content.count("<!-- YODA:BEGIN -->") == 1


def test_init_dry_run_does_not_write(tmp_path: Path) -> None:
    _seed_manual(tmp_path)

    result = run_script(
        "init.py",
        ["--dev", TEST_DEV, "--root", str(tmp_path), "--dry-run"],
    )
    assert result.returncode == 0, result.stderr

    for name in AGENT_FILES:
        assert not (tmp_path / name).exists()
    assert not (tmp_path / "yoda" / "todos" / f"TODO.{TEST_DEV}.yaml").exists()


def test_init_appends_to_existing_agent_file(tmp_path: Path) -> None:
    _seed_manual(tmp_path)
    agents_path = tmp_path / "AGENTS.md"
    agents_path.write_text("Custom\n", encoding="utf-8")

    result = run_script(
        "init.py",
        ["--dev", TEST_DEV, "--root", str(tmp_path)],
    )
    assert result.returncode == 0, result.stderr
    content = agents_path.read_text(encoding="utf-8")
    assert "Custom" in content
    assert "<!-- YODA:BEGIN -->" in content


def test_init_conflict_on_agent_path_directory(tmp_path: Path) -> None:
    _seed_manual(tmp_path)
    (tmp_path / "GEMINI.md").mkdir()

    result = run_script(
        "init.py",
        ["--dev", TEST_DEV, "--root", str(tmp_path)],
    )
    assert result.returncode == 4, result.stderr
    assert (tmp_path / "GEMINI.md").is_dir()


def test_init_reconcile_layout_updates_schema_and_front_matter(tmp_path: Path) -> None:
    _seed_manual(tmp_path)

    todo_path = tmp_path / "yoda" / "todos" / f"TODO.{TEST_DEV}.yaml"
    issues_dir = tmp_path / "yoda" / "project" / "issues"
    issues_dir.mkdir(parents=True, exist_ok=True)
    (tmp_path / "README.md").write_text("hello\n", encoding="utf-8")

    todo_path.parent.mkdir(parents=True, exist_ok=True)
    todo_path.write_text(
        "schema_version: '1.0'\n"
        "developer_name: Test\n"
        "developer_slug: test\n"
        "timezone: UTC\n"
        "updated_at: '2026-01-01T00:00:00+00:00'\n"
        "issues:\n"
        "- schema_version: '1.0'\n"
        "  id: test-0001\n"
        "  title: Legacy issue\n"
        "  slug: legacy-issue\n"
        "  description: Legacy\n"
        "  status: to-do\n"
        "  priority: 5\n"
        "  tags: [legacy]\n"
        "  depends_on: []\n"
        "  pending_reason: ''\n"
        "  created_at: '2026-01-01T00:00:00+00:00'\n"
        "  updated_at: '2026-01-01T00:00:00+00:00'\n"
        "  origin: {system: '', external_id: '', requester: ''}\n",
        encoding="utf-8",
    )

    issue_path = issues_dir / "test-0001-legacy-issue.md"
    issue_path.write_text(
        "---\n"
        "schema_version: '1.0'\n"
        "id: test-0001\n"
        "title: Legacy issue\n"
        "slug: legacy-issue\n"
        "description: Legacy\n"
        "status: to-do\n"
        "priority: 5\n"
        "tags: [legacy]\n"
        "depends_on: []\n"
        "pending_reason: ''\n"
        "created_at: '2026-01-01T00:00:00+00:00'\n"
        "updated_at: '2026-01-01T00:00:00+00:00'\n"
        "origin: {system: '', external_id: '', requester: ''}\n"
        "---\n\n# Legacy\n",
        encoding="utf-8",
    )

    result = run_script(
        "init.py",
        ["--dev", TEST_DEV, "--root", str(tmp_path), "--reconcile-layout"],
    )
    assert result.returncode == 0, result.stderr

    todo = yaml.safe_load(todo_path.read_text(encoding="utf-8"))
    assert todo["schema_version"] == "1.01"
    assert "tags" not in todo["issues"][0]
    assert "agent" not in todo["issues"][0]

    issue_doc = issue_path.read_text(encoding="utf-8")
    assert "schema_version: '1.01'" in issue_doc
    assert "tags:" not in issue_doc
    assert "agent:" not in issue_doc


def test_init_creates_repo_intent_files(tmp_path: Path) -> None:
    _seed_manual(tmp_path)

    result = run_script(
        "init.py",
        ["--dev", TEST_DEV, "--root", str(tmp_path)],
    )
    assert result.returncode == 0, result.stderr

    repo_intent = tmp_path / "REPO_INTENT.md"
    repo_yaml = tmp_path / "repo.intent.yaml"

    assert repo_intent.exists()
    assert repo_yaml.exists()

    content = repo_intent.read_text(encoding="utf-8")
    assert "Repository Intent" in content
    assert "<!-- YODA:BEGIN -->" in content
    assert "yoda/yoda.md" in content

    data = yaml.safe_load(repo_yaml.read_text(encoding="utf-8"))
    assert "yoda" in data
    assert data["yoda"]["manual"] == "yoda/yoda.md"


def test_init_merges_repo_intent_yaml(tmp_path: Path) -> None:
    _seed_manual(tmp_path)

    repo_yaml = tmp_path / "repo.intent.yaml"
    repo_yaml.write_text(
        "mode: host\n"
        "custom: true\n"
        "yoda:\n"
        "  embedded: false\n",
        encoding="utf-8",
    )

    result = run_script(
        "init.py",
        ["--dev", TEST_DEV, "--root", str(tmp_path)],
    )
    assert result.returncode == 0, result.stderr

    data = yaml.safe_load(repo_yaml.read_text(encoding="utf-8"))
    assert data["mode"] == "host"
    assert data["custom"] is True
    assert data["yoda"]["embedded"] is False
    assert data["yoda"]["manual"] == "yoda/yoda.md"
    assert "agent_entry_order" in data["yoda"]


def test_init_repo_intent_markers_idempotent(tmp_path: Path) -> None:
    _seed_manual(tmp_path)

    repo_intent = tmp_path / "REPO_INTENT.md"
    repo_intent.write_text("Custom intro\n", encoding="utf-8")

    first = run_script(
        "init.py",
        ["--dev", TEST_DEV, "--root", str(tmp_path)],
    )
    assert first.returncode == 0, first.stderr

    second = run_script(
        "init.py",
        ["--dev", TEST_DEV, "--root", str(tmp_path)],
    )
    assert second.returncode == 0, second.stderr

    content = repo_intent.read_text(encoding="utf-8")
    assert content.count("<!-- YODA:BEGIN -->") == 1
