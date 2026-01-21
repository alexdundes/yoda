# YODA Issue Templates - Usage Guide

This guide explains how agents and scripts should create and fill issue files using the templates in yoda/templates/.

## Templates

- Standard template: yoda/templates/issue.md
- Lightweight template: yoda/templates/issue-lightweight-process.md

## When to use each template

- Standard template: use for most work, especially when requirements, scope, or risks need explicit documentation.
- Lightweight template: use for small changes when the Study step is skipped and the issue is already clear.

## Script-driven creation

Issues are created by a script (issue_add.py). The script must:

1) Generate the next sequential id.
2) Add the issue entry to TODO.dev.yaml.
3) Create the issue Markdown file from the selected template.
4) Fill the basic fields using agent-provided inputs (id, title, summary, labels, priority, entrypoints).

After the script finishes, the agent must open the issue Markdown file and complete the remaining sections.

## How to fill the template

### Standard template (issue.md)

- Summary: short description of what will be built or changed.
- Context: current situation and why the work is needed.
- Objective: expected outcome.
- Scope / Out of scope: clear boundaries.
- Requirements: functional requirements.
- Acceptance criteria: testable checkboxes.
- Dependencies: related issues (or "None").
- Entry points: references to files or artifacts.
- Implementation notes: technical constraints or decisions.
- Tests: planned tests or "Not applicable".
- Risks and edge cases: potential failures to consider.
- Result log: final summary and commit text.

### Lightweight template (issue-lightweight-process.md)

- Summary: short, direct description.
- What to implement: exact steps or changes.
- Files to touch: files to create or edit.
- Acceptance check: testable checkboxes.
- Result log: final summary and commit text.

## Commit format

The commit text in Result log must follow this format:

First line: conventional commit message.
Body:
Issue: <ID>
Path: <issue path>

Example:

feat(yoda): add issue template guide

Issue: A-005
Path: yoda/project/issues/alex-005-template-issue-regras-uso.md

## Notes

- Templates are designed to be agent-friendly and must remain consistent with project/specs.
- If the template lacks required information, update project/specs first.
