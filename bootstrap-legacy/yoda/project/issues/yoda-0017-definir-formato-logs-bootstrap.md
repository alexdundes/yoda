---
agent: Human
created_at: '2026-01-27T13:32:12-03:00'
depends_on: []
description: Document the log format difference between the bootstrap meta-implementation
  (Markdown) and the future framework (YAML).
entrypoints: []
id: yoda-0017
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 7
schema_version: '1.0'
slug: definir-formato-logs-bootstrap
status: done
tags: []
title: Definir formato de logs no bootstrap vs framework
updated_at: '2026-01-27T13:32:36-03:00'
---

# yoda-0017 - Definir formato de logs no bootstrap vs framework

## Summary
Document the log format difference between the bootstrap meta-implementation (Markdown) and the future framework (YAML).

## Context
Specs currently describe logs as YAML, while the meta-implementation uses Markdown until scripts exist. This should be explicitly stated in the specs to avoid confusion.

## Objective
Update specs to clarify the bootstrap log format and the transition to YAML logs when scripts are available.

## Scope
- Add an explicit bootstrap exception for logs in the relevant specs.
- Keep the canonical future behavior as YAML logs.
- Document that bootstrap specifications live in a separate file that explains the bootstrap concept.
- State that the bootstrap concept will be removed from documentation in the future.

## Out of scope
- Implementing log scripts.
- Changing log schemas.

## Requirements
- Specs mention that bootstrap logs are Markdown until scripts exist.
- Canonical framework behavior remains YAML logs.
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
- Keep the exception scoped to the meta-implementation.

## Tests
Not applicable.

## Risks and edge cases
- Agents may write logs in the wrong format if the exception is not explicit.

## Result log
Confirmed bootstrap log format in the dedicated bootstrap spec and documented the transition to YAML logs.

Commit:
docs(specs): document bootstrap log format

Issue: yoda-0017
Path: yoda/project/issues/yoda-0017-definir-formato-logs-bootstrap.md