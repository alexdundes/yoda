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


def _backup_file(path: Path) -> bytes | None:
    if not path.exists():
        return None
    return path.read_bytes()


def _restore_file(path: Path, content: bytes | None) -> None:
    if content is None:
        if path.exists():
            path.unlink()
        return
    path.write_bytes(content)


def test_package_builds_and_excludes_tests(tmp_path: Path) -> None:
    license_existed = _ensure_license()
    changelog_path = REPO_ROOT / "CHANGELOG.yaml"
    latest_json_path = REPO_ROOT / "docs" / "install" / "latest.json"
    changelog_backup = _backup_file(changelog_path)
    latest_backup = _backup_file(latest_json_path)
    try:
        result = run_script(
            "package.py",
            [
                "--dev",
                TEST_DEV,
                "--next-version",
                "1.2.10",
                "--summary",
                "Test package build",
                "--dir",
                str(tmp_path),
            ],
        )
        assert result.returncode == 0, result.stderr
        matches = sorted(tmp_path.glob("yoda-framework-1.2.10+*.tar.gz"))
        assert len(matches) == 1
        output_path = matches[0]
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
        _restore_file(changelog_path, changelog_backup)
        _restore_file(latest_json_path, latest_backup)
        _cleanup_license(license_existed)


def test_package_dry_run_does_not_write(tmp_path: Path) -> None:
    license_existed = _ensure_license()
    changelog_path = REPO_ROOT / "CHANGELOG.yaml"
    latest_json_path = REPO_ROOT / "docs" / "install" / "latest.json"
    changelog_before = changelog_path.read_text(encoding="utf-8")
    latest_before = latest_json_path.read_text(encoding="utf-8")

    try:
        result = run_script(
            "package.py",
            [
                "--dev",
                TEST_DEV,
                "--next-version",
                "1.2.11",
                "--summary",
                "Test dry-run package",
                "--dry-run",
            ],
        )
        assert result.returncode == 0, result.stderr
        assert not list(REPO_ROOT.glob("yoda-framework-1.2.11+*.tar.gz"))
        assert changelog_path.read_text(encoding="utf-8") == changelog_before
        assert latest_json_path.read_text(encoding="utf-8") == latest_before
    finally:
        _cleanup_license(license_existed)


def test_package_next_version_updates_changelog(tmp_path: Path) -> None:
    license_existed = _ensure_license()
    changelog_path = REPO_ROOT / "CHANGELOG.yaml"
    latest_json_path = REPO_ROOT / "docs" / "install" / "latest.json"
    changelog_backup = _backup_file(changelog_path)
    latest_backup = _backup_file(latest_json_path)

    try:
        result = run_script(
            "package.py",
            [
                "--dev",
                TEST_DEV,
                "--next-version",
                "1.2.12",
                "--summary",
                "Automated changelog entry",
                "--addition",
                "New packaging contract",
                "--dir",
                str(tmp_path),
            ],
        )
        assert result.returncode == 0, result.stderr
        content = changelog_path.read_text(encoding="utf-8")
        assert "version: 1.2.12" in content
        assert 'summary:' in content
        assert "Automated changelog entry" in content
        assert re.search(r"build: \d{8}\.[0-9a-f]{7}", content)
    finally:
        _restore_file(changelog_path, changelog_backup)
        _restore_file(latest_json_path, latest_backup)
        _cleanup_license(license_existed)
