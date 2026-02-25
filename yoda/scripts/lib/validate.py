"""Validation helpers for YODA scripts."""

from __future__ import annotations

import re
from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, Iterable

from .errors import YodaError, ExitCode

SLUG_RE = re.compile(r"^[a-z][a-z0-9-]*$")
ISSUE_ID_RE = re.compile(r"^[a-z][a-z0-9-]*-\d{4}$")
ALLOWED_STATUS = {"to-do", "doing", "done", "pending"}
ALLOWED_ENTRY_TYPES = {"doc", "code", "config", "schema", "data", "asset", "other"}
SUPPORTED_SCHEMA_VERSIONS = {"1.0", "1.01"}


def validate_slug(slug: str) -> None:
    if not SLUG_RE.match(slug):
        raise YodaError(f"Invalid slug: {slug}", exit_code=ExitCode.VALIDATION)


def validate_issue_id(issue_id: str, dev: str) -> None:
    if not ISSUE_ID_RE.match(issue_id):
        raise YodaError(f"Invalid issue id: {issue_id}", exit_code=ExitCode.VALIDATION)
    if not issue_id.startswith(f"{dev}-"):
        raise YodaError(
            f"Issue id {issue_id} does not match developer slug {dev}",
            exit_code=ExitCode.VALIDATION,
        )


def _validate_timestamp(value: str, label: str) -> None:
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError as exc:
        raise YodaError(f"Invalid {label} timestamp: {value}", exit_code=ExitCode.VALIDATION) from exc
    if parsed.tzinfo is None:
        raise YodaError(f"Timestamp missing timezone: {label}", exit_code=ExitCode.VALIDATION)


def _validate_timezone(value: str) -> None:
    try:
        ZoneInfo(value)
    except Exception as exc:
        raise YodaError(f"Invalid timezone: {value}", exit_code=ExitCode.VALIDATION) from exc


def _ensure_required(obj: dict[str, Any], fields: Iterable[str], label: str) -> None:
    missing = [field for field in fields if field not in obj]
    if missing:
        raise YodaError(
            f"Missing required fields in {label}: {', '.join(missing)}",
            exit_code=ExitCode.VALIDATION,
        )


def validate_todo_root(todo: dict[str, Any], dev: str) -> None:
    _ensure_required(
        todo,
        ["schema_version", "developer_name", "developer_slug", "timezone", "updated_at", "issues"],
        "TODO root",
    )
    if str(todo.get("schema_version")) not in SUPPORTED_SCHEMA_VERSIONS:
        raise YodaError("Unsupported schema_version", exit_code=ExitCode.VALIDATION)
    if todo.get("developer_slug") != dev:
        raise YodaError("developer_slug does not match --dev", exit_code=ExitCode.VALIDATION)
    validate_slug(dev)
    _validate_timezone(str(todo.get("timezone")))
    _validate_timestamp(str(todo.get("updated_at")), "updated_at")
    if not isinstance(todo.get("issues"), list):
        raise YodaError("issues must be a list", exit_code=ExitCode.VALIDATION)


def validate_issue_item(item: dict[str, Any], dev: str) -> None:
    _ensure_required(
        item,
        [
            "id",
            "title",
            "slug",
            "description",
            "status",
            "priority",
            "depends_on",
            "pending_reason",
            "created_at",
            "updated_at",
        ],
        "issue item",
    )
    validate_issue_id(str(item.get("id")), dev)
    validate_slug(str(item.get("slug")))
    if item.get("status") not in ALLOWED_STATUS:
        raise YodaError("Invalid status", exit_code=ExitCode.VALIDATION)
    if not isinstance(item.get("priority"), int) or not (0 <= item.get("priority") <= 10):
        raise YodaError("Invalid priority", exit_code=ExitCode.VALIDATION)
    if item.get("status") == "pending" and not item.get("pending_reason"):
        raise YodaError("pending_reason required for pending status", exit_code=ExitCode.VALIDATION)
    if not isinstance(item.get("depends_on"), list):
        raise YodaError("depends_on must be a list", exit_code=ExitCode.VALIDATION)
    if item.get("entrypoints") is not None:
        if not isinstance(item.get("entrypoints"), list):
            raise YodaError("entrypoints must be a list", exit_code=ExitCode.VALIDATION)
        for entry in item.get("entrypoints"):
            if not isinstance(entry, dict):
                raise YodaError("entrypoints must contain objects", exit_code=ExitCode.VALIDATION)
            if "path" not in entry or "type" not in entry:
                raise YodaError("entrypoints require path and type", exit_code=ExitCode.VALIDATION)
            if entry.get("type") not in ALLOWED_ENTRY_TYPES:
                raise YodaError("Invalid entrypoint type", exit_code=ExitCode.VALIDATION)
    _validate_timestamp(str(item.get("created_at")), "created_at")
    _validate_timestamp(str(item.get("updated_at")), "updated_at")


def validate_todo(todo: dict[str, Any], dev: str) -> None:
    validate_todo_root(todo, dev)
    ids = set()
    for item in todo.get("issues", []):
        if not isinstance(item, dict):
            raise YodaError("Issue item must be an object", exit_code=ExitCode.VALIDATION)
        validate_issue_item(item, dev)
        issue_id = str(item.get("id"))
        if issue_id in ids:
            raise YodaError("Duplicate issue id in TODO", exit_code=ExitCode.VALIDATION)
        ids.add(issue_id)
    for item in todo.get("issues", []):
        depends_on = item.get("depends_on", [])
        if not isinstance(depends_on, list):
            raise YodaError("depends_on must be a list", exit_code=ExitCode.VALIDATION)
        missing = [dep for dep in depends_on if dep not in ids]
        if missing:
            raise YodaError(
                f"depends_on references missing ids: {', '.join(missing)}",
                exit_code=ExitCode.VALIDATION,
            )
