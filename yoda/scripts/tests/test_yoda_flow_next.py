from __future__ import annotations

import json
import re
from pathlib import Path

import frontmatter

from conftest import REPO_ROOT, TEST_DEV, cleanup_test_files, run_script


def _write_issue_file(name: str, front_matter: dict[str, object], body: str = "# Test\n") -> Path:
    path = REPO_ROOT / "yoda" / "project" / "issues" / name
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    for key, value in front_matter.items():
        if isinstance(value, list):
            lines.append(f"{key}:")
            for item in value:
                lines.append(f"- {item}")
        elif isinstance(value, int):
            lines.append(f"{key}: {value}")
        else:
            lines.append(f"{key}: '{value}'")
    lines.extend(["---", "", body.rstrip("\n"), ""])
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def _read_front_matter(path: Path) -> dict:
    return dict(frontmatter.load(path).metadata)


def _read_flow_log_lines(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"(?m)^## Flow log\s*$", text)
    assert match is not None
    section = text[match.end() :]
    next_header = re.search(r"(?m)^##\s+", section)
    if next_header:
        section = section[: next_header.start()]
    return [line for line in section.splitlines() if line.strip()]


def _last_log_line(path: Path) -> str:
    lines = _read_flow_log_lines(path)
    assert lines
    return lines[-1]


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


def test_flow_next_requires_explicit_dev_slug() -> None:
    result = run_script("yoda_flow_next.py", [])
    assert result.returncode == 2
    assert "--dev is required" in result.stderr


def test_flow_next_transitions_todo_to_doing_study_and_logs() -> None:
    path = _write_issue_file(
        "test-0001-todo.md",
        {
            "schema_version": "1.02",
            "status": "to-do",
            "title": "Todo",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Todo\n\n## Flow log\n",
    )

    result = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["issue_id"] == "test-0001"
    assert payload["status"] == "doing"
    assert payload["phase"] == "study"
    assert payload["next_step"] == "study"
    assert payload["runbook_line"].startswith("Run Study:")
    assert payload["log_timestamp"]

    meta = _read_front_matter(path)
    assert meta["status"] == "doing"
    assert meta["phase"] == "study"
    assert meta["updated_at"] == payload["log_timestamp"]
    assert _last_log_line(path).endswith("test-0001 transition to-do->doing phase=study")


def test_flow_next_advances_doing_phases_and_finishes_done() -> None:
    path = _write_issue_file(
        "test-0001-doing.md",
        {
            "schema_version": "1.02",
            "status": "doing",
            "phase": "study",
            "title": "Doing",
            "description": "Desc",
            "priority": 5,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Doing\n\n## Flow log\n",
    )
    _write_issue_file(
        "test-0002-next.md",
        {
            "schema_version": "1.02",
            "status": "to-do",
            "title": "Next",
            "description": "Desc",
            "priority": 1,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Next\n\n## Flow log\n",
    )

    first = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert first.returncode == 0, first.stderr
    p1 = json.loads(first.stdout)
    assert p1["status"] == "doing"
    assert p1["phase"] == "document"
    assert p1["next_step"] == "document"

    second = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert second.returncode == 0, second.stderr
    p2 = json.loads(second.stdout)
    assert p2["phase"] == "implement"
    assert p2["next_step"] == "implement"

    third = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert third.returncode == 0, third.stderr
    p3 = json.loads(third.stdout)
    assert p3["phase"] == "evaluate"
    assert p3["next_step"] == "evaluate"
    assert "conventional-commit line" in p3["runbook_line"]

    fourth = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert fourth.returncode == 0, fourth.stderr
    p4 = json.loads(fourth.stdout)
    assert p4["status"] == "done"
    assert p4["phase"] == ""
    assert p4["next_step"] == "done"
    assert p4["runbook_line"].startswith("Issue moved to done.")
    assert p4["next_issue_id"] == "test-0002"
    assert p4["continue_prompt"]

    meta = _read_front_matter(path)
    assert meta["status"] == "done"
    assert "phase" not in meta
    assert _last_log_line(path).endswith("test-0001 transition doing/evaluate->done")


def test_flow_next_ignores_pending_and_reports_hint() -> None:
    _write_issue_file(
        "test-0001-pending.md",
        {
            "schema_version": "1.02",
            "status": "pending",
            "title": "Pending",
            "description": "Desc",
            "priority": 9,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Pending\n\n## Flow log\n",
    )
    selectable = _write_issue_file(
        "test-0002-selectable.md",
        {
            "schema_version": "1.02",
            "status": "to-do",
            "title": "Selectable",
            "description": "Desc",
            "priority": 7,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Selectable\n\n## Flow log\n",
    )

    result = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["issue_id"] == "test-0002"
    assert payload["pending"][0]["id"] == "test-0001"
    assert payload["status"] == "doing"
    assert payload["phase"] == "study"
    assert _last_log_line(selectable).endswith("test-0002 transition to-do->doing phase=study")


def test_flow_next_logs_blocked_reason_for_dependency_blocked() -> None:
    _write_issue_file(
        "test-0001-pending-dep.md",
        {
            "schema_version": "1.02",
            "status": "pending",
            "title": "Dep",
            "description": "Desc",
            "priority": 7,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Dep\n\n## Flow log\n",
    )
    blocked = _write_issue_file(
        "test-0002-todo-blocked.md",
        {
            "schema_version": "1.02",
            "status": "to-do",
            "depends_on": ["test-0001"],
            "title": "Blocked",
            "description": "Desc",
            "priority": 9,
            "created_at": "2026-01-01T00:00:00+00:00",
            "updated_at": "2026-01-01T00:00:00+00:00",
        },
        body="# Blocked\n\n## Flow log\n",
    )

    result = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--format", "json"])
    assert result.returncode == 3, result.stderr
    payload = json.loads(result.stdout)
    assert payload["next_step"] == "blocked"
    assert payload["blocked_reason"] == "dependency_blocked"
    assert payload["log_timestamp"]
    assert _last_log_line(blocked).endswith("test-0002 blocked dependency_blocked")
