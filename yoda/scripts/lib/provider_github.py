"""GitHub provider helpers for YODA Intake."""

from __future__ import annotations

import json
import re
import subprocess
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import Any

from .errors import ExitCode, YodaError


API_BASE_URL = "https://api.github.com"
API_VERSION = "2022-11-28"
HTTP_TIMEOUT_SECONDS = 15
ENDPOINT_UNAVAILABLE_STATUSES = {404, 410, 415, 422}


class GitHubAPIError(YodaError):
    def __init__(
        self,
        message: str,
        *,
        status_code: int | None = None,
        kind: str = "api",
        exit_code: int = ExitCode.ERROR,
    ) -> None:
        super().__init__(message, exit_code=exit_code)
        self.status_code = status_code
        self.kind = kind


ApiGet = Callable[..., Any]


def _status_from_gh_error(stderr: str) -> int | None:
    match = re.search(r"(?:HTTP|status(?: code)?)\D+(\d{3})", stderr, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def _error_kind(status_code: int | None, message: str = "") -> str:
    lowered = message.lower()
    if status_code == 429 or "rate limit" in lowered:
        return "rate_limit"
    if status_code in {401, 403}:
        return "permission"
    if status_code == 404:
        return "not_found"
    return "api"


def _run_gh_api(path: str, headers: list[str] | None = None) -> Any:
    cmd = ["gh", "api"]
    for header in headers or []:
        cmd.extend(["-H", header])
    cmd.append(path)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        status_code = _status_from_gh_error(stderr)
        kind = _error_kind(status_code, stderr)
        raise GitHubAPIError(
            f"Authenticated GitHub API request failed for '{path}'"
            + (f" (HTTP {status_code})" if status_code else ""),
            status_code=status_code,
            kind=kind,
        )
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise GitHubAPIError("Invalid JSON returned by gh api", kind="payload") from exc


def _header_value(headers: Any, name: str) -> str:
    if headers is None:
        return ""
    value = headers.get(name, "")
    return str(value or "").strip()


def _public_http_error(exc: urllib.error.HTTPError, path: str) -> GitHubAPIError:
    status_code = int(exc.code)
    remaining = _header_value(exc.headers, "X-RateLimit-Remaining")
    retry_after = _header_value(exc.headers, "Retry-After")
    reset = _header_value(exc.headers, "X-RateLimit-Reset")
    is_rate_limit = status_code == 429 or (status_code == 403 and (remaining == "0" or bool(retry_after)))
    if is_rate_limit:
        retry_hint = retry_after or reset or "the limit reset reported by GitHub"
        return GitHubAPIError(
            "GitHub public API rate limit reached. "
            f"Retry after {retry_hint} or authenticate with 'gh auth login' for a higher limit.",
            status_code=status_code,
            kind="rate_limit",
        )
    if status_code in {401, 403, 404}:
        return GitHubAPIError(
            "GitHub resource was not found or is not publicly accessible. "
            "The repository may be private; install/authenticate GitHub CLI with 'gh auth login'.",
            status_code=status_code,
            kind="permission" if status_code in {401, 403} else "not_found",
            exit_code=ExitCode.NOT_FOUND,
        )
    return GitHubAPIError(
        f"GitHub public API request failed for '{path}' (HTTP {status_code}).",
        status_code=status_code,
    )


def _run_public_api(
    path: str,
    headers: list[str] | None = None,
    *,
    opener: Callable[..., Any] | None = None,
) -> Any:
    request_headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
        "User-Agent": "yoda-get-extern-issue",
    }
    for header in headers or []:
        name, separator, value = header.partition(":")
        if separator:
            request_headers[name.strip()] = value.strip()
    request = urllib.request.Request(f"{API_BASE_URL}/{path.lstrip('/')}", headers=request_headers)
    open_request = opener or urllib.request.urlopen
    try:
        with open_request(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        raise _public_http_error(exc, path) from exc
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise GitHubAPIError(
            f"GitHub public API network failure for '{path}'. Check connectivity and retry.",
            kind="network",
        ) from exc
    try:
        return json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise GitHubAPIError("Invalid JSON returned by GitHub public API", kind="payload") from exc


def _fetch_issue_comments(
    repo_slug: str,
    issue_number: str,
    api_get: ApiGet,
) -> list[dict[str, str]]:
    raw_comments = api_get(f"repos/{repo_slug}/issues/{issue_number}/comments?per_page=100", None)
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


def _fetch_issue_timeline(repo_slug: str, issue_number: str, api_get: ApiGet) -> list[dict[str, str]]:
    paths = [
        f"repos/{repo_slug}/issues/{issue_number}/timeline?per_page=100",
        f"repos/{repo_slug}/issues/{issue_number}/events?per_page=100",
    ]
    headers = ["Accept: application/vnd.github+json"]
    for path in paths:
        try:
            raw_entries = api_get(path, headers)
        except GitHubAPIError as exc:
            if exc.status_code in ENDPOINT_UNAVAILABLE_STATUSES:
                continue
            raise
        if not isinstance(raw_entries, list):
            raise GitHubAPIError("Invalid timeline payload returned by GitHub API", kind="payload")
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


def _fetch_issue(repo_slug: str, issue_number: str, api_get: ApiGet) -> dict[str, Any]:
    raw = api_get(f"repos/{repo_slug}/issues/{issue_number}", None)
    if not isinstance(raw, dict):
        raise GitHubAPIError("Invalid issue payload returned by GitHub API", kind="payload")
    comments = _fetch_issue_comments(repo_slug, issue_number, api_get)
    timeline = _fetch_issue_timeline(repo_slug, issue_number, api_get)
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


def fetch_issue(repo_slug: str, issue_number: str) -> dict[str, Any]:
    return _fetch_issue(repo_slug, issue_number, _run_gh_api)


def fetch_issue_public(
    repo_slug: str,
    issue_number: str,
    *,
    opener: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    def api_get(path: str, headers: list[str] | None = None) -> Any:
        return _run_public_api(path, headers, opener=opener)

    return _fetch_issue(repo_slug, issue_number, api_get)
