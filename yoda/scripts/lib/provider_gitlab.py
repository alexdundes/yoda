"""GitLab provider helpers for YODA Intake."""

from __future__ import annotations

import json
import subprocess
from typing import Any
from urllib.parse import quote

from .errors import ExitCode, YodaError


def _run_glab_api(path: str) -> Any:
    cmd = ["glab", "api", path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        raise YodaError(f"Failed to fetch GitLab API '{path}': {stderr}", exit_code=ExitCode.ERROR)
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise YodaError("Invalid JSON returned by glab api", exit_code=ExitCode.ERROR) from exc


def _fetch_issue_notes(encoded_slug: str, issue_number: str) -> list[dict[str, str]]:
    raw_notes = _run_glab_api(f"projects/{encoded_slug}/issues/{issue_number}/notes?per_page=100")
    if not isinstance(raw_notes, list):
        raise YodaError("Invalid notes payload returned by glab api", exit_code=ExitCode.ERROR)
    notes: list[dict[str, str]] = []
    for item in raw_notes:
        if not isinstance(item, dict):
            continue
        notes.append(
            {
                "type": "note" if not bool(item.get("system")) else "system-note",
                "id": str(item.get("id", "")),
                "author": str((item.get("author") or {}).get("username", "")),
                "created_at": str(item.get("created_at", "")),
                "updated_at": str(item.get("updated_at", "")),
                "body": str(item.get("body", "")),
                "url": str(item.get("url", "")),
            }
        )
    return notes


def fetch_issue(repo_slug: str, issue_number: str) -> dict[str, Any]:
    encoded_slug = quote(repo_slug, safe="")
    raw = _run_glab_api(f"projects/{encoded_slug}/issues/{issue_number}")
    if not isinstance(raw, dict):
        raise YodaError("Invalid issue payload returned by glab api", exit_code=ExitCode.ERROR)
    notes = _fetch_issue_notes(encoded_slug, issue_number)

    labels = [str(label) for label in raw.get("labels", []) if isinstance(label, str)]
    return {
        "provider": "gitlab",
        "number": str(raw.get("iid", issue_number)),
        "title": str(raw.get("title", "")),
        "description": str(raw.get("description", "")),
        "state": str(raw.get("state", "")),
        "author": str((raw.get("author") or {}).get("username", "")),
        "url": str(raw.get("web_url", "")),
        "labels": labels,
        "log": notes,
    }
