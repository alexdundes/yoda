---
agent: Human
created_at: '2026-01-27T16:41:42-03:00'
depends_on: []
description: 'Add spec text: log_add resolves slug via TODO and fails if id missing'
entrypoints: []
id: yoda-0002
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: document-log-add-slug-resolution
status: done
tags: []
title: Document log_add slug resolution
updated_at: '2026-01-27T17:04:47-03:00'
---

# yoda-0002 - Document log_add slug resolution

## Summary
Document in the specs that `log_add.py` resolves the slug from the TODO entry (by issue id) and fails when the id or issue file is missing.

## Context
The current implementation loads `yoda/todos/TODO.<dev>.yaml`, locates the issue by id, and derives the slug and paths from that entry. The spec does not explicitly state this resolution or the failure behavior.

## Objective
Align the written contract with the implemented behavior of `log_add.py`, documenting changes only in `project/specs/19-log-add-script.md`.

## Scope
- Update `project/specs/19-log-add-script.md` to describe slug resolution via TODO.
- Note the NOT_FOUND behavior when the issue id or issue file is missing.

## Out of scope
- Changes to the script implementation.

## Requirements
- State that `log_add.py` loads the TODO file and resolves the slug from the issue item.
- State that missing issue id or missing issue file results in ExitCode.NOT_FOUND.
- Clarify that the slug is not supplied via CLI and is derived from TODO.

## Acceptance criteria
- [x] `project/specs/19-log-add-script.md` includes the slug resolution step.
- [x] Error behavior for missing issue id/file is documented.
- [x] No code changes are required.

## Dependencies
None.

## Entry points
- path: project/specs/19-log-add-script.md
  type: doc
- path: yoda/scripts/log_add.py
  type: code

## Implementation notes
Match the documented steps to the current implementation order: load TODO, find issue item, resolve slug, build issue/log paths.

## Tests
Not applicable.

## Risks and edge cases
- If the TODO schema changes, update the spec and implementation in tandem.

## Result log
Documented that `log_add.py` resolves the slug from the TODO item and does not accept slug input, keeping the NOT_FOUND behavior for missing issue id/file explicit in the behavior steps.

Commit suggestion:
docs(specs): clarify log_add slug resolution

Issue: `yoda-0002`
Path: `yoda/project/issues/yoda-0002-document-log-add-slug-resolution.md`
