---
schema_version: '2.00'
status: done
title: Slug immutability rule
description: Document that issue slugs are immutable; renames require migration
priority: 5
created_at: '2026-01-27T16:41:37-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0001 - Slug immutability rule

## Summary
Define slug immutability in the framework specs so issue slugs never change after creation; renames are handled via explicit migrations, not regular updates, with `project/specs/04-todo-dev-yaml-issues.md` as the primary reference.

## Context
Slug is embedded in issue and log paths (`yoda/project/issues/<id>-<slug>.md`, `yoda/logs/<id>-<slug>.yaml`). The specs do not explicitly state whether slug can change, which risks path drift if titles are edited or if future scripts regenerate slugs.

## Objective
Add explicit guidance in specs that slugs are immutable and document how rename/migration should be handled, anchored in `project/specs/04-todo-dev-yaml-issues.md`.

## Scope
- Add the primary rule text to `project/specs/04-todo-dev-yaml-issues.md`.
- Add a brief supporting note in `project/specs/00-conventions.md`.
- Mention path coupling to slug and the impact on issue/log filenames.

## Out of scope
- Implementing a rename/migration script.
- Modifying existing TODO/issue data.

## Requirements
- State that `slug` is immutable once created.
- Clarify that renames require an explicit migration operation (not `todo_update`).
- Note that scripts must not auto-change slug when updating other fields.

## Acceptance criteria
- [x] `project/specs/04-todo-dev-yaml-issues.md` explicitly states slug immutability.
- [x] `project/specs/00-conventions.md` includes a brief supporting note.
- [x] Spec mentions that renames require migration and are out of the regular update flow.
- [x] No code changes are required.


## Entry points
- `project/specs/04-todo-dev-yaml-issues.md`
- `project/specs/00-conventions.md`
- `yoda/scripts/issue_add.py`

## Implementation notes
Keep wording consistent with existing TODO schema and path patterns (`yoda/project/issues/<id>-<slug>.md`, `yoda/logs/<id>-<slug>.yaml`). State that slug is created at issue creation time and must not be modified by update scripts.

## Tests
Not applicable.

## Risks and edge cases
- If a future tool regenerates slugs, paths can drift; highlight migration-only renames.

## Result log
Added slug immutability rules to the TODO/issue spec (including migration guidance) and a supporting convention note highlighting that slug-based paths must remain stable.

Commit suggestion:
docs(specs): enforce slug immutability

Issue: `yoda-0001`
Path: `yoda/project/issues/yoda-0001-slug-immutability-rule.md`

## Flow log
- 2026-01-27T16:41:37-03:00 issue_add created | title: Slug immutability rule | description: Document that issue slugs are immutable; renames require migration | slug: slug-immutability-rule
- 2026-01-27T16:56:25-03:00 todo_update | status: to-do -> doing
- 2026-01-27T16:56:28-03:00 issue updated: Document step updated summary/objective/scope/criteria to anchor 04-todo-dev-yaml-issues.md as primary
- 2026-01-27T16:57:20-03:00 implement: documented slug immutability in 04-todo-dev-yaml-issues.md and added conventions note
- 2026-01-27T16:58:55-03:00 todo_update | status: doing -> done
- 2026-01-27T16:58:59-03:00 evaluate: acceptance criteria checked and result log updated in issue
