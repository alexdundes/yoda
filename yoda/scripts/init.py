#!/usr/bin/env python3
"""Initialize a host project for the embedded YODA package."""

from __future__ import annotations

import argparse
import difflib
import logging
import sys
from pathlib import Path
from typing import Any

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.errors import ExitCode, YodaError
from lib.flow_log import append_flow_log_line, locate_flow_log_bounds, sanitize_flow_message
from lib.front_matter import update_front_matter
from lib.issue_metadata import canonicalize_issue_metadata
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.time_utils import detect_local_timezone, now_iso
from lib.validate import validate_slug, validate_todo

try:
    import yaml
except Exception as exc:  # pragma: no cover - runtime dependency
    raise YodaError(
        "PyYAML is required. Install dependencies from yoda/scripts/requirements.txt.",
        exit_code=ExitCode.ERROR,
    ) from exc

try:
    import frontmatter
except Exception as exc:  # pragma: no cover - runtime dependency
    raise YodaError(
        "python-frontmatter is required. Install dependencies from yoda/scripts/requirements.txt.",
        exit_code=ExitCode.ERROR,
    ) from exc


AGENT_FILES = ["AGENTS.md", "GEMINI.md", "CLAUDE.md"]
REPO_INTENT_FILE = "REPO_INTENT.md"
REPO_INTENT_YAML = "repo.intent.yaml"
REPO_INTENT_HEADER = "# Repository Intent\n\nThis repository embeds the YODA Framework.\n"
YODA_BLOCK = (
    "<!-- YODA:BEGIN -->\n"
    "## YODA Framework\n\n"
    "Read in order:\n\n"
    "1) yoda/yoda.md\n"
    "<!-- YODA:END -->\n"
)
REPO_INTENT_BLOCK = (
    "<!-- YODA:BEGIN -->\n"
    "## YODA Framework\n\n"
    "Read in order:\n\n"
    "1) REPO_INTENT.md\n"
    "2) yoda/yoda.md\n"
    "<!-- YODA:END -->\n"
)
REPO_INTENT_YODA_DEFAULT = {
    "embedded": True,
    "manual": "yoda/yoda.md",
    "agent_entry_order": ["REPO_INTENT.md", "yoda/yoda.md"],
}
DIFF_LIMIT = 40
SCHEMA_VERSION = "2.00"


def _apply_phase_rules(item: dict[str, Any]) -> None:
    if item.get("status") == "doing":
        phase = str(item.get("phase", "")).strip().lower()
        if phase:
            item["phase"] = phase
        else:
            item.pop("phase", None)
        return
    item.pop("phase", None)


