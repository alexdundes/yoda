---
agent: Human
created_at: '2026-01-27T13:32:12-03:00'
depends_on: []
description: Define a validatable schema for `TODO.<dev>.yaml`, including field types,
  required keys, enums, and constraints. The schema must be explicit enough to support
  future validation tooling. This removes ambiguity for agents and scripts.
entrypoints: []
id: yoda-0007
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 9
schema_version: '1.0'
slug: schema-formal-todo-dev-yaml
status: done
tags: []
title: Schema formal do `TODO.<dev>.yaml`
updated_at: '2026-01-27T13:32:34-03:00'
---

# yoda-0007 - Define `TODO.<dev>.yaml` formal schema

## Summary
Define a validatable schema for `TODO.<dev>.yaml`, including field types, required keys, enums, and constraints. The schema must be explicit enough to support future validation tooling. This removes ambiguity for agents and scripts.

## Context
The framework defines `TODO.<dev>.yaml` as the canonical metadata source, but a formal schema has not been finalized. Without it, scripts and agents may diverge in expectations.

## Objective
Specify the formal `TODO.<dev>.yaml` schema and document it in the canonical specs.

## Scope
- Define required fields, types, and constraints for `TODO.<dev>.yaml`.
- Provide a canonical example aligned with the schema.
- Update relevant specs to reflect the finalized schema.

## Out of scope
- Implementing validation scripts.
- Changing the core TODO workflow.

## Requirements
- Schema is explicit and unambiguous.
- Field constraints are documented (types, enums, required/optional).
- Canonical specs include the final schema.

## Acceptance criteria
- [ ] `TODO.<dev>.yaml` formal schema is documented in canonical specs.
- [ ] Example reflects the finalized schema.

## Dependencies
None

## Entry points
- path: project/specs/04-todo-dev-yaml-issues.md
  type: issue
- path: project/specs/00-conventions.md
  type: issue

## Implementation notes
- Keep the schema compatible with existing decisions in summary.

## Tests
Not applicable.

## Risks and edge cases
- Overly strict schema could reduce flexibility for early adopters.

## Result log
Defined the formal `TODO.<dev>.yaml` schema with required fields, constraints, and updated examples.

Commit:
docs(specs): define TODO schema

Issue: yoda-0007
Path: yoda/project/issues/yoda-0007-schema-formal-todo-dev-yaml.md