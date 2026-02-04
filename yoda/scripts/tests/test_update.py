from __future__ import annotations

import hashlib
import json
import tarfile
from pathlib import Path

from conftest import run_script, write_yaml


def _write_manifest(path: Path, version: str, build: str) -> None:
    write_yaml(path, {"version": version, "build": build})


def _sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _setup_root(root: Path, version: str, build: str) -> None:
    yoda_dir = root / "yoda"
    (yoda_dir / "project" / "issues").mkdir(parents=True, exist_ok=True)
    (yoda_dir / "todos").mkdir(parents=True, exist_ok=True)
    (yoda_dir / "logs").mkdir(parents=True, exist_ok=True)
    _write_manifest(yoda_dir / "PACKAGE_MANIFEST.yaml", version, build)
    (yoda_dir / "yoda.md").write_text("old manual\n", encoding="utf-8")
    (yoda_dir / "todos" / "keep.txt").write_text("keep todo\n", encoding="utf-8")
    (yoda_dir / "logs" / "keep.txt").write_text("keep log\n", encoding="utf-8")
    (yoda_dir / "project" / "issues" / "keep.md").write_text("keep issue\n", encoding="utf-8")


def _build_tarball(tmp_path: Path, version: str, build: str) -> Path:
    pkg_root = tmp_path / "pkg"
    yoda_dir = pkg_root / "yoda"
    (yoda_dir / "scripts").mkdir(parents=True, exist_ok=True)
    _write_manifest(yoda_dir / "PACKAGE_MANIFEST.yaml", version, build)
    (yoda_dir / "yoda.md").write_text(f"new manual {version}\n", encoding="utf-8")
    (yoda_dir / "scripts" / "dummy.py").write_text("print('ok')\n", encoding="utf-8")
    tar_path = tmp_path / f"yoda-framework-{version}+{build}.tar.gz"
    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(yoda_dir, arcname="yoda")
    return tar_path


def test_update_check_reports_update(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    _setup_root(root, "1.0.0", "20260204.a")

    latest_path = tmp_path / "latest.json"
    latest_payload = {
        "version": "1.0.1",
        "build": "20260204.b",
        "package_url": "file:///unused",
        "sha256": "deadbeef",
    }
    latest_path.write_text(json.dumps(latest_payload), encoding="utf-8")

    result = run_script(
        "update.py",
        [
            "--check",
            "--root",
            str(root),
            "--latest",
            str(latest_path),
            "--format",
            "json",
        ],
    )

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["update_available"] is True
    assert payload["current_version"] == "1.0.0+20260204.a"
    assert payload["latest_version"] == "1.0.1+20260204.b"


def test_update_apply_installs_and_preserves(tmp_path: Path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    _setup_root(root, "1.0.0", "20260204.a")

    tar_path = _build_tarball(tmp_path, "1.0.1", "20260204.b")
    latest_path = tmp_path / "latest.json"
    latest_payload = {
        "version": "1.0.1",
        "build": "20260204.b",
        "package_url": "file:///unused",
        "sha256": _sha256(tar_path),
    }
    latest_path.write_text(json.dumps(latest_payload), encoding="utf-8")

    result = run_script(
        "update.py",
        [
            "--apply",
            "--root",
            str(root),
            "--latest",
            str(latest_path),
            "--source",
            str(tar_path),
            "--format",
            "json",
        ],
    )

    assert result.returncode == 0, result.stderr
    backup_dir = root / "yoda" / "_previous" / "1.0.0+20260204.a"
    assert backup_dir.is_dir()
    assert (backup_dir / "yoda.md").read_text(encoding="utf-8") == "old manual\n"
    assert (root / "yoda" / "yoda.md").read_text(encoding="utf-8") == "new manual 1.0.1\n"
    assert (root / "yoda" / "todos" / "keep.txt").read_text(encoding="utf-8") == "keep todo\n"
    assert (root / "yoda" / "logs" / "keep.txt").read_text(encoding="utf-8") == "keep log\n"
    assert (
        root / "yoda" / "project" / "issues" / "keep.md"
    ).read_text(encoding="utf-8") == "keep issue\n"
