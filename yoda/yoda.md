# YODA Agent Instructions

This file is the root entry for agents in this repository. It defines how to enter the YODA Flow and how to use the project sources of truth.

## Entry

When the user indicates they want to enter YODA Flow, the agent must:

1) Confirm entry into YODA Flow.
2) Load the TODO for the current developer (this implementation: yoda/todos/TODO-alex.md).
3) Select the highest-priority issue without dependencies.
4) Follow the YODA Flow for that issue.

Example natural entry phrase:
"Vamos entrar no YODA Flow e pegar a issue prioritaria sem dependencias."

## Source of truth

- project/specs/ is the source of truth for the framework and this project.
- The issue Markdown file is the source of truth for the current task.

## TODO (this implementation)

This implementation does not have YODA scripts yet. Until they exist:

- Use yoda/todos/TODO-alex.md as the TODO source.
- Do not edit TODO-alex.md directly unless the user requests it.
- A future migration will replace this with TODO.dev.yaml and scripts.

## Flow rules

- Follow the YODA Flow: Study -> Document -> Implement -> Evaluate.
- For lightweight process, skip Study and follow the preliminary issue directly.
- Implement only what is documented in the issue.
- If a blocker is found, mark the issue as pending and record the reason in the TODO.
- Logs for this project are in Markdown: yoda/logs/dev-id-slug.md.
- Commit format:
  - First line: conventional commit message.
  - Body:
    - Issue: <ID>
    - Path: <issue path>

## Notes

- If the TODO file is missing, ask the user which TODO to use.
- If the top issue has dependencies, move to the next issue without dependencies.
