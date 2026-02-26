#!/usr/bin/env python3
"""Create a new issue entry and issue Markdown file."""

from __future__ import annotations

import argparse
import logging
import os
import re
import sys
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.errors import ExitCode, YodaError
from lib.error_messages import (
    conflict_issue_file,
    conflict_issue_id,
    conflict_log_file,
    required_flag,
)
from lib.external_issue_utils import detect_origin_url, parse_origin, provider_from_host
from lib.front_matter import render_issue
from lib.io import write_text_atomic
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.paths import issue_path, log_path, repo_root, template_path, todo_path
from lib.templates import load_template
from lib.time_utils import detect_local_timezone, now_iso
from lib.validate import (
    ISSUE_ID_RE,
    SLUG_RE,
    validate_slug,
    validate_todo,
    validate_todo_root,
)
from lib.yaml_io import read_yaml, write_yaml_atomic


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


def _create_default_todo(dev: str) -> dict[str, Any]:
    timezone = detect_local_timezone()
    return {
        "schema_version": "1.01",
        "developer_name": dev.title(),
        "developer_slug": dev,
        "timezone": timezone,
        "updated_at": now_iso(timezone),
        "issues": [],
    }


def _next_issue_id(dev: str, issues: list[dict[str, Any]]) -> str:
    max_num = 0
    for item in issues:
        issue_id = str(item.get("id", ""))
        match = ISSUE_ID_RE.match(issue_id)
        if not match:
            continue
        if not issue_id.startswith(f"{dev}-"):
            continue
        try:
            num = int(issue_id.split("-")[-1])
        except ValueError:
            continue
        max_num = max(max_num, num)
    return f"{dev}-{max_num + 1:04d}"


