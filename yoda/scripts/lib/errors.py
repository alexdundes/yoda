"""Error helpers and exit codes."""

from dataclasses import dataclass


class ExitCode:
    SUCCESS = 0
    ERROR = 1
    VALIDATION = 2
    NOT_FOUND = 3
    CONFLICT = 4


@dataclass
class YodaError(Exception):
    message: str
    exit_code: int = ExitCode.ERROR

    def __str__(self) -> str:
        return self.message
