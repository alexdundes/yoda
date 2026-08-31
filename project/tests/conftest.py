"""Shared fixtures for the repository boundary test suite.

This suite validates the frontier between the development repository and the
distributed YODA product. It is intentionally separate from
`yoda/scripts/tests/`, which validates the product itself.
"""

from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SPECS_ROOT = REPO_ROOT / "project" / "specs"
ISSUES_ROOT = REPO_ROOT / "yoda" / "project" / "issues"

ISSUE_FILENAME_RE = re.compile(r"^([a-z][a-z0-9-]*)-(\d{4})-[a-z0-9-]+\.md$")


def spec_files() -> list[Path]:
    """Every Markdown file in the portable specification set."""
    return sorted(SPECS_ROOT.rglob("*.md"))


def normative_spec_files() -> list[Path]:
    """Numbered specs only, excluding the `influences/` reference material.

    `influences/` summarizes third-party practices and legitimately quotes
    external commit hashes and article links, so hash-shaped detection applies
    to the normative specs alone.
    """
    return sorted(SPECS_ROOT.glob("*.md"))


def origin_repo() -> tuple[str, str] | None:
    """Return `(host, slug)` for this repository's git origin, when resolvable.

    Falls back to `None` (never raises) so a clone without an origin still runs
    the origin-independent checks instead of silently passing everything.
    """
    override = os.environ.get("YODA_ORIGIN_URL", "").strip()
    if override:
        raw = override
    else:
        result = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        if result.returncode != 0:
            return None
        raw = result.stdout.strip()

    if not raw:
        return None
    value = raw.removesuffix(".git")

    ssh_match = re.match(r"^git@([^:]+):(.+)$", value)
    if ssh_match:
        return ssh_match.group(1).lower(), ssh_match.group(2).strip("/").lower()

    http_match = re.match(r"^https?://([^/]+)/(.+)$", value)
    if http_match:
        return http_match.group(1).lower(), http_match.group(2).strip("/").lower()

    return None


def known_issue_ids() -> set[str]:
    """Concrete issue IDs that exist in this repository's backlog."""
    ids: set[str] = set()
    for path in ISSUES_ROOT.glob("*.md"):
        match = ISSUE_FILENAME_RE.match(path.name)
        if match:
            ids.add(f"{match.group(1)}-{match.group(2)}")
    return ids


def known_dev_slugs() -> set[str]:
    """Developer slugs actually used by this repository's issue files."""
    slugs: set[str] = set()
    for path in ISSUES_ROOT.glob("*.md"):
        match = ISSUE_FILENAME_RE.match(path.name)
        if match:
            slugs.add(match.group(1))
    return slugs
