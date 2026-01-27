# YODA Agent Instructions

This file is the root entry for agents in this repository. It defines how to enter the YODA Flow and how to use the project sources of truth.

## Entry

When the user indicates they want to enter YODA Flow, the agent must:

1) Confirm entry into YODA Flow.
2) Resolve developer slug in this order:
   - --dev `<slug>` flag
   - YODA_DEV environment variable
   - Ask the user
3) Load `yoda/todos/TODO.<dev>.yaml`; if missing, ask the user which TODO to use.
4) Select the highest-priority selectable issue (with all dependencies resolved).
5) Follow the YODA Flow for that issue.

Example natural entry phrase:
"Vamos entrar no YODA Flow e pegar a issue prioritaria sem dependencias."
Entry phrase criteria:
- Must explicitly mention "YODA Flow" (or "YODA") and intent to take the highest-priority selectable issue (with all dependencies resolved).

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

- If the TODO file is missing, ask the user which TODO to use.
- If the top issue has dependencies, move to the next selectable issue (with all dependencies resolved).
