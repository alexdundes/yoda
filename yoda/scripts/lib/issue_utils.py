"""Issue path helpers for YODA scripts."""

from __future__ import annotations

from pathlib import Path

from .errors import ExitCode, YodaError
from .paths import issue_path


def ensure_issue_file_exists(issue_id: str, slug: str) -> Path:
    issue_file = issue_path(issue_id, slug)
    if not issue_file.exists():
        raise YodaError(
            f"Issue file not found: {issue_file}",
            exit_code=ExitCode.NOT_FOUND,
        )
    return issue_file
