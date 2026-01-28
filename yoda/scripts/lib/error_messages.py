"""Standardized error helpers."""

from __future__ import annotations

from pathlib import Path

from .errors import ExitCode, YodaError


def required_flag(flag: str) -> None:
    raise YodaError(f"{flag} is required", exit_code=ExitCode.VALIDATION)


def conflict_issue_id(issue_id: str) -> None:
    raise YodaError(
        f"Issue id already exists in TODO: {issue_id}",
        exit_code=ExitCode.CONFLICT,
    )


def conflict_issue_file(path: Path) -> None:
    raise YodaError(
        f"Issue file already exists: {path}",
        exit_code=ExitCode.CONFLICT,
    )


def conflict_log_file(path: Path) -> None:
    raise YodaError(
        f"Log file already exists: {path}",
        exit_code=ExitCode.CONFLICT,
    )
