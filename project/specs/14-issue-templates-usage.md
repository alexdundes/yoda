# YODA Issue Templates - Usage Guide

This guide explains how agents and scripts should create and fill issue files using the templates in `yoda/templates/`.

## Templates

- Standard template: `yoda/templates/issue.md`

## Template policy

- Standard template: use for all issue creation in v1.

## Script-driven creation

Issues are created by a script (`issue_add.py`). The script must:

1) Generate the next sequential id.
2) Add the issue entry to `yoda/todos/TODO.<dev>.yaml`.
3) Create the issue Markdown file from the standard template.
4) Fill the basic fields using agent-provided inputs (id, title, summary, priority).

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
- Result log: keep the section heading only; formatting instructions come from the playbook.

## Commit format

The Result log format is defined in `yoda/yoda.md` (Evaluate section) and must follow:

- `<First line: conventional commit message.>`
- blank line
- `<descricao do que foi feito>`
- blank line
- `- **<GitLab|GitHub> Issue** :   #NNN` (only when `extern_issue_file` exists)
- blank line
- `- **Issue**: \`<ID>\``
- blank line
- `- **Path**: \`<issue path>\``

Example:

feat(yoda): add issue template guide

Summary of what was done.

- **Issue**: `dev-0005`

- **Path**: `yoda/project/issues/dev-0005-template-issue-regras-uso.md`

## Notes

- Templates are designed to be agent-ready and must remain consistent with `project/specs/`.
- The opening instruction comment that asks to replace `[ID]` and `[TITLE]` must not appear in final templates used by `issue_add.py`.
- Keep `## Result log` empty in `yoda/templates/issue.md`; the playbook is the single source of truth for formatting.
- If the template lacks required information, update `project/specs/` first.
