#!/usr/bin/env python3
"""Resolve and apply the next deterministic YODA Flow step from markdown issues."""

from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path
from typing import Any

import frontmatter

from lib.cli import add_global_flags, resolve_format
from lib.errors import ExitCode, YodaError
from lib.flow_log import append_flow_log_line, sanitize_flow_message
from lib.front_matter import update_front_matter
from lib.issue_index import load_issue_index
from lib.logging_utils import configure_logging
from lib.output import render_output
from lib.paths import repo_root
from lib.time_utils import detect_local_timezone, now_iso
from lib.validate import validate_slug


BLOCKED_NO_SELECTABLE = "no_selectable_issue"
BLOCKED_ONLY_PENDING = "only_pending_issues"
BLOCKED_DEPENDENCY = "dependency_blocked"


RUNBOOK_BY_STEP = {
    "study": "Run Study: gather context, list open decisions, and wait for explicit approval.",
    "document": "Run Document: update issue text with approved decisions and request explicit approval.",
    "implement": "Run Implement: execute only approved scope and keep changes aligned with the issue.",
    "evaluate": "Run Evaluate: validate acceptance criteria and fill Result log as yoda.md (conventional-commit line, description, optional external issue, Issue, Path), then request final approval.",
}
RUNBOOK_DONE = "Issue moved to done. Check next issue and ask the human if flow should continue now."
STEP_ORDER = ("study", "document", "implement", "evaluate")
NEXT_PHASE = {"study": "document", "document": "implement", "implement": "evaluate", "evaluate": ""}


def _relative(path_value: str) -> str:
    path = Path(path_value)
    try:
        return str(path.relative_to(repo_root()))
    except ValueError:
        return path_value


def _collect_pending(issues: list[dict[str, Any]]) -> list[dict[str, str]]:
    pending: list[dict[str, str]] = []
    for item in issues:
        if item.get("status") != "pending":
            continue
        pending.append(
            {
                "id": str(item.get("id", "")),
                "reason": "Issue is pending and not selectable.",
            }
        )
    return pending


def _collect_dependency_blocked(issues: list[dict[str, Any]]) -> list[dict[str, Any]]:
    blocked: list[dict[str, Any]] = []
    for item in issues:
        if item.get("status") != "to-do":
            continue
        deps = list(item.get("blocked_by", []))
        if deps:
            blocked.append({"id": str(item.get("id", "")), "depends_on": deps})
    return blocked


def _blocked_reason(pending: list[dict[str, str]], blocked: list[dict[str, Any]]) -> str:
    if blocked:
        return BLOCKED_DEPENDENCY
    if pending:
        return BLOCKED_ONLY_PENDING
    return BLOCKED_NO_SELECTABLE


def _blocked_message(code: str) -> str:
    if code == BLOCKED_DEPENDENCY:
        return "Blocked by unresolved dependencies. Use todo_update.py only if manual correction is needed."
    if code == BLOCKED_ONLY_PENDING:
        return "Only pending issues found. Resolve pending items before continuing flow."
    return "No selectable issue found for this developer slug."


def _pick_target(issues: list[dict[str, Any]]) -> dict[str, Any] | None:
    doing = [item for item in issues if item.get("status") == "doing"]
    if doing:
        return doing[0]
    selectable = [item for item in issues if item.get("selectable")]
    if selectable:
        return selectable[0]
    return None


def _now_ts() -> str:
    return now_iso(detect_local_timezone())


def _append_log(issue: dict[str, Any], message: str) -> str:
    ts = _now_ts()
    issue_path = Path(str(issue.get("path", "")))
    _line = sanitize_flow_message(message)
    append_flow_log_line(issue_path, f"{ts} {_line}")
    return ts


def _load_issue_front_matter(issue: dict[str, Any]) -> tuple[Path, dict[str, Any]]:
    issue_path = Path(str(issue.get("path", "")))
    post = frontmatter.load(str(issue_path))
    return issue_path, dict(post.metadata)


def _apply_transition(issue: dict[str, Any]) -> dict[str, Any]:
    status = str(issue.get("status", "")).strip()
    phase = str(issue.get("phase") or "").strip().lower()
    issue_id = str(issue.get("id", ""))
    issue_path, metadata = _load_issue_front_matter(issue)
    ts = _now_ts()

    if status == "to-do":
        metadata["status"] = "doing"
        metadata["phase"] = "study"
        metadata["updated_at"] = ts
        update_front_matter(issue_path, metadata)
        log_ts = _append_log(issue, f"{issue_id} transition to-do->doing phase=study")
        return {
            "status": "doing",
            "phase": "study",
            "next_step": "study",
            "runbook_line": RUNBOOK_BY_STEP["study"],
            "log_timestamp": log_ts,
        }

    if status != "doing":
        raise YodaError(
            f"Invalid target state for transition: status='{status}'",
            exit_code=ExitCode.VALIDATION,
        )
    if phase not in STEP_ORDER:
        raise YodaError(
            f"Invalid phase for doing issue: '{phase}'",
            exit_code=ExitCode.VALIDATION,
        )

    next_phase = NEXT_PHASE[phase]
    if next_phase:
        metadata["status"] = "doing"
        metadata["phase"] = next_phase
        metadata["updated_at"] = ts
        update_front_matter(issue_path, metadata)
        log_ts = _append_log(issue, f"{issue_id} transition doing/{phase}->doing/{next_phase}")
        return {
            "status": "doing",
            "phase": next_phase,
            "next_step": next_phase,
            "runbook_line": RUNBOOK_BY_STEP[next_phase],
            "log_timestamp": log_ts,
        }

    metadata["status"] = "done"
    metadata.pop("phase", None)
    metadata["updated_at"] = ts
    update_front_matter(issue_path, metadata)
    log_ts = _append_log(issue, f"{issue_id} transition doing/{phase}->done")
    return {
        "status": "done",
        "phase": "",
        "next_step": "done",
        "runbook_line": RUNBOOK_DONE,
        "log_timestamp": log_ts,
    }


