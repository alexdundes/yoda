from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Iterable

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
TEST_DEV = "test"
TEST_TODO = REPO_ROOT / "yoda" / "todos" / f"TODO.{TEST_DEV}.yaml"


def run_script(script_name: str, args: Iterable[str]) -> subprocess.CompletedProcess[str]:
    script_path = REPO_ROOT / "yoda" / "scripts" / script_name
    if not script_path.exists():
        script_path = REPO_ROOT / script_name
    cmd = [sys.executable, str(script_path), *args]
    return subprocess.run(cmd, capture_output=True, text=True)


def write_yaml(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False)


def cleanup_test_files() -> None:
    paths = [
        TEST_TODO,
        *REPO_ROOT.glob("yoda/project/issues/test-*.md"),
        *REPO_ROOT.glob("yoda/logs/test-*.yaml"),
    ]
    for path in paths:
        if path.exists():
            path.unlink()


class TodoFactory:
    def __init__(self, dev: str, timezone: str = "UTC") -> None:
        self.dev = dev
        self.timezone = timezone
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"{self.dev}-{self._counter:04d}"

    def issue(
        self,
        *,
        title: str,
        status: str = "to-do",
        priority: int = 5,
        slug: str | None = None,
        depends_on: list[str] | None = None,
        pending_reason: str = "",
        tags: list[str] | None = None,
        agent: str = "Test",
        created_at: str | None = None,
        updated_at: str | None = None,
    ) -> dict:
        issue_id = self._next_id()
        created_at_value = created_at or "2026-01-01T00:00:00+00:00"
        updated_at_value = updated_at or created_at_value
        slug_value = slug or title.lower().replace(" ", "-")
        return {
            "schema_version": "1.0",
            "id": issue_id,
            "title": title,
            "slug": slug_value,
            "description": "Test issue",
            "status": status,
            "priority": priority,
            "agent": agent,
            "depends_on": depends_on or [],
            "pending_reason": pending_reason,
            "created_at": created_at_value,
            "updated_at": updated_at_value,
            "tags": tags or [],
            "origin": {"system": "", "external_id": "", "requester": ""},
        }

    def todo(self, issues: list[dict]) -> dict:
        return {
            "schema_version": "1.0",
            "developer_name": "Test",
            "developer_slug": self.dev,
            "timezone": self.timezone,
            "updated_at": "2026-01-01T00:00:00+00:00",
            "issues": issues,
        }
