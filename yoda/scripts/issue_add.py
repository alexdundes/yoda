#!/usr/bin/env python3
"""Create a new markdown issue in schema 2.00."""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.error_messages import conflict_issue_file, required_flag
from lib.errors import ExitCode, YodaError
from lib.external_issue_utils import detect_origin_url, parse_origin, provider_from_host
from lib.flow_log import append_flow_log_line, sanitize_flow_message
from lib.front_matter import render_issue
from lib.io import write_text_atomic
from lib.issue_metadata import canonicalize_issue_metadata
from lib.issue_utils import find_issue_files_by_id
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.paths import issue_path, repo_root, template_path
from lib.slug_utils import generate_issue_slug
from lib.templates import load_template
from lib.time_utils import detect_local_timezone, now_iso
from lib.validate import validate_slug


LOCK_RETRIES = 3
LOCK_BASE_WAIT_SECONDS = 0.1


def _lock_path(dev: str) -> Path:
    return repo_root() / "yoda" / "locks" / f"issue_add.{dev}.lock"


@contextmanager
def _issue_add_lock(dev: str) -> Any:
    lock_file = _lock_path(dev)
    lock_file.parent.mkdir(parents=True, exist_ok=True)
    acquired = False
    for attempt in range(1, LOCK_RETRIES + 1):
        try:
            fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(f"pid={os.getpid()}\n")
                handle.write(f"attempt={attempt}\n")
            acquired = True
            break
        except FileExistsError:
            if attempt == LOCK_RETRIES:
                raise YodaError(
                    f"Failed to acquire issue_add lock for dev '{dev}' after {LOCK_RETRIES} attempts: {lock_file}",
                    exit_code=ExitCode.CONFLICT,
                )
            time.sleep(LOCK_BASE_WAIT_SECONDS * attempt)
    if not acquired:
        raise YodaError("Unexpected lock acquisition failure", exit_code=ExitCode.ERROR)
    try:
        yield
    finally:
        lock_file.unlink(missing_ok=True)


def _resolve_extern_issue_file(extern_issue: str | None) -> str:
    external_id = (extern_issue or "").strip()
    if not external_id:
        return ""
    if not external_id.isdigit():
        raise YodaError("--extern-issue must be numeric (NNN).", exit_code=ExitCode.VALIDATION)
    origin_url = detect_origin_url()
    host, _ = parse_origin(origin_url)
    provider = provider_from_host(host)
    return f"../extern_issues/{provider}-{external_id}.json"


def _next_issue_id(dev: str) -> str:
    max_num = 0
    for path in sorted((repo_root() / "yoda" / "project" / "issues").glob(f"{dev}-*.md")):
        parts = path.stem.split("-")
        if len(parts) < 3:
            continue
        if parts[0] != dev:
            continue
        try:
            num = int(parts[1])
        except ValueError:
            continue
        max_num = max(max_num, num)
    return f"{dev}-{max_num + 1:04d}"


def _build_issue_item(
    issue_id: str,
    title: str,
    description: str,
    priority: int,
    extern_issue_file: str,
    timestamp: str,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "schema_version": "2.00",
        "id": issue_id,
        "status": "to-do",
        "depends_on": [],
        "title": title,
        "description": description,
        "priority": priority,
        "extern_issue_file": extern_issue_file,
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    return canonicalize_issue_metadata(item)


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    lines = [
        f"Issue ID: {payload['issue_id']}",
        f"Issue path: {payload['issue_path']}",
        f"Template: {payload['template']}",
    ]
    return render_output(payload, output_format, lines, dry_run=bool(payload.get("dry_run")))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new issue",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Agent guidance:\n"
            "- Purpose: create a new issue markdown with canonical front matter and initial flow log entry.\n"
            "- When to use: during YODA Intake after backlog review and issue structuring.\n"
            "- Mutability: writes a new file in yoda/project/issues/.\n\n"
            "Required input: --title and (--description or --summary).\n"
            "Use --extern-issue <NNN> to link an external source.\n"
            "Priority default is 5; change only with explicit relative justification."
        ),
    )
    add_global_flags(parser)
    parser.add_argument("--title", required=False, help="Issue title")
    parser.add_argument("--description", required=False, help="Issue description")
    parser.add_argument("--summary", required=False, help="Alias for description")
    parser.add_argument("--slug", required=False, help="Explicit issue slug")
    parser.add_argument("--priority", type=int, default=None, help="Priority 0-10")
    parser.add_argument("--extern-issue", dest="extern_issue", help="External issue number (NNN)")

    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = resolve_dev(args.dev).strip()
        validate_slug(dev)
        title = (args.title or "").strip()
        if not title:
            required_flag("--title")
        description = (args.summary or args.description or "").strip()
        if not description:
            required_flag("--description")
        priority = args.priority if args.priority is not None else 5
        if not isinstance(priority, int) or not (0 <= priority <= 10):
            raise YodaError("priority must be between 0 and 10", exit_code=ExitCode.VALIDATION)
        extern_issue_file = _resolve_extern_issue_file(args.extern_issue)

        slug = args.slug.strip() if args.slug else generate_issue_slug(title)
        validate_slug(slug)
        template_file = template_path()
        template_text = load_template(template_file)

        with _issue_add_lock(dev):
            issue_id = _next_issue_id(dev)
            if find_issue_files_by_id(issue_id):
                raise YodaError(f"Issue id already exists: {issue_id}", exit_code=ExitCode.CONFLICT)
            issue_file = issue_path(issue_id, slug)
            if issue_file.exists():
                conflict_issue_file(issue_file)

            timestamp = now_iso(detect_local_timezone())
            issue_metadata = _build_issue_item(
                issue_id=issue_id,
                title=title,
                description=description,
                priority=priority,
                extern_issue_file=extern_issue_file,
                timestamp=timestamp,
            )
            rendered_issue = render_issue(
                template_text,
                metadata=issue_metadata,
                replacements={
                    "[ID]": issue_id,
                    "[TITLE]": title,
                    "[SUMMARY]": description,
                    "[CREATED_AT]": timestamp,
                    "[UPDATED_AT]": timestamp,
                },
            )

            payload = {
                "issue_id": issue_id,
                "issue_path": str(issue_file.relative_to(repo_root())),
                "template": str(template_file.relative_to(repo_root())),
                "dry_run": bool(args.dry_run),
            }

            if not args.dry_run:
                write_text_atomic(issue_file, rendered_issue)
                message = sanitize_flow_message(
                    f"issue_add created title={title}; priority={priority}"
                )
                append_flow_log_line(issue_file, f"{timestamp} {message}")

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
