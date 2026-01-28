"""TODO helpers for YODA scripts."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import ExitCode, YodaError
from .validate import validate_todo
from .yaml_io import read_yaml


def load_todo_file(todo_file: Path, dev: str) -> dict[str, Any]:
    if not todo_file.exists():
        raise YodaError(
            f"TODO file not found: {todo_file}",
            exit_code=ExitCode.NOT_FOUND,
        )
    todo = read_yaml(todo_file)
    validate_todo(todo, dev)
    return todo


def find_issue(todo: dict[str, Any], issue_id: str) -> dict[str, Any]:
    for item in todo.get("issues", []):
        if item.get("id") == issue_id:
            return item
    raise YodaError(
        f"Issue id not found in TODO: {issue_id}",
        exit_code=ExitCode.NOT_FOUND,
    )
