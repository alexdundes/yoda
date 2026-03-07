#!/usr/bin/env python3
"""Append a single-line entry to an issue markdown Flow log."""

from __future__ import annotations

import argparse
import logging
import sys

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.error_messages import required_flag
from lib.errors import ExitCode, YodaError
from lib.flow_log import append_flow_log_line, sanitize_flow_message
from lib.issue_utils import resolve_issue_file_by_id
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.paths import repo_root
from lib.time_utils import detect_local_timezone, now_iso, validate_timestamp
from lib.validate import validate_issue_id, validate_slug


def _render_output(payload: dict[str, str], output_format: str) -> str:
    lines = [
        f"Issue ID: {payload['issue_id']}",
        f"Issue path: {payload['issue_path']}",
        f"Timestamp: {payload['timestamp']}",
    ]
    return render_output(payload, output_format, lines, dry_run=bool(payload.get("dry_run")))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Append a compact one-line Flow log entry to an issue markdown.",
        epilog=(
            "Agent guidance:\n"
            "- Purpose: append issue context notes outside the default yoda_flow_next transition path.\n"
            "- When to use: exceptional/manual issue logging only.\n"
            "- Mutability: appends one line to ## Flow log in the target issue.\n\n"
            "Required: --dev, --issue, --message.\n"
            "Entry format: <timestamp> <single-line-message>.\n"
            "Use this when recording issue context outside YODA Flow automation."
        ),
    )
    add_global_flags(parser)
    parser.add_argument("--issue", required=False, help="Issue id (dev-####)")
    parser.add_argument("--message", required=False, help="Compact log message (single line)")
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
        message = sanitize_flow_message((args.message or "").strip())
        if not message:
            required_flag("--message")

        timestamp = args.timestamp or now_iso(detect_local_timezone())
        validate_timestamp(timestamp)

        issue_path = resolve_issue_file_by_id(issue_id)
        line = f"{timestamp} {message}"
        if not args.dry_run:
            append_flow_log_line(issue_path, line)

        payload = {
            "issue_id": issue_id,
            "issue_path": str(issue_path.relative_to(repo_root())),
            "timestamp": timestamp,
            "dry_run": bool(args.dry_run),
        }
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
