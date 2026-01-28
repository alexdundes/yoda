"""Parsing helpers for CLI arguments."""

from __future__ import annotations

from datetime import datetime

from .errors import ExitCode, YodaError


def parse_csv(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def parse_bool(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise YodaError("Invalid boolean value", exit_code=ExitCode.VALIDATION)


def parse_timestamp(value: str | None) -> datetime | None:
    if value is None:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise YodaError("Invalid timestamp format", exit_code=ExitCode.VALIDATION) from exc
    if parsed.tzinfo is None:
        raise YodaError("Timestamp missing timezone", exit_code=ExitCode.VALIDATION)
    return parsed