def _render_md(payload: dict[str, Any]) -> list[str]:
    lines = [
        f"Issue ID: {payload['issue_id']}",
        f"Issue path: {payload['issue_path']}",
        f"Status: {payload['status']}",
        f"Phase: {payload['phase']}",
        f"Next step: {payload['next_step']}",
    ]
    if payload.get("log_timestamp"):
        lines.append(f"Log timestamp: {payload['log_timestamp']}")
    if payload.get("next_issue_id"):
        lines.append(f"Next issue ID: {payload['next_issue_id']}")
    if payload.get("next_issue_path"):
        lines.append(f"Next issue path: {payload['next_issue_path']}")
    if payload.get("continue_prompt"):
        lines.append(f"Continue prompt: {payload['continue_prompt']}")
    blocked_reason = payload.get("blocked_reason", "")
    if blocked_reason:
        lines.append(f"Blocked reason: {blocked_reason}")
        lines.append(f"Blocked message: {payload.get('blocked_message', '')}")

    pending = payload.get("pending", [])
    if pending:
        lines.append("Pending issues:")
        for item in pending:
            lines.append(f"- {item['id']}: {item['reason']}")

    blocked = payload.get("blocked", [])
    if blocked:
        lines.append("Dependency blocked:")
        for item in blocked:
            deps = ", ".join(item.get("depends_on", []))
            lines.append(f"- {item.get('id', '')}: {deps}")

    lines.append("Runbook:")
    lines.append(f"- {payload['runbook_line']}")
    return lines


def _render_output(payload: dict[str, Any], output_format: str) -> str:
    return render_output(payload, output_format, _render_md(payload))


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resolve and execute the next deterministic YODA Flow step",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Agent runbook:\n"
            "- Purpose: select/resume issue, apply one valid flow transition, and return the runbook line\n"
            "  for the next phase action.\n"
            "- Use in YODA Framework: this is the primary command for YODA Flow execution.\n"
            "- Expected moment: call once per flow step, execute returned phase instructions, then call again\n"
            "  after explicit human authorization to continue."
        ),
    )
    add_global_flags(parser)
    args = parser.parse_args()
    configure_logging(args.verbose)
    output_format = resolve_format(args)

    try:
        dev = (args.dev or "").strip()
        if not dev:
            raise YodaError(
                "--dev is required. Use the developer slug prefix from issue filenames <dev>-<NNNN>-<slug>.md.",
                exit_code=ExitCode.VALIDATION,
            )
        validate_slug(dev)
        index = load_issue_index(dev, ensure_flow_log=False)
        issues = list(index.get("issues", []))
        pending = _collect_pending(issues)
        blocked = _collect_dependency_blocked(issues)

        selected = _pick_target(issues)
        if selected is None:
            blocked_reason = _blocked_reason(pending, blocked)
            payload = {
                "issue_id": "",
                "issue_path": "",
                "status": "",
                "phase": "",
                "next_step": "blocked",
                "blocked_reason": blocked_reason,
                "blocked_message": _blocked_message(blocked_reason),
                "runbook_line": "No flow step available. Resolve blockers and run again.",
                "log_timestamp": "",
                "pending": pending,
                "blocked": blocked,
            }
            if blocked and blocked[0].get("id"):
                blocked_id = str(blocked[0]["id"])
                blocked_issue = index.get("by_id", {}).get(blocked_id)
                if isinstance(blocked_issue, dict):
                    payload["log_timestamp"] = _append_log(
                        blocked_issue,
                        f"{blocked_id} blocked dependency_blocked",
                    )
            elif pending and pending[0].get("id"):
                pending_id = str(pending[0]["id"])
                pending_issue = index.get("by_id", {}).get(pending_id)
                if isinstance(pending_issue, dict):
                    payload["log_timestamp"] = _append_log(
                        pending_issue,
                        f"{pending_id} blocked only_pending_issues",
                    )
            print(_render_output(payload, output_format))
            return ExitCode.NOT_FOUND

        transition = _apply_transition(selected)
        next_issue_id = ""
        next_issue_path = ""
        continue_prompt = ""
        if transition["status"] == "done":
            refreshed = load_issue_index(dev, ensure_flow_log=False)
            next_target = _pick_target(list(refreshed.get("issues", [])))
            if next_target is not None:
                next_issue_id = str(next_target.get("id", ""))
                next_issue_path = _relative(str(next_target.get("path", "")))
            continue_prompt = "Issue concluida. Deseja continuar o YODA Flow para a proxima issue?"
        payload = {
            "issue_id": str(selected.get("id", "")),
            "issue_path": _relative(str(selected.get("path", ""))),
            "status": str(transition["status"]),
            "phase": str(transition["phase"]),
            "next_step": str(transition["next_step"]),
            "blocked_reason": "",
            "blocked_message": "",
            "runbook_line": str(transition["runbook_line"]),
            "log_timestamp": str(transition["log_timestamp"]),
            "next_issue_id": next_issue_id,
            "next_issue_path": next_issue_path,
            "continue_prompt": continue_prompt,
            "pending": pending,
            "blocked": blocked,
        }
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
