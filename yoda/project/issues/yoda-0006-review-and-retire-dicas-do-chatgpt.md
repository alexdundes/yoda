---
agent: Human
created_at: '2026-01-27T16:44:23-03:00'
depends_on: []
description: Review yoda/dicas-do-chatgpt.md; if contents are fully captured elsewhere, remove the file
entrypoints: []
id: yoda-0006
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: review-and-retire-dicas-do-chatgpt
status: to-do
tags: []
title: Review and retire dicas-do-chatgpt
updated_at: '2026-01-27T16:44:23-03:00'
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
- [ ] A review of `yoda/dicas-do-chatgpt.md` is completed.
- [ ] Any missing guidance is moved into specs or tracked by issues.
- [ ] The file is removed if redundant.

## Dependencies
None.

## Entry points
- path: yoda/dicas-do-chatgpt.md
  type: doc
- path: project/specs
  type: doc

## Implementation notes
Cross-check against the recent issues created from dicas-do-chatgpt feedback.

## Tests
Not applicable.

## Risks and edge cases
- Removing the file without capturing a unique requirement could lose intent.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
<!-- AGENT: Logs are YAML: `yoda/logs/<id>-<slug>.yaml`. -->
