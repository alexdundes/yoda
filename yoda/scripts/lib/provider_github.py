"""GitHub provider helpers for YODA Intake."""

from __future__ import annotations

import json
import subprocess
from typing import Any

from .errors import ExitCode, YodaError


def fetch_issue(repo_slug: str, issue_number: str) -> dict[str, Any]:
    cmd = ["gh", "api", f"repos/{repo_slug}/issues/{issue_number}"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        raise YodaError(
            f"Failed to fetch GitHub issue #{issue_number}: {stderr}",
            exit_code=ExitCode.ERROR,
        )

    try:
        raw = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise YodaError(
            "Invalid JSON returned by gh api",
            exit_code=ExitCode.ERROR,
        ) from exc

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
    }
