---
agent: Human
created_at: '2026-01-27T13:32:12-03:00'
depends_on: []
description: 'Define the tooling policy: scripts are mandatory when available, optional
  only during bootstrap. Document the rule in the canonical specs and remove ambiguity
  from the framework guidance.'
entrypoints: []
id: yoda-0019
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 7
schema_version: '1.0'
slug: definir-politica-tooling
status: done
tags: []
title: Definir politica de tooling (obrigatorio vs opcional)
updated_at: '2026-01-27T13:32:37-03:00'
---

# yoda-0019 - Define tooling policy (mandatory vs optional)

## Summary
Define the tooling policy: scripts are mandatory when available, optional only during bootstrap. Document the rule in the canonical specs and remove ambiguity from the framework guidance.

## Context
The summary lists an open decision about tooling policy. Without a clear rule, agents and users may disagree on whether scripts are required or merely recommended.

## Objective
Document the tooling policy and update the relevant spec files so the rule is consistent across the framework.

## Scope
- Decide the official tooling policy for YODA v1.
- Document the rule in the canonical specs.
- Update the summary to reflect the decision.

## Out of scope
- Implementing tooling or scripts.
- Changing unrelated framework concepts.

## Requirements
- The policy states that scripts are mandatory when available.
- The policy states that tooling is optional only during bootstrap.
- The policy is recorded in the canonical spec file(s).
- project/specs/summary.md reflects the closed decision.

## Acceptance criteria
- [ ] Specs state that scripts are mandatory when available and optional only during bootstrap.
- [ ] project/specs/summary.md no longer lists tooling policy as open.

## Dependencies
None

## Entry points
- path: project/specs/summary.md
  type: issue
- path: project/specs/05-scripts-and-automation.md
  type: issue
- path: project/specs/06-agent-playbook.md
  type: issue
- path: project/specs/01-yoda-overview.md
  type: issue

## Implementation notes
- Keep the policy consistent with bootstrap rules in project/specs/15-bootstrap.md.

## Tests
Not applicable.

## Risks and edge cases
- If the policy is too strict, it may block bootstrap usage.

## Result log
Defined the tooling policy: scripts are mandatory when available, optional only during bootstrap.

Commit:
docs(specs): define tooling policy

Issue: yoda-0019
Path: yoda/project/issues/yoda-0019-definir-politica-tooling.md