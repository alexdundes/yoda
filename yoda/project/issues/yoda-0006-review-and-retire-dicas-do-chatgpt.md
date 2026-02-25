---
created_at: '2026-01-27T16:47:31-03:00'
depends_on: []
description: Review yoda/dicas-do-chatgpt.md; if contents are fully captured elsewhere,
  remove the file
id: yoda-0006
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.01'
slug: review-and-retire-dicas-do-chatgpt
status: done
title: Review and retire dicas-do-chatgpt
updated_at: '2026-02-25T20:02:28-03:00'
---

# yoda-0006 - Review and retire dicas-do-chatgpt

## Summary
Review `yoda/dicas-do-chatgpt.md` against current specs and scripts; if all guidance is already captured elsewhere, delete the file.

## Context
The file aggregates advice from earlier iterations. With v6 in place, we need to confirm what remains relevant and ensure any useful guidance is codified in the canonical specs, not in a loose tips file.

## Objective
Either absorb remaining valid guidance into specs/issues or remove the file if it no longer adds value.

## Scope
- Review the contents of `yoda/dicas-do-chatgpt.md`.
- Identify any guidance not present in `project/specs/` or existing issues.
- Update specs or create issues if needed.
- Remove `yoda/dicas-do-chatgpt.md` if it is fully covered.

## Out of scope
- Implementing new scripts.
- Large refactors unrelated to the guidance.

## Requirements
- All unique guidance from `yoda/dicas-do-chatgpt.md` is captured in canonical specs or issues.
- If no unique guidance remains, delete the file.

## Acceptance criteria
- [x] A review of `yoda/dicas-do-chatgpt.md` is completed.
- [x] Any missing guidance is moved into specs or tracked by issues.
- [x] The file is removed if redundant.

## Dependencies
None.

## Entry points
- path: yoda/dicas-do-chatgpt.md
  type: doc
- path: project/specs
  type: doc

## Implementation notes
Cross-check against the recent issues created from dicas-do-chatgpt feedback and confirm the current locations:
- Slug immutability: `project/specs/04-todo-dev-yaml-issues.md` + `project/specs/00-conventions.md`.
- log_add slug resolution: `project/specs/19-log-add-script.md`.
- JSON output minimums: `project/specs/13-yoda-scripts-v1.md`.
- Happy path: `project/specs/05-scripts-and-automation.md`.
- Markdown indent fix: `project/specs/02-yoda-flow-process.md`.

## Tests
Not applicable.

## Risks and edge cases
- Removing the file without capturing a unique requirement could lose intent.

## Result log
Confirmed all items are already captured in specs or completed issues; removed `yoda/dicas-do-chatgpt.md` as redundant.

Commit suggestion:
docs: retire dicas-do-chatgpt

Issue: `yoda-0006`
Path: `yoda/project/issues/yoda-0006-review-and-retire-dicas-do-chatgpt.md`