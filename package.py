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
from urllib.parse import urlsplit, urlunsplit

SCRIPT_DIR = Path(__file__).resolve().parent
LIB_ROOT = SCRIPT_DIR / "yoda" / "scripts"
if str(LIB_ROOT) not in sys.path:
    sys.path.insert(0, str(LIB_ROOT))

from lib.cli import add_global_flags, resolve_format
from lib.dev import resolve_dev
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


SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
MANIFEST_REL = Path("yoda/PACKAGE_MANIFEST.yaml")
CHANGELOG_REL = Path("CHANGELOG.yaml")
README_REL = Path("README.md")
LICENSE_REL = Path("LICENSE")
YODA_LICENSE_REL = Path("yoda/LICENSE")
YODA_MANUAL_REL = Path("yoda/yoda.md")
TEMPLATES_REL = Path("yoda/templates")
SCRIPTS_REL = Path("yoda/scripts")
FAVICONS_REL = Path("yoda/favicons")
LATEST_JSON_REL = Path("docs/install/latest.json")

INCLUDE_GLOBS = [
    "README.md",
    "LICENSE",
    "yoda/LICENSE",
    "yoda/yoda.md",
    "yoda/templates/**",
    "yoda/scripts/**",
    "yoda/favicons/**",
    "CHANGELOG.yaml",
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

HELP_DESCRIPTION = (
    "Build a deterministic YODA package (tar.gz) and create a CHANGELOG entry."
)

HELP_EPILOG = """Agent runbook (read this before packaging):
Goal:
- Produce one release archive with traceable metadata and a matching changelog entry.

1) Read the packaging contract first:
   - project/specs/23-distribution-and-packaging.md

2) Build release notes from repository history (never guess):
   - Check working tree: git status --short
   - Inspect recent commits: git log --oneline --decorate -n 20
   - Review release scope files: git diff --name-only <base>..HEAD
   - Read the changed files and derive changelog text from those real changes.
   - Use those findings to define --summary/--addition/--fix/--breaking.

3) Default mode:
   - Use --next-version.

4) Release mode:
   - Use --next-version with release text fields
     (--summary/--addition/--fix/--breaking/--notes).

5) Rules for changelog text:
   - Write all changelog text in English.
   - Use direct and concise language.
   - Keep summaries factual.

6) What package.py does in new release entry mode:
   - package.py computes build metadata as YYYYMMDD.<short-commit>.
   - package.py prepends the entry in CHANGELOG.yaml before packaging.
   - package.py updates docs/install/latest.json (version/build/package_url/sha256).
   - SemVer rules: breaking=MAJOR, additive=MINOR, fixes=PATCH.

7) Validate content with dry-run:
   - python3 package.py --dev <slug> --next-version <semver> --summary "<summary>" --dry-run
   - Confirm only allowed files are included and excluded paths are absent.

8) Build the final archive:
   - python3 package.py --dev <slug> --next-version <semver> --summary "<summary>" --dir dist
   - Output folder: dist/
   - Output file: dist/yoda-framework-<semver+build>.tar.gz

9) Final verification:
   - tar -tzf <archive> | sort
   - Required files: README.md, LICENSE, yoda/LICENSE, yoda/yoda.md,
     CHANGELOG.yaml, yoda/PACKAGE_MANIFEST.yaml.

10) Human handoff for GitLab distribution publish:
   - Instruct the human step by step on where to upload the dist archive in GitLab.
   - Provide ready-to-copy text for each relevant screen field
     (for example: tag/version, release title, release notes/description, asset name, asset URL or uploaded file label).
   - Base this text on the generated version/build and the changelog entry.
"""


def _validate_semver(value: str) -> str:
    result = value.strip()
    if not SEMVER_RE.match(result):
        raise YodaError(
            "Invalid next version (expected semver without build, e.g. 1.3.0)",
            exit_code=ExitCode.VALIDATION,
        )
    return result


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


def _write_changelog_entries(path: Path, entries: list[dict[str, Any]]) -> None:
    payload = yaml.safe_dump(entries, sort_keys=False, allow_unicode=False)
    path.write_text(payload, encoding="utf-8")


def _find_changelog_entry(
    entries: Iterable[dict[str, Any]], version: str, build: str
) -> dict[str, Any]:
    for entry in entries:
        if str(entry.get("version")) == version and str(entry.get("build")) == build:
            return entry
    raise YodaError(
        f"Missing changelog entry for {version}+{build}", exit_code=ExitCode.NOT_FOUND
    )


def _entry_exists(entries: Iterable[dict[str, Any]], version: str, build: str) -> bool:
    for entry in entries:
        if str(entry.get("version")) == version and str(entry.get("build")) == build:
            return True
    return False


def _digest_entry(entry: dict[str, Any]) -> str:
    payload = json.dumps(entry, sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _ensure_required_paths(root: Path) -> None:
    required_files = [README_REL, LICENSE_REL, YODA_LICENSE_REL, YODA_MANUAL_REL]
    required_dirs = [TEMPLATES_REL, SCRIPTS_REL]
    for rel in required_files:
        path = root / rel
        if not path.is_file():
            raise YodaError(f"Missing required file: {rel}", exit_code=ExitCode.NOT_FOUND)
    changelog_source = root / CHANGELOG_REL
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
    for rel in (README_REL, LICENSE_REL, YODA_LICENSE_REL, YODA_MANUAL_REL, CHANGELOG_REL):
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
    if args.dir:
        return Path(args.dir) / filename
    return root / filename


def _sha256_file(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _github_release_url_from_origin(root: Path, version: str, filename: str) -> str:
    try:
        remote = (
            subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"], cwd=root, text=True
            )
            .strip()
        )
    except Exception:
        remote = ""

    repo = ""
    if remote.startswith("git@github.com:"):
        repo = remote.split(":", 1)[1]
    elif remote.startswith("https://github.com/") or remote.startswith("http://github.com/"):
        repo = remote.split("github.com/", 1)[1]
    if repo.endswith(".git"):
        repo = repo[:-4]
    repo = repo.strip("/")
    if not repo:
        raise YodaError(
            "Could not derive GitHub release URL from remote.origin.url",
            exit_code=ExitCode.VALIDATION,
        )
    return f"https://github.com/{repo}/releases/download/v{version}/{filename}"


def _derive_package_url(root: Path, latest_path: Path, version: str, filename: str) -> str:
    if latest_path.is_file():
        try:
            data = json.loads(latest_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise YodaError(
                f"Invalid JSON in {LATEST_JSON_REL.as_posix()}",
                exit_code=ExitCode.VALIDATION,
            ) from exc
        current_url = str(data.get("package_url", "")).strip()
        if current_url:
            parsed = urlsplit(current_url)
            parts = [part for part in parsed.path.split("/") if part]
            if parsed.scheme in {"http", "https"} and parsed.netloc and len(parts) >= 2:
                parts[-2] = f"v{version}"
                parts[-1] = filename
                return urlunsplit((parsed.scheme, parsed.netloc, "/" + "/".join(parts), "", ""))
    return _github_release_url_from_origin(root, version, filename)


def _write_latest_json(
    latest_path: Path, version: str, build: str, package_url: str, sha256: str
) -> None:
    latest_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": version,
        "build": build,
        "package_url": package_url,
        "sha256": sha256,
    }
    latest_path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )


def _build_release_entry(
    *,
    version: str,
    build: str,
    built_at: str,
    commit: str,
    summary: list[str],
    additions: list[str],
    fixes: list[str],
    breaking: list[str],
    notes: str,
) -> dict[str, Any]:
    return {
        "version": version,
        "build": build,
        "date": built_at,
        "summary": summary,
        "breaking": breaking,
        "additions": additions,
        "fixes": fixes,
        "notes": notes,
        "commit": commit,
    }


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    lines = [
        f"Package filename: {payload['package_filename']}",
        f"Output path: {payload['output_path']}",
        f"Format: {payload['format']}",
        f"Version: {payload['version']}",
        f"Manifest path: {payload['manifest_path']}",
        f"Files: {payload['file_count']}",
    ]
    if payload.get("changelog_action"):
        lines.append(
            f"Changelog entry {payload['changelog_action']}: "
            f"{payload['version']} ({payload['changelog_path']})"
        )
    if payload.get("dry_run"):
        lines.append("Included files:")
        for item in payload.get("files", []):
            lines.append(f"- {item}")
    return render_output(payload, output_format, lines, dry_run=bool(payload.get("dry_run")))


def main() -> int:
    parser = argparse.ArgumentParser(
        description=HELP_DESCRIPTION,
        epilog=HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    add_global_flags(parser)
    parser.add_argument(
        "--next-version",
        required=True,
        help=(
            "Next release SemVer (without build), e.g. 1.3.0. "
            "Generates build metadata and prepends an entry in CHANGELOG."
        ),
    )
    parser.add_argument(
        "--summary",
        action="append",
        default=[],
        help=(
            "Release summary bullet (repeat 1 to 3 times with --next-version). "
            "Example: --summary \"New package workflow\""
        ),
    )
    parser.add_argument(
        "--addition",
        action="append",
        default=[],
        help="Addition bullet for changelog entry (repeatable, used with --next-version).",
    )
    parser.add_argument(
        "--fix",
        action="append",
        default=[],
        help="Fix bullet for changelog entry (repeatable, used with --next-version).",
    )
    parser.add_argument(
        "--breaking",
        action="append",
        default=[],
        help="Breaking change bullet for changelog entry (repeatable, used with --next-version).",
    )
    parser.add_argument(
        "--notes",
        default="",
        help="Optional notes for changelog entry (used with --next-version).",
    )
    parser.add_argument(
        "--dir",
        help=(
            "Output directory where the default archive name is written "
            "(yoda-framework-<version>.tar.gz)."
        ),
    )
    if len(sys.argv) == 1:
        parser.print_help()
        return ExitCode.SUCCESS

    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = resolve_dev(args.dev).strip()
        validate_slug(dev)

        fmt = "tar.gz"

        root = repo_root()
        _ensure_required_paths(root)
        changelog_source = root / CHANGELOG_REL
        changelog_path = root / CHANGELOG_REL

        built_at = now_iso(detect_local_timezone())
        commit, dirty = _git_info(root)
        short_commit = commit[:7]

        next_version_raw = (args.next_version or "").strip()

        changelog_updated = False
        changelog_action = ""
        tmp_paths: list[Path] = []
        source_overrides: dict[Path, Path] = {}
        entries = _load_changelog_entries(changelog_source)
        version = _validate_semver(next_version_raw)
        summary = [item.strip() for item in args.summary if item.strip()]
        additions = [item.strip() for item in args.addition if item.strip()]
        fixes = [item.strip() for item in args.fix if item.strip()]
        breaking = [item.strip() for item in args.breaking if item.strip()]
        if not (1 <= len(summary) <= 3):
            raise YodaError(
                "--next-version requires 1 to 3 --summary entries",
                exit_code=ExitCode.VALIDATION,
            )
        build = f"{built_at[:10].replace('-', '')}.{short_commit}"
        version_input = f"{version}+{build}"
        if _entry_exists(entries, version, build):
            raise YodaError(
                f"Changelog entry already exists for {version_input}",
                exit_code=ExitCode.CONFLICT,
            )
        new_entry = _build_release_entry(
            version=version,
            build=build,
            built_at=built_at,
            commit=commit,
            summary=summary,
            additions=additions,
            fixes=fixes,
            breaking=breaking,
            notes=(args.notes or "").strip(),
        )
        updated_entries = [new_entry, *entries]
        if args.dry_run:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                suffix=".yaml",
                delete=False,
            ) as tmp_file:
                tmp_path = Path(tmp_file.name)
                tmp_file.write(yaml.safe_dump(updated_entries, sort_keys=False, allow_unicode=False))
            tmp_paths.append(tmp_path)
            source_overrides[CHANGELOG_REL] = tmp_path
            changelog_source_for_validation = tmp_path
            changelog_action = "prepared"
        else:
            _write_changelog_entries(changelog_path, updated_entries)
            changelog_updated = True
            changelog_action = "added"
            changelog_source_for_validation = changelog_source

        entries = _load_changelog_entries(changelog_source_for_validation)
        entry = _find_changelog_entry(entries, version, build)
        entry_digest = _digest_entry(entry)

        filename = f"yoda-framework-{version_input}.tar.gz"
        output_path = _resolve_output_path(args, filename, root)
        if output_path.exists() and not args.dry_run:
            raise YodaError(f"Output already exists: {output_path}", exit_code=ExitCode.CONFLICT)

        files = _collect_files(root)

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
            "changelog_updated": changelog_updated,
            "changelog_action": changelog_action,
            "changelog_path": str(changelog_source),
        }

        if args.dry_run:
            print(_render_output(payload, output_format))
            for tmp_path in tmp_paths:
                try:
                    tmp_path.unlink(missing_ok=True)
                except Exception:
                    pass
            return ExitCode.SUCCESS

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory() as tmp_dir:
            manifest_path = Path(tmp_dir) / "PACKAGE_MANIFEST.yaml"
            manifest_path.write_text(manifest_final, encoding="utf-8")
            _build_tar(output_path, files, root, manifest_path, source_overrides)

        tar_sha256 = _sha256_file(output_path)
        latest_json_path = root / LATEST_JSON_REL
        package_url = _derive_package_url(root, latest_json_path, version, filename)
        _write_latest_json(latest_json_path, version, build, package_url, tar_sha256)

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
