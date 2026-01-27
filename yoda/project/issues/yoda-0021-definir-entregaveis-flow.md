---
agent: Human
created_at: '2026-01-27T13:32:12-03:00'
depends_on: []
description: Define the minimum required deliverables for each YODA Flow phase (Study,
  Document, Implement, Evaluate). The decision should specify what artifacts are mandatory
  so agents and users have consistent expectations. This removes ambiguity about what
  "done" means per phase.
entrypoints: []
id: yoda-0021
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 7
schema_version: '1.0'
slug: definir-entregaveis-flow
status: done
tags: []
title: Definir entregaveis minimos por fase do YODA Flow
updated_at: '2026-01-27T13:32:37-03:00'
---

# yoda-0021 - Define minimum deliverables per YODA Flow phase

## Summary
Define the minimum required deliverables for each YODA Flow phase (Study, Document, Implement, Evaluate). The decision should specify what artifacts are mandatory so agents and users have consistent expectations. This removes ambiguity about what "done" means per phase.

## Context
The summary lists flow deliverables as open. Several specs mention outputs but not a consolidated minimum set.

## Objective
Define the minimum deliverables per phase and update the canonical specs and summary.

## Scope
- Specify minimum deliverables for Study, Document, Implement, Evaluate.
- Update the flow and playbook specs with the agreed list.
- Update the summary to close the decision.

## Out of scope
- Adding new phases or changing the core YODA Flow.
- Implementing tooling that enforces the deliverables.

## Requirements
- Deliverables are explicit and testable.
- The decision is reflected in the canonical spec file(s).
- project/specs/summary.md reflects the closure.

## Acceptance criteria
- [ ] Minimum deliverables per phase are documented in canonical specs.
- [ ] project/specs/summary.md no longer lists flow deliverables as open.

## Dependencies
None

## Entry points
- path: project/specs/summary.md
  type: issue
- path: project/specs/02-yoda-flow-process.md
  type: issue
- path: project/specs/06-agent-playbook.md
  type: issue

## Implementation notes
- Ensure the deliverables align with existing language about logs and commit text.

## Tests
Not applicable.

## Risks and edge cases
- Overly strict deliverables may reduce flexibility for lightweight tasks.

## Result log
Defined minimum deliverables per phase, including the lightweight rule and approval checkpoints.

Commit:
docs(specs): define flow deliverables

Issue: yoda-0021
Path: yoda/project/issues/yoda-0021-definir-entregaveis-flow.md