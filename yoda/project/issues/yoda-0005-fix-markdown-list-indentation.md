---
agent: Human
created_at: '2026-01-27T16:41:51-03:00'
depends_on: []
description: Adjust indentation in 02-yoda-flow-process.md for list consistency
entrypoints: []
id: yoda-0005
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: fix-markdown-list-indentation
status: done
tags: []
title: Fix markdown list indentation
updated_at: '2026-01-27T17:16:44-03:00'
---

# yoda-0005 - Fix markdown list indentation

## Summary
Fix the list indentation in `project/specs/02-yoda-flow-process.md` so the Notes section renders consistently.

## Context
The "Next issue selection" line is mis-indented, which breaks list formatting in Markdown renderers.

## Objective
Align the indentation of the stray bullet with the rest of the list in the Notes section.

## Scope
- Adjust indentation for the single mis-indented bullet in Notes in `project/specs/02-yoda-flow-process.md`.

## Out of scope
- Any content changes to the YODA Flow rules.

## Requirements
- Correct the indentation of the "Next issue selection" bullet so it is part of the Notes list.

## Acceptance criteria
- [x] The Notes list renders as a consistent bullet list.
- [x] No wording changes are introduced.

## Dependencies
None.

## Entry points
- path: project/specs/02-yoda-flow-process.md
  type: doc

## Implementation notes
Keep the bullet text unchanged; only adjust whitespace.

## Tests
Not applicable.

## Risks and edge cases
- None.

## Result log
Fixed the indentation of the "Next issue selection" bullet so it renders as part of the Notes list.

Commit suggestion:
docs(specs): fix notes indentation

Issue: `yoda-0005`
Path: `yoda/project/issues/yoda-0005-fix-markdown-list-indentation.md`