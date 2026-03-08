"""Helpers for reading/writing inline Flow log in issue markdown files."""

from __future__ import annotations

import re
from pathlib import Path

from .io import write_text_atomic


def sanitize_flow_message(message: str) -> str:
    """Normalize message to a compact single line."""
    return " | ".join(part.strip() for part in message.splitlines() if part.strip())


def locate_flow_log_bounds(content: str) -> tuple[int, int] | None:
    header_match = re.search(r"(?m)^## Flow log\s*$", content)
    if header_match is None:
        return None
    start = header_match.end()
    next_header = re.search(r"(?m)^##\s+", content[start:])
    if next_header is None:
        return start, len(content)
    return start, start + next_header.start()


def append_flow_log_line(issue_path: Path, line: str) -> None:
    normalized = line.strip()
    if normalized.startswith("- "):
        formatted = normalized
    else:
        formatted = f"- {normalized}"

    content = issue_path.read_text(encoding="utf-8")
    bounds = locate_flow_log_bounds(content)
    if bounds is None:
        trimmed = content.rstrip("\n")
        updated = f"{trimmed}\n\n## Flow log\n{formatted}\n"
        write_text_atomic(issue_path, updated)
        return

    start, end = bounds
    section = content[start:end]
    if not section.startswith("\n"):
        section = f"\n{section}"
    if section and not section.endswith("\n"):
        section = f"{section}\n"
    updated_section = f"{section}{formatted}\n"
    updated = f"{content[:start]}{updated_section}{content[end:]}"
    write_text_atomic(issue_path, updated)
