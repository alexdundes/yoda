#!/usr/bin/env python3
"""Update an embedded YODA package in a host project."""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import shutil
import sys
import tarfile
import tempfile
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from lib.cli import add_global_flags, resolve_format
from lib.errors import ExitCode, YodaError
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.validate import validate_slug

try:
    import yaml
except Exception as exc:  # pragma: no cover - runtime dependency
    raise YodaError(
        "PyYAML is required. Install dependencies from yoda/scripts/requirements.txt.",
        exit_code=ExitCode.ERROR,
    ) from exc


DEFAULT_LATEST_URL = "https://alexdundes.github.io/yoda/install/latest.json"
BACKUP_GITIGNORE = "*\n!.gitignore\n"


def _is_url(value: str) -> bool:
    return urlparse(value).scheme in {"http", "https", "file"}


def _download_to(url: str, dest: Path) -> None:
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
    except Exception as exc:
        raise YodaError(f"Failed to download {url}", exit_code=ExitCode.ERROR) from exc
    dest.write_bytes(data)


def _load_json_from_source(source: str, tmp_dir: Path) -> dict[str, Any]:
    path = Path(source).expanduser()
    if path.is_file():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise YodaError("Invalid JSON in latest.json", exit_code=ExitCode.VALIDATION) from exc
    if not _is_url(source):
        raise YodaError(f"latest.json not found: {source}", exit_code=ExitCode.NOT_FOUND)
    target = tmp_dir / "latest.json"
    _download_to(source, target)
    try:
        return json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise YodaError("Invalid JSON in latest.json", exit_code=ExitCode.VALIDATION) from exc


def _load_manifest(path: Path, label: str) -> tuple[str, str]:
    if not path.is_file():
        raise YodaError(f"Missing {label} manifest: {path}", exit_code=ExitCode.NOT_FOUND)
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise YodaError(f"Invalid {label} manifest format", exit_code=ExitCode.VALIDATION)
    version = str(data.get("version", "")).strip()
    build = str(data.get("build", "")).strip()
    if not version or not build:
        raise YodaError(
            f"{label} manifest missing version/build",
            exit_code=ExitCode.VALIDATION,
        )
    return version, build


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _ensure_backup_gitignore(backup_root: Path) -> None:
    backup_root.mkdir(parents=True, exist_ok=True)
    gitignore_path = backup_root / ".gitignore"
    if gitignore_path.exists():
        return
    gitignore_path.write_text(BACKUP_GITIGNORE, encoding="utf-8")


def _copy_entry(src: Path, dest: Path) -> None:
    if dest.exists():
        if dest.is_dir():
            shutil.rmtree(dest)
        else:
            dest.unlink()
    if src.is_dir():
        shutil.copytree(src, dest)
    else:
        shutil.copy2(src, dest)


def _copy_project(src_project: Path, dest_project: Path) -> None:
    dest_project.mkdir(parents=True, exist_ok=True)
    for entry in src_project.iterdir():
        if entry.name == "issues":
            continue
        _copy_entry(entry, dest_project / entry.name)


def _run_init(root: Path, dev: str, dry_run: bool) -> None:
    init_script = Path(__file__).resolve().parent / "init.py"
    cmd = [sys.executable, str(init_script), "--dev", dev, "--root", str(root)]
    if dry_run:
        cmd.append("--dry-run")
    result = os.spawnv(os.P_WAIT, sys.executable, cmd)
    if result != 0:
        raise YodaError("init.py failed", exit_code=ExitCode.ERROR)


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    lines = [
        f"Mode: {payload['mode']}",
        f"Root: {payload['root']}",
        f"Current version: {payload['current_version']}",
        f"Latest version: {payload['latest_version']}",
        f"Target version: {payload['target_version']}",
        f"Update available: {payload['update_available']}",
    ]
    if payload.get("package_source"):
        lines.append(f"Package source: {payload['package_source']}")
    if payload.get("backup_path"):
        lines.append(f"Backup path: {payload['backup_path']}")
    if payload.get("installed_version"):
        lines.append(f"Installed version: {payload['installed_version']}")
    if payload.get("actions"):
        lines.append("Actions:")
        for action in payload["actions"]:
            lines.append(f"- {action}")
    return render_output(payload, output_format, lines, dry_run=bool(payload.get("dry_run")))