def _generate_slug(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not slug:
        slug = "issue"
    if not slug[0].isalpha():
        slug = f"issue-{slug}"
    return slug


def _build_issue_item(
    issue_id: str,
    title: str,
    slug: str,
    description: str,
    priority: int,
    origin: dict[str, str],
    timestamp: str,
) -> dict[str, Any]:
    return {
        "schema_version": "1.01",
        "id": issue_id,
        "title": title,
        "slug": slug,
        "description": description,
        "status": "to-do",
        "priority": priority,
        "depends_on": [],
        "pending_reason": "",
        "created_at": timestamp,
        "updated_at": timestamp,
        "origin": origin,
    }


def _build_log(
    issue_id: str,
    issue_path_str: str,
    status: str,
    timestamp: str,
    message: str,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "issue_id": issue_id,
        "issue_path": issue_path_str,
        "todo_id": issue_id,
        "status": status,
        "entries": [
            {
                "timestamp": timestamp,
                "message": message,
            }
        ],
    }


def _flag_present(flag: str) -> bool:
    return any(arg == flag or arg.startswith(f"{flag}=") for arg in sys.argv)


def _build_issue_log_message(
    issue_id: str,
    title: str,
    description: str,
    slug: str,
    priority: int,
) -> str:
    lines = [f"[{issue_id}] issue_add created"]
    lines.append(f"title: {title}")
    lines.append(f"description: {description}")
    lines.append(f"slug: {slug}")

    if _flag_present("--priority"):
        lines.append(f"priority: {priority}")
    if _flag_present("--extern-issue"):
        lines.append("origin: external issue linked")

    return "\n".join(lines)


def _resolve_origin(extern_issue: str | None, origin_system: str | None, origin_requester: str | None) -> dict[str, str]:
    system = (origin_system or "").strip().lower()
    external_id = (extern_issue or "").strip()
    requester = (origin_requester or "").strip()

    if not external_id:
        return {"system": system, "external_id": "", "requester": requester}
    if not external_id.isdigit():
        raise YodaError("--extern-issue must be numeric (NNN).", exit_code=ExitCode.VALIDATION)
    if not system:
        try:
            origin_url = detect_origin_url()
            host, _ = parse_origin(origin_url)
            system = provider_from_host(host)
        except YodaError as exc:
            raise YodaError(
                f"Could not infer origin system for --extern-issue {external_id}. Use --origin-system.",
                exit_code=exc.exit_code,
            ) from exc
    return {"system": system, "external_id": external_id, "requester": requester}


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    lines = [
        f"Issue ID: {payload['issue_id']}",
        f"Issue path: {payload['issue_path']}",
        f"TODO path: {payload['todo_path']}",
        f"Log path: {payload['log_path']}",
        f"Template: {payload['template']}",
    ]
    return render_output(
        payload,
        output_format,
        lines,
        dry_run=bool(payload.get("dry_run")),
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a new issue",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Required input: --title and (--description or --summary).\n"
            "Use --extern-issue <NNN> to link an external source.\n"
            "Optional origin fields: --origin-system and --origin-requester.\n"
            "Priority default is 5; change it only with justified higher/lower importance versus other open issues."
        ),
    )
    add_global_flags(parser)
    parser.add_argument("--title", required=False, help="Issue title")
    parser.add_argument("--description", required=False, help="Issue description")
    parser.add_argument("--summary", required=False, help="Alias for description")
    parser.add_argument("--slug", required=False, help="Explicit issue slug")
    parser.add_argument("--priority", type=int, default=None, help="Priority 0-10")
    parser.add_argument("--extern-issue", dest="extern_issue", help="External issue number (NNN)")
    parser.add_argument("--origin-system", dest="origin_system", help="Origin system (github/gitlab)")
    parser.add_argument("--origin-requester", dest="origin_requester", help="Origin requester")

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
        origin = _resolve_origin(args.extern_issue, args.origin_system, args.origin_requester)

        slug = args.slug.strip() if args.slug else _generate_slug(title)
        validate_slug(slug)

        template_file = template_path()
        template_text = load_template(template_file)
        with _issue_add_lock(dev):
            todo_file = todo_path(dev)
            if todo_file.exists():
                todo = read_yaml(todo_file)
            else:
                todo = _create_default_todo(dev)

            validate_todo_root(todo, dev)

            issue_id = _next_issue_id(dev, todo.get("issues", []))
            issues = list(todo.get("issues", []))
            if any(item.get("id") == issue_id for item in issues):
                conflict_issue_id(issue_id)

            issue_file = issue_path(issue_id, slug)
            log_file = log_path(issue_id, slug)
            if issue_file.exists():
                conflict_issue_file(issue_file)
            if log_file.exists():
                conflict_log_file(log_file)

            timestamp = now_iso(todo.get("timezone"))
            issue_item = _build_issue_item(
                issue_id=issue_id,
                title=title,
            slug=slug,
            description=description,
            priority=priority,
            origin=origin,
            timestamp=timestamp,
        )

            issues.append(issue_item)
            todo["issues"] = issues
            todo["updated_at"] = timestamp
            validate_todo(todo, dev)

            issue_metadata = issue_item.copy()
            issue_metadata.pop("schema_version", None)
            issue_metadata["schema_version"] = "1.01"

            rendered_issue = render_issue(
                template_text,
                metadata=issue_metadata,
                replacements={
                    "[ID]": issue_id,
                    "[TITLE]": title,
                    "[SLUG]": slug,
                    "[SUMMARY]": description,
                    "[CREATED_AT]": timestamp,
                    "[UPDATED_AT]": timestamp,
                },
            )

            log_payload = _build_log(
                issue_id=issue_id,
                issue_path_str=str(issue_file.relative_to(repo_root())),
                status="to-do",
                timestamp=timestamp,
                message=_build_issue_log_message(
                    issue_id=issue_id,
                    title=title,
                    description=description,
                    slug=slug,
                    priority=priority,
                ),
            )

            payload = {
                "issue_id": issue_id,
                "issue_path": str(issue_file.relative_to(repo_root())),
                "todo_path": str(todo_file.relative_to(repo_root())),
                "log_path": str(log_file.relative_to(repo_root())),
                "template": str(template_file.relative_to(repo_root())),
                "dry_run": bool(args.dry_run),
            }

            if not args.dry_run:
                write_text_atomic(issue_file, rendered_issue)
                write_yaml_atomic(log_file, log_payload)
                write_yaml_atomic(todo_file, todo)

        print(_render_output(payload, output_format))
        return ExitCode.SUCCESS
    except YodaError as exc:
        logging.error(str(exc))
        return exc.exit_code
    except Exception as exc:  # pragma: no cover - catch-all
        logging.error("Unexpected error: %s", exc)
        return ExitCode.ERROR


if __name__ == "__main__":
    sys.exit(main())
