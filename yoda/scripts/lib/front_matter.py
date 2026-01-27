"""Front matter helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import YodaError, ExitCode

try:
    import frontmatter
except Exception as exc:  # pragma: no cover - runtime dependency
    raise YodaError(
        "python-frontmatter is required. Install dependencies from yoda/scripts/requirements.txt.",
        exit_code=ExitCode.ERROR,
    ) from exc


def render_issue(template_text: str, metadata: dict[str, Any], replacements: dict[str, str]) -> str:
    post = frontmatter.loads(template_text)
    post.metadata = metadata
    content = post.content
    for key, value in replacements.items():
        content = content.replace(key, value)
    post.content = content
    return frontmatter.dumps(post)


def update_front_matter(path: Path, metadata: dict[str, Any]) -> None:
    post = frontmatter.load(str(path))
    post.metadata = metadata
    path.write_text(frontmatter.dumps(post), encoding="utf-8")
