---
schema_version: '2.00'
status: done
title: Implement todo_next with single-issue rule
description: Implement todo_next.py to select only to-do items and block when any
  issue is doing
priority: 5
created_at: '2026-01-27T17:57:51-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0008 - Implement todo_next with single-issue rule

## Summary
Implement `todo_next.py` according to the updated spec: only `to-do` issues are selectable, and any `doing` issue blocks selection with a conflict error.

## Context
We corrected the selection rules in the spec. The implementation must follow the single-issue execution rule and provide pending hints even on success.

## Objective
Create `yoda/scripts/todo_next.py` with deterministic selection and the updated blocking rules, following `project/specs/21-todo-next-script.md`.

## Scope
- Implement `yoda/scripts/todo_next.py`.
- Use existing helpers in `yoda/scripts/lib` for CLI, validation, and paths.
- Output in md/json formats per spec.

## Out of scope
- Changes to TODO schema.
- Changes to other scripts.

## Requirements
- Resolve `--dev` using the standard order.
- Load and validate TODO.
- If any issue is `doing`, return conflict with a list of doing issues.
- Select only `to-do` issues (pending/done excluded).
- Enforce dependency resolution (`depends_on` must all be done).
- If none selectable, return NOT_FOUND with pending/blocked lists.
- Always include pending hints when pending issues exist, even on success.
- JSON output includes `issue_id`, `issue_path`, `todo_path`, `pending`, `blocked`, `doing`.
- Implementation must follow `project/specs/21-todo-next-script.md` exactly.

## Acceptance criteria
- [x] `yoda/scripts/todo_next.py` exists and matches the updated spec.
- [x] Done and pending issues are not selectable.
- [x] Any `doing` issue produces a conflict error and includes the doing list.
- [x] Success output includes pending hints when pending issues exist.


## Entry points
- `project/specs/21-todo-next-script.md`
- `project/specs/13-yoda-scripts-v1.md`
- `project/specs/04-todo-dev-yaml-issues.md`
- `yoda/scripts/lib/cli.py`
- `yoda/scripts/lib/validate.py`
- `yoda/scripts/lib/paths.py`

## Implementation notes
Implement selection logic in a pure function to simplify testing.

## Tests
Manual run of `todo_next.py` against the current TODO.

## Risks and edge cases
- Ensure conflict errors take precedence over normal selection.

## Result log
Implemented `yoda/scripts/todo_next.py` with single-issue blocking, to-do-only selection, pending hints, and JSON output including doing/blocked/pending lists. Verified it returns conflict while `yoda-0008` is doing.

Commit suggestion:
feat(scripts): add todo_next command

Issue: `yoda-0008`
Path: `yoda/project/issues/yoda-0008-implement-todo-next-with-single-issue-rule.md`

## Flow log
- 2026-01-27T17:57:51-03:00 issue_add created | title: Implement todo_next with single-issue rule | description: Implement todo_next.py to select only to-do items and block when any issue is doing | slug: implement-todo-next-with-single-issue-rule
- 2026-01-27T18:00:20-03:00 todo_update | status: to-do -> doing
- 2026-01-27T18:01:15-03:00 implement: added todo_next.py with single-issue blocking and to-do-only selection
- 2026-01-27T18:01:19-03:00 todo_update | status: doing -> done
- 2026-01-27T18:01:24-03:00 evaluate: acceptance criteria checked and result log updated in issue
