#!/usr/bin/env python3
"""Build the distributable YODA package artefact."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path
from typing import Any, Iterable

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
from lib.error_messages import required_flag
from lib.errors import ExitCode, YodaError
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.paths import repo_root
from lib.time_utils import detect_local_timezone, now_iso
from lib.validate import validate_slug

try:
    import yaml
except Exception as exc:  # pragma: no cover - runtime dependency
    raise YodaError(
        "PyYAML is required. Install dependencies from yoda/scripts/requirements.txt.",
        exit_code=ExitCode.ERROR,
    ) from exc


SEMVER_BUILD_RE = re.compile(
    r"^(?P<version>\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)\+(?P<build>[0-9A-Za-z.-]+)$"
)
MANIFEST_REL = Path("yoda/PACKAGE_MANIFEST.yaml")
CHANGELOG_REL = Path("yoda/CHANGELOG.yaml")
README_REL = Path("README.md")
LICENSE_REL = Path("LICENSE")
YODA_MANUAL_REL = Path("yoda/yoda.md")
TEMPLATES_REL = Path("yoda/templates")
SCRIPTS_REL = Path("yoda/scripts")
FAVICONS_REL = Path("yoda/favicons")

INCLUDE_GLOBS = [
    "README.md",
    "LICENSE",
    "yoda/yoda.md",
    "yoda/templates/**",
    "yoda/scripts/**",
    "yoda/favicons/**",
    "yoda/CHANGELOG.yaml",
    "yoda/PACKAGE_MANIFEST.yaml",
]
EXCLUDE_GLOBS = [
    "project/**",
    "project/specs/**",
    "bootstrap-legacy/**",
    "yoda/logs/**",
    "yoda/todos/**",
    "yoda/project/issues/**",
    "yoda/scripts/tests/**",
    "**/__pycache__/**",
    "**/*.pyc",
    ".git/**",
    ".pytest_cache/**",
    ".DS_Store",
]


def _parse_version(value: str) -> tuple[str, str]:
    match = SEMVER_BUILD_RE.match(value)
    if not match:
        raise YodaError(
            "Invalid version (expected semver+build, e.g. 1.3.0+20260129.a1b2c3)",
            exit_code=ExitCode.VALIDATION,
        )
    return match.group("version"), match.group("build")


def _git_info(root: Path) -> tuple[str, bool]:
    try:
        commit = (
            subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True)
            .strip()
        )
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=root, text=True
        )
    except Exception as exc:  # pragma: no cover - depends on git
        raise YodaError("Failed to resolve git metadata", exit_code=ExitCode.ERROR) from exc
    return commit, bool(status.strip())


def _load_changelog_entries(path: Path) -> list[dict[str, Any]]:
    try:
        content = path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise YodaError(f"Missing file: {path}", exit_code=ExitCode.NOT_FOUND) from exc
    data = yaml.safe_load(content) or []
    if isinstance(data, dict):
        entries = data.get("entries")
    else:
        entries = data
    if not isinstance(entries, list):
        raise YodaError("Invalid changelog format", exit_code=ExitCode.VALIDATION)
    result: list[dict[str, Any]] = []
    for entry in entries:
        if isinstance(entry, dict):
            result.append(entry)
    return result


def _find_changelog_entry(
    entries: Iterable[dict[str, Any]], version: str, build: str
) -> dict[str, Any]:
    for entry in entries:
        if str(entry.get("version")) == version and str(entry.get("build")) == build:
            return entry
    raise YodaError(
        f"Missing changelog entry for {version}+{build}", exit_code=ExitCode.NOT_FOUND
    )


def _digest_entry(entry: dict[str, Any]) -> str:
    payload = json.dumps(entry, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _ensure_required_paths(root: Path, changelog_source: Path) -> None:
    required_files = [README_REL, LICENSE_REL, YODA_MANUAL_REL]
    required_dirs = [TEMPLATES_REL, SCRIPTS_REL]
    for rel in required_files:
        path = root / rel
        if not path.is_file():
            raise YodaError(f"Missing required file: {rel}", exit_code=ExitCode.NOT_FOUND)
    if not changelog_source.is_file():
        raise YodaError(
            f"Missing changelog file: {changelog_source}",
            exit_code=ExitCode.NOT_FOUND,
        )
    for rel in required_dirs:
        path = root / rel
        if not path.is_dir():
            raise YodaError(f"Missing required directory: {rel}", exit_code=ExitCode.NOT_FOUND)


def _is_excluded(rel_path: Path) -> bool:
    parts = rel_path.parts
    if parts[:3] == ("yoda", "scripts", "tests"):
        return True
    for part in parts:
        if part in {".git", "__pycache__", ".pytest_cache"}:
            return True
    if rel_path.name == ".DS_Store":
        return True
    if rel_path.suffix == ".pyc":
        return True
    return False


def _collect_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    for rel in (README_REL, LICENSE_REL, YODA_MANUAL_REL, CHANGELOG_REL):
        files.add(rel)

    for rel_dir in (TEMPLATES_REL, SCRIPTS_REL):
        for path in (root / rel_dir).rglob("*"):
            if not path.is_file():
                continue
            rel_path = path.relative_to(root)
            if _is_excluded(rel_path):
                continue
            files.add(rel_path)

    favicons_dir = root / FAVICONS_REL
    if favicons_dir.is_dir():
        for path in favicons_dir.rglob("*"):
            if not path.is_file():
                continue
            rel_path = path.relative_to(root)
            if _is_excluded(rel_path):
                continue
            files.add(rel_path)

    files.add(MANIFEST_REL)
    return sorted(files, key=lambda path: path.as_posix())


def _dump_yaml(data: dict[str, Any]) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=False)


def _compute_package_sha(
    files: Iterable[Path],
    root: Path,
    manifest_content: str,
    source_overrides: dict[Path, Path],
) -> str:
    hasher = hashlib.sha256()
    manifest_bytes = manifest_content.encode("utf-8")
    for rel in files:
        rel_str = rel.as_posix()
        hasher.update(rel_str.encode("utf-8"))
        hasher.update(b"\0")
        if rel == MANIFEST_REL:
            hasher.update(manifest_bytes)
        else:
            source = source_overrides.get(rel, root / rel)
            hasher.update(source.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


def _tar_filter(info: tarfile.TarInfo) -> tarfile.TarInfo:
    info.uid = 0
    info.gid = 0
    info.uname = ""
    info.gname = ""
    info.mtime = 0
    return info


def _build_tar(
    output_path: Path,
    files: Iterable[Path],
    root: Path,
    manifest_path: Path,
    source_overrides: dict[Path, Path],
) -> None:
    with tarfile.open(output_path, "w:gz") as tar:
        for rel in files:
            arcname = rel.as_posix()
            if rel == MANIFEST_REL:
                tar.add(manifest_path, arcname=arcname, recursive=False, filter=_tar_filter)
            else:
                source = source_overrides.get(rel, root / rel)
                tar.add(source, arcname=arcname, recursive=False, filter=_tar_filter)


def _resolve_output_path(
    args: argparse.Namespace, filename: str, root: Path
) -> Path:
    if args.output and args.dir:
        raise YodaError("Use either --output or --dir, not both", exit_code=ExitCode.VALIDATION)
    if args.output:
        return Path(args.output)
    if args.dir:
        return Path(args.dir) / filename
    return root / filename


def _resolve_path(root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return root / path


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    lines = [
        f"Package filename: {payload['package_filename']}",
        f"Output path: {payload['output_path']}",
        f"Format: {payload['format']}",
        f"Version: {payload['version']}",
        f"Manifest path: {payload['manifest_path']}",
        f"Files: {payload['file_count']}",
    ]
    if payload.get("dry_run"):
        lines.append("Included files:")
        for item in payload.get("files", []):
            lines.append(f"- {item}")
    return render_output(payload, output_format, lines, dry_run=bool(payload.get("dry_run")))


def main() -> int:
    parser = argparse.ArgumentParser(description="Build YODA package artefact")
    add_global_flags(parser)
    parser.add_argument("--version", required=False, help="SemVer+build (e.g. 1.3.0+20260129.a1b2c3)")
    parser.add_argument("--output", help="Output file path")
    parser.add_argument("--dir", help="Output directory")
    parser.add_argument("--archive-format", default="tar.gz", help="Archive format (tar.gz)")
    parser.add_argument("--changelog", help="Override changelog path (default yoda/CHANGELOG.yaml)")

    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = resolve_dev(args.dev).strip()
        validate_slug(dev)

        version_input = (args.version or "").strip()
        if not version_input:
            required_flag("--version")
        version, build = _parse_version(version_input)

        fmt = (args.archive_format or "tar.gz").strip().lower()
        if fmt != "tar.gz":
            raise YodaError("Only tar.gz is supported", exit_code=ExitCode.VALIDATION)

        root = repo_root()
        changelog_source = _resolve_path(root, args.changelog or str(CHANGELOG_REL))
        _ensure_required_paths(root, changelog_source)

        entries = _load_changelog_entries(changelog_source)
        entry = _find_changelog_entry(entries, version, build)
        entry_digest = _digest_entry(entry)

        commit, dirty = _git_info(root)
        built_at = now_iso(detect_local_timezone())

        filename = f"yoda-framework-{version_input}.tar.gz"
        output_path = _resolve_output_path(args, filename, root)
        if output_path.exists() and not args.dry_run:
            raise YodaError(f"Output already exists: {output_path}", exit_code=ExitCode.CONFLICT)

        files = _collect_files(root)
        source_overrides: dict[Path, Path] = {}
        if changelog_source != root / CHANGELOG_REL:
            source_overrides[CHANGELOG_REL] = changelog_source

        manifest: dict[str, Any] = {
            "schema_version": "1.0",
            "package_filename": filename,
            "format": fmt,
            "version": version,
            "build": build,
            "built_at": built_at,
            "built_by": dev,
            "source_commit": commit,
            "source_dirty": dirty,
            "package_sha256": "",
            "includes": INCLUDE_GLOBS,
            "excludes": EXCLUDE_GLOBS,
            "changelog_version": version_input,
            "changelog_entry_digest": entry_digest,
        }

        manifest_blank = _dump_yaml(manifest)
        package_sha = _compute_package_sha(files, root, manifest_blank, source_overrides)
        manifest["package_sha256"] = package_sha
        manifest_final = _dump_yaml(manifest)

        payload = {
            "package_filename": filename,
            "output_path": str(output_path),
            "manifest_path": MANIFEST_REL.as_posix(),
            "format": fmt,
            "version": version_input,
            "build": build,
            "package_sha256": package_sha,
            "file_count": len(files),
            "files": [path.as_posix() for path in files],
            "dry_run": bool(args.dry_run),
        }

        if args.dry_run:
            print(_render_output(payload, output_format))
            return ExitCode.SUCCESS

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "PACKAGE_MANIFEST.yaml"
            manifest_path.write_text(manifest_final, encoding="utf-8")
            _build_tar(output_path, files, root, manifest_path, source_overrides)

        print(_render_output(payload, output_format))
        return ExitCode.SUCCESS
    except YodaError as exc:
        logging.error(str(exc))
        return exc.exit_code
    except Exception as exc:  # pragma: no cover
        logging.error("Unexpected error: %s", exc)
        return ExitCode.ERROR


if __name__ == "__main__":
    sys.exit(main())
