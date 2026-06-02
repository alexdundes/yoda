#!/usr/bin/env python3
"""Run YODA Prep Flow for one issue without entering implementation."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any

import frontmatter

from lib.cli import add_global_flags, resolve_format
from lib.errors import ExitCode, YodaError
from lib.flow_log import append_flow_log_line, sanitize_flow_message
from lib.front_matter import update_front_matter
from lib.issue_metadata import canonicalize_issue_metadata
from lib.issue_utils import resolve_issue_file_by_id
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.paths import repo_root
from lib.time_utils import detect_local_timezone, now_iso
from lib.validate import validate_issue_id, validate_slug


ALLOWED_PREPARED_UNTIL = {"", "study", "document"}
NEXT_PREP_STEP = {"": "study", "study": "document", "document": "document"}
RUNBOOK_BY_STEP = {
    "study": "Run Prep Study: gather context and list open decisions for this issue; do not implement.",
    "document": "Run Prep Document: update issue text with approved decisions; do not implement.",
}


def _relative(path_value: Path) -> str:
    try:
        return str(path_value.relative_to(repo_root()))
    except ValueError:
        return str(path_value)


def _now_ts() -> str:
    return now_iso(detect_local_timezone())


def _load_issue(issue_id: str) -> tuple[Path, dict[str, Any]]:
    issue_path = resolve_issue_file_by_id(issue_id)
    post = frontmatter.load(str(issue_path))
    metadata = dict(post.metadata)
    schema_version = str(metadata.get("schema_version", "")).strip()
    if schema_version != "2.00":
        raise YodaError(
            f"Unsupported schema_version '{schema_version}'. Run init.py migration first.",
            exit_code=ExitCode.VALIDATION,
        )
    return issue_path, metadata


def _prepared_until(metadata: dict[str, Any]) -> str:
    prepared = str(metadata.get("flow_prepared_until") or "").strip().lower()
    if prepared not in ALLOWED_PREPARED_UNTIL:
        raise YodaError(
            f"Invalid flow_prepared_until '{prepared}'. Expected study or document.",
            exit_code=ExitCode.VALIDATION,
        )
    return prepared


def _append_log(issue_path: Path, message: str, dry_run: bool) -> str:
    timestamp = _now_ts()
    if not dry_run:
        append_flow_log_line(issue_path, f"{timestamp} {sanitize_flow_message(message)}")
    return timestamp


def _apply_prep_step(issue_path: Path, metadata: dict[str, Any], dry_run: bool) -> dict[str, Any]:
    status = str(metadata.get("status", "")).strip()
    if status == "done":
        raise YodaError("YODA Prep Flow cannot run on done issues.", exit_code=ExitCode.VALIDATION)

    current = _prepared_until(metadata)
    next_step = NEXT_PREP_STEP[current]
    timestamp = _now_ts()

    updated = dict(metadata)
    updated["status"] = "to-do"
    updated.pop("phase", None)
    updated["flow_prepared_until"] = next_step
    updated["updated_at"] = timestamp
    normalized = canonicalize_issue_metadata(updated)

    if not dry_run:
        update_front_matter(issue_path, normalized)

    if current == "document":
        log_message = "prep already prepared_until=document"
    else:
        log_message = f"prep transition prepared_until={current or 'none'}->{next_step}"
    log_timestamp = _append_log(issue_path, log_message, dry_run)

    return {
        "status": "to-do",
        "phase": "",
        "flow_prepared_until": next_step,
        "next_step": next_step,
        "runbook_line": RUNBOOK_BY_STEP[next_step],
        "log_timestamp": log_timestamp,
    }


def _render_md(payload: dict[str, Any]) -> list[str]:
    lines = [
        f"Issue ID: {payload['issue_id']}",
        f"Issue path: {payload['issue_path']}",
        f"Status: {payload['status']}",
        f"Flow prepared until: {payload['flow_prepared_until']}",
        f"Next step: {payload['next_step']}",
    ]
    if payload.get("log_timestamp"):
        lines.append(f"Log timestamp: {payload['log_timestamp']}")
    lines.append("Runbook:")
    lines.append(f"- {payload['runbook_line']}")
    return lines


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    return render_output(payload, output_format, _render_md(payload), dry_run=bool(payload.get("dry_run")))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run YODA Prep Flow for one issue",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Agent guidance:\n"
            "- Purpose: prepare Study/Document for one issue without entering implementation.\n"
            "- Use in YODA Framework: run this when the human explicitly enters YODA Prep Flow.\n"
            "- Selection: requires --issue and ignores backlog order/dependencies for preparation only.\n"
            "- Expected moment: call once per prep step, execute returned Study/Document instructions,\n"
            "  then call again after explicit human authorization to continue.\n"
            "- Result: after Document, the issue remains to-do with flow_prepared_until=document;\n"
            "  YODA Flow later starts it directly in Implement."
        ),
    )
    add_global_flags(parser)
    parser.add_argument("--issue", required=False, help="Issue id (dev-####)")

    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = (args.dev or "").strip()
        if not dev:
            raise YodaError(
                "--dev is required. Use the developer slug prefix from issue filenames <dev>-<NNNN>-<slug>.md.",
                exit_code=ExitCode.VALIDATION,
            )
        validate_slug(dev)
        issue_id = (args.issue or "").strip()
        if not issue_id:
            raise YodaError("--issue is required", exit_code=ExitCode.VALIDATION)
        validate_issue_id(issue_id, dev)

        issue_path, metadata = _load_issue(issue_id)
        transition = _apply_prep_step(issue_path, metadata, bool(args.dry_run))
        payload = {
            "issue_id": issue_id,
            "issue_path": _relative(issue_path),
            "status": transition["status"],
            "phase": transition["phase"],
            "flow_prepared_until": transition["flow_prepared_until"],
            "next_step": transition["next_step"],
            "runbook_line": transition["runbook_line"],
            "log_timestamp": transition["log_timestamp"],
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
