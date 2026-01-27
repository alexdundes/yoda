---
agent: Human
created_at: '2026-01-27T13:32:12-03:00'
depends_on: []
description: Decide whether the TODO metadata schema needs additional required fields
  beyond the current baseline. The decision should clarify what is mandatory in YAML
  vs Markdown. This removes ambiguity for scripts and agents.
entrypoints: []
id: yoda-0022
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 7
schema_version: '1.0'
slug: definir-campos-schema-metadados
status: done
tags: []
title: Definir campos adicionais do schema de metadados
updated_at: '2026-01-27T13:32:37-03:00'
---

# yoda-0022 - Define additional required metadata fields

## Summary
Decide whether the TODO metadata schema needs additional required fields beyond the current baseline. The decision should clarify what is mandatory in YAML vs Markdown. This removes ambiguity for scripts and agents.

## Context
The summary lists metadata schema as open regarding additional required fields. The current schema basics are defined but may be incomplete.

## Objective
Decide any additional required fields and update the canonical specs and summary accordingly.

## Scope
- Review current metadata schema in specs.
- Decide if additional required fields are needed.
- Update the canonical spec file(s) and summary.

## Out of scope
- Implementing schema validation tooling.
- Changing unrelated TODO or issue workflows.

## Requirements
- The required fields list is explicit and unambiguous.
- The decision is recorded in canonical specs.
- project/specs/summary.md reflects the closure.

## Acceptance criteria
- [ ] Additional required fields (if any) are documented in canonical specs.
- [ ] project/specs/summary.md no longer lists metadata schema as open.

## Dependencies
None

## Entry points
- path: project/specs/summary.md
  type: issue
- path: project/specs/04-todo-dev-yaml-issues.md
  type: issue
- path: project/specs/03-document-first-yaml-markdown.md
  type: issue

## Implementation notes
- Clarify what belongs in YAML vs what stays in Markdown narrative fields.

## Tests
Not applicable.

## Risks and edge cases
- Adding too many required fields may make the schema heavy for small projects.

## Result log
Confirmed minimal schema (no new required fields), renamed labels to tags, and documented optional origin fields.

Commit:
docs(specs): finalize metadata schema fields

Issue: yoda-0022
Path: yoda/project/issues/yoda-0022-definir-campos-schema-metadados.md