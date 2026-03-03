"""Issue path helpers for YODA scripts."""

from __future__ import annotations

from pathlib import Path

from .errors import ExitCode, YodaError
from .paths import issues_dir, logs_dir


def _derive_slug_from_name(name: str, issue_id: str, suffix: str) -> str:
    prefix = f"{issue_id}-"
    if not name.startswith(prefix) or not name.endswith(suffix):
        raise YodaError(f"Invalid issue filename for id {issue_id}: {name}", exit_code=ExitCode.VALIDATION)
    slug = name[len(prefix) : -len(suffix)]
    if not slug:
        raise YodaError(f"Missing slug segment for id {issue_id}: {name}", exit_code=ExitCode.VALIDATION)
    return slug


def find_issue_files_by_id(issue_id: str) -> list[Path]:
    return sorted(path for path in issues_dir().glob(f"{issue_id}-*.md") if path.is_file())


def find_log_files_by_id(issue_id: str) -> list[Path]:
    return sorted(path for path in logs_dir().glob(f"{issue_id}-*.yaml") if path.is_file())


def resolve_issue_file_by_id(issue_id: str) -> Path:
    matches = find_issue_files_by_id(issue_id)
    if not matches:
        raise YodaError(
            f"Issue file not found for id: {issue_id}",
            exit_code=ExitCode.NOT_FOUND,
        )
    if len(matches) > 1:
        names = ", ".join(path.name for path in matches)
        raise YodaError(
            f"Multiple issue files found for id {issue_id}: {names}",
            exit_code=ExitCode.CONFLICT,
        )
    return matches[0]


def resolve_log_file_by_id(issue_id: str) -> Path | None:
    matches = find_log_files_by_id(issue_id)
    if not matches:
        return None
    if len(matches) > 1:
        names = ", ".join(path.name for path in matches)
        raise YodaError(
            f"Multiple log files found for id {issue_id}: {names}",
            exit_code=ExitCode.CONFLICT,
        )
    return matches[0]


def issue_slug_from_path(path: Path, issue_id: str) -> str:
    return _derive_slug_from_name(path.name, issue_id, ".md")


def log_slug_from_path(path: Path, issue_id: str) -> str:
    return _derive_slug_from_name(path.name, issue_id, ".yaml")
