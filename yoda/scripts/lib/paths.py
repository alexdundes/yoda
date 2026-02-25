"""Path helpers for YODA scripts."""

from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def todo_path(dev: str) -> Path:
    return repo_root() / "yoda" / "todos" / f"TODO.{dev}.yaml"


def issue_path(issue_id: str, slug: str) -> Path:
    return repo_root() / "yoda" / "project" / "issues" / f"{issue_id}-{slug}.md"


def log_path(issue_id: str, slug: str) -> Path:
    return repo_root() / "yoda" / "logs" / f"{issue_id}-{slug}.yaml"


def template_path() -> Path:
    return repo_root() / "yoda" / "templates" / "issue.md"
