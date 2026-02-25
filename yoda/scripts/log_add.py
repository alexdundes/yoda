#!/usr/bin/env python3
"""Append a log entry for an issue."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.error_messages import required_flag
from lib.errors import ExitCode, YodaError
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.issue_utils import ensure_issue_file_exists
from lib.paths import log_path, repo_root, todo_path
from lib.time_utils import now_iso, validate_timestamp
from lib.todo_utils import find_issue, load_todo_file
from lib.validate import validate_issue_id, validate_slug
from lib.yaml_io import read_yaml, write_yaml


def _load_or_init_log(
    path: Path,
    issue_id: str,
    issue_path_str: str,
    status: str,
) -> dict[str, Any]:
    if path.exists():
        data = read_yaml(path)
    else:
        data = {
            "schema_version": "1.0",
            "issue_id": issue_id,
            "issue_path": issue_path_str,
            "todo_id": issue_id,
            "status": status,
            "entries": [],
        }
    if not isinstance(data.get("entries"), list):
        raise YodaError("Log entries must be a list", exit_code=ExitCode.VALIDATION)
    return data


def _validate_log(log_doc: dict[str, Any]) -> None:
    required = ["schema_version", "issue_id", "issue_path", "todo_id", "status", "entries"]
    for field in required:
        if field not in log_doc:
            raise YodaError("Log schema missing required fields", exit_code=ExitCode.VALIDATION)
    if str(log_doc.get("schema_version")) != "1.0":
        raise YodaError("Unsupported log schema_version", exit_code=ExitCode.VALIDATION)
    if log_doc.get("status") not in {"to-do", "doing", "done", "pending"}:
        raise YodaError("Invalid log status", exit_code=ExitCode.VALIDATION)
    if not isinstance(log_doc.get("entries"), list):
        raise YodaError("Log entries must be a list", exit_code=ExitCode.VALIDATION)
    for entry in log_doc.get("entries", []):
        if not isinstance(entry, dict):
            raise YodaError("Log entry must be an object", exit_code=ExitCode.VALIDATION)
        if "timestamp" not in entry or "message" not in entry:
            raise YodaError("Log entry missing timestamp or message", exit_code=ExitCode.VALIDATION)
        if not entry.get("message"):
            raise YodaError("Log entry message cannot be empty", exit_code=ExitCode.VALIDATION)
        validate_timestamp(str(entry.get("timestamp")))


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    lines = [
        f"Issue ID: {payload['issue_id']}",
        f"Log path: {payload['log_path']}",
        f"Timestamp: {payload['timestamp']}",
    ]
    return render_output(
        payload,
        output_format,
        lines,
        dry_run=bool(payload.get("dry_run")),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Append a log entry")
    add_global_flags(parser)
    parser.add_argument("--issue", required=False, help="Issue id (dev-####)")
    parser.add_argument("--message", required=False, help="Log message text")
    parser.add_argument("--timestamp", required=False, help="ISO 8601 timestamp override")

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
        message = (args.message or "").strip()
        if not message:
            required_flag("--message")
        if issue_id not in message:
            raise YodaError(
                "Log message must mention the issue id",
                exit_code=ExitCode.VALIDATION,
            )

        todo_file = todo_path(dev)
        todo = load_todo_file(todo_file, dev)
        issue_item = find_issue(todo, issue_id)

        slug = str(issue_item.get("slug"))
        validate_slug(slug)

        issue_file = ensure_issue_file_exists(issue_id, slug)

        log_file = log_path(issue_id, slug)

        status = str(issue_item.get("status", "to-do"))
        log_doc = _load_or_init_log(
            log_file,
            issue_id=issue_id,
            issue_path_str=str(issue_file.relative_to(repo_root())),
            status=status,
        )
        log_doc["status"] = status

        timestamp = args.timestamp or now_iso(todo.get("timezone"))
        validate_timestamp(timestamp)

        log_doc["entries"].append({"timestamp": timestamp, "message": message})

        _validate_log(log_doc)

        payload = {
            "issue_id": issue_id,
            "log_path": str(log_file.relative_to(repo_root())),
            "timestamp": timestamp,
            "dry_run": bool(args.dry_run),
        }

        if not args.dry_run:
            write_yaml(log_file, log_doc)

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
