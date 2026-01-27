---
agent: Human
created_at: '2026-01-27T13:32:12-03:00'
depends_on: []
description: Clarify in the specs how agent entry should resolve TODO sources during
  bootstrap (Markdown) vs the future YAML format.
entrypoints: []
id: yoda-0016
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 7
schema_version: '1.0'
slug: alinhar-entrada-todo-bootstrap
status: done
tags: []
title: Alinhar entrada do agente com TODO no bootstrap
updated_at: '2026-01-27T13:32:36-03:00'
---

# yoda-0016 - Alinhar entrada do agente com TODO no bootstrap

## Summary
Clarify in the specs how agent entry should resolve TODO sources during bootstrap (Markdown) vs the future YAML format.

## Context
The entry flow in project/specs/07-agent-entry-and-root-file.md points to `TODO.<dev>.yaml`, while the bootstrap structure uses `TODO.<dev>.md`. The specs should explicitly define the conditional behavior.

## Objective
Update the specs to state how agent entry resolves TODO files in bootstrap mode and when to switch to YAML.

## Scope
- Define the bootstrap fallback behavior for `TODO.<dev>.md`.
- Keep the canonical rule for `TODO.<dev>.yaml` as the future framework default.
- Document that bootstrap specifications live in a separate file that explains the bootstrap concept.
- State that the bootstrap concept will be removed from documentation in the future.

## Out of scope
- Implementing scripts or tooling.
- Changing the underlying YODA Flow steps.

## Requirements
- Bootstrap specifications live in a separate file that explains the bootstrap concept.
- The bootstrap concept is marked as temporary and will be removed from documentation in the future.

## Acceptance criteria
- [ ] Bootstrap specs are documented in a separate file that explains the bootstrap concept.
- [ ] Specs state that bootstrap is temporary and will be removed from documentation in the future.

## Dependencies
None

## Entry points
- path: project/specs/15-bootstrap.md
  type: issue

## Implementation notes
- Keep the framework default (YAML) as the canonical target.

## Tests
Not applicable.

## Risks and edge cases
- Agents may diverge if the bootstrap rule is not explicit.

## Result log
Defined a separate bootstrap spec file and documented the temporary bootstrap rules and exit criteria.

Commit:
docs(specs): add bootstrap specification

Issue: yoda-0016
Path: yoda/project/issues/yoda-0016-alinhar-entrada-todo-bootstrap.md