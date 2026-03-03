"""Front matter helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .errors import YodaError, ExitCode
from .issue_metadata import canonicalize_issue_metadata
from .io import write_text

try:
    import frontmatter
except Exception as exc:  # pragma: no cover - runtime dependency
    raise YodaError(
        "python-frontmatter is required. Install dependencies from yoda/scripts/requirements.txt.",
        exit_code=ExitCode.ERROR,
    ) from exc

try:
    import yaml
except Exception as exc:  # pragma: no cover - runtime dependency
    raise YodaError(
        "PyYAML is required. Install dependencies from yoda/scripts/requirements.txt.",
        exit_code=ExitCode.ERROR,
    ) from exc


def _dump_with_front_matter(metadata: dict[str, Any], content: str) -> str:
    metadata_text = yaml.safe_dump(metadata, sort_keys=False, allow_unicode=False).strip()
    body = content.lstrip("\n")
    if body:
        return f"---\n{metadata_text}\n---\n\n{body}"
    return f"---\n{metadata_text}\n---\n"


def render_issue(template_text: str, metadata: dict[str, Any], replacements: dict[str, str]) -> str:
    post = frontmatter.loads(template_text)
    content = post.content
    for key, value in replacements.items():
        content = content.replace(key, value)
    return _dump_with_front_matter(canonicalize_issue_metadata(metadata), content)


def update_front_matter(path: Path, metadata: dict[str, Any]) -> None:
    post = frontmatter.load(str(path))
    rendered = _dump_with_front_matter(canonicalize_issue_metadata(metadata), post.content)
    write_text(path, rendered)
