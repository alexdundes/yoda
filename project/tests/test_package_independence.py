"""Prove the distributed product does not depend on the specification set.

The package must neither ship `project/specs/` nor need it at runtime. The
smoke test below runs the real entrypoints from an extracted package, in a
directory where `project/specs/` does not exist.

Contract: `project/specs/28-spec-independence-and-portability.md`.
"""

from __future__ import annotations

import subprocess
import sys
import tarfile
from pathlib import Path

from conftest import REPO_ROOT


SMOKE_DEV = "smoke"


def _backup(path: Path) -> bytes | None:
    return path.read_bytes() if path.exists() else None


def _restore(path: Path, content: bytes | None) -> None:
    if content is None:
        if path.exists():
            path.unlink()
        return
    path.write_bytes(content)


def _build_package(out_dir: Path) -> Path:
    """Build a real archive, restoring the repository files package.py mutates."""
    changelog = REPO_ROOT / "CHANGELOG.yaml"
    latest_json = REPO_ROOT / "docs" / "install" / "latest.json"
    changelog_backup = _backup(changelog)
    latest_backup = _backup(latest_json)
    try:
        result = subprocess.run(
            [
                sys.executable,
                str(REPO_ROOT / "package.py"),
                "--dev",
                SMOKE_DEV,
                "--next-version",
                "99.0.0",
                "--summary",
                "Package independence smoke build",
                "--dir",
                str(out_dir),
            ],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, result.stderr
    finally:
        _restore(changelog, changelog_backup)
        _restore(latest_json, latest_backup)

    archives = sorted(out_dir.glob("yoda-framework-99.0.0+*.tar.gz"))
    assert len(archives) == 1, f"expected one archive, got {archives}"
    return archives[0]


def _run_in(extracted: Path, script: str, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(extracted / "yoda" / "scripts" / script), *args],
        capture_output=True,
        text=True,
        cwd=extracted,
    )


def test_package_inventory_excludes_repository_project_tree(tmp_path: Path) -> None:
    archive = _build_package(tmp_path)

    with tarfile.open(archive, "r:gz") as tar:
        names = tar.getnames()

    offenders = [name for name in names if name == "project" or name.startswith("project/")]
    assert not offenders, (
        "Packaged paths under project/ found: "
        + ", ".join(offenders)
        + ". The specification set must not be distributed."
    )
    assert "yoda/yoda.md" in names
    assert "yoda/scripts/yoda_flow_next.py" in names


def test_product_operates_without_the_specs_tree(tmp_path: Path) -> None:
    archive = _build_package(tmp_path / "dist")
    extracted = tmp_path / "extracted"
    extracted.mkdir()
    with tarfile.open(archive, "r:gz") as tar:
        tar.extractall(extracted)

    assert not (extracted / "project").exists(), "extracted tree must not contain project/"

    init = _run_in(extracted, "init.py", ["--dev", SMOKE_DEV])
    assert init.returncode == 0, init.stderr

    created = _run_in(
        extracted,
        "issue_add.py",
        [
            "--dev",
            SMOKE_DEV,
            "--title",
            "Smoke issue",
            "--description",
            "Created from an extracted package without project/specs.",
            "--format",
            "json",
        ],
    )
    assert created.returncode == 0, created.stderr

    issue_files = sorted((extracted / "yoda" / "project" / "issues").glob(f"{SMOKE_DEV}-*.md"))
    assert len(issue_files) == 1, f"expected one issue in the extracted tree, got {issue_files}"

    flow = _run_in(extracted, "yoda_flow_next.py", ["--dev", SMOKE_DEV, "--format", "json"])
    assert flow.returncode == 0, flow.stderr
    assert '"phase": "study"' in flow.stdout

    # The original checkout must be untouched: nothing resolved back to it.
    leaked = sorted((REPO_ROOT / "yoda" / "project" / "issues").glob(f"{SMOKE_DEV}-*.md"))
    assert not leaked, f"extracted product wrote into the development checkout: {leaked}"
