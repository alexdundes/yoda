#!/usr/bin/env python3
"""Select the next actionable issue from a TODO file."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from typing import Any

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.errors import ExitCode, YodaError
from lib.logging_utils import configure_logging
from lib.paths import issue_path, repo_root, todo_path
from lib.todo_utils import load_todo_file
from lib.validate import validate_slug


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(payload, indent=2, ensure_ascii=True)

    lines = []
    issue_id = payload.get("issue_id")
    issue_path_value = payload.get("issue_path")
    todo_path_value = payload.get("todo_path")
    if issue_id:
        lines.append(f"Issue ID: {issue_id}")
    if issue_path_value:
        lines.append(f"Issue path: {issue_path_value}")
    if todo_path_value:
        lines.append(f"TODO path: {todo_path_value}")

    doing = payload.get("doing", [])
    if doing:
        lines.append("Doing issues:")
        for item in doing:
            lines.append(f"- {item.get('id', '')}")

    pending = payload.get("pending", [])
    if pending:
        lines.append("Pending issues:")
        for item in pending:
            issue_id_value = item.get("id", "")
            reason = item.get("reason", "")
            lines.append(f"- {issue_id_value}: {reason}")

    blocked = payload.get("blocked", [])
    if blocked:
        lines.append("Blocked issues:")
        for item in blocked:
            issue_id_value = item.get("id", "")
            deps = ", ".join(item.get("depends_on", []))
            lines.append(f"- {issue_id_value}: {deps}")

    return "\n".join(lines)


def _collect_doing(issues: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {"id": str(item.get("id"))}
        for item in issues
        if item.get("status") == "doing"
    ]


def _collect_pending(issues: list[dict[str, Any]]) -> list[dict[str, str]]:
    pending = []
    for item in issues:
        if item.get("status") == "pending":
            pending.append(
                {
                    "id": str(item.get("id")),
                    "reason": str(item.get("pending_reason", "")),
                }
            )
    return pending


def _collect_blocked(issues: list[dict[str, Any]], done_ids: set[str]) -> list[dict[str, Any]]:
    blocked = []
    for item in issues:
        if item.get("status") != "to-do":
            continue
        depends_on = [str(dep) for dep in item.get("depends_on", [])]
        if not depends_on:
            continue
        unresolved = [dep for dep in depends_on if dep not in done_ids]
        if unresolved:
            blocked.append({"id": str(item.get("id")), "depends_on": unresolved})
    return blocked


def _is_selectable(issue: dict[str, Any], done_ids: set[str]) -> bool:
    if issue.get("status") != "to-do":
        return False
    depends_on = [str(dep) for dep in issue.get("depends_on", [])]
    return all(dep in done_ids for dep in depends_on)


def _select_next(issues: list[dict[str, Any]], done_ids: set[str]) -> dict[str, Any] | None:
    selectable: list[tuple[int, int, dict[str, Any]]] = []
    for idx, item in enumerate(issues):
        if _is_selectable(item, done_ids):
            priority = int(item.get("priority", 0))
            selectable.append((-priority, idx, item))
    if not selectable:
        return None
    selectable.sort(key=lambda entry: (entry[0], entry[1]))
    return selectable[0][2]


def main() -> int:
    parser = argparse.ArgumentParser(description="Select next actionable issue")
    add_global_flags(parser)
    parser.add_argument("--todo", required=False, help="Override TODO path")

    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = resolve_dev(args.dev).strip()
        validate_slug(dev)

        if args.todo:
            todo_file = repo_root() / args.todo
        else:
            todo_file = todo_path(dev)

        todo = load_todo_file(todo_file, dev)

        issues = list(todo.get("issues", []))
        done_ids = {
            str(item.get("id"))
            for item in issues
            if item.get("status") == "done"
        }

        doing = _collect_doing(issues)
        pending = _collect_pending(issues)
        blocked = _collect_blocked(issues, done_ids)

        payload = {
            "issue_id": "",
            "issue_path": "",
            "todo_path": str(todo_file.relative_to(repo_root())),
            "pending": pending,
            "blocked": blocked,
            "doing": doing,
        }

        if doing:
            logging.error("Conflict: resolve the doing issue(s) before selecting the next one.")
            print(_render_output(payload, output_format))
            return ExitCode.CONFLICT

        selected = _select_next(issues, done_ids)
        if selected is None:
            logging.error("No selectable issues found. Resolve pending or blocked items.")
            print(_render_output(payload, output_format))
            return ExitCode.NOT_FOUND

        issue_id = str(selected.get("id"))
        slug = str(selected.get("slug"))
        issue_file = issue_path(issue_id, slug)

        payload["issue_id"] = issue_id
        payload["issue_path"] = str(issue_file.relative_to(repo_root()))

        print(_render_output(payload, output_format))
        return ExitCode.SUCCESS
    except YodaError as exc:
        logging.error(str(exc))
        return exc.exit_code
    except Exception as exc:  # pragma: no cover
        logging.error("Unexpected error: %s", exc)
        return ExitCode.ERROR


if __name__ == "__main__":
    sys.exit(main())
