"""Issue markdown indexing helpers for 0.3.0 flow contracts."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .errors import ExitCode, YodaError
from .io import write_text_atomic
from .paths import issues_dir
from .validate import ALLOWED_STATUS, validate_slug

try:
    import frontmatter
except Exception as exc:  # pragma: no cover - runtime dependency
    raise YodaError(
        "python-frontmatter is required. Install dependencies from yoda/scripts/requirements.txt.",
        exit_code=ExitCode.ERROR,
    ) from exc


ALLOWED_PHASE = {"study", "document", "implement", "evaluate"}


def _issue_filename_re(dev: str) -> re.Pattern[str]:
    return re.compile(rf"^{re.escape(dev)}-(\d{{4}})-([a-z0-9-]+)\.md$")


def _derive_from_filename(path: Path, dev: str) -> tuple[str, str]:
    match = _issue_filename_re(dev).match(path.name)
    if not match:
        raise YodaError(
            f"INVALID_ISSUE_FILENAME: expected <dev>-<NNNN>-<slug>.md; got {path.name}",
            exit_code=ExitCode.VALIDATION,
        )
    number, slug = match.group(1), match.group(2)
    return f"{dev}-{number}", slug


def _has_flow_log(content: str) -> bool:
    return re.search(r"(?m)^## Flow log\s*$", content) is not None


def _ensure_flow_log(path: Path, content: str) -> str:
    if _has_flow_log(content):
        return content
    trimmed = content.rstrip("\n")
    updated = f"{trimmed}\n\n## Flow log\n"
    write_text_atomic(path, updated)
    return updated


def _require_string(metadata: dict[str, Any], key: str, path: Path, issue_id: str) -> str:
    value = metadata.get(key)
    if not isinstance(value, str) or not value.strip():
        raise YodaError(
            f"{path}: {issue_id}: invalid or missing '{key}'",
            exit_code=ExitCode.VALIDATION,
        )
    return value.strip()


def _require_int_priority(metadata: dict[str, Any], path: Path, issue_id: str) -> int:
    value = metadata.get("priority")
    if not isinstance(value, int) or not (0 <= value <= 10):
        raise YodaError(
            f"{path}: {issue_id}: invalid 'priority' (expected integer 0..10)",
            exit_code=ExitCode.VALIDATION,
        )
    return value


def _normalize_depends_on(metadata: dict[str, Any], path: Path, issue_id: str) -> list[str]:
    depends_on = metadata.get("depends_on", [])
    if depends_on in (None, ""):
        return []
    if not isinstance(depends_on, list):
        raise YodaError(
            f"{path}: {issue_id}: invalid 'depends_on' (expected list)",
            exit_code=ExitCode.VALIDATION,
        )
    normalized: list[str] = []
    for dep in depends_on:
        dep_id = str(dep).strip()
        if dep_id:
            normalized.append(dep_id)
    return normalized


def _normalize_phase(metadata: dict[str, Any], status: str, path: Path, issue_id: str) -> str | None:
    phase = metadata.get("phase")
    if status != "doing":
        return None
    if phase in (None, ""):
        return None
    phase_value = str(phase).strip().lower()
    if phase_value not in ALLOWED_PHASE:
        raise YodaError(
            f"{path}: {issue_id}: invalid 'phase' value '{phase_value}'",
            exit_code=ExitCode.VALIDATION,
        )
    return phase_value


def _build_issue_record(path: Path, dev: str, source_index: int) -> dict[str, Any]:
    issue_id, slug = _derive_from_filename(path, dev)
    content = path.read_text(encoding="utf-8")
    content = _ensure_flow_log(path, content)
    post = frontmatter.loads(content)
    metadata = dict(post.metadata)

    status = _require_string(metadata, "status", path, issue_id)
    if status not in ALLOWED_STATUS:
        raise YodaError(
            f"{path}: {issue_id}: invalid 'status' value '{status}'",
            exit_code=ExitCode.VALIDATION,
        )

    return {
        "id": issue_id,
        "dev": dev,
        "slug": slug,
        "path": str(path),
        "status": status,
        "phase": _normalize_phase(metadata, status, path, issue_id),
        "depends_on": _normalize_depends_on(metadata, path, issue_id),
        "title": _require_string(metadata, "title", path, issue_id),
        "description": _require_string(metadata, "description", path, issue_id),
        "priority": _require_int_priority(metadata, path, issue_id),
        "extern_issue_file": str(metadata.get("extern_issue_file", "") or ""),
        "created_at": _require_string(metadata, "created_at", path, issue_id),
        "updated_at": _require_string(metadata, "updated_at", path, issue_id),
        "flow_log_exists": True,
        "_source_index": source_index,
    }


def _is_dependency_done(dep_id: str, by_id: dict[str, dict[str, Any]]) -> bool:
    dep_issue = by_id.get(dep_id)
    if dep_issue is None:
        # Missing dependencies are treated as done by decision in yoda-0049 Study.
        return True
    return dep_issue.get("status") == "done"


def _decorate_selectability(issues: list[dict[str, Any]], by_id: dict[str, dict[str, Any]]) -> None:
    for issue in issues:
        blocked_by = [dep for dep in issue.get("depends_on", []) if not _is_dependency_done(dep, by_id)]
        issue["blocked_by"] = blocked_by
        issue["selectable"] = issue.get("status") == "to-do" and not blocked_by


def _ordered_for_selection(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        issues,
        key=lambda item: (-int(item.get("priority", 0)), int(item.get("_source_index", 0))),
    )


def load_issue_index(dev: str) -> dict[str, Any]:
    """Load deterministic issue index from markdown files for one developer slug."""
    validate_slug(dev)
    files = sorted(path for path in issues_dir().glob(f"{dev}-*.md") if path.is_file())

    issues: list[dict[str, Any]] = []
    by_id: dict[str, dict[str, Any]] = {}
    for idx, path in enumerate(files):
        issue = _build_issue_record(path, dev, idx)
        issue_id = str(issue["id"])
        if issue_id in by_id:
            raise YodaError(
                f"{path}: duplicate derived issue id '{issue_id}'",
                exit_code=ExitCode.CONFLICT,
            )
        issues.append(issue)
        by_id[issue_id] = issue

    _decorate_selectability(issues, by_id)
    ordered = _ordered_for_selection(issues)
    for item in ordered:
        item.pop("_source_index", None)

    return {
        "issues": ordered,
        "by_id": {str(item["id"]): item for item in ordered},
        "errors": [],
    }

