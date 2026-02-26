"""GitLab provider helpers for YODA Intake."""

from __future__ import annotations

import json
import subprocess
from typing import Any
from urllib.parse import quote

from .errors import ExitCode, YodaError


def fetch_issue(repo_slug: str, issue_number: str) -> dict[str, Any]:
    encoded_slug = quote(repo_slug, safe="")
    cmd = ["glab", "api", f"projects/{encoded_slug}/issues/{issue_number}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        raise YodaError(
            f"Failed to fetch GitLab issue #{issue_number}: {stderr}",
            exit_code=ExitCode.ERROR,
        )

    try:
        raw = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise YodaError(
            "Invalid JSON returned by glab api",
            exit_code=ExitCode.ERROR,
        ) from exc

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
    }
