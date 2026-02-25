---
agent: Human
created_at: '2026-01-27T16:41:45-03:00'
depends_on: []
description: Document minimal JSON fields for issue_add, todo_update, log_add
entrypoints: []
id: yoda-0003
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: define-json-output-minimums
status: done
tags: []
title: Define JSON output minimums
updated_at: '2026-01-27T17:07:50-03:00'
---

# yoda-0003 - Define JSON output minimums

## Summary
Define the minimal JSON payload contract for `--format json` across `issue_add.py`, `todo_update.py`, and `log_add.py` so agents can rely on stable keys.

## Context
The scripts already emit JSON, but the specs do not guarantee which fields are present. This makes automation and agent parsing fragile.

## Objective
Document the required JSON keys for each script and note that consumers must ignore unknown fields, centralized in `project/specs/13-yoda-scripts-v1.md`.

## Scope
- Add a centralized JSON output contract to `project/specs/13-yoda-scripts-v1.md`.
- Cover only the three scripts currently implemented.

## Out of scope
- Changing script output behavior.
- Defining JSON for future scripts not yet implemented.

## Requirements
- Specify minimal JSON keys for each script in a centralized section:
  - `issue_add.py`: `issue_id`, `issue_path`, `todo_path`, `log_path`, `template`, `dry_run`.
  - `todo_update.py`: `issue_id`, `updated_fields`, `todo_path`, `dry_run`.
  - `log_add.py`: `issue_id`, `log_path`, `timestamp`, `dry_run`.
- State that additional fields may be added and consumers should ignore unknown keys.

## Acceptance criteria
- [x] `project/specs/13-yoda-scripts-v1.md` documents the minimal JSON keys for each script.
- [x] Specs clarify forward-compatibility (ignore unknown keys).
- [x] No code changes are required.

## Dependencies
None.

## Entry points
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: yoda/scripts/issue_add.py
  type: code
- path: yoda/scripts/todo_update.py
  type: code
- path: yoda/scripts/log_add.py
  type: code

## Implementation notes
Match the documented keys to the payloads emitted by the scripts today; avoid promising values that are not always present.

## Tests
Not applicable.

## Risks and edge cases
- If a script adds/removes keys, update the spec to keep the contract accurate.

## Result log
Added a centralized JSON output contract in `project/specs/13-yoda-scripts-v1.md` with minimum keys per script and a forward-compatibility rule to ignore unknown fields.

Commit suggestion:
docs(specs): define JSON output minimums

Issue: `yoda-0003`
Path: `yoda/project/issues/yoda-0003-define-json-output-minimums.md`