def main() -> int:
    parser = argparse.ArgumentParser(description="Update an embedded YODA package")
    add_global_flags(parser)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--check", action="store_true", help="Check for updates only")
    group.add_argument("--apply", action="store_true", help="Apply the update")
    parser.add_argument("--root", help="Project root (default: cwd)")
    parser.add_argument("--source", help="Override package URL with local path or URL")
    parser.add_argument("--version", help="Target SemVer+build to apply/check")
    parser.add_argument("--latest", help="Override latest.json location (path or URL)")

    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = args.dev or os.environ.get("YODA_DEV") or ""
        if dev:
            validate_slug(dev)

        root = Path(args.root or Path.cwd()).expanduser().resolve()
        if not root.exists() or not root.is_dir():
            raise YodaError(f"Invalid root directory: {root}", exit_code=ExitCode.VALIDATION)

        current_manifest = root / "yoda" / "PACKAGE_MANIFEST.yaml"
        current_version, current_build = _load_manifest(current_manifest, "current")
        current_full = f"{current_version}+{current_build}"

        latest_source = args.latest or os.environ.get("YODA_LATEST_URL") or DEFAULT_LATEST_URL

        with tempfile.TemporaryDirectory() as tmp_dir_str:
            tmp_dir = Path(tmp_dir_str)
            latest = _load_json_from_source(latest_source, tmp_dir)
            latest_version = str(latest.get("version", "")).strip()
            latest_build = str(latest.get("build", "")).strip()
            latest_sha = str(latest.get("sha256", "")).strip().lower()
            package_url = str(latest.get("package_url", "")).strip()

            if not latest_version or not latest_build or not latest_sha or not package_url:
                raise YodaError("latest.json missing required fields", exit_code=ExitCode.VALIDATION)

            latest_full = f"{latest_version}+{latest_build}"
            target_version = args.version or latest_full
            update_available = current_full != target_version

            payload: dict[str, Any] = {
                "mode": "apply" if args.apply else "check",
                "root": str(root),
                "current_version": current_full,
                "latest_version": latest_full,
                "target_version": target_version,
                "update_available": update_available,
                "package_source": "",
                "backup_path": "",
                "installed_version": "",
                "actions": [],
                "dry_run": bool(args.dry_run),
            }

            if args.check:
                print(_render_output(payload, output_format))
                return ExitCode.SUCCESS

            package_source = args.source or package_url
            payload["package_source"] = package_source

            if args.version and args.version != latest_full:
                payload["actions"].append(
                    "Requested version differs from latest.json; proceeding with provided version"
                )

            if Path(package_source).expanduser().is_file():
                tar_path = Path(package_source).expanduser().resolve()
            elif _is_url(package_source):
                tar_path = tmp_dir / "yoda-framework.tar.gz"
                _download_to(package_source, tar_path)
            else:
                raise YodaError(
                    f"Invalid --source (not a file or URL): {package_source}",
                    exit_code=ExitCode.VALIDATION,
                )

            actual_sha = _sha256(tar_path)
            if actual_sha != latest_sha:
                raise YodaError(
                    f"Checksum mismatch (expected {latest_sha}, got {actual_sha})",
                    exit_code=ExitCode.VALIDATION,
                )

            extract_dir = tmp_dir / "extract"
            extract_dir.mkdir(parents=True, exist_ok=True)
            with tarfile.open(tar_path, "r:gz") as tar:
                tar.extractall(extract_dir)

            package_root = extract_dir
            package_yoda = package_root / "yoda"
            package_manifest = package_yoda / "PACKAGE_MANIFEST.yaml"
            package_version, package_build = _load_manifest(package_manifest, "package")
            package_full = f"{package_version}+{package_build}"

            if args.version and package_full != args.version:
                raise YodaError(
                    f"Package version {package_full} does not match --version {args.version}",
                    exit_code=ExitCode.VALIDATION,
                )
            if not args.version and package_full != latest_full:
                raise YodaError(
                    f"Package version {package_full} does not match latest.json {latest_full}",
                    exit_code=ExitCode.VALIDATION,
                )

            if package_full == current_full:
                payload["installed_version"] = package_full
                payload["actions"].append("Already at target version; no update applied")
                print(_render_output(payload, output_format))
                return ExitCode.SUCCESS

            backup_dir = root / "yoda" / "_previous" / current_full
            payload["backup_path"] = str(backup_dir)
            payload["installed_version"] = package_full

            if args.dry_run:
                payload["actions"].extend(
                    [
                        f"Would back up yoda/ to {backup_dir}",
                        "Would replace framework files under yoda/",
                    ]
                )
                if dev:
                    payload["actions"].append(f"Would run init.py for dev {dev}")
                else:
                    payload["actions"].append("Would skip init (no --dev provided)")
                print(_render_output(payload, output_format))
                return ExitCode.SUCCESS

            dest_yoda = root / "yoda"
            if not dest_yoda.is_dir():
                raise YodaError(f"Missing yoda directory at {dest_yoda}", exit_code=ExitCode.NOT_FOUND)

            _ensure_backup_gitignore(backup_dir.parent)
            if backup_dir.exists():
                if not backup_dir.is_dir():
                    raise YodaError(
                        f"Backup path exists and is not a directory: {backup_dir}",
                        exit_code=ExitCode.CONFLICT,
                    )
                payload["actions"].append("Backup already exists; leaving as-is")
            else:
                shutil.copytree(
                    dest_yoda,
                    backup_dir,
                    ignore=shutil.ignore_patterns("_previous"),
                )
                payload["actions"].append("Backup created")

            if not package_yoda.is_dir():
                raise YodaError(
                    "Package does not contain yoda/ directory",
                    exit_code=ExitCode.NOT_FOUND,
                )

            for entry in package_yoda.iterdir():
                if entry.name in {"todos", "logs"}:
                    continue
                if entry.name == "project":
                    _copy_project(entry, dest_yoda / "project")
                else:
                    _copy_entry(entry, dest_yoda / entry.name)

            payload["actions"].append("Framework files replaced")

            if dev:
                _run_init(root, dev, args.dry_run)
                payload["actions"].append("init.py executed")
            else:
                payload["actions"].append("init.py skipped (no --dev provided)")

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
