#!/usr/bin/env python3
"""Create a new issue entry and issue Markdown file."""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

from lib.cli import add_global_flags, resolve_format
from lib.errors import ExitCode, YodaError
from lib.front_matter import render_issue
from lib.io import write_text
from lib.paths import issue_path, log_path, repo_root, template_path, todo_path
from lib.templates import load_template
from lib.validate import (
    ALLOWED_ENTRY_TYPES,
    ISSUE_ID_RE,
    SLUG_RE,
    validate_slug,
    validate_todo,
    validate_todo_root,
)
from lib.yaml_io import read_yaml, write_yaml


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


def _is_valid_timezone(name: str) -> bool:
    try:
        ZoneInfo(name)
        return True
    except Exception:
        return False


def _detect_local_timezone() -> str:
    tz_env = os.environ.get("TZ")
    if tz_env and _is_valid_timezone(tz_env):
        return tz_env

    localtime = Path("/etc/localtime")
    try:
        if localtime.exists():
            target = localtime.resolve()
            parts = target.parts
            if "zoneinfo" in parts:
                idx = parts.index("zoneinfo")
                candidate = "/".join(parts[idx + 1 :])
                if candidate and _is_valid_timezone(candidate):
                    return candidate
    except Exception:
        pass

    return "UTC"


def _create_default_todo(dev: str) -> dict[str, Any]:
    timezone = _detect_local_timezone()
    return {
        "schema_version": "1.0",
        "developer_name": dev.title(),
        "developer_slug": dev,
        "timezone": timezone,
        "updated_at": _now_iso(timezone),
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


def _parse_entrypoints(values: list[str]) -> list[dict[str, str]]:
    entrypoints: list[dict[str, str]] = []
    for raw in values:
        if ":" not in raw:
            raise YodaError("Entry point must be <path>:<type>", exit_code=ExitCode.VALIDATION)
        path, entry_type = raw.split(":", 1)
        if entry_type not in ALLOWED_ENTRY_TYPES:
            raise YodaError("Invalid entrypoint type", exit_code=ExitCode.VALIDATION)
        entrypoints.append({"path": path, "type": entry_type})
    return entrypoints


def _parse_tags(value: str | None) -> list[str]:
    if not value:
        return []
    return [tag.strip() for tag in value.split(",") if tag.strip()]


def _build_issue_item(
    issue_id: str,
    title: str,
    slug: str,
    description: str,
    priority: int,
    lightweight: bool,
    agent: str,
    entrypoints: list[dict[str, str]],
    tags: list[str],
    timestamp: str,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "id": issue_id,
        "title": title,
        "slug": slug,
        "description": description,
        "status": "to-do",
        "priority": priority,
        "lightweight": lightweight,
        "agent": agent,
        "depends_on": [],
        "pending_reason": "",
        "created_at": timestamp,
        "updated_at": timestamp,
        "entrypoints": entrypoints,
        "tags": tags,
        "origin": {"system": "", "external_id": "", "requester": ""},
    }


def _build_log(issue_id: str, issue_path_str: str, status: str, timestamp: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "issue_id": issue_id,
        "issue_path": issue_path_str,
        "todo_id": issue_id,
        "status": status,
        "entries": [
            {
                "timestamp": timestamp,
                "message": f"[{issue_id}] Issue created",
            }
        ],
    }


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    if output_format == "json":
        return json.dumps(payload, indent=2, ensure_ascii=True)
    lines = [
        f"Issue ID: {payload['issue_id']}",
        f"Issue path: {payload['issue_path']}",
        f"TODO path: {payload['todo_path']}",
        f"Log path: {payload['log_path']}",
        f"Template: {payload['template']}",
    ]
    if payload.get("dry_run"):
        lines.append("Dry-run: no files written")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new issue")
    add_global_flags(parser)
    parser.add_argument("--title", required=False, help="Issue title")
    parser.add_argument("--description", required=False, help="Issue description")
    parser.add_argument("--summary", required=False, help="Alias for description")
    parser.add_argument("--slug", required=False, help="Explicit issue slug")
    parser.add_argument("--priority", type=int, default=5, help="Priority 0-10")
    parser.add_argument("--lightweight", action="store_true", help="Use lightweight template")
    parser.add_argument("--agent", default="Human", help="Agent name")
    parser.add_argument("--tags", help="Comma-separated tags")
    parser.add_argument(
        "--entrypoint",
        action="append",
        default=[],
        help="Entrypoint item as <path>:<type>",
    )

    args = parser.parse_args()
    _configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = _resolve_dev(args.dev).strip()
        validate_slug(dev)
        title = (args.title or "").strip()
        if not title:
            raise YodaError("--title is required", exit_code=ExitCode.VALIDATION)
        description = (args.summary or args.description or "").strip()
        if not description:
            raise YodaError("--description is required", exit_code=ExitCode.VALIDATION)
        if not isinstance(args.priority, int) or not (0 <= args.priority <= 10):
            raise YodaError("priority must be between 0 and 10", exit_code=ExitCode.VALIDATION)

        todo_file = todo_path(dev)
        if todo_file.exists():
            todo = read_yaml(todo_file)
        else:
            todo = _create_default_todo(dev)

        validate_todo_root(todo, dev)

        slug = args.slug.strip() if args.slug else _generate_slug(title)
        validate_slug(slug)
        issue_id = _next_issue_id(dev, todo.get("issues", []))

        issues = list(todo.get("issues", []))
        if any(item.get("id") == issue_id for item in issues):
            raise YodaError("Issue id already exists in TODO", exit_code=ExitCode.CONFLICT)

        issue_file = issue_path(issue_id, slug)
        log_file = log_path(issue_id, slug)
        if issue_file.exists():
            raise YodaError("Issue file already exists", exit_code=ExitCode.CONFLICT)
        if log_file.exists():
            raise YodaError("Log file already exists", exit_code=ExitCode.CONFLICT)

        template_file = template_path(args.lightweight)
        template_text = load_template(template_file)

        timestamp = _now_iso(todo.get("timezone"))
        entrypoints = _parse_entrypoints(args.entrypoint)
        tags = _parse_tags(args.tags)

        issue_item = _build_issue_item(
            issue_id=issue_id,
            title=title,
            slug=slug,
            description=description,
            priority=args.priority,
            lightweight=bool(args.lightweight),
            agent=args.agent,
            entrypoints=entrypoints,
            tags=tags,
            timestamp=timestamp,
        )

        issues.append(issue_item)
        todo["issues"] = issues
        todo["updated_at"] = timestamp

        validate_todo(todo, dev)

        issue_metadata = issue_item.copy()
        issue_metadata.pop("schema_version", None)
        issue_metadata["schema_version"] = "1.0"

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
            write_yaml(todo_file, todo)
            write_text(issue_file, rendered_issue)
            write_yaml(log_file, log_payload)

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
