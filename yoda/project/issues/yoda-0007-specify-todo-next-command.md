---
agent: Human
created_at: '2026-01-27T17:22:15-03:00'
depends_on: []
description: Write a spec for todo_next.py behavior, inputs, outputs, and error handling
entrypoints: []
id: yoda-0007
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: specify-todo-next-command
status: done
tags: []
title: Specify todo_next command
updated_at: '2026-01-27T17:32:49-03:00'
---

# yoda-0007 - Specify todo_next command

## Summary
Define the full specification for `todo_next.py`, including selection rules, inputs/outputs, and error handling so the implementation is deterministic and testable.

## Context
The specs already mention `todo_next.py` at a high level, but there is no detailed contract covering CLI behavior, outputs, or error reporting.

## Objective
Create a complete spec for `todo_next.py` to remove ambiguity before implementation.

## Scope
- Create `project/specs/21-todo-next-script.md` with a detailed `todo_next.py` specification.
- Add a reference to the new spec in `project/specs/README.md`.
- Keep the minimal JSON contract in `project/specs/13-yoda-scripts-v1.md`.
- Align with existing TODO schema and selection rules.

## Out of scope
- Implementing the script.
- Changing the TODO schema.

## Requirements
- Specify deterministic selection rules (priority desc, list order, dependency resolution, pending exclusion).
- Define inputs (`--dev`, optional TODO path override if allowed) and outputs (issue id + paths).
- Specify error behavior when no selectable issues exist, including reporting pending/blocking reasons.
- Require a pending hint even when a selectable issue is returned.
- Define minimal JSON output keys in `project/specs/13-yoda-scripts-v1.md`.

## Acceptance criteria
- [x] `project/specs/21-todo-next-script.md` contains a detailed `todo_next.py` specification.
- [x] `project/specs/README.md` references the new spec file.
- [x] JSON output minimums for `todo_next.py` are documented in `project/specs/13-yoda-scripts-v1.md`.
- [x] Error behavior includes listing pending items and blocked dependencies.
- [x] Success output includes a pending hint when pending issues exist.

## Dependencies
None.

## Entry points
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/21-todo-next-script.md
  type: doc
- path: project/specs/04-todo-dev-yaml-issues.md
  type: doc

## Implementation notes
Keep the spec consistent with the selection rule already defined in `project/specs/04-todo-dev-yaml-issues.md`.

## Tests
Not applicable.

## Risks and edge cases
- If output is underspecified, downstream automation may diverge.

## Result log
Created a dedicated `todo_next.py` specification file, updated the specs index, and added JSON minimum keys plus pending-hint guidance in the scripts v1 spec.

Commit suggestion:
docs(specs): add todo_next spec

Issue: `yoda-0007`
Path: `yoda/project/issues/yoda-0007-specify-todo-next-command.md`