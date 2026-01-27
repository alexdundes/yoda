#!/usr/bin/env python3
"""Update fields in yoda/todos/TODO.<dev>.yaml."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from lib.cli import add_global_flags, resolve_format
from lib.errors import ExitCode, YodaError
from lib.paths import repo_root, todo_path
from lib.validate import validate_issue_id, validate_slug, validate_todo
from lib.yaml_io import read_yaml, write_yaml


ALLOWED_STATUS = {"to-do", "doing", "done", "pending"}


def _configure_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )


def _resolve_dev(explicit_dev: str | None) -> str:
    if explicit_dev:
        return explicit_dev
    env_dev = os.environ.get("YODA_DEV")
    if env_dev:
        return env_dev
    try:
        return input("Developer slug: ").strip()
    except EOFError as exc:
        raise YodaError("Developer slug is required", exit_code=ExitCode.VALIDATION) from exc


def _now_iso(tz_name: str) -> str:
    tz = ZoneInfo(tz_name)
    return datetime.now(tz).isoformat(timespec="seconds")


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(payload, indent=2, ensure_ascii=True)
    lines = [
        f"Issue ID: {payload['issue_id']}",
        f"Updated fields: {', '.join(payload['updated_fields'])}",
        f"TODO path: {payload['todo_path']}",
    ]
    if payload.get("dry_run"):
        lines.append("Dry-run: no files written")
    return "\n".join(lines)


def _update_issue(item: dict[str, Any], args: argparse.Namespace) -> list[str]:
    updated = []

    if args.status is not None:
        if args.status not in ALLOWED_STATUS:
            raise YodaError("Invalid status", exit_code=ExitCode.VALIDATION)
        item["status"] = args.status
        updated.append("status")

    if args.priority is not None:
        if args.priority < 0 or args.priority > 10:
            raise YodaError("priority must be between 0 and 10", exit_code=ExitCode.VALIDATION)
        item["priority"] = args.priority
        updated.append("priority")

    if args.agent is not None:
        item["agent"] = args.agent
        updated.append("agent")

    if args.clear_tags:
        item["tags"] = []
        updated.append("tags")
    elif args.tags is not None:
        item["tags"] = _parse_csv(args.tags)
        updated.append("tags")

    if args.clear_depends_on:
        item["depends_on"] = []
        updated.append("depends_on")
    elif args.depends_on is not None:
        item["depends_on"] = _parse_csv(args.depends_on)
        updated.append("depends_on")

    if args.pending_reason is not None:
        item["pending_reason"] = args.pending_reason
        updated.append("pending_reason")

    return updated


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
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument("--depends-on", dest="depends_on", help="Comma-separated issue ids")
    parser.add_argument("--pending-reason", dest="pending_reason", help="Pending reason")
    parser.add_argument("--agent", help="Agent name")
    parser.add_argument("--clear-tags", action="store_true", help="Clear tags")
    parser.add_argument("--clear-depends-on", action="store_true", help="Clear dependencies")

    args = parser.parse_args()
    _configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = _resolve_dev(args.dev).strip()
        validate_slug(dev)
        issue_id = (args.issue or "").strip()
        if not issue_id:
            raise YodaError("--issue is required", exit_code=ExitCode.VALIDATION)
        validate_issue_id(issue_id, dev)

        todo_file = todo_path(dev)
        todo = read_yaml(todo_file)
        validate_todo(todo, dev)

        issue_item = None
        for item in todo.get("issues", []):
            if item.get("id") == issue_id:
                issue_item = item
                break
        if issue_item is None:
            raise YodaError("Issue id not found in TODO", exit_code=ExitCode.NOT_FOUND)

        updated_fields = _update_issue(issue_item, args)
        pending_reason_provided = args.pending_reason is not None
        _apply_pending_rules(issue_item, pending_reason_provided)

        timestamp = _now_iso(todo.get("timezone"))
        issue_item["updated_at"] = timestamp
        todo["updated_at"] = timestamp

        validate_todo(todo, dev)

        payload = {
            "issue_id": issue_id,
            "updated_fields": updated_fields,
            "todo_path": str(todo_file.relative_to(repo_root())),
            "dry_run": bool(args.dry_run),
        }

        if not args.dry_run:
            write_yaml(todo_file, todo)
            log_message = f"[{issue_id}] todo_update updated fields: {', '.join(updated_fields)}"
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
