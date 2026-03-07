"""Developer resolution helpers."""

from __future__ import annotations

from .errors import ExitCode, YodaError


def resolve_dev(explicit_dev: str | None) -> str:
    value = (explicit_dev or "").strip()
    if value:
        return value
    raise YodaError(
        "--dev is required. Ask the human for the developer slug and rerun the command with --dev <slug>.",
        exit_code=ExitCode.VALIDATION,
    )
