# YODA Agent Instructions

This file is the root entry for agents in this repository. It defines how to enter the YODA Flow and how to use the project sources of truth.

## Entry

When the user indicates they want to enter YODA Flow, the agent must:

1) Confirm entry into YODA Flow.
2) Resolve developer slug in this order:
   - --dev `<slug>` flag
   - YODA_DEV environment variable
   - Ask the user
3) Run `todo_next.py` to select the next issue.
   - Always surface pending hints (if any).
   - If it returns conflict (any `doing` issue), stop and ask the user to resolve it.
   - If it returns not found, surface blocked hints and ask what to do next.
4) Ask for confirmation: "Start YODA Flow for issue <id>?" (translate to the human's language if needed).
5) If approved, set status to `doing` via `todo_update.py` and follow the YODA Flow.

Example natural entry phrase:
"Let's enter YODA Flow and take the highest-priority selectable issue (no issue doing, dependencies resolved)."
Entry phrase criteria:
- Must explicitly mention "YODA Flow" (or "YODA") and intent to take the highest-priority selectable issue.
Examples (allowed):
- "Let's do YODA Flow"
- "YODA Flow, here we go"
- "YODA Flow, next issue"

## YODA Intake (backlog cycle)

When the user signals intent to create issues or says “YODA Intake”, the agent must:

1) Confirm entry into YODA Intake.
2) Review the backlog using `todo_list.py` to avoid duplicates.
3) Collect and shape requirements until each issue meets the Definition of Ready (DoR).
4) Create issues via `issue_add.py` and complete the Markdown sections.
5) Review ordering (optionally with `todo_reorder.py`) and propose the next YODA Flow issue.
6) Exit Intake explicitly and ask whether to start YODA Flow.

Slug format:
- Use lowercase ASCII, digits, and hyphens only.
- Must start with a letter and contain no spaces.

## Source of truth

- project/specs/ is the source of truth for the framework and this project.
- The issue Markdown file is the source of truth for the current issue.
- If there is a conflict between project/specs and yoda/, resolve it via an explicit issue.

## Meta-implementation exception (this repo)

- project/specs/ describes the future YODA Framework and is the canonical reference.
- This repository implements the YODA Framework specs directly.
- yoda/ is the implementation workspace for the framework.
- This repository follows the YODA Framework specs as the current source of truth.

## TODO (this implementation)

Use `yoda/todos/TODO.<dev>.yaml` as the TODO source.

- If `yoda/todos/TODO.<dev>.yaml` is missing, ask the user which TODO to use.
- Do not edit TODO files directly; use scripts to update metadata.

## Flow rules

- Follow the YODA Flow: Study -> Document -> Implement -> Evaluate.
- For lightweight process, skip Study and follow the preliminary issue directly.
  - Use lightweight only when the issue is already clear, has explicit acceptance criteria, and no open questions remain.
  - If there is ambiguity, new requirements, or non-trivial risk, include Study.
- Implement only what is documented in the issue.
- If a blocker is found, mark the issue as pending and record the reason in the TODO.
- If Study discovers dependencies, update `depends_on` (and priority if needed) using `todo_update.py`, set status back to `to-do`, and end the cycle.
- Logs for this project are YAML: `yoda/logs/<id>-<slug>.yaml`.
- Log entries should include the canonical issue id (dev-id) in the message.
- Status names: to-do -> doing -> done; any state can transition to pending.
- Log timestamps should use ISO 8601 with Brasilia offset (e.g., 2026-01-21T19:40:50-03:00).
- If the issue is ambiguous, return to Document before coding.
- Do not invent files or paths; verify the repo structure first.
- Any change to project/specs must be tracked by an issue.
- Commit format:
  - First line: conventional commit message.
  - Body:
    - Issue: `<ID>`
    - Path: `<issue path>`

## Notes

- If the TODO file is missing, `todo_next.py` will fail; ask the user which TODO to use and retry.
- Issue creation (`issue_add.py`) is out of scope for YODA Flow and defined elsewhere.
