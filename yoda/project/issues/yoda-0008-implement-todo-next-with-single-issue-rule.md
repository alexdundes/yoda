---
agent: Human
created_at: '2026-01-27T17:57:51-03:00'
depends_on: []
description: Implement todo_next.py to select only to-do items and block when any
  issue is doing
entrypoints: []
id: yoda-0008
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: implement-todo-next-with-single-issue-rule
status: done
tags: []
title: Implement todo_next with single-issue rule
updated_at: '2026-01-27T18:01:19-03:00'
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

## Dependencies
None.

## Entry points
- path: project/specs/21-todo-next-script.md
  type: doc
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/04-todo-dev-yaml-issues.md
  type: doc
- path: yoda/scripts/lib/cli.py
  type: code
- path: yoda/scripts/lib/validate.py
  type: code
- path: yoda/scripts/lib/paths.py
  type: code

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