# YODA Agent Instructions

This file is the root entry for agents in this repository. It defines how to enter the YODA Flow and how to use the project sources of truth.

## Entry

When the user indicates they want to enter YODA Flow, the agent must:

1) Confirm entry into YODA Flow.
2) Resolve developer slug in this order:
   - --dev <slug> flag
   - YODA_DEV environment variable
   - Ask the user
3) Load yoda/todos/TODO.<slug>.md (bootstrap); fallback to yoda/todos/TODO.alex.md if missing.
4) Select the highest-priority issue without dependencies.
5) Follow the YODA Flow for that issue.

Example natural entry phrase:
"Vamos entrar no YODA Flow e pegar a issue prioritaria sem dependencias."

## Source of truth

- project/specs/ is the source of truth for the framework and this project.
- The issue Markdown file is the source of truth for the current task.
- If there is a conflict between project/specs and yoda/, assume yoda/ is in bootstrap and do not migrate formats without an explicit issue.

## TODO (this implementation)

This implementation does not have YODA scripts yet. Until they exist:

- Use yoda/todos/TODO.<slug>.md as the TODO source.
- If TODO.<slug>.md is missing, fallback to yoda/todos/TODO.alex.md.
- Do not edit TODO files directly unless the user requests it.
- A future migration will replace this with TODO.<dev>.yaml and scripts.

## Flow rules

- Follow the YODA Flow: Study -> Document -> Implement -> Evaluate.
- For lightweight process, skip Study and follow the preliminary issue directly.
- Implement only what is documented in the issue.
- If a blocker is found, mark the issue as pending and record the reason in the TODO.
- Logs for this project are in Markdown: yoda/logs/dev-id-slug.md.
- Log entries should include the canonical issue id (dev-id) in the message.
- Status names: to-do -> doing -> done; any state can transition to pending.
- If the issue is ambiguous, return to Document before coding.
- Do not invent files or paths; verify the repo structure first.
- Any change to project/specs must be tracked by an issue.
- Commit format:
  - First line: conventional commit message.
  - Body:
    - Issue: <ID>
    - Path: <issue path>

## Notes

- If the TODO file is missing, ask the user which TODO to use.
- If the top issue has dependencies, move to the next issue without dependencies.
