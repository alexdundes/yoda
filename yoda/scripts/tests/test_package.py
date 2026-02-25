from __future__ import annotations

import re
import tarfile
from pathlib import Path

from conftest import REPO_ROOT, TEST_DEV, run_script


def _ensure_license() -> bool:
    license_path = REPO_ROOT / "LICENSE"
    if license_path.exists():
        return True
    license_path.write_text("Test License\n", encoding="utf-8")
    return False


def _cleanup_license(existed: bool) -> None:
    if existed:
        return
    license_path = REPO_ROOT / "LICENSE"
    if license_path.exists():
        license_path.unlink()


def _write_changelog(path: Path, version: str, build: str) -> None:
    content = (
        "- version: \"{version}\"\n"
        "  build: \"{build}\"\n"
        "  date: \"2026-02-02T00:00:00+00:00\"\n"
        "  summary:\n"
        "    - \"Test release\"\n"
        "  breaking: []\n"
        "  additions: []\n"
        "  fixes: []\n"
        "  notes: \"\"\n"
        "  commit: \"deadbeef\"\n"
    ).format(version=version, build=build)
    path.write_text(content, encoding="utf-8")


def test_package_builds_and_excludes_tests(tmp_path: Path) -> None:
    license_existed = _ensure_license()
    changelog_path = tmp_path / "CHANGELOG.yaml"
    version = "1.0.0"
    build = "20260202.test"
    version_input = f"{version}+{build}"
    _write_changelog(changelog_path, version, build)
    output_path = tmp_path / "yoda-framework-test.tar.gz"

    try:
        result = run_script(
            "package.py",
            [
                "--dev",
                TEST_DEV,
                "--version",
                version_input,
                "--output",
                str(output_path),
                "--changelog",
                str(changelog_path),
            ],
        )
        assert result.returncode == 0, result.stderr
        assert output_path.exists()

        with tarfile.open(output_path, "r:gz") as tar:
            names = tar.getnames()

        assert "README.md" in names
        assert "LICENSE" in names
        assert "yoda/LICENSE" in names
        assert "yoda/yoda.md" in names
        assert "yoda/PACKAGE_MANIFEST.yaml" in names
        assert "CHANGELOG.yaml" in names
        assert not any(name.startswith("yoda/scripts/tests") for name in names)
    finally:
        _cleanup_license(license_existed)


def test_package_dry_run_does_not_write(tmp_path: Path) -> None:
    license_existed = _ensure_license()
    changelog_path = tmp_path / "CHANGELOG.yaml"
    version = "1.0.1"
    build = "20260202.dry"
    version_input = f"{version}+{build}"
    _write_changelog(changelog_path, version, build)
    output_path = tmp_path / "yoda-framework-dry.tar.gz"

    try:
        result = run_script(
            "package.py",
            [
                "--dev",
                TEST_DEV,
                "--version",
                version_input,
                "--output",
                str(output_path),
                "--changelog",
                str(changelog_path),
                "--dry-run",
            ],
        )
        assert result.returncode == 0, result.stderr
        assert not output_path.exists()
    finally:
        _cleanup_license(license_existed)


def test_package_next_version_updates_changelog(tmp_path: Path) -> None:
    license_existed = _ensure_license()
    changelog_path = tmp_path / "CHANGELOG.yaml"
    _write_changelog(changelog_path, "1.1.0", "20260202.base")

    try:
        result = run_script(
            "package.py",
            [
                "--dev",
                TEST_DEV,
                "--next-version",
                "1.2.0",
                "--summary",
                "Automated changelog entry",
                "--addition",
                "New packaging contract",
                "--output",
                str(tmp_path / "yoda-framework-next.tar.gz"),
                "--changelog",
                str(changelog_path),
            ],
        )
        assert result.returncode == 0, result.stderr
        content = changelog_path.read_text(encoding="utf-8")
        assert "version: 1.2.0" in content
        assert 'summary:' in content
        assert "Automated changelog entry" in content
        assert re.search(r"build: \d{8}\.[0-9a-f]{7}", content)
    finally:
        _cleanup_license(license_existed)
