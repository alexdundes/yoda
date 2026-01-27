---
agent: Human
created_at: '2026-01-27T18:04:27-03:00'
depends_on: []
description: Create unit tests for implemented scripts, starting with todo_next and
  existing helpers
entrypoints: []
id: yoda-0009
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: add-unit-tests-for-yoda-scripts
status: done
tags: []
title: Add unit tests for YODA scripts
updated_at: '2026-01-27T18:14:19-03:00'
---

# yoda-0009 - Add unit tests for YODA scripts

## Summary
Add unit tests for the implemented YODA scripts, starting with `todo_next.py` and core helpers.

## Context
We now have several scripts in `yoda/scripts/` with non-trivial behavior. Tests are needed to prevent regressions.

## Objective
Create a minimal, repeatable test suite for the scripts and supporting utilities.

## Scope
- Add a test harness for `yoda/scripts/`.
- Add unit tests for `todo_next.py` selection rules.
- Add unit tests for validation and CLI helpers as needed.

## Out of scope
- Integration tests across the whole repo.

## Requirements
- Tests must run locally with a single command.
- Tests must cover: done/pending/doing selection, dependency resolution, and output formats for `todo_next.py`.
- Include basic tests for other implemented commands (`issue_add.py`, `todo_update.py`, `log_add.py`).
- Use dev slug `test` in fixtures and delete all created files at test end.
- Use pytest per `project/specs/15-scripts-python-structure.md`.

## Acceptance criteria
- [x] Test suite exists under `yoda/scripts/tests/`.
- [x] `todo_next.py` has unit tests covering main selection paths (success, conflict, not-found, pending hint).
- [x] Basic tests exist for `issue_add.py`, `todo_update.py`, and `log_add.py`.
- [x] Tests document how to run them.

## Dependencies
None.

## Entry points
- path: yoda/scripts/todo_next.py
  type: code
- path: yoda/scripts/lib/validate.py
  type: code
- path: yoda/scripts/lib/cli.py
  type: code
- path: project/specs/15-scripts-python-structure.md
  type: doc

## Implementation notes
Use temporary TODO fixtures in tests; avoid modifying real TODO files.

## Tests
Not applicable (this issue creates tests).

## Risks and edge cases
- Ensure tests do not depend on local timezone or filesystem state.

## Result log
Added pytest-based unit tests under `yoda/scripts/tests/` covering `todo_next.py` and basic flows for `issue_add.py`, `todo_update.py`, and `log_add.py`. Tests use dev `test` fixtures and clean up created files; added a test command to the scripts README.

Commit suggestion:
test(scripts): add unit tests

Issue: `yoda-0009`
Path: `yoda/project/issues/yoda-0009-add-unit-tests-for-yoda-scripts.md`