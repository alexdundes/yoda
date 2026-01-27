"""Template helpers."""

from pathlib import Path

from .errors import YodaError, ExitCode


def load_template(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise YodaError(f"Missing template: {path}", exit_code=ExitCode.NOT_FOUND) from exc
