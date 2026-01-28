#!/usr/bin/env python3
"""List and filter TODO issues."""

from __future__ import annotations

import argparse
import json
import logging
import re
import sys
from dataclasses import dataclass
from typing import Any, Iterable

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.errors import ExitCode, YodaError
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.parse_utils import parse_bool, parse_csv, parse_timestamp
from lib.paths import issue_path, repo_root, todo_path
from lib.todo_utils import load_todo_file
from lib.time_utils import parse_timestamp as parse_issue_timestamp
from lib.validate import validate_slug


@dataclass(frozen=True)
class _Match:
    issue_id: str
    line_no: int
    line: str


ORDER_MODES = {"created-asc", "created-desc", "updated-asc", "updated-desc"}


def _filter_issues(issues: list[dict[str, Any]], args: argparse.Namespace) -> list[dict[str, Any]]:
    statuses = parse_csv(args.status)
    tags = parse_csv(args.tags)
    depends_on = args.depends_on
    agent = args.agent
    priority_min = args.priority_min
    priority_max = args.priority_max
    lightweight = parse_bool(args.lightweight)
    created_from = parse_timestamp(args.created_from)
    created_to = parse_timestamp(args.created_to)
    updated_from = parse_timestamp(args.updated_from)
    updated_to = parse_timestamp(args.updated_to)

    filtered: list[dict[str, Any]] = []
    for issue in issues:
        status = str(issue.get("status"))
        if statuses:
            if status not in statuses:
                continue
        else:
            if status == "done":
                continue

        if tags:
            issue_tags = set(issue.get("tags", []))
            if not all(tag in issue_tags for tag in tags):
                continue

        if agent and str(issue.get("agent", "")) != agent:
            continue

        if depends_on and depends_on not in issue.get("depends_on", []):
            continue

        if lightweight is not None and bool(issue.get("lightweight")) != lightweight:
            continue

        priority = int(issue.get("priority", 0))
        if priority_min is not None and priority < priority_min:
            continue
        if priority_max is not None and priority > priority_max:
            continue

        if created_from or created_to:
            created_at = parse_issue_timestamp(str(issue.get("created_at", "")), "created_at")
            if created_from and created_at < created_from:
                continue
            if created_to and created_at > created_to:
                continue

        if updated_from or updated_to:
            updated_at = parse_issue_timestamp(str(issue.get("updated_at", "")), "updated_at")
            if updated_from and updated_at < updated_from:
                continue
            if updated_to and updated_at > updated_to:
                continue

        filtered.append(issue)
    return filtered


def _base_order(
    issues: list[dict[str, Any]], yaml_index: dict[str, int], order: str | None
) -> list[dict[str, Any]]:
    if order in ORDER_MODES:
        reverse = order.endswith("desc")
        field = "created_at" if order.startswith("created") else "updated_at"
        return sorted(
            issues,
            key=lambda item: (
                parse_issue_timestamp(str(item.get(field, "")), field),
                yaml_index[str(item.get("id"))],
            ),
            reverse=reverse,
        )
    return sorted(
        issues,
        key=lambda item: (-int(item.get("priority", 0)), yaml_index[str(item.get("id"))]),
    )


def _apply_dependency_order(
    issues: list[dict[str, Any]], done_ids: set[str], order_index: dict[str, int]
) -> list[dict[str, Any]]:
    id_to_issue = {str(item.get("id")): item for item in issues}
    indegree = {issue_id: 0 for issue_id in id_to_issue}
    dependents: dict[str, list[str]] = {issue_id: [] for issue_id in id_to_issue}

    for issue_id, issue in id_to_issue.items():
        for dep in issue.get("depends_on", []):
            dep_id = str(dep)
            if dep_id in done_ids:
                continue
            if dep_id not in id_to_issue:
                continue
            indegree[issue_id] += 1
            dependents[dep_id].append(issue_id)

    zero = sorted(
        [issue_id for issue_id, count in indegree.items() if count == 0],
        key=lambda issue_id: order_index[issue_id],
    )
    ordered: list[str] = []
    while zero:
        current = zero.pop(0)
        ordered.append(current)
        for dep in dependents[current]:
            indegree[dep] -= 1
            if indegree[dep] == 0:
                zero.append(dep)
        zero.sort(key=lambda issue_id: order_index[issue_id])

    if len(ordered) != len(issues):
        return issues
    return [id_to_issue[issue_id] for issue_id in ordered]


def _find_matches(
    issues: list[dict[str, Any]],
    pattern: str,
    case_sensitive: bool,
) -> tuple[list[dict[str, Any]], list[_Match]]:
    flags = 0 if case_sensitive else re.IGNORECASE
    try:
        regex = re.compile(pattern, flags)
    except re.error as exc:
        raise YodaError("Invalid regex pattern", exit_code=ExitCode.VALIDATION) from exc

    matches: list[_Match] = []
    for issue in issues:
        issue_id = str(issue.get("id"))
        slug = str(issue.get("slug"))
        path = issue_path(issue_id, slug)
        if not path.exists():
            continue
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for idx, line in enumerate(lines, start=1):
            if regex.search(line):
                matches.append(_Match(issue_id=issue_id, line_no=idx, line=line))

    return issues, matches


def _truncate(value: str, max_len: int) -> str:
    if len(value) <= max_len:
        return value
    if max_len <= 3:
        return value[:max_len]
    return value[: max_len - 3] + "..."


def _render_table(issues: list[dict[str, Any]]) -> str:
    headers = ["id", "status", "priority", "title"]
    rows = []
    for item in issues:
        rows.append(
            [
                str(item.get("id", "")),
                str(item.get("status", "")),
                str(item.get("priority", "")),
                str(item.get("title", "")),
            ]
        )

    max_widths = [len(header) for header in headers]
    for row in rows:
        for idx, value in enumerate(row):
            max_widths[idx] = max(max_widths[idx], len(value))

    max_widths[0] = min(max_widths[0], 16)
    max_widths[1] = min(max_widths[1], 10)
    max_widths[2] = min(max_widths[2], 8)
    max_widths[3] = min(max_widths[3], 60)

    def format_row(values: Iterable[str]) -> str:
        padded = []
        for idx, value in enumerate(values):
            trimmed = _truncate(value, max_widths[idx])
            padded.append(trimmed.ljust(max_widths[idx]))
        return "| " + " | ".join(padded) + " |"

    header_line = format_row(headers)
    divider = "| " + " | ".join("-" * width for width in max_widths) + " |"
    body = [format_row(row) for row in rows]
    return "\n".join([header_line, divider, *body])


def _render_pending_block(issues: list[dict[str, Any]]) -> str:
    lines = ["## Pending issues", "", "ALERT: pending issues require attention.", ""]
    for issue in issues:
        line = (
            f"- {issue.get('id')} | {issue.get('title')} "
            f"({issue.get('status')})"
        )
        reason = str(issue.get("pending_reason", "")).strip()
        if reason:
            line += f" — {reason}"
        lines.append(line)
    return "\n".join(lines)


def _render_grep_output(
    issues: list[dict[str, Any]], matches: list[_Match]
) -> str:
    if not matches:
        return "No matches found."

    id_to_issue = {str(issue.get("id")): issue for issue in issues}
    lines: list[str] = []
    matches_by_issue: dict[str, list[_Match]] = {}
    for match in matches:
        matches_by_issue.setdefault(match.issue_id, []).append(match)

    for issue_id in matches_by_issue:
        issue = id_to_issue.get(issue_id)
        if not issue:
            continue
        slug = str(issue.get("slug"))
        path = issue_path(issue_id, slug).relative_to(repo_root())
        lines.append(f"## {issue_id} - {issue.get('title')}")
        lines.append(f"Path: {path}")
        for match in matches_by_issue[issue_id]:
            lines.append(f"- L{match.line_no}: {match.line}")
        lines.append("")
    return "\n".join(lines).rstrip()


def _render_json_payload(
    issues: list[dict[str, Any]], matches: list[_Match] | None
) -> dict[str, Any]:
    payload: dict[str, Any] = {"issues": issues}
    if matches is not None:
        payload["matches"] = [
            {"issue_id": match.issue_id, "line_no": match.line_no, "line": match.line}
            for match in matches
        ]
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="List TODO issues")
    add_global_flags(parser)
    parser.add_argument("--status", help="Comma-separated status filter")
    parser.add_argument("--tags", help="Comma-separated tags filter (AND)")
    parser.add_argument("--agent", help="Agent name filter")
    parser.add_argument("--priority-min", type=int, dest="priority_min")
    parser.add_argument("--priority-max", type=int, dest="priority_max")
    parser.add_argument("--depends-on", dest="depends_on", help="Include issues that depend on id")
    parser.add_argument("--lightweight", help="Filter by lightweight true|false")
    parser.add_argument("--created-from", dest="created_from", help="ISO 8601 timestamp")
    parser.add_argument("--created-to", dest="created_to", help="ISO 8601 timestamp")
    parser.add_argument("--updated-from", dest="updated_from", help="ISO 8601 timestamp")
    parser.add_argument("--updated-to", dest="updated_to", help="ISO 8601 timestamp")
    parser.add_argument("--order", help="Ordering mode")
    parser.add_argument("--grep", help="Regex search pattern")
    parser.add_argument("--case-sensitive", action="store_true", help="Case-sensitive grep")

    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = resolve_dev(args.dev).strip()
        validate_slug(dev)

        todo_file = todo_path(dev)
        todo = load_todo_file(todo_file, dev)
        issues = list(todo.get("issues", []))
        yaml_index = {str(item.get("id")): idx for idx, item in enumerate(issues)}
        done_ids = {
            str(item.get("id"))
            for item in issues
            if item.get("status") == "done"
        }

        filtered = _filter_issues(issues, args)
        ordered = _base_order(filtered, yaml_index, args.order)
        order_index = {str(item.get("id")): idx for idx, item in enumerate(ordered)}
        ordered = _apply_dependency_order(ordered, done_ids, order_index)

        matches: list[_Match] | None = None
        if args.grep:
            ordered, matches = _find_matches(ordered, args.grep, args.case_sensitive)

        pending = [item for item in ordered if item.get("status") == "pending"]
        table_items = [item for item in ordered if item.get("status") != "pending"]

        if output_format == "json":
            payload = _render_json_payload(ordered, matches)
            print(json.dumps(payload, indent=2, ensure_ascii=True))
            return ExitCode.SUCCESS

        if args.grep:
            print(_render_grep_output(ordered, matches or []))
            return ExitCode.SUCCESS

        lines: list[str] = []
        if pending:
            lines.append(_render_pending_block(pending))
            lines.append("")
        if table_items:
            lines.append(_render_table(table_items))
        else:
            lines.append("No issues found.")

        payload = {"issues": ordered, "dry_run": bool(args.dry_run)}
        print(render_output(payload, output_format, lines, dry_run=bool(args.dry_run)))
        return ExitCode.SUCCESS
    except YodaError as exc:
        logging.error(str(exc))
        return exc.exit_code
    except Exception as exc:  # pragma: no cover
        logging.error("Unexpected error: %s", exc)
        return ExitCode.ERROR


if __name__ == "__main__":
    sys.exit(main())
