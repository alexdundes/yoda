#!/usr/bin/env python3
"""Resolve the next deterministic YODA Flow step from markdown issues."""

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
from lib.output import render_output
from lib.paths import repo_root
from lib.validate import validate_slug


BLOCKED_NO_SELECTABLE = "no_selectable_issue"
BLOCKED_ONLY_PENDING = "only_pending_issues"
BLOCKED_DEPENDENCY = "dependency_blocked"


RUNBOOK_BY_STEP = {
    "study": "Run Study: gather context, list open decisions, and wait for explicit approval.",
    "document": "Run Document: update issue text with approved decisions and request explicit approval.",
    "implement": "Run Implement: execute only approved scope and keep changes aligned with the issue.",
    "evaluate": "Run Evaluate: validate acceptance criteria, update Result log, and request final approval.",
}


def _relative(path_value: str) -> str:
    path = Path(path_value)
    try:
        return str(path.relative_to(repo_root()))
    except ValueError:
        return path_value


def _collect_pending(issues: list[dict[str, Any]]) -> list[dict[str, str]]:
    pending: list[dict[str, str]] = []
    for item in issues:
        if item.get("status") != "pending":
            continue
        pending.append(
            {
                "id": str(item.get("id", "")),
                "reason": "Issue is pending and not selectable.",
            }
        )
    return pending


def _collect_dependency_blocked(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blocked: list[dict[str, Any]] = []
    for item in issues:
        if item.get("status") != "to-do":
            continue
        deps = list(item.get("blocked_by", []))
        if deps:
            blocked.append({"id": str(item.get("id", "")), "depends_on": deps})
    return blocked


def _resolve_next_step(issue: dict[str, Any]) -> str:
    status = str(issue.get("status", ""))
    if status == "to-do":
        return "study"
    if status == "doing":
        phase = str(issue.get("phase") or "").strip().lower()
        if phase in RUNBOOK_BY_STEP:
            return phase
        return "study"
    return "blocked"


def _blocked_reason(pending: list[dict[str, str]], blocked: list[dict[str, Any]]) -> str:
    if blocked:
        return BLOCKED_DEPENDENCY
    if pending:
        return BLOCKED_ONLY_PENDING
    return BLOCKED_NO_SELECTABLE


def _blocked_message(code: str) -> str:
    if code == BLOCKED_DEPENDENCY:
        return "Blocked by unresolved dependencies. Use todo_update.py only if manual correction is needed."
    if code == BLOCKED_ONLY_PENDING:
        return "Only pending issues found. Resolve pending items before continuing flow."
    return "No selectable issue found for this developer slug."


def _pick_target(issues: list[dict[str, Any]]) -> dict[str, Any] | None:
    doing = [item for item in issues if item.get("status") == "doing"]
    if doing:
        return doing[0]
    selectable = [item for item in issues if item.get("selectable")]
    if selectable:
        return selectable[0]
    return None


def _render_md(payload: dict[str, Any]) -> list[str]:
    lines = [
        f"Issue ID: {payload['issue_id']}",
        f"Issue path: {payload['issue_path']}",
        f"Status: {payload['status']}",
        f"Phase: {payload['phase']}",
        f"Next step: {payload['next_step']}",
    ]
    blocked_reason = payload.get("blocked_reason", "")
    if blocked_reason:
        lines.append(f"Blocked reason: {blocked_reason}")
        lines.append(f"Blocked message: {payload.get('blocked_message', '')}")

    pending = payload.get("pending", [])
    if pending:
        lines.append("Pending issues:")
        for item in pending:
            lines.append(f"- {item['id']}: {item['reason']}")

    blocked = payload.get("blocked", [])
    if blocked:
        lines.append("Dependency blocked:")
        for item in blocked:
            deps = ", ".join(item.get("depends_on", []))
            lines.append(f"- {item.get('id', '')}: {deps}")

    lines.append("Runbook:")
    lines.append(f"- {payload['runbook_line']}")
    return lines


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    return render_output(payload, output_format, _render_md(payload))


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve next deterministic YODA Flow step")
    add_global_flags(parser)
    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = resolve_dev(args.dev).strip()
        validate_slug(dev)
        index = load_issue_index(dev, ensure_flow_log=False)
        issues = list(index.get("issues", []))
        pending = _collect_pending(issues)
        blocked = _collect_dependency_blocked(issues)

        selected = _pick_target(issues)
        if selected is None:
            blocked_reason = _blocked_reason(pending, blocked)
            payload = {
                "issue_id": "",
                "issue_path": "",
                "status": "",
                "phase": "",
                "next_step": "blocked",
                "blocked_reason": blocked_reason,
                "blocked_message": _blocked_message(blocked_reason),
                "runbook_line": "No flow step available. Resolve blockers and run again.",
                "pending": pending,
                "blocked": blocked,
            }
            print(_render_output(payload, output_format))
            return ExitCode.NOT_FOUND

        next_step = _resolve_next_step(selected)
        payload = {
            "issue_id": str(selected.get("id", "")),
            "issue_path": _relative(str(selected.get("path", ""))),
            "status": str(selected.get("status", "")),
            "phase": str(selected.get("phase") or ""),
            "next_step": next_step,
            "blocked_reason": "",
            "blocked_message": "",
            "runbook_line": RUNBOOK_BY_STEP.get(next_step, RUNBOOK_BY_STEP["study"]),
            "pending": pending,
            "blocked": blocked,
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

