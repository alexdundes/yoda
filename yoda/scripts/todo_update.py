#!/usr/bin/env python3
"""Update fields in yoda/todos/TODO.<dev>.yaml."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from copy import deepcopy
from typing import Any

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.error_messages import required_flag
from lib.errors import ExitCode, YodaError
from lib.front_matter import update_front_matter
from lib.issue_utils import ensure_issue_file_exists
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.paths import repo_root, todo_path
from lib.time_utils import now_iso
from lib.todo_utils import find_issue, load_todo_file
from lib.validate import validate_issue_id, validate_slug, validate_todo
from lib.yaml_io import write_yaml


ALLOWED_STATUS = {"to-do", "doing", "done", "pending"}


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    lines = [
        f"Issue ID: {payload['issue_id']}",
        f"Updated fields: {', '.join(payload['updated_fields'])}",
        f"TODO path: {payload['todo_path']}",
    ]
    return render_output(
        payload,
        output_format,
        lines,
        dry_run=bool(payload.get("dry_run")),
    )


def _update_issue(item: dict[str, Any], args: argparse.Namespace) -> None:
    if args.status is not None:
        if args.status not in ALLOWED_STATUS:
            raise YodaError("Invalid status", exit_code=ExitCode.VALIDATION)
        item["status"] = args.status

    if args.priority is not None:
        if args.priority < 0 or args.priority > 10:
            raise YodaError("priority must be between 0 and 10", exit_code=ExitCode.VALIDATION)
        item["priority"] = args.priority

    if args.clear_depends_on:
        item["depends_on"] = []
    elif args.depends_on is not None:
        item["depends_on"] = _parse_csv(args.depends_on)

    if args.pending_reason is not None:
        item["pending_reason"] = args.pending_reason


def _apply_pending_rules(item: dict[str, Any], pending_reason_provided: bool) -> None:
    status = item.get("status")
    if status == "pending":
        if not item.get("pending_reason"):
            raise YodaError("pending_reason required for pending status", exit_code=ExitCode.VALIDATION)
    else:
        if pending_reason_provided:
            return
        if item.get("pending_reason"):
            item["pending_reason"] = ""


def _format_value(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "[]"
    return "" if value is None else str(value)


def _diff_fields(before: dict[str, Any], after: dict[str, Any]) -> tuple[list[str], list[str]]:
    fields = ["status", "priority", "depends_on", "pending_reason"]
    updated_fields = []
    lines = []
    for field in fields:
        before_val = before.get(field)
        after_val = after.get(field)
        if before_val != after_val:
            updated_fields.append(field)
            lines.append(f"{field}: {_format_value(before_val)} -> {_format_value(after_val)}")
    return updated_fields, lines


def _append_log(dev: str, issue_id: str, message: str, dry_run: bool) -> None:
    if dry_run:
        return
    script = repo_root() / "yoda" / "scripts" / "log_add.py"
    cmd = [sys.executable, str(script), "--dev", dev, "--issue", issue_id, "--message", message]
    result = os.spawnv(os.P_WAIT, sys.executable, cmd)
    if result != 0:
        raise YodaError("Failed to append log entry", exit_code=ExitCode.ERROR)


def main() -> int:
    parser = argparse.ArgumentParser(description="Update TODO issue fields")
    add_global_flags(parser)
    parser.add_argument("--issue", required=False, help="Issue id (dev-####)")
    parser.add_argument("--status", help="New status")
    parser.add_argument("--priority", type=int, help="Priority 0-10")
    parser.add_argument("--depends-on", dest="depends_on", help="Comma-separated issue ids")
    parser.add_argument("--pending-reason", dest="pending_reason", help="Pending reason")
    parser.add_argument("--clear-depends-on", action="store_true", help="Clear dependencies")

    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = resolve_dev(args.dev).strip()
        validate_slug(dev)
        issue_id = (args.issue or "").strip()
        if not issue_id:
            required_flag("--issue")
        validate_issue_id(issue_id, dev)

        todo_file = todo_path(dev)
        todo = load_todo_file(todo_file, dev)
        issue_item = find_issue(todo, issue_id)

        before_item = deepcopy(issue_item)
        _update_issue(issue_item, args)
        pending_reason_provided = args.pending_reason is not None
        _apply_pending_rules(issue_item, pending_reason_provided)

        timestamp = now_iso(todo.get("timezone"))
        issue_item["updated_at"] = timestamp
        todo["updated_at"] = timestamp

        validate_todo(todo, dev)

        updated_fields, log_lines = _diff_fields(before_item, issue_item)
        issue_file = ensure_issue_file_exists(issue_id, str(issue_item.get("slug")))

        payload = {
            "issue_id": issue_id,
            "updated_fields": updated_fields,
            "todo_path": str(todo_file.relative_to(repo_root())),
            "dry_run": bool(args.dry_run),
        }

        if not args.dry_run:
            write_yaml(todo_file, todo)
            update_front_matter(issue_file, issue_item)
            if log_lines:
                log_message = f"[{issue_id}] todo_update\n" + "\n".join(log_lines)
            else:
                log_message = f"[{issue_id}] todo_update (no changes)"
            _append_log(dev, issue_id, log_message, args.dry_run)

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
