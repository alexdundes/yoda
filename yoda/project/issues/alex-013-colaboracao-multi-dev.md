# alex-013 - Define multi-dev collaboration rules

## Summary
Define collaboration rules for multi-developer YODA usage, including TODO conflicts, cross-dependencies, and branch conventions. The goal is to ensure consistent behavior when multiple devs are active. This removes ambiguity for team workflows.

## Context
YODA currently focuses on per-dev TODOs, but cross-dev coordination rules are not documented. Without guidance, teams may diverge in practice.

## Objective
Document multi-dev collaboration rules in the canonical specs.

## Scope
- Define how cross-dependencies are represented.
- Define conflict resolution expectations for TODO updates.
- Define branch naming or coordination conventions if needed.

## Out of scope
- Implementing collaboration tooling.
- Defining org-specific policies beyond the framework baseline.

## Requirements
- Rules are explicit and unambiguous.
- Canonical specs reflect the collaboration policy.

## Acceptance criteria
- [ ] Multi-dev collaboration rules are documented in canonical specs.
- [ ] Rules cover cross-dependencies and TODO conflicts.

## Dependencies
alex-007

## Entry points
- path: project/specs/04-todo-dev-yaml-issues.md
  type: issue
- path: project/specs/12-yoda-structure.md
  type: issue

## Implementation notes
- Keep rules compatible with the one-TODO-per-dev model.

## Tests
Not applicable.

## Risks and edge cases
- Overly strict rules could slow collaboration in small teams.

## Result log
Defined multi-dev rules: depends_on is same-dev only, each dev edits only their TODO, manual conflict resolution, no branch conventions.

Commit:
docs(specs): define multi-dev rules

Issue: alex-013
Path: yoda/project/issues/alex-013-colaboracao-multi-dev.md
