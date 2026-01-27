---
agent: Human
created_at: '2026-01-27T16:41:37-03:00'
depends_on: []
description: Document that issue slugs are immutable; renames require migration
entrypoints: []
id: yoda-0001
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: slug-immutability-rule
status: to-do
tags: []
title: Slug immutability rule
updated_at: '2026-01-27T16:41:37-03:00'
---

# yoda-0001 - Slug immutability rule

## Summary
Define slug immutability in the framework specs so issue slugs never change after creation; renames are handled via explicit migrations, not regular updates.

## Context
Slug is embedded in issue and log paths (`yoda/project/issues/<id>-<slug>.md`, `yoda/logs/<id>-<slug>.yaml`). The specs do not explicitly state whether slug can change, which risks path drift if titles are edited or if future scripts regenerate slugs.

## Objective
Add explicit guidance in specs that slugs are immutable and document how rename/migration should be handled.

## Scope
- Add rule text to specs that define TODO/issue metadata and conventions.
- Mention path coupling to slug and the impact on issue/log filenames.

## Out of scope
- Implementing a rename/migration script.
- Modifying existing TODO/issue data.

## Requirements
- State that `slug` is immutable once created.
- Clarify that renames require an explicit migration operation (not `todo_update`).
- Note that scripts must not auto-change slug when updating other fields.

## Acceptance criteria
- [ ] Spec text explicitly states slug immutability.
- [ ] Spec mentions that renames require migration and are out of the regular update flow.
- [ ] No code changes are required.

## Dependencies
None.

## Entry points
- path: project/specs/04-todo-dev-yaml-issues.md
  type: doc
- path: project/specs/00-conventions.md
  type: doc
- path: yoda/scripts/issue_add.py
  type: code

## Implementation notes
Keep wording consistent with existing TODO schema and path patterns (`yoda/project/issues/<id>-<slug>.md`, `yoda/logs/<id>-<slug>.yaml`).

## Tests
Not applicable.

## Risks and edge cases
- If a future tool regenerates slugs, paths can drift; highlight migration-only renames.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
<!-- AGENT: Logs are YAML: `yoda/logs/<id>-<slug>.yaml`. -->
