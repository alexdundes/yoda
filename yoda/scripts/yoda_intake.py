#!/usr/bin/env python3
"""Provide YODA Intake runbooks, optionally enriched from external issues."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from typing import Any

from lib.cli import add_global_flags, resolve_format
from lib.errors import ExitCode, YodaError
from lib.external_issue_utils import (
    detect_origin_url,
    extern_issue_dir,
    extern_issue_path,
    parse_origin,
    provider_from_host,
)
from lib.logging_utils import configure_logging
from lib.validate import validate_slug


def _cmd_block(command: str) -> list[str]:
    return ["```bash", command, "```"]


def _initial_runbook(dev: str) -> str:
    lines = [
        "## AGENT runbook (initial)",
        "",
        f"Developer: `{dev}`",
        "",
        "1. Ask the human: do you have an external issue to use as intake source?",
        "2. If yes, run:",
    ]
    lines.extend(_cmd_block(f"python3 yoda/scripts/yoda_intake.py --dev {dev} --extern-issue <NNN>"))
    lines.extend(
        [
            "3. If no, run:",
        ]
    )
    lines.extend(_cmd_block(f"python3 yoda/scripts/yoda_intake.py --dev {dev} --no-extern-issue"))
    lines.extend(["", "Do not proceed with intake execution before one of these two calls."])
    return "\n".join(lines)


def _missing_dev_runbook() -> str:
    lines = [
        "## AGENT runbook (missing dev)",
        "",
        "1. Ask the human exactly: **What is your YODA slug?**",
        "2. After receiving the slug, run:",
    ]
    lines.extend(_cmd_block("python3 yoda/scripts/yoda_intake.py --dev <slug>"))
    lines.extend(["", "Do not continue Intake until the developer slug is defined."])
    return "\n".join(lines)


def _resolve_dev_no_prompt(explicit_dev: str | None) -> str | None:
    if explicit_dev:
        return explicit_dev.strip()
    env_dev = os.environ.get("YODA_DEV", "").strip()
    if env_dev:
        return env_dev
    return None


def _full_runbook(dev: str, external: bool, external_file: str | None = None) -> str:
    if external:
        file_hint = external_file or "yoda/project/extern-issues/<provider>-<NNN>.json"
        lines = [
            "## AGENT runbook",
            "",
            f"Developer: `{dev}`",
            "",
            f"1. Read external source details from `{file_hint}` to help the human define local micro issues.",
            "2. Review current backlog with `todo_list.py --dev <DEV>` to know what is already covered.",
            "3. Deliver a short summary of step 1, point out what is already covered in step 2, then ask the human what they want to execute now.",
            "4. Translate human demand into structured issue content (Summary/Context/Objective/Scope/AC).",
            "5. Create issue(s) with `issue_add.py` and complete issue markdown sections.",
            "6. Before creating issues, run this command to review usage details:",
        ]
        lines.extend(_cmd_block("python3 yoda/scripts/issue_add.py --help"))
        lines.extend(["7. For each generated YODA issue, keep `origin` traceability to external source."])
    else:
        lines = [
            "## AGENT runbook",
            "",
            f"Developer: `{dev}`",
            "",
            "1. Review current backlog with `todo_list.py --dev <DEV>` to know what is already covered.",
            "2. Translate human demand into structured issue content (Summary/Context/Objective/Scope/AC).",
            "3. Create issue(s) with `issue_add.py` and complete issue markdown sections.",
            "4. Before creating issues, run this command to review usage details:",
        ]
        lines.extend(_cmd_block("python3 yoda/scripts/issue_add.py --help"))
        lines.extend(["5. No external source was declared; document assumptions directly in issue markdown."])
    return "\n".join(lines)


def _render_external_markdown(issue: dict[str, Any], origin_url: str, external_file: str) -> str:
    labels = ", ".join(issue.get("labels", [])) or "-"
    return "\n".join(
        [
            "## External Issue Summary",
            "",
            f"- Provider: `{issue.get('provider')}`",
            f"- Origin: `{origin_url}`",
            f"- External ID: `#{issue.get('number')}`",
            f"- Title: {issue.get('title')}",
            f"- State: `{issue.get('state')}`",
            f"- Author: `{issue.get('author')}`",
            f"- URL: {issue.get('url')}",
            f"- Labels: {labels}",
            f"- File: {external_file}",
        ]
    )


def _extern_fetch_runbook(dev: str, issue_number: str) -> str:
    lines = [
        "## AGENT runbook (external source required)",
        "",
        f"Developer: `{dev}`",
        f"External issue: `#{issue_number}`",
        "",
        "1. Ask the human to run this command locally:",
    ]
    lines.extend(_cmd_block(f"python3 yoda/scripts/get_extern_issue.py --dev {dev} --extern-issue {issue_number}"))
    lines.extend(
        [
            "2. Wait for confirmation that the JSON file was created in `yoda/project/extern-issues/`.",
            "3. Read the saved `*.json` file details to guide micro-issue decomposition with the human.",
            "4. After confirmation, rerun this command:",
        ]
    )
    lines.extend(_cmd_block(f"python3 yoda/scripts/yoda_intake.py --dev {dev} --extern-issue {issue_number}"))
    return "\n".join(lines)


def _load_external_issue(issue_number: str) -> tuple[dict[str, Any], str, str, str] | None:
    try:
        origin_url = detect_origin_url()
        host, _repo_slug = parse_origin(origin_url)
        provider = provider_from_host(host)
        candidate = extern_issue_path(provider, issue_number)
        if candidate.exists():
            raw = json.loads(candidate.read_text(encoding="utf-8"))
            if isinstance(raw, dict):
                return raw, provider, origin_url, str(candidate)
    except YodaError:
        pass

    matches = sorted(extern_issue_dir().glob(f"*-{issue_number}.json"))
    if not matches:
        return None
    selected = matches[0]
    provider = selected.stem.split("-")[0]
    raw = json.loads(selected.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise YodaError(f"Invalid JSON in {selected}", exit_code=ExitCode.VALIDATION)
    return raw, provider, "", str(selected)


def _render_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, ensure_ascii=True)


def run(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="YODA Intake runbook helper")
    add_global_flags(parser)
    parser.add_argument("--extern-issue", dest="extern_issue", help="External issue number (NNN)")
    parser.add_argument("--no-extern-issue", action="store_true", help="Run intake without external issue")

    args = parser.parse_args(argv)
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = _resolve_dev_no_prompt(args.dev)
        if not dev:
            runbook = _missing_dev_runbook()
            payload = {
                "mode": "missing-dev",
                "runbook": runbook,
            }
            if output_format == "json":
                print(_render_json(payload))
            else:
                print(runbook)
            return ExitCode.SUCCESS

        validate_slug(dev)

        if args.extern_issue and args.no_extern_issue:
            raise YodaError(
                "Use either --extern-issue or --no-extern-issue, not both.",
                exit_code=ExitCode.VALIDATION,
            )

        if not args.extern_issue and not args.no_extern_issue:
            runbook = _initial_runbook(dev)
            payload = {
                "mode": "initial",
                "dev": dev,
                "runbook": runbook,
            }
            if output_format == "json":
                print(_render_json(payload))
            else:
                print(runbook)
            return ExitCode.SUCCESS

        if args.no_extern_issue:
            runbook = _full_runbook(dev, external=False)
            payload = {
                "mode": "no-extern-issue",
                "dev": dev,
                "runbook": runbook,
            }
            if output_format == "json":
                print(_render_json(payload))
            else:
                print(runbook)
            return ExitCode.SUCCESS

        issue_number = str(args.extern_issue or "").strip()
        if not issue_number or not issue_number.isdigit():
            raise YodaError("--extern-issue must be numeric (NNN).", exit_code=ExitCode.VALIDATION)

        loaded = _load_external_issue(issue_number)
        if loaded is None:
            runbook = _extern_fetch_runbook(dev, issue_number)
            payload = {
                "mode": "extern-issue-missing-file",
                "dev": dev,
                "extern_issue": issue_number,
                "runbook": runbook,
            }
            if output_format == "json":
                print(_render_json(payload))
            else:
                print(runbook)
            return ExitCode.SUCCESS

        external_issue, provider, origin_url, external_file = loaded
        runbook = _full_runbook(dev, external=True, external_file=external_file)
        external_md = _render_external_markdown(external_issue, origin_url, external_file)
        payload = {
            "mode": "extern-issue",
            "dev": dev,
            "provider": provider,
            "origin_url": origin_url,
            "external_file": external_file,
            "external_issue": external_issue,
            "runbook": runbook,
            "external_markdown": external_md,
        }
        if output_format == "json":
            print(_render_json(payload))
        else:
            print(runbook)
            print("")
            print(external_md)
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