def _migrate_legacy_workspace(root: Path, dev: str, dry_run: bool) -> tuple[list[str], list[str]]:
    written: list[str] = []
    skipped: list[str] = []
    todo_file = root / "yoda" / "todos" / f"TODO.{dev}.yaml"
    logs_root = root / "yoda" / "logs"
    issues_root = root / "yoda" / "project" / "issues"

    if not todo_file.exists():
        skipped.append(f"{todo_file.relative_to(root)} (already migrated)")
        return written, skipped

    raw = yaml.safe_load(todo_file.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise YodaError("Invalid TODO YAML root for migration", exit_code=ExitCode.VALIDATION)
    issues = raw.get("issues", [])
    if not isinstance(issues, list):
        raise YodaError("Invalid TODO YAML issues list for migration", exit_code=ExitCode.VALIDATION)

    # Validate all issue files first (full-success rule before deletion).
    resolved_paths: dict[str, Path] = {}
    for item in issues:
        if not isinstance(item, dict):
            raise YodaError("Invalid TODO issue entry (expected mapping)", exit_code=ExitCode.VALIDATION)
        issue_id = str(item.get("id", "")).strip()
        if not issue_id:
            raise YodaError("TODO issue entry missing id", exit_code=ExitCode.VALIDATION)
        matches = sorted(path for path in issues_root.glob(f"{issue_id}-*.md") if path.is_file())
        if len(matches) != 1:
            raise YodaError(
                f"Migration requires exactly one markdown issue file for {issue_id}",
                exit_code=ExitCode.CONFLICT,
            )
        resolved_paths[issue_id] = matches[0]

    for item in issues:
        issue_id = str(item.get("id", "")).strip()
        issue_file = resolved_paths[issue_id]
        metadata = {
            "schema_version": "2.00",
            "id": issue_id,
            "status": str(item.get("status", "to-do")),
            "phase": str(item.get("phase", "")),
            "pending_reason": str(item.get("pending_reason", "")),
            "depends_on": list(item.get("depends_on", []) or []),
            "title": str(item.get("title", "")),
            "description": str(item.get("description", "")),
            "priority": int(item.get("priority", 5)),
            "extern_issue_file": str(item.get("extern_issue_file", "")),
            "created_at": str(item.get("created_at", "")),
            "updated_at": str(item.get("updated_at", "")),
        }
        _apply_phase_rules(metadata)
        normalized = canonicalize_issue_metadata(metadata)
        if not dry_run:
            update_front_matter(issue_file, normalized)
        written.append(f"{issue_file.relative_to(root)} (front matter migrated to 2.00)")

        content = issue_file.read_text(encoding="utf-8")
        has_flow_log = locate_flow_log_bounds(content) is not None
        if has_flow_log:
            skipped.append(f"{issue_file.relative_to(root)} (flow log section exists, legacy log skipped)")
            continue

        log_matches = sorted(path for path in logs_root.glob(f"{issue_id}-*.yaml") if path.is_file())
        if not log_matches:
            continue
        if len(log_matches) > 1:
            raise YodaError(
                f"Migration requires at most one legacy log file for {issue_id}",
                exit_code=ExitCode.CONFLICT,
            )
        log_file = log_matches[0]
        log_doc = yaml.safe_load(log_file.read_text(encoding="utf-8")) or {}
        entries = log_doc.get("entries", [])
        if not isinstance(entries, list):
            raise YodaError(
                f"Invalid legacy log entries for {issue_id}",
                exit_code=ExitCode.VALIDATION,
            )
        if not dry_run:
            for entry in entries:
                if not isinstance(entry, dict):
                    continue
                timestamp = str(entry.get("timestamp", "")).strip()
                message = sanitize_flow_message(str(entry.get("message", "")))
                if not timestamp or not message:
                    continue
                append_flow_log_line(issue_file, f"{timestamp} {message}")
        written.append(f"{issue_file.relative_to(root)} (legacy log migrated)")

    if not dry_run:
        for path in sorted(logs_root.glob(f"{dev}-*.yaml")):
            path.unlink(missing_ok=True)
        todo_file.unlink(missing_ok=True)
    written.append(f"{todo_file.relative_to(root)} (removed)")
    written.append(f"yoda/logs/{dev}-*.yaml (removed)")
    return written, skipped


def _touch_markdown_files(root: Path, dry_run: bool) -> int:
    files = sorted(path for path in root.rglob("*.md") if path.is_file())
    if not dry_run:
        for path in files:
            path.touch()
    return len(files)


def _reconcile_todo_and_issues(
    root: Path,
    dev: str,
    dry_run: bool,
) -> tuple[list[str], list[str]]:
    todo_file = root / "yoda" / "todos" / f"TODO.{dev}.yaml"
    if not todo_file.exists():
        return [], [f"{todo_file.relative_to(root)} (missing, reconcile skipped)"]

    raw = yaml.safe_load(todo_file.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise YodaError("Invalid TODO YAML root for reconcile", exit_code=ExitCode.VALIDATION)

    timezone = str(raw.get("timezone") or detect_local_timezone())
    timestamp = now_iso(timezone)

    raw["schema_version"] = SCHEMA_VERSION
    raw["updated_at"] = timestamp
    issues = raw.get("issues", [])
    if not isinstance(issues, list):
        raise YodaError("TODO issues must be a list", exit_code=ExitCode.VALIDATION)

    written: list[str] = []
    skipped: list[str] = []
    for idx, issue in enumerate(issues):
        if not isinstance(issue, dict):
            continue
        issue["schema_version"] = SCHEMA_VERSION
        issue.pop("agent", None)
        issue.pop("tags", None)
        issue.pop("entrypoints", None)
        issue.pop("lightweight", None)
        issue.pop("origin", None)
        issue.pop("slug", None)
        issue["extern_issue_file"] = str(issue.get("extern_issue_file", "") or "")
        issue["updated_at"] = timestamp
        normalized = canonicalize_issue_metadata(issue)
        issues[idx] = normalized

        issue_id = str(normalized.get("id", ""))
        if not issue_id:
            skipped.append("issue metadata missing id")
            continue
        matches = sorted(
            path
            for path in (root / "yoda" / "project" / "issues").glob(f"{issue_id}-*.md")
            if path.is_file()
        )
        if not matches:
            skipped.append(f"yoda/project/issues/{issue_id}-*.md (missing, reconcile skipped)")
            continue
        if len(matches) > 1:
            names = ", ".join(path.name for path in matches)
            skipped.append(f"{issue_id} has multiple issue files ({names}), reconcile skipped")
            continue
        issue_file = matches[0]
        if not dry_run:
            update_front_matter(issue_file, normalized)
        written.append(f"{issue_file.relative_to(root)} (reconciled)")

    validate_todo(raw, dev)
    if not dry_run:
        todo_file.write_text(
            yaml.safe_dump(raw, sort_keys=False, allow_unicode=False),
            encoding="utf-8",
        )
    written.append(f"{todo_file.relative_to(root)} (reconciled)")
    return written, skipped


def _sanitize_issue_front_matter_ids(
    root: Path,
    dev: str,
    dry_run: bool,
) -> tuple[list[str], list[str]]:
    issues_root = root / "yoda" / "project" / "issues"
    written: list[str] = []
    skipped: list[str] = []
    if not issues_root.exists():
        return written, skipped

    for issue_file in sorted(path for path in issues_root.glob(f"{dev}-*.md") if path.is_file()):
        post = frontmatter.load(str(issue_file))
        metadata = dict(post.metadata)
        if "id" not in metadata:
            continue
        metadata.pop("id", None)
        normalized = canonicalize_issue_metadata(metadata)
        if not dry_run:
            update_front_matter(issue_file, normalized)
        written.append(f"{issue_file.relative_to(root)} (removed front matter id)")
    return written, skipped


def _diff_summary(expected: str, existing: str, label: str) -> list[str]:
    diff = list(
        difflib.unified_diff(
            expected.splitlines(),
            existing.splitlines(),
            fromfile=f"{label} (expected)",
            tofile=f"{label} (existing)",
            lineterm="",
        )
    )
    if len(diff) > DIFF_LIMIT:
        return diff[:DIFF_LIMIT] + ["... (diff truncated)"]
    return diff


def _append_block(existing: str, block: str) -> str:
    if not existing.strip():
        return block
    return existing.rstrip("\n") + "\n\n" + block


def _upsert_block(existing: str, block: str) -> tuple[str, str, str | None]:
    begin = "<!-- YODA:BEGIN -->"
    end = "<!-- YODA:END -->"
    start = existing.find(begin)
    if start == -1:
        return _append_block(existing, block), "appended", None
    end_pos = existing.find(end, start)
    if end_pos == -1:
        return existing, "conflict", "missing YODA:END marker"
    tail_start = end_pos + len(end)
    extra_begin = existing.find(begin, tail_start)
    if extra_begin != -1:
        return existing, "conflict", "multiple YODA blocks found"
    current_block = existing[start:tail_start]
    if current_block.strip("\n") == block.strip("\n"):
        return existing, "unchanged", None
    updated = existing[:start] + block + existing[tail_start:]
    return updated, "updated", None


def _merge_repo_intent(data: dict[str, Any]) -> tuple[dict[str, Any], bool, str | None]:
    yoda_section = data.get("yoda")
    if yoda_section is None:
        updated = dict(data)
        updated["yoda"] = dict(REPO_INTENT_YODA_DEFAULT)
        return updated, True, None
    if not isinstance(yoda_section, dict):
        return data, False, "yoda section is not a mapping"

    changed = False
    updated = dict(data)
    merged_section = dict(yoda_section)
    for key, value in REPO_INTENT_YODA_DEFAULT.items():
        if key not in merged_section:
            merged_section[key] = value
            changed = True
    updated["yoda"] = merged_section
    return updated, changed, None


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    lines = [
        f"Root: {payload['root']}",
        f"Developer: {payload['dev']}",
    ]

    if payload.get("dirs_created"):
        lines.append("Directories created:")
        for item in payload["dirs_created"]:
            lines.append(f"- {item}")

    if payload.get("files_written"):
        lines.append("Files written:")
        for item in payload["files_written"]:
            lines.append(f"- {item}")

    if payload.get("files_skipped"):
        lines.append("Files skipped:")
        for item in payload["files_skipped"]:
            lines.append(f"- {item}")

    conflicts = payload.get("conflicts", [])
    if conflicts:
        lines.append("Conflicts:")
        for item in conflicts:
            lines.append(f"- {item['path']}: {item['reason']}")
            for diff_line in item.get("diff", []):
                lines.append(diff_line)

    return render_output(payload, output_format, lines, dry_run=bool(payload.get("dry_run")))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Initialize an embedded YODA project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Agent guidance:\n"
            "- Purpose: prepare/reconcile a host project with embedded YODA structure and metadata.\n"
            "- When to use: after install/update, or to reconcile legacy files with current schema.\n"
            "- Mutability: creates/updates project files and may migrate/remove legacy TODO/log YAML."
        ),
    )
    add_global_flags(parser)
    parser.add_argument("--root", help="Project root to initialize (default: cwd)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument(
        "--reconcile-layout",
        action="store_true",
        help="Touch markdown files and reconcile TODO/issues front matter to current schema",
    )

    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = resolve_dev(args.dev).strip()
        validate_slug(dev)

        root = Path(args.root or Path.cwd()).expanduser().resolve()
        if not root.exists() or not root.is_dir():
            raise YodaError(f"Invalid root directory: {root}", exit_code=ExitCode.VALIDATION)

        manual_path = root / "yoda" / "yoda.md"
        if not manual_path.is_file():
            raise YodaError(
                f"Missing embedded manual at {manual_path}",
                exit_code=ExitCode.NOT_FOUND,
            )

        dirs = [
            root / "yoda" / "todos",
            root / "yoda" / "logs",
            root / "yoda" / "project" / "issues",
        ]

        dirs_created: list[str] = []
        files_written: list[str] = []
        files_skipped: list[str] = []
        conflicts: list[dict[str, Any]] = []
        exit_code = ExitCode.SUCCESS

        for path in dirs:
            if path.exists():
                if not path.is_dir():
                    raise YodaError(
                        f"Path exists and is not a directory: {path}",
                        exit_code=ExitCode.VALIDATION,
                    )
                continue
            if not args.dry_run:
                path.mkdir(parents=True, exist_ok=True)
            dirs_created.append(str(path.relative_to(root)))

        for filename in AGENT_FILES:
            agents_path = root / filename
            if agents_path.exists():
                if agents_path.is_dir():
                    conflicts.append(
                        {
                            "path": filename,
                            "reason": "path exists and is a directory",
                            "diff": [],
                        }
                    )
                    files_skipped.append(f"{filename} (kept)")
                    exit_code = ExitCode.CONFLICT
                    continue
                try:
                    existing = agents_path.read_text(encoding="utf-8")
                except OSError:
                    conflicts.append(
                        {
                            "path": filename,
                            "reason": "unreadable file",
                            "diff": [],
                        }
                    )
                    files_skipped.append(f"{filename} (kept)")
                    exit_code = ExitCode.CONFLICT
                    continue

                updated, status, reason = _upsert_block(existing, YODA_BLOCK)
                if status == "conflict":
                    conflicts.append(
                        {
                            "path": filename,
                            "reason": reason or "invalid YODA block",
                            "diff": [],
                        }
                    )
                    files_skipped.append(f"{filename} (kept)")
                    exit_code = ExitCode.CONFLICT
                elif status == "unchanged":
                    files_skipped.append(f"{filename} (unchanged)")
                else:
                    if not args.dry_run:
                        agents_path.write_text(updated, encoding="utf-8")
                    action = "updated" if status == "updated" else "appended"
                    files_written.append(f"{filename} ({action})")
            else:
                if not args.dry_run:
                    agents_path.write_text(YODA_BLOCK, encoding="utf-8")
                files_written.append(f"{filename} (created)")

        intent_path = root / REPO_INTENT_FILE
        if intent_path.exists():
            if intent_path.is_dir():
                conflicts.append(
                    {
                        "path": REPO_INTENT_FILE,
                        "reason": "path exists and is a directory",
                        "diff": [],
                    }
                )
                files_skipped.append(f"{REPO_INTENT_FILE} (kept)")
                exit_code = ExitCode.CONFLICT
            else:
                try:
                    existing = intent_path.read_text(encoding="utf-8")
                except OSError:
                    conflicts.append(
                        {
                            "path": REPO_INTENT_FILE,
                            "reason": "unreadable file",
                            "diff": [],
                        }
                    )
                    files_skipped.append(f"{REPO_INTENT_FILE} (kept)")
                    exit_code = ExitCode.CONFLICT
                else:
                    updated, status, reason = _upsert_block(existing, REPO_INTENT_BLOCK)
                    if status == "conflict":
                        conflicts.append(
                            {
                                "path": REPO_INTENT_FILE,
                                "reason": reason or "invalid YODA block",
                                "diff": [],
                            }
                        )
                        files_skipped.append(f"{REPO_INTENT_FILE} (kept)")
                        exit_code = ExitCode.CONFLICT
                    elif status == "unchanged":
                        files_skipped.append(f"{REPO_INTENT_FILE} (unchanged)")
                    else:
                        if not args.dry_run:
                            intent_path.write_text(updated, encoding="utf-8")
                        action = "updated" if status == "updated" else "appended"
                        files_written.append(f"{REPO_INTENT_FILE} ({action})")
        else:
            content = _append_block(REPO_INTENT_HEADER, REPO_INTENT_BLOCK)
            if not args.dry_run:
                intent_path.write_text(content, encoding="utf-8")
            files_written.append(f"{REPO_INTENT_FILE} (created)")

        intent_yaml_path = root / REPO_INTENT_YAML
        if intent_yaml_path.exists():
            if intent_yaml_path.is_dir():
                conflicts.append(
                    {
                        "path": REPO_INTENT_YAML,
                        "reason": "path exists and is a directory",
                        "diff": [],
                    }
                )
                files_skipped.append(f"{REPO_INTENT_YAML} (kept)")
                exit_code = ExitCode.CONFLICT
            else:
                try:
                    raw = intent_yaml_path.read_text(encoding="utf-8")
                    data = yaml.safe_load(raw)
                except Exception:
                    conflicts.append(
                        {
                            "path": REPO_INTENT_YAML,
                            "reason": "invalid YAML",
                            "diff": [],
                        }
                    )
                    files_skipped.append(f"{REPO_INTENT_YAML} (kept)")
                    exit_code = ExitCode.CONFLICT
                else:
                    if data is None:
                        data = {}
                    if not isinstance(data, dict):
                        conflicts.append(
                            {
                                "path": REPO_INTENT_YAML,
                                "reason": "YAML root is not a mapping",
                                "diff": [],
                            }
                        )
                        files_skipped.append(f"{REPO_INTENT_YAML} (kept)")
                        exit_code = ExitCode.CONFLICT
                    else:
                        merged, changed, reason = _merge_repo_intent(data)
                        if reason:
                            conflicts.append(
                                {
                                    "path": REPO_INTENT_YAML,
                                    "reason": reason,
                                    "diff": [],
                                }
                            )
                            files_skipped.append(f"{REPO_INTENT_YAML} (kept)")
                            exit_code = ExitCode.CONFLICT
                        elif not changed:
                            files_skipped.append(f"{REPO_INTENT_YAML} (unchanged)")
                        else:
                            if not args.dry_run:
                                intent_yaml_path.write_text(
                                    yaml.safe_dump(
                                        merged, sort_keys=False, allow_unicode=False
                                    ),
                                    encoding="utf-8",
                                )
                            files_written.append(f"{REPO_INTENT_YAML} (updated)")
        else:
            if not args.dry_run:
                intent_yaml_path.write_text(
                    yaml.safe_dump(
                        {"yoda": REPO_INTENT_YODA_DEFAULT},
                        sort_keys=False,
                        allow_unicode=False,
                    ),
                    encoding="utf-8",
                )
            files_written.append(f"{REPO_INTENT_YAML} (created)")

        migrated_written, migrated_skipped = _migrate_legacy_workspace(
            root=root,
            dev=dev,
            dry_run=bool(args.dry_run),
        )
        files_written.extend(migrated_written)
        files_skipped.extend(migrated_skipped)

        if args.reconcile_layout:
            touched = _touch_markdown_files(root, args.dry_run)
            files_written.append(f"*.md touched: {touched}")
            reconcile_written, reconcile_skipped = _reconcile_todo_and_issues(
                root=root,
                dev=dev,
                dry_run=bool(args.dry_run),
            )
            files_written.extend(reconcile_written)
            files_skipped.extend(reconcile_skipped)

        sanitize_written, sanitize_skipped = _sanitize_issue_front_matter_ids(
            root=root,
            dev=dev,
            dry_run=bool(args.dry_run),
        )
        files_written.extend(sanitize_written)
        files_skipped.extend(sanitize_skipped)

        payload = {
            "root": str(root),
            "dev": dev,
            "dirs_created": dirs_created,
            "files_written": files_written,
            "files_skipped": files_skipped,
            "conflicts": conflicts,
            "dry_run": bool(args.dry_run),
        }

        print(_render_output(payload, output_format))
        return exit_code
    except YodaError as exc:
        logging.error(str(exc))
        return exc.exit_code
    except Exception as exc:  # pragma: no cover
        logging.error("Unexpected error: %s", exc)
        return ExitCode.ERROR


if __name__ == "__main__":
    sys.exit(main())
