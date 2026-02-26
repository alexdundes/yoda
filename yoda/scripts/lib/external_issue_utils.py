"""Shared helpers for external issue provider detection and access."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

from .errors import ExitCode, YodaError
from .paths import repo_root


def parse_origin(origin_url: str) -> tuple[str, str]:
    value = origin_url.strip()
    value = value.removesuffix(".git")
    ssh_match = re.match(r"^git@([^:]+):(.+)$", value)
    if ssh_match:
        host = ssh_match.group(1).lower()
        slug = ssh_match.group(2).strip("/")
        return host, slug

    http_match = re.match(r"^https?://([^/]+)/(.+)$", value)
    if http_match:
        host = http_match.group(1).lower()
        slug = http_match.group(2).strip("/")
        return host, slug

    raise YodaError(f"Unsupported origin URL format: {origin_url}", exit_code=ExitCode.VALIDATION)


def provider_from_host(host: str) -> str:
    if "gitlab" in host:
        return "gitlab"
    if "github" in host:
        return "github"
    raise YodaError(
        f"Unsupported provider from origin host '{host}'. Supported: GitLab, GitHub.",
        exit_code=ExitCode.NOT_FOUND,
    )


def detect_origin_url() -> str:
    override = os.getenv("YODA_ORIGIN_URL", "").strip()
    if override:
        return override

    result = subprocess.run(
        ["git", "config", "--get", "remote.origin.url"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise YodaError(
            "Could not resolve git remote.origin.url. Configure origin before external intake.",
            exit_code=ExitCode.NOT_FOUND,
        )
    return result.stdout.strip()


def ensure_cli_and_auth(provider: str) -> None:
    cli = "glab" if provider == "gitlab" else "gh"
    if shutil.which(cli) is None:
        install = (
            "Install GitLab CLI (glab): https://docs.gitlab.com/editor_extensions/gitlab_cli/"
            if provider == "gitlab"
            else "Install GitHub CLI (gh): https://cli.github.com/"
        )
        raise YodaError(
            f"Required CLI '{cli}' is not installed.\n{install}",
            exit_code=ExitCode.NOT_FOUND,
        )

    auth_cmd = [cli, "auth", "status"]
    auth_result = subprocess.run(auth_cmd, capture_output=True, text=True)
    if auth_result.returncode != 0:
        hint = "Run: glab auth login" if provider == "gitlab" else "Run: gh auth login"
        stderr = auth_result.stderr.strip() or auth_result.stdout.strip() or "authentication failed"
        raise YodaError(
            f"{cli} authentication is not ready: {stderr}\n{hint}",
            exit_code=ExitCode.NOT_FOUND,
        )


def extern_issue_dir() -> Path:
    return repo_root() / "yoda" / "project" / "extern-issues"


def extern_issue_path(provider: str, issue_number: str) -> Path:
    return extern_issue_dir() / f"{provider}-{issue_number}.json"
