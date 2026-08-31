#!/usr/bin/env python3
"""Fetch an external issue and persist it locally for YODA Intake."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from typing import Any

from lib.cli import AGENT_OUTPUT_RULE, add_global_flags, resolve_format
from lib.errors import ExitCode, YodaError
from lib.error_messages import required_flag
from lib.external_issue_utils import (
    check_cli_and_auth,
    detect_origin_url,
    ensure_cli_and_auth,
    extern_issue_path,
    parse_origin,
    provider_from_host,
)
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.provider_github import (
    GitHubAPIError,
    fetch_issue as fetch_github_issue,
    fetch_issue_public as fetch_public_github_issue,
)
from lib.provider_gitlab import fetch_issue as fetch_gitlab_issue
from lib.validate import validate_slug


def _public_github_fallback(
    repo_slug: str,
    issue_number: str,
    authenticated_error: YodaError | None = None,
) -> tuple[dict[str, Any], str]:
    try:
        return fetch_public_github_issue(repo_slug, issue_number), "public-http"
    except YodaError as public_error:
        if authenticated_error is None:
            raise
        raise YodaError(
            "Both GitHub transports failed. "
            f"Authenticated transport: {authenticated_error} "
            f"Public transport: {public_error}",
            exit_code=public_error.exit_code,
        ) from public_error


def _fetch_external(
    provider: str,
    host: str,
    repo_slug: str,
    issue_number: str,
) -> tuple[dict[str, Any], str]:
    if provider == "gitlab":
        ensure_cli_and_auth(provider)
        return fetch_gitlab_issue(repo_slug, issue_number), "authenticated-cli"
    if provider == "github":
        auth_state = check_cli_and_auth(provider)
        if auth_state.ready:
            try:
                return fetch_github_issue(repo_slug, issue_number), "authenticated-cli"
            except GitHubAPIError as exc:
                if host == "github.com" and exc.kind == "permission":
                    return _public_github_fallback(repo_slug, issue_number, exc)
                raise
        if host == "github.com":
            return _public_github_fallback(repo_slug, issue_number, auth_state.error)
        if auth_state.error is not None:
            raise auth_state.error
        raise YodaError("GitHub authentication is not ready.", exit_code=ExitCode.NOT_FOUND)
    raise YodaError(f"Unsupported provider: {provider}", exit_code=ExitCode.NOT_FOUND)


def _render(payload: dict[str, Any], output_format: str) -> str:
    lines = [
        f"Provider: {payload['provider']}",
        f"External issue: #{payload['issue_number']}",
        f"Transport: {payload['transport']}",
        f"Saved file: {payload['saved_file']}",
        f"Next step: python3 yoda/scripts/yoda_intake.py --dev {payload['dev']} --extern-issue {payload['issue_number']}",
    ]
    return render_output(payload, output_format, lines, dry_run=bool(payload.get("dry_run")))


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Fetch external issue into yoda/project/extern_issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Agent guidance:\n"
            "- Purpose: fetch one external issue and persist it as local JSON for YODA Intake.\n"
            "- When to use: before running yoda_intake.py with --extern-issue <NNN>.\n"
            "- Access: prefers authenticated provider CLI; public github.com issues fall back to "
            "unauthenticated HTTP. Private repositories require valid CLI authentication.\n"
            "- Mutability: writes yoda/project/extern_issues/<provider>-<NNN>.json (unless --dry-run)."
        )
        + AGENT_OUTPUT_RULE,
    )
    add_global_flags(parser)
    parser.add_argument("--extern-issue", dest="extern_issue", required=False, help="External issue number (NNN)")

    args = parser.parse_args(argv)
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = (args.dev or "").strip()
        if not dev:
            required_flag("--dev")
        validate_slug(dev)

        issue_number = str(args.extern_issue or "").strip()
        if not issue_number:
            required_flag("--extern-issue")
        if not issue_number.isdigit():
            raise YodaError("--extern-issue must be numeric (NNN).", exit_code=ExitCode.VALIDATION)

        origin_url = detect_origin_url()
        host, repo_slug = parse_origin(origin_url)
        provider = provider_from_host(host)
        external_issue, transport = _fetch_external(provider, host, repo_slug, issue_number)

        out_path = extern_issue_path(provider, issue_number)
        payload = {
            "dev": dev,
            "provider": provider,
            "issue_number": issue_number,
            "origin_url": origin_url,
            "repo_slug": repo_slug,
            "transport": transport,
            "external_issue": external_issue,
            "saved_file": str(out_path),
            "dry_run": bool(args.dry_run),
        }

        if not args.dry_run:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(json.dumps(external_issue, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

        print(_render(payload, output_format))
        return ExitCode.SUCCESS
    except YodaError as exc:
        logging.error(str(exc))
        return exc.exit_code
    except Exception as exc:  # pragma: no cover
        logging.error("Unexpected error: %s", exc)
        return ExitCode.ERROR


def main() -> int:
    return run()


if __name__ == "__main__":
    sys.exit(main())
