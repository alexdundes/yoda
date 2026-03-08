---
schema_version: '2.00'
status: done
title: Fix markdown list indentation
description: Adjust indentation in 02-yoda-flow-process.md for list consistency
priority: 5
created_at: '2026-01-27T16:41:51-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
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


## Entry points
- `project/specs/02-yoda-flow-process.md`

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

## Flow log
2026-01-27T16:41:51-03:00 | [yoda-0005] issue_add created | title: Fix markdown list indentation | description: Adjust indentation in 02-yoda-flow-process.md for list consistency | slug: fix-markdown-list-indentation
2026-01-27T17:15:07-03:00 | [yoda-0005] docs: removed obsolete result-log comment from issue markdown
2026-01-27T17:16:16-03:00 | [yoda-0005] document: scope confirmed for indentation fix in project/specs/02-yoda-flow-process.md
2026-01-27T17:16:40-03:00 | [yoda-0005] implement: fixed indentation in 02-yoda-flow-process.md
2026-01-27T17:16:44-03:00 | [yoda-0005] todo_update | status: to-do -> done
2026-01-27T17:16:48-03:00 | [yoda-0005] evaluate: acceptance criteria checked and result log updated in issue