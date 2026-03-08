"""Helpers for issue metadata normalization."""

from __future__ import annotations

from typing import Any


OPTIONAL_EMPTY_KEYS = ("phase", "depends_on", "pending_reason", "extern_issue_file")
CANONICAL_ISSUE_FIELD_ORDER = (
    "schema_version",
    "id",
    "status",
    "phase",
    "pending_reason",
    "depends_on",
    "title",
    "description",
    "priority",
    "extern_issue_file",
    "created_at",
    "updated_at",
)


def prune_empty_optionals(item: dict[str, Any]) -> dict[str, Any]:
    """Remove optional keys when they carry empty values."""
    for key in OPTIONAL_EMPTY_KEYS:
        if key not in item:
            continue
        value = item.get(key)
        if value in ("", None, [], {}):
            item.pop(key, None)
    return item


def canonicalize_issue_metadata(item: dict[str, Any]) -> dict[str, Any]:
    """Return issue metadata ordered by canonical field order."""
    normalized = dict(item)
    normalized.pop("slug", None)
    prune_empty_optionals(normalized)

    ordered: dict[str, Any] = {}
    for key in CANONICAL_ISSUE_FIELD_ORDER:
        if key in normalized:
            ordered[key] = normalized[key]
    for key, value in normalized.items():
        if key not in ordered:
            ordered[key] = value
    return ordered


def canonicalize_issue_front_matter_metadata(item: dict[str, Any]) -> dict[str, Any]:
    """Return canonical issue metadata for markdown front matter.

    The canonical issue id is derived from the filename and must not be
    persisted in front matter.
    """
    normalized = canonicalize_issue_metadata(item)
    normalized.pop("id", None)
    return normalized
