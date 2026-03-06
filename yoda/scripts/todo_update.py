#!/usr/bin/env python3
"""Update fields in yoda/todos/TODO.<dev>.yaml."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

import frontmatter

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.error_messages import required_flag
from lib.errors import ExitCode, YodaError
from lib.external_issue_utils import detect_origin_url, parse_origin, provider_from_host
from lib.front_matter import render_issue_document, update_front_matter
from lib.io import write_text_atomic
from lib.issue_utils import (
    issue_slug_from_path,
    resolve_issue_file_by_id,
    resolve_log_file_by_id,
)
from lib.issue_metadata import canonicalize_issue_metadata, prune_empty_optionals
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.paths import log_path, repo_root, todo_path
from lib.slug_utils import generate_issue_slug
from lib.time_utils import now_iso
from lib.todo_utils import find_issue, load_todo_file
from lib.validate import validate_issue_id, validate_slug, validate_todo
from lib.yaml_io import write_yaml


ALLOWED_STATUS = {"to-do", "doing", "done", "pending"}
ALLOWED_PHASE = {"study", "document", "implement", "evaluate"}


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
        item["pending_reason"] = args.pending_reason

    if args.clear_extern_issue_file:
        item["extern_issue_file"] = ""
    elif args.extern_issue is not None:
        external_id = str(args.extern_issue).strip()
        if not external_id.isdigit():
            raise YodaError("--extern-issue must be numeric (NNN).", exit_code=ExitCode.VALIDATION)
        try:
            origin_url = detect_origin_url()
            host, _ = parse_origin(origin_url)
            provider = provider_from_host(host)
        except YodaError as exc:
            raise YodaError(
                f"Could not infer provider for --extern-issue {external_id}. Check git remote origin.",
                exit_code=exc.exit_code,
            ) from exc
        item["extern_issue_file"] = f"../extern_issues/{provider}-{external_id}.json"
    elif args.extern_issue_file is not None:
        item["extern_issue_file"] = args.extern_issue_file


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


def _resolve_target_slug(args: argparse.Namespace, current_slug: str) -> str:
    if args.slug is not None:
        slug = args.slug.strip()
        if not slug:
            raise YodaError("slug cannot be empty", exit_code=ExitCode.VALIDATION)
        return slug
    if args.title is not None:
        return generate_issue_slug(args.title.strip())
    return current_slug


def _prepare_renamed_issue_file(
    issue_file: Path,
    issue_id: str,
    target_slug: str,
    metadata: dict[str, Any],
) -> tuple[Path, bool]:
    target_issue_file = issue_file.with_name(f"{issue_id}-{target_slug}.md")
    renamed = target_issue_file != issue_file
    if renamed and target_issue_file.exists():
        raise YodaError(
            f"Issue file already exists: {target_issue_file}",
            exit_code=ExitCode.CONFLICT,
        )
    if not renamed:
        return issue_file, False

    post = frontmatter.load(str(issue_file))
    rendered = render_issue_document(post.content, metadata)
    write_text_atomic(target_issue_file, rendered)
    issue_file.unlink(missing_ok=True)
    return target_issue_file, True


def _prepare_renamed_log_file(issue_id: str, target_slug: str, dry_run: bool) -> None:
    if dry_run:
        return
    current_log = resolve_log_file_by_id(issue_id)
    if current_log is None:
        return
    target_log = log_path(issue_id, target_slug)
    if target_log == current_log:
        return
    if target_log.exists():
        raise YodaError(
            f"Log file already exists: {target_log}",
            exit_code=ExitCode.CONFLICT,
        )
    os.replace(current_log, target_log)


def main() -> int:
    parser = argparse.ArgumentParser(description="Update TODO issue fields")
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
    parser.add_argument(
        "--clear-extern-issue-file",
        action="store_true",
        help="Clear extern_issue_file",
    )

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
        issue_file = resolve_issue_file_by_id(issue_id)
        current_slug = issue_slug_from_path(issue_file, issue_id)

        before_item = deepcopy(issue_item)
        _update_issue(issue_item, args)
        pending_reason_provided = args.pending_reason is not None
        _apply_pending_rules(issue_item, pending_reason_provided)
        _apply_phase_rules(issue_item)
        target_slug = _resolve_target_slug(args, current_slug)
        normalized_issue = canonicalize_issue_metadata(issue_item)
        issue_item.clear()
        issue_item.update(normalized_issue)

        timestamp = now_iso(todo.get("timezone"))
        issue_item["updated_at"] = timestamp
        todo["updated_at"] = timestamp

        validate_todo(todo, dev)

        updated_fields, log_lines = _diff_fields(before_item, issue_item)
        payload = {
            "issue_id": issue_id,
            "updated_fields": updated_fields,
            "todo_path": str(todo_file.relative_to(repo_root())),
            "dry_run": bool(args.dry_run),
        }

        if not args.dry_run:
            _prepare_renamed_log_file(issue_id, target_slug, args.dry_run)
            new_issue_file, renamed = _prepare_renamed_issue_file(
                issue_file=issue_file,
                issue_id=issue_id,
                target_slug=target_slug,
                metadata=issue_item,
            )
            write_yaml(todo_file, todo)
            if not renamed:
                update_front_matter(new_issue_file, issue_item)
            if log_lines:
                log_message = f"{issue_id}: todo_update " + "; ".join(log_lines)
            else:
                log_message = f"{issue_id}: todo_update no changes"
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
