---
agent: Human
created_at: '2026-01-27T13:32:12-03:00'
depends_on:
- yoda-0004
description: Define deterministic rules for priority, ordering, pending status, and
  depends_on handling. The goal is to ensure all agents select the same next issue.
  This removes ambiguity in issue selection.
entrypoints: []
id: yoda-0010
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 8
schema_version: '1.0'
slug: regras-deterministicas-ordenacao-selecao
status: done
tags: []
title: Regras deterministicas de ordenacao e selecao
updated_at: '2026-01-27T13:32:35-03:00'
---

# yoda-0010 - Define deterministic ordering and selection rules

## Summary
Define deterministic rules for priority, ordering, pending status, and depends_on handling. The goal is to ensure all agents select the same next issue. This removes ambiguity in issue selection.

## Context
Specs mention priority and dependencies, but a consolidated, deterministic selection rule is not documented. This is needed for consistent automation.

## Objective
Document deterministic ordering and selection rules in the canonical specs.

## Scope
- Define how priority is interpreted.
- Define tie-breakers and ordering rules.
- Define how pending and depends_on affect selection.

## Out of scope
- Implementing selection scripts.
- Changing the YODA Flow phases.

## Requirements
- Rules are explicit and deterministic.
- Canonical specs reflect the rules.

## Acceptance criteria
- [ ] Deterministic selection rules are documented in canonical specs.
- [ ] Rules cover priority, ordering, pending, and dependencies.

## Dependencies
yoda-0004

## Entry points
- path: project/specs/04-todo-dev-yaml-issues.md
  type: issue
- path: project/specs/13-yoda-scripts-v1.md
  type: issue
- path: project/specs/02-yoda-flow-process.md
  type: issue

## Implementation notes
- Ensure rules align with todo_next.py behavior expectations.

## Tests
Not applicable.

## Risks and edge cases
- Ambiguous tie-breakers could cause inconsistent agent behavior.

## Result log
Defined deterministic selection rules for priority, ordering, pending handling, and dependencies.

Commit:
docs(specs): define selection rules

Issue: yoda-0010
Path: yoda/project/issues/yoda-0010-regras-deterministicas-ordenacao-selecao.md