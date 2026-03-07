#!/usr/bin/env python3
"""Select the next actionable issue from markdown issues."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.errors import ExitCode, YodaError
from lib.issue_index import load_issue_index
from lib.logging_utils import configure_logging
from lib.order_utils import apply_dependency_order
from lib.output import render_output
from lib.paths import repo_root
from lib.validate import validate_slug


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    lines: list[str] = []
    if payload.get("issue_id"):
        lines.append(f"Issue ID: {payload['issue_id']}")
    if payload.get("issue_path"):
        lines.append(f"Issue path: {payload['issue_path']}")

    pending = payload.get("pending", [])
    if pending:
        lines.append("Pending issues:")
        for item in pending:
            lines.append(f"- {item.get('id', '')}: {item.get('reason', '')}")

    blocked = payload.get("blocked", [])
    if blocked:
        lines.append("Blocked issues:")
        for item in blocked:
            deps = ", ".join(item.get("depends_on", []))
            lines.append(f"- {item.get('id', '')}: {deps}")
    return render_output(payload, output_format, lines, dry_run=bool(payload.get("dry_run")))


def _collect_pending(issues: list[dict[str, Any]]) -> list[dict[str, str]]:
    return [
        {"id": str(item.get("id", "")), "reason": "Issue is pending and not selectable."}
        for item in issues
        if item.get("status") == "pending"
    ]


def _collect_blocked(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blocked: list[dict[str, Any]] = []
    for item in issues:
        if item.get("status") != "to-do":
            continue
        deps = list(item.get("blocked_by", []))
        if deps:
            blocked.append({"id": str(item.get("id", "")), "depends_on": deps})
    return blocked


def _pick_target(issues: list[dict[str, Any]]) -> dict[str, Any] | None:
    doing = [item for item in issues if item.get("status") == "doing"]
    if doing:
        return doing[0]
    selectable = [item for item in issues if item.get("selectable")]
    if selectable:
        return selectable[0]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Select next actionable YODA issue",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Agent runbook:\n"
            "- Purpose: resolve which issue should be worked next (or resumed) based on status/dependencies.\n"
            "- Use in YODA Framework: as an inspection helper when you need quick next-issue visibility,\n"
            "  especially before entering or resuming YODA Flow.\n"
            "- For deterministic phase execution and transitions, prefer yoda_flow_next.py."
        ),
    )
    add_global_flags(parser)
    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = resolve_dev(args.dev).strip()
        validate_slug(dev)
        index = load_issue_index(dev, ensure_flow_log=False)
        issues = list(index.get("issues", []))
        done_ids = {
            str(item.get("id", ""))
            for item in issues
            if item.get("status") == "done"
        }
        order_index = {str(item.get("id", "")): idx for idx, item in enumerate(issues)}
        issues = apply_dependency_order(issues, done_ids, order_index)
        pending = _collect_pending(issues)
        blocked = _collect_blocked(issues)

        selected = _pick_target(issues)
        if selected is None:
            payload = {
                "issue_id": "",
                "issue_path": "",
                "pending": pending,
                "blocked": blocked,
                "dry_run": bool(args.dry_run),
            }
            logging.error("No selectable issues found.")
            print(_render_output(payload, output_format))
            return ExitCode.NOT_FOUND

        issue_path = str(selected.get("path", ""))
        try:
            issue_path = str(Path(issue_path).resolve().relative_to(repo_root()))
        except Exception:
            pass

        payload = {
            "issue_id": str(selected.get("id", "")),
            "issue_path": issue_path,
            "pending": pending,
            "blocked": blocked,
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
