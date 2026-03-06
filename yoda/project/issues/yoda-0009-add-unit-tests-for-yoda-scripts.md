---
schema_version: '2.00'
id: yoda-0009
status: done
title: Add unit tests for YODA scripts
description: Create unit tests for implemented scripts, starting with todo_next and
  existing helpers
priority: 5
created_at: '2026-01-27T18:04:27-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
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

## Flow log
2026-01-27T18:04:27-03:00 | [yoda-0009] issue_add created | title: Add unit tests for YODA scripts | description: Create unit tests for implemented scripts, starting with todo_next and existing helpers | slug: add-unit-tests-for-yoda-scripts
2026-01-27T18:12:16-03:00 | [yoda-0009] todo_update | status: to-do -> doing
2026-01-27T18:12:29-03:00 | [yoda-0009] document: expanded requirements to cover all scripts, pytest, and cleanup for dev test
2026-01-27T18:14:06-03:00 | [yoda-0009] implement: added pytest suite for scripts with dev test fixtures and cleanup
2026-01-27T18:14:19-03:00 | [yoda-0009] todo_update | status: doing -> done
2026-01-27T18:14:23-03:00 | [yoda-0009] evaluate: acceptance criteria checked and result log updated in issue
2026-01-27T18:22:43-03:00 | [yoda-0009] tests: pytest yoda/scripts/tests passed (6 tests)
