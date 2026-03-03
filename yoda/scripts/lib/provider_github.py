"""GitHub provider helpers for YODA Intake."""

from __future__ import annotations

import json
import subprocess
from typing import Any

from .errors import ExitCode, YodaError


def _run_gh_api(path: str, headers: list[str] | None = None) -> Any:
    cmd = ["gh", "api"]
    for header in headers or []:
        cmd.extend(["-H", header])
    cmd.append(path)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        raise YodaError(f"Failed to fetch GitHub API '{path}': {stderr}", exit_code=ExitCode.ERROR)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise YodaError("Invalid JSON returned by gh api", exit_code=ExitCode.ERROR) from exc


def _fetch_issue_comments(repo_slug: str, issue_number: str) -> list[dict[str, str]]:
    raw_comments = _run_gh_api(f"repos/{repo_slug}/issues/{issue_number}/comments?per_page=100")
    if not isinstance(raw_comments, list):
        raise YodaError("Invalid comments payload returned by gh api", exit_code=ExitCode.ERROR)
    comments: list[dict[str, str]] = []
    for item in raw_comments:
        if not isinstance(item, dict):
            continue
        comments.append(
            {
                "type": "comment",
                "id": str(item.get("id", "")),
                "author": str((item.get("user") or {}).get("login", "")),
                "created_at": str(item.get("created_at", "")),
                "updated_at": str(item.get("updated_at", "")),
                "body": str(item.get("body", "")),
                "url": str(item.get("html_url", "")),
            }
        )
    return comments


def _timeline_body(item: dict[str, Any]) -> str:
    body = str(item.get("body", "")).strip()
    if body:
        return body
    event = str(item.get("event", "")).strip() or "timeline-event"
    commit_id = str(item.get("commit_id", "")).strip()
    if commit_id:
        return f"event: {event}; commit: {commit_id}"
    label_name = str((item.get("label") or {}).get("name", "")).strip()
    if label_name:
        return f"event: {event}; label: {label_name}"
    return f"event: {event}"


def _normalize_timeline_entry(item: dict[str, Any]) -> dict[str, str]:
    return {
        "type": f"timeline:{str(item.get('event', '')).strip() or 'event'}",
        "id": str(item.get("id", "")),
        "author": str((item.get("actor") or {}).get("login", "")),
        "created_at": str(item.get("created_at", "")),
        "updated_at": str(item.get("updated_at", "")),
        "body": _timeline_body(item),
        "url": str(item.get("html_url", "")),
    }


def _fetch_issue_timeline(repo_slug: str, issue_number: str) -> list[dict[str, str]]:
    paths = [
        f"repos/{repo_slug}/issues/{issue_number}/timeline?per_page=100",
        f"repos/{repo_slug}/issues/{issue_number}/events?per_page=100",
    ]
    headers = ["Accept: application/vnd.github+json"]
    for path in paths:
        try:
            raw_entries = _run_gh_api(path, headers=headers)
        except YodaError:
            continue
        if not isinstance(raw_entries, list):
            continue
        entries: list[dict[str, str]] = []
        for item in raw_entries:
            if not isinstance(item, dict):
                continue
            entries.append(_normalize_timeline_entry(item))
        return entries
    return []


def _deduplicate_logs(entries: list[dict[str, str]]) -> list[dict[str, str]]:
    # GitHub can return the same user comment both in /comments and in timeline as "commented".
    # Prefer keeping the canonical "comment" entry and drop duplicate timeline copies.
    best_by_key: dict[tuple[str, str], dict[str, str]] = {}
    for entry in entries:
        entry_id = entry.get("id", "")
        entry_url = entry.get("url", "")
        key = (entry_id, entry_url)
        current = best_by_key.get(key)
        if current is None:
            best_by_key[key] = entry
            continue
        current_is_comment = current.get("type") == "comment"
        incoming_is_comment = entry.get("type") == "comment"
        if incoming_is_comment and not current_is_comment:
            best_by_key[key] = entry
    return list(best_by_key.values())


def fetch_issue(repo_slug: str, issue_number: str) -> dict[str, Any]:
    raw = _run_gh_api(f"repos/{repo_slug}/issues/{issue_number}")
    if not isinstance(raw, dict):
        raise YodaError("Invalid issue payload returned by gh api", exit_code=ExitCode.ERROR)
    comments = _fetch_issue_comments(repo_slug, issue_number)
    timeline = _fetch_issue_timeline(repo_slug, issue_number)
    logs = _deduplicate_logs(comments + timeline)
    logs.sort(key=lambda entry: (entry.get("created_at", "") == "", entry.get("created_at", ""), entry.get("id", "")))

    labels = [str(item.get("name", "")) for item in raw.get("labels", []) if isinstance(item, dict)]
    return {
        "provider": "github",
        "number": str(raw.get("number", issue_number)),
        "title": str(raw.get("title", "")),
        "description": str(raw.get("body", "")),
        "state": str(raw.get("state", "")),
        "author": str((raw.get("user") or {}).get("login", "")),
        "url": str(raw.get("html_url", "")),
        "labels": [label for label in labels if label],
        "log": logs,
    }
