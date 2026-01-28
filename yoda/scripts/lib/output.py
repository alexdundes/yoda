"""Output rendering helpers."""

from __future__ import annotations

import json
from typing import Any, Iterable


def render_output(
    payload: dict[str, Any],
    output_format: str,
    md_lines: Iterable[str],
    *,
    dry_run: bool = False,
) -> str:
    if output_format == "json":
        return json.dumps(payload, indent=2, ensure_ascii=True)
    lines = list(md_lines)
    if dry_run:
        lines.append("Dry-run: no files written")
    return "\n".join(lines)
