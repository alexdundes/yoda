"""YAML IO helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import YodaError, ExitCode

try:
    import yaml
except Exception as exc:  # pragma: no cover - runtime dependency
    raise YodaError(
        "PyYAML is required. Install dependencies from yoda/scripts/requirements.txt.",
        exit_code=ExitCode.ERROR,
    ) from exc


def read_yaml(path: Path) -> dict[str, Any]:
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise YodaError(f"Missing file: {path}", exit_code=ExitCode.NOT_FOUND) from exc
    data = yaml.safe_load(content) or {}
    if not isinstance(data, dict):
        raise YodaError(f"Invalid YAML root in {path}", exit_code=ExitCode.VALIDATION)
    return data


def write_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(data, sort_keys=False, allow_unicode=False)
    path.write_text(text, encoding="utf-8")
