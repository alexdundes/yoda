---
agent: Human
created_at: '2026-01-27T13:32:12-03:00'
depends_on:
- yoda-0004
description: Define the CLI interface for YODA scripts v1 (args, outputs, exit codes,
  dry-run, errors). The goal is to make script usage consistent and predictable. This
  removes ambiguity for tooling integration.
entrypoints: []
id: yoda-0009
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 8
schema_version: '1.0'
slug: contrato-cli-scripts-v1
status: done
tags: []
title: Contrato CLI dos scripts v1
updated_at: '2026-01-27T13:32:35-03:00'
---

# yoda-0009 - Define scripts v1 CLI contract

## Summary
Define the CLI interface for YODA scripts v1 (args, outputs, exit codes, dry-run, errors). The goal is to make script usage consistent and predictable. This removes ambiguity for tooling integration.

## Context
Scripts v1 are specified at a high level, but the CLI contract (flags, outputs, exit behavior) is not finalized. Agents and tools need a clear interface.

## Objective
Document the scripts v1 CLI contract in the canonical specs.

## Scope
- Define CLI flags and arguments for required scripts.
- Define outputs and exit code behavior.
- Document error handling and dry-run behavior.

## Out of scope
- Implementing the scripts.
- Adding new script commands beyond v1.

## Requirements
- CLI contract is explicit and unambiguous.
- Canonical specs reflect the agreed interface.

## Acceptance criteria
- [ ] Scripts v1 CLI contract is documented in canonical specs.
- [ ] Interface includes args, outputs, exit codes, and errors.

## Dependencies
yoda-0004

## Entry points
- path: project/specs/05-scripts-and-automation.md
  type: issue
- path: project/specs/13-yoda-scripts-v1.md
  type: issue

## Implementation notes
- Keep the interface consistent with the developer selection rules.

## Tests
Not applicable.

## Risks and edge cases
- Inconsistent CLI behavior could break agent tooling.

## Result log
Defined the CLI contract with global flags, output formats, exit codes, and error handling.

Commit:
docs(specs): define CLI contract

Issue: yoda-0009
Path: yoda/project/issues/yoda-0009-contrato-cli-scripts-v1.md