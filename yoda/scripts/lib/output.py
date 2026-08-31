"""Output rendering helpers."""

from __future__ import annotations

import json
from typing import Any, Iterable


def runbook_md_lines(runbook_line: str) -> list[str]:
    """Render a runbook as one Markdown list item, tolerating multiple lines.

    `runbook_line` is no longer restricted to a single line, so continuation
    lines are indented to stay inside the same list item.
    """
    first, *rest = str(runbook_line).splitlines() or [""]
    return [f"- {first}", *(f"  {line}" for line in rest)]


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
