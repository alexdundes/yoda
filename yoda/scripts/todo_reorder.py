#!/usr/bin/env python3
"""Reorder TODO issues to match desired execution order."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from typing import Any

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.errors import ExitCode, YodaError
from lib.logging_utils import configure_logging
from lib.order_utils import apply_dependency_order
from lib.output import render_output
from lib.paths import repo_root, todo_path
from lib.time_utils import now_iso, parse_timestamp
from lib.todo_utils import load_todo_file
from lib.validate import validate_issue_id, validate_slug
from lib.yaml_io import write_yaml


def _validate_prefer_args(prefer: str | None, over: str | None) -> None:
    if (prefer and not over) or (over and not prefer):
        raise YodaError("Both --prefer and --over are required together", exit_code=ExitCode.VALIDATION)


def _build_index(issues: list[dict[str, Any]]) -> dict[str, int]:
    return {str(item.get("id")): idx for idx, item in enumerate(issues)}


def _base_order_active(
    active: list[dict[str, Any]], yaml_index: dict[str, int]
) -> list[dict[str, Any]]:
    return sorted(
        active,
        key=lambda item: (-int(item.get("priority", 0)), yaml_index[str(item.get("id"))]),
    )


def _sort_pending(pending: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        pending,
        key=lambda item: parse_timestamp(str(item.get("updated_at", "")), "updated_at"),
    )


def _sort_done(done: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        done,
        key=lambda item: parse_timestamp(str(item.get("updated_at", "")), "updated_at"),
        reverse=True,
    )


def _reorder_issues(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    done_ids = {
        str(item.get("id"))
        for item in issues
        if item.get("status") == "done"
    }
    pending = [item for item in issues if item.get("status") == "pending"]
    active = [item for item in issues if item.get("status") not in {"done", "pending"}]
    done = [item for item in issues if item.get("status") == "done"]

    pending_sorted = _sort_pending(pending)

    yaml_index = _build_index(issues)
    base_active = _base_order_active(active, yaml_index)
    order_index = _build_index(base_active)
    active_sorted = apply_dependency_order(base_active, done_ids, order_index)

    done_sorted = _sort_done(done)
    return [*pending_sorted, *active_sorted, *done_sorted]


def _apply_prefer(
    issues: list[dict[str, Any]],
    issue_id: str,
    other_id: str,
    dev: str,
    timestamp: str,
) -> bool:
    validate_issue_id(issue_id, dev)
    validate_issue_id(other_id, dev)
    if issue_id == other_id:
        raise YodaError("--prefer and --over must be different ids", exit_code=ExitCode.VALIDATION)

    index = {str(item.get("id")): item for item in issues}
    if issue_id not in index or other_id not in index:
        raise YodaError("Issue id not found in TODO", exit_code=ExitCode.VALIDATION)

    issue = index[issue_id]
    other = index[other_id]

    if issue.get("status") != "to-do" or other.get("status") != "to-do":
        raise YodaError("Both issues must be in status to-do", exit_code=ExitCode.VALIDATION)

    if other_id in [str(dep) for dep in issue.get("depends_on", [])]:
        raise YodaError("Cannot prefer a dependent over its dependency", exit_code=ExitCode.VALIDATION)

    priority_updated = False
    if int(issue.get("priority", 0)) < int(other.get("priority", 0)):
        issue["priority"] = int(other.get("priority", 0))
        issue["updated_at"] = timestamp
        priority_updated = True

    return priority_updated


def _render_md(reordered: bool, priority_updated: bool, issue_id: str | None) -> str:
    lines = [
        f"Reordered: {'yes' if reordered else 'no'}",
        f"Priority updated: {'yes' if priority_updated else 'no'}",
    ]
    if issue_id:
        lines.append(f"Prefer issue: {issue_id}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Reorder TODO issues")
    add_global_flags(parser)
    parser.add_argument("--prefer", help="Prefer issue id")
    parser.add_argument("--over", help="Over issue id")

    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = resolve_dev(args.dev).strip()
        validate_slug(dev)
        _validate_prefer_args(args.prefer, args.over)

        todo_file = todo_path(dev)
        todo = load_todo_file(todo_file, dev)
        issues = list(todo.get("issues", []))
        original_ids = [str(item.get("id")) for item in issues]

        timestamp = now_iso(todo.get("timezone"))
        priority_updated = False
        if args.prefer and args.over:
            priority_updated = _apply_prefer(
                issues, args.prefer, args.over, dev, timestamp
            )

        reordered_issues = _reorder_issues(issues)
        reordered_ids = [str(item.get("id")) for item in reordered_issues]
        reordered = reordered_ids != original_ids

        payload = {
            "todo_path": str(todo_file.relative_to(repo_root())),
            "reordered": reordered,
            "priority_updated": priority_updated,
            "issue_id": args.prefer or "",
            "dry_run": bool(args.dry_run),
        }

        if not args.dry_run and (reordered or priority_updated):
            todo["issues"] = reordered_issues
            todo["updated_at"] = timestamp
            write_yaml(todo_file, todo)

        if output_format == "json":
            print(json.dumps(payload, indent=2, ensure_ascii=True))
            return ExitCode.SUCCESS

        md_lines = _render_md(reordered, priority_updated, args.prefer).splitlines()
        print(render_output(payload, output_format, md_lines, dry_run=bool(args.dry_run)))
        return ExitCode.SUCCESS
    except YodaError as exc:
        logging.error(str(exc))
        return exc.exit_code
    except Exception as exc:  # pragma: no cover
        logging.error("Unexpected error: %s", exc)
        return ExitCode.ERROR


if __name__ == "__main__":
    sys.exit(main())
