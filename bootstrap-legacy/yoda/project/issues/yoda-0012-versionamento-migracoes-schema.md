---
agent: Human
created_at: '2026-01-27T13:32:12-03:00'
depends_on:
- yoda-0007
- yoda-0008
description: Define how schema versioning and migrations work for YODA YAML and Markdown
  artifacts. The goal is to standardize how changes are introduced and upgraded. This
  removes ambiguity for long-term maintenance.
entrypoints: []
id: yoda-0012
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 7
schema_version: '1.0'
slug: versionamento-migracoes-schema
status: done
tags: []
title: Versionamento e migracoes de schema
updated_at: '2026-01-27T13:32:35-03:00'
---

# yoda-0012 - Define schema versioning and migrations

## Summary
Define how schema versioning and migrations work for YODA YAML and Markdown artifacts. The goal is to standardize how changes are introduced and upgraded. This removes ambiguity for long-term maintenance.

## Context
The TODO and issue schemas will evolve, but no versioning or migration policy exists. This creates risk for tooling compatibility.

## Objective
Document a schema versioning and migration policy in the canonical specs.

## Scope
- Define schema version identifiers and placement.
- Define migration expectations and strategy.
- Update canonical specs to reflect the policy.

## Out of scope
- Implementing migration tooling.
- Defining migrations for external systems.

## Requirements
- Versioning policy is explicit and unambiguous.
- Canonical specs include the policy.

## Acceptance criteria
- [ ] Schema versioning and migration policy is documented in canonical specs.

## Dependencies
yoda-0007, yoda-0008

## Entry points
- path: project/specs/04-todo-dev-yaml-issues.md
  type: issue
- path: project/specs/05-scripts-and-automation.md
  type: issue

## Implementation notes
- Ensure compatibility with existing TODO and issue formats.

## Tests
Not applicable.

## Risks and edge cases
- Incomplete policy may lead to incompatible tooling updates.

## Result log
Defined schema_version (1.0) for TODO and issue metadata with major/minor rules and migration policy.

Commit:
docs(specs): define schema versioning

Issue: yoda-0012
Path: yoda/project/issues/yoda-0012-versionamento-migracoes-schema.md