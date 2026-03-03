"""Helpers for issue metadata normalization."""

from __future__ import annotations

from typing import Any


OPTIONAL_EMPTY_KEYS = ("depends_on", "pending_reason", "extern_issue_file")


def prune_empty_optionals(item: dict[str, Any]) -> dict[str, Any]:
    """Remove optional keys when they carry empty values."""
    for key in OPTIONAL_EMPTY_KEYS:
        if key not in item:
            continue
        value = item.get(key)
        if value in ("", None, [], {}):
            item.pop(key, None)
    return item

