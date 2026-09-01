"""Shared phase runbook composition for YODA Flow and YODA Prep Flow.

Both flows need the same conditional guidance when an issue declares a
`source_doc`, so the conditional text lives here instead of being duplicated in
each script. The base text per step still differs between the two flows.
"""

from __future__ import annotations

from typing import Any

from .source_doc import source_doc_alert


FLOW_RUNBOOK_BY_STEP = {
    "study": (
        "Run Study: gather context and produce findings, constraints, and the open decisions "
        "the human must settle.\n"
        "Present that deliverable and stop. Do not start Document without new authorization."
    ),
    "document": (
        "Run Document: update the issue with the approved decisions and close the "
        "document-first contract.\n"
        "Present that deliverable and stop. Do not start Implement without new authorization."
    ),
    "implement": (
        "Run Implement: execute only approved scope and keep changes aligned with the issue.\n"
        "Present the changes and the verifications you ran, then stop. Do not start Evaluate "
        "without new authorization."
    ),
    "evaluate": (
        "Run Evaluate: validate acceptance criteria and fill Result log as yoda.md "
        "(conventional-commit line, description, optional external issue, Issue, Path).\n"
        "Present the checked criteria and any remaining findings, then request final approval."
    ),
}

PREP_RUNBOOK_BY_STEP = {
    "study": (
        "Run Prep Study: gather context and list open decisions for this issue; do not implement. "
        "Present the findings and open decisions as the deliverable, then stop and wait for "
        "explicit human authorization before Prep Document."
    ),
    "document": (
        "Run Prep Document: update issue text with approved decisions; do not implement. "
        "Present the updated issue as the deliverable, then stop and wait for explicit human "
        "authorization before normal YODA Flow can continue."
    ),
}

# Conditional guidance added only when the issue declares a `source_doc`.
# Implement and Evaluate get no extra line: the reference stays visible in the
# header, without an obligation attached to it.
SOURCE_DOC_RUNBOOK_BY_STEP = {
    "study": (
        "Read source_doc `{path}` as qualified context, not as settled truth: confront it with "
        "the current project state, and separate decisions it already settles from questions "
        "still open."
    ),
    "document": (
        "Consider source_doc `{path}` when consolidating approved decisions. The association "
        "does not authorize editing it; any update depends on approved issue scope."
    ),
}


def compose_runbook(base: str, step: str, issue: dict[str, Any]) -> str:
    """Return the runbook for `step`, extended by conditional issue guidance."""
    path = str(issue.get("source_doc", "") or "").strip()
    if not path:
        return base
    extra = SOURCE_DOC_RUNBOOK_BY_STEP.get(step)
    if not extra:
        return base
    return f"{base}\n{extra.format(path=path)}"


def reference_lines(issue: dict[str, Any]) -> list[str]:
    """Return header lines exposing the issue's source references.

    Without these, a reference stored in front matter stays invisible to every
    later phase and has to be repeated by hand to be noticed.
    """
    lines: list[str] = []
    extern_issue_file = str(issue.get("extern_issue_file", "") or "").strip()
    if extern_issue_file:
        lines.append(f"External issue file: {extern_issue_file}")
    source_doc = str(issue.get("source_doc", "") or "").strip()
    if source_doc:
        lines.append(f"Source doc: {source_doc}")
        alert = source_doc_alert(source_doc)
        if alert:
            lines.append(alert)
    return lines
