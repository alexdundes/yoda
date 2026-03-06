#!/usr/bin/env python3
"""Update issue front matter fields in markdown source-of-truth."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Any

import frontmatter

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.errors import ExitCode, YodaError
from lib.external_issue_utils import detect_origin_url, parse_origin, provider_from_host
from lib.flow_log import append_flow_log_line, sanitize_flow_message
from lib.front_matter import update_front_matter
from lib.issue_metadata import canonicalize_issue_metadata, prune_empty_optionals
from lib.issue_utils import issue_slug_from_path, resolve_issue_file_by_id
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.paths import repo_root
from lib.slug_utils import generate_issue_slug
from lib.time_utils import detect_local_timezone, now_iso
from lib.validate import validate_issue_id, validate_slug


ALLOWED_STATUS = {"to-do", "doing", "done", "pending"}
ALLOWED_PHASE = {"study", "document", "implement", "evaluate"}


def _parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _format_value(value: Any) -> str:
    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "[]"
    return "" if value is None else str(value)


def _diff_fields(before: dict[str, Any], after: dict[str, Any]) -> tuple[list[str], list[str]]:
    fields = [
        "title",
        "description",
        "status",
        "phase",
        "priority",
        "depends_on",
        "pending_reason",
        "extern_issue_file",
    ]
    updated_fields: list[str] = []
    lines: list[str] = []
    for field in fields:
        before_val = before.get(field)
        after_val = after.get(field)
        if before_val != after_val:
            updated_fields.append(field)
            lines.append(f"{field}: {_format_value(before_val)} -> {_format_value(after_val)}")
    return updated_fields, lines


def _update_issue(item: dict[str, Any], args: argparse.Namespace) -> None:
    if args.extern_issue_file is not None and args.clear_extern_issue_file:
        raise YodaError(
            "Use either --extern-issue-file or --clear-extern-issue-file, not both.",
            exit_code=ExitCode.VALIDATION,
        )
    if args.extern_issue is not None and args.clear_extern_issue_file:
        raise YodaError(
            "Use either --extern-issue or --clear-extern-issue-file, not both.",
            exit_code=ExitCode.VALIDATION,
        )
    if args.extern_issue is not None and args.extern_issue_file is not None:
        raise YodaError(
            "Use either --extern-issue or --extern-issue-file, not both.",
            exit_code=ExitCode.VALIDATION,
        )

    if args.status is not None:
        if args.status not in ALLOWED_STATUS:
            raise YodaError("Invalid status", exit_code=ExitCode.VALIDATION)
        item["status"] = args.status

    if args.phase is not None:
        phase = args.phase.strip().lower()
        if phase not in ALLOWED_PHASE:
            raise YodaError("Invalid phase", exit_code=ExitCode.VALIDATION)
        item["phase"] = phase

    if args.priority is not None:
        if args.priority < 0 or args.priority > 10:
            raise YodaError("priority must be between 0 and 10", exit_code=ExitCode.VALIDATION)
        item["priority"] = args.priority

    if args.title is not None:
        title = args.title.strip()
        if not title:
            raise YodaError("title cannot be empty", exit_code=ExitCode.VALIDATION)
        item["title"] = title

    if args.description is not None:
        description = args.description.strip()
        if not description:
            raise YodaError("description cannot be empty", exit_code=ExitCode.VALIDATION)
        item["description"] = description

    if args.clear_depends_on:
        item["depends_on"] = []
    elif args.depends_on is not None:
        item["depends_on"] = _parse_csv(args.depends_on)

    if args.pending_reason is not None:
        item["pending_reason"] = args.pending_reason.strip()

    if args.clear_extern_issue_file:
        item["extern_issue_file"] = ""
    elif args.extern_issue is not None:
        external_id = str(args.extern_issue).strip()
        if not external_id.isdigit():
            raise YodaError("--extern-issue must be numeric (NNN).", exit_code=ExitCode.VALIDATION)
        origin_url = detect_origin_url()
        host, _ = parse_origin(origin_url)
        provider = provider_from_host(host)
        item["extern_issue_file"] = f"../extern_issues/{provider}-{external_id}.json"
    elif args.extern_issue_file is not None:
        item["extern_issue_file"] = args.extern_issue_file.strip()


def _apply_pending_rules(item: dict[str, Any], pending_reason_provided: bool) -> None:
    status = item.get("status")
    if status == "pending":
        if not item.get("pending_reason"):
            raise YodaError("pending_reason required for pending status", exit_code=ExitCode.VALIDATION)
    else:
        if not pending_reason_provided and item.get("pending_reason"):
            item["pending_reason"] = ""
    prune_empty_optionals(item)


def _apply_phase_rules(item: dict[str, Any]) -> None:
    if item.get("status") == "doing":
        phase = str(item.get("phase") or "").strip().lower()
        if phase:
            item["phase"] = phase
        else:
            item.pop("phase", None)
        return
    item.pop("phase", None)


def _resolve_target_slug(args: argparse.Namespace, current_slug: str) -> str:
    if args.slug is not None:
        slug = args.slug.strip()
        if not slug:
            raise YodaError("slug cannot be empty", exit_code=ExitCode.VALIDATION)
        return slug
    if args.title is not None:
        return generate_issue_slug(args.title.strip())
    return current_slug


def _append_issue_log(issue_path: Path, issue_id: str, lines: list[str], dry_run: bool) -> str:
    timestamp = now_iso(detect_local_timezone())
    if lines:
        message = sanitize_flow_message(f"{issue_id}: todo_update " + "; ".join(lines))
    else:
        message = f"{issue_id}: todo_update no changes"
    if not dry_run:
        append_flow_log_line(issue_path, f"{timestamp} {message}")
    return timestamp


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    lines = [
        f"Issue ID: {payload['issue_id']}",
        f"Updated fields: {', '.join(payload['updated_fields']) if payload['updated_fields'] else '(none)'}",
        f"Issue path: {payload['issue_path']}",
    ]
    return render_output(payload, output_format, lines, dry_run=bool(payload.get("dry_run")))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Update issue fields",
        epilog=(
            "Use this command for manual semantic/process corrections.\n"
            "Supports status/phase updates while keeping phase only for status=doing."
        ),
    )
    add_global_flags(parser)
    parser.add_argument("--issue", required=False, help="Issue id (dev-####)")
    parser.add_argument("--status", help="New status")
    parser.add_argument("--phase", help="New phase (study|document|implement|evaluate)")
    parser.add_argument("--priority", type=int, help="Priority 0-10")
    parser.add_argument("--title", help="New title")
    parser.add_argument("--description", help="New description")
    parser.add_argument("--slug", help="Override slug used in issue filename")
    parser.add_argument("--depends-on", dest="depends_on", help="Comma-separated issue ids")
    parser.add_argument("--pending-reason", dest="pending_reason", help="Pending reason")
    parser.add_argument("--clear-depends-on", action="store_true", help="Clear dependencies")
    parser.add_argument(
        "--extern-issue-file",
        dest="extern_issue_file",
        help="Relative path to external issue JSON (example: ../extern_issues/github-2.json)",
    )
    parser.add_argument(
        "--extern-issue",
        dest="extern_issue",
        help="External issue number (NNN); generates extern_issue_file automatically",
    )
    parser.add_argument("--clear-extern-issue-file", action="store_true", help="Clear extern_issue_file")

    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = resolve_dev(args.dev).strip()
        validate_slug(dev)
        issue_id = (args.issue or "").strip()
        if not issue_id:
            raise YodaError("--issue is required", exit_code=ExitCode.VALIDATION)
        validate_issue_id(issue_id, dev)

        issue_file = resolve_issue_file_by_id(issue_id)
        current_slug = issue_slug_from_path(issue_file, issue_id)
        post = frontmatter.load(str(issue_file))
        metadata = dict(post.metadata)
        schema_version = str(metadata.get("schema_version", "")).strip()
        if schema_version != "2.00":
            raise YodaError(
                f"Unsupported schema_version '{schema_version}'. Run init.py migration first.",
                exit_code=ExitCode.VALIDATION,
            )

        before_item = dict(metadata)
        _update_issue(metadata, args)
        _apply_pending_rules(metadata, args.pending_reason is not None)
        _apply_phase_rules(metadata)
        metadata["updated_at"] = now_iso(detect_local_timezone())
        metadata["schema_version"] = "2.00"
        normalized = canonicalize_issue_metadata(metadata)

        target_slug = _resolve_target_slug(args, current_slug)
        target_issue_file = issue_file.with_name(f"{issue_id}-{target_slug}.md")
        if target_issue_file != issue_file and target_issue_file.exists():
            raise YodaError(f"Issue file already exists: {target_issue_file}", exit_code=ExitCode.CONFLICT)

        updated_fields, log_lines = _diff_fields(before_item, normalized)
        payload = {
            "issue_id": issue_id,
            "updated_fields": updated_fields,
            "issue_path": str(target_issue_file.relative_to(repo_root())),
            "dry_run": bool(args.dry_run),
        }

        if not args.dry_run:
            if target_issue_file != issue_file:
                issue_file.rename(target_issue_file)
                issue_file = target_issue_file
            update_front_matter(issue_file, normalized)
            _append_issue_log(issue_file, issue_id, log_lines, args.dry_run)

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
