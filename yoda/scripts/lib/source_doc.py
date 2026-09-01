"""Helpers for the optional `source_doc` issue association.

`source_doc` points at documentation that already exists in the consumer
project and that grounded the demand behind an issue. It is a source of
context, not an entry point, not a dependency, and not an external issue.

Write path validation is blocking: the value is normalized to a project
relative path and must exist. Read path validation never blocks; a reference
that stopped resolving produces an alert so it is not ignored silently.
"""

from __future__ import annotations

from pathlib import Path

from .errors import ExitCode, YodaError
from .paths import repo_root


def normalize_source_doc(raw: str, *, base_dir: Path | None = None) -> str:
    """Return `raw` as a project relative path, or raise for invalid input.

    Accepts absolute paths and paths relative to `base_dir` (the current
    working directory by default). The machine specific prefix never survives:
    the stored value is always relative to the project root so it stays
    portable across machines.
    """
    value = (raw or "").strip()
    if not value:
        return ""

    root = repo_root().resolve()
    candidate = Path(value).expanduser()
    if not candidate.is_absolute():
        candidate = (base_dir or Path.cwd()) / candidate

    resolved = candidate.resolve()
    try:
        relative = resolved.relative_to(root)
    except ValueError:
        raise YodaError(
            f"source_doc must stay inside the project root ({root}): {value}",
            exit_code=ExitCode.VALIDATION,
        ) from None

    if not resolved.exists():
        raise YodaError(
            f"source_doc path not found: {value}",
            exit_code=ExitCode.VALIDATION,
        )

    normalized = relative.as_posix()
    if not normalized or normalized == ".":
        raise YodaError(
            "source_doc must not point at the project root itself",
            exit_code=ExitCode.VALIDATION,
        )
    return normalized


def source_doc_alert(source_doc: str) -> str:
    """Return an alert line when `source_doc` no longer resolves, else "".

    Never raises: a stale reference must not break any command.
    """
    value = (source_doc or "").strip()
    if not value:
        return ""
    try:
        target = (repo_root() / value).resolve()
        if target.exists():
            return ""
    except OSError:
        pass
    return f"Alert: source_doc path not found: {value}"
