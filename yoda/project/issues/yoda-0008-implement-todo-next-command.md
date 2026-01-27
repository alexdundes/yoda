---
agent: Human
created_at: '2026-01-27T17:22:02-03:00'
depends_on: []
description: Implement todo_next.py per spec, including selection rules and outputs
entrypoints: []
id: yoda-0008
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: implement-todo-next-command
status: to-do
tags: []
title: Implement todo_next command
updated_at: '2026-01-27T17:22:02-03:00'
---

# yoda-0008 - Implement todo_next command

## Summary
Implement `todo_next.py` using the finalized spec, including deterministic selection rules, outputs, and error behavior.

## Context
We need a deterministic command to select the next actionable issue, consistent with the framework selection rules.

## Objective
Create `yoda/scripts/todo_next.py` and wire it into the CLI conventions and validation utilities.

## Scope
- Implement `yoda/scripts/todo_next.py`.
- Use existing helpers in `yoda/scripts/lib` for CLI, validation, and paths.
- Output in md/json formats per spec.

## Out of scope
- Changes to other scripts or specs beyond what is required to implement `todo_next.py`.
- Adding tests unless required by the spec.

## Requirements
- Resolve `--dev` using the standard order.
- Load and validate TODO.
- Select the highest-priority selectable issue (tie-breaker: list order).
- Exclude pending issues and those with unresolved dependencies.
- If none selectable, return NOT_FOUND and list pending/blocked info.
- Output issue id and paths; include JSON output format.

## Acceptance criteria
- [ ] `yoda/scripts/todo_next.py` exists and matches the spec.
- [ ] Command outputs the next issue id and paths deterministically.
- [ ] Error path reports pending and blocked items.

## Dependencies
- Depends on `yoda-0007` (spec) being completed.

## Entry points
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
Implement selection logic in a pure function to simplify testing, even if tests are not added yet.

## Tests
Not applicable (unless required by spec).

## Risks and edge cases
- TODO ordering must be preserved; ensure the YAML list order is used as tie-breaker.
- Dependencies must only consider ids within the same TODO.

## Result log

