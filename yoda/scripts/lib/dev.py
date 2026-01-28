"""Developer resolution helpers."""

from __future__ import annotations

import os

from .errors import ExitCode, YodaError


def resolve_dev(explicit_dev: str | None) -> str:
    if explicit_dev:
        return explicit_dev
    env_dev = os.environ.get("YODA_DEV")
    if env_dev:
        return env_dev
    try:
        return input("Developer slug: ").strip()
    except EOFError as exc:
        raise YodaError("Developer slug is required", exit_code=ExitCode.VALIDATION) from exc
