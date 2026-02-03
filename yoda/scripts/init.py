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


AGENT_FILES = ["AGENTS.md", "gemini.md", "CLAUDE.md", "agent.md"]
YODA_BLOCK = (
    "<!-- YODA:BEGIN -->\n"
    "## YODA Framework\n\n"
    "Read in order:\n\n"
    "1) yoda/yoda.md\n"
    "<!-- YODA:END -->\n"
)
DIFF_LIMIT = 40


def _build_todo(dev: str, timezone: str) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "developer_name": dev,
        "developer_slug": dev,
        "timezone": timezone,
        "updated_at": now_iso(timezone),
        "issues": [],
    }


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
    parser = argparse.ArgumentParser(description="Initialize an embedded YODA project")
    add_global_flags(parser)
    parser.add_argument("--root", help="Project root to initialize (default: cwd)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")

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

        timezone = detect_local_timezone()
        expected_todo = _build_todo(dev, timezone)
        expected_todo_text = yaml.safe_dump(expected_todo, sort_keys=False, allow_unicode=False)

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

        todo_path = root / "yoda" / "todos" / f"TODO.{dev}.yaml"
        if todo_path.exists():
            if args.force:
                if not args.dry_run:
                    todo_path.write_text(expected_todo_text, encoding="utf-8")
                files_written.append(f"{todo_path.relative_to(root)} (overwritten)")
            else:
                try:
                    data = yaml.safe_load(todo_path.read_text(encoding="utf-8")) or {}
                    if isinstance(data, dict):
                        validate_todo(data, dev)
                        issues = data.get("issues", [])
                        files_skipped.append(
                            f"{todo_path.relative_to(root)} (exists, issues={len(issues)})"
                        )
                    else:
                        raise YodaError("Invalid YAML root", exit_code=ExitCode.VALIDATION)
                except YodaError as exc:
                    conflicts.append(
                        {
                            "path": str(todo_path.relative_to(root)),
                            "reason": f"invalid TODO ({exc})",
                            "diff": _diff_summary(
                                expected_todo_text,
                                todo_path.read_text(encoding="utf-8"),
                                str(todo_path.relative_to(root)),
                            ),
                        }
                    )
                    files_skipped.append(f"{todo_path.relative_to(root)} (kept)")
                    exit_code = ExitCode.CONFLICT
        else:
            if not args.dry_run:
                todo_path.write_text(expected_todo_text, encoding="utf-8")
            files_written.append(f"{todo_path.relative_to(root)} (created)")

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
