"""Time helpers for YODA scripts."""

from __future__ import annotations

import os
from datetime import datetime
from zoneinfo import ZoneInfo

from .errors import ExitCode, YodaError


def now_iso(tz_name: str) -> str:
    tz = ZoneInfo(tz_name)
    return datetime.now(tz).isoformat(timespec="seconds")


def validate_timestamp(value: str) -> None:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise YodaError("Invalid timestamp format", exit_code=ExitCode.VALIDATION) from exc
    if parsed.tzinfo is None:
        raise YodaError("Timestamp missing timezone", exit_code=ExitCode.VALIDATION)


def is_valid_timezone(name: str) -> bool:
    try:
        ZoneInfo(name)
        return True
    except Exception:
        return False


def detect_local_timezone() -> str:
    tz_env = os.environ.get("TZ")
    if tz_env and is_valid_timezone(tz_env):
        return tz_env

    try:
        realpath = os.path.realpath("/etc/localtime")
        for marker_name in ("zoneinfo", "zoneinfo.default", "zoneinfo.posix"):
            marker = f"{os.sep}{marker_name}{os.sep}"
            if marker in realpath:
                candidate = realpath.split(marker, 1)[1]
                if candidate and is_valid_timezone(candidate):
                    return candidate
    except Exception:
        pass

    return "UTC"
