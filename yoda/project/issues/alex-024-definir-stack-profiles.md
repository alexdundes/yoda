# alex-024 - Define stack profiles policy

## Summary
Define the stack profile policy for YODA v1. The decision should clarify whether profiles exist in v1 or are deferred as a future extension.

## Context
Stack profiles are listed as an open decision in the summary. The current framework is process-first (agent behavior, artifacts, and scripts) and should remain generic in v1.

## Objective
Document the policy that YODA v1 is stack-agnostic and defers stack profiles to a future, optional extension.

## Scope
- Record that stack profiles are not part of v1.
- Clarify that profiles, if ever added, are optional extensions outside the core framework.
- Document the policy in canonical specs.
- Update the summary to close the decision.

## Out of scope
- Designing or implementing specific profiles.
- Changing the core YODA Flow.

## Requirements
- The policy states that YODA v1 is generic and stack-agnostic.
- Any stack profiles are explicitly future extensions, not required by the core.
- The decision is recorded in canonical spec file(s).
- project/specs/summary.md reflects the closure.

## Acceptance criteria
- [ ] Specs state that YODA v1 is stack-agnostic and does not include profiles.
- [ ] Specs note that profiles are optional, future extensions outside the core.
- [ ] project/specs/summary.md no longer lists stack profiles as open.

## Dependencies
None

## Entry points
- path: project/specs/summary.md
  type: issue
- path: project/specs/01-yoda-overview.md
  type: issue
- path: project/specs/10-approaches-and-references.md
  type: issue

## Implementation notes
- Keep the language consistent with the brand voice and simplicity goals.

## Tests
Not applicable.

## Risks and edge cases
- Introducing profiles too early may add complexity without clear value.

## Result log
Recorded the stack profile policy: YODA v1 is stack-agnostic, and profiles are optional future extensions.

Commit:
docs(specs): define stack profile policy

Issue: alex-024
Path: yoda/project/issues/alex-024-definir-stack-profiles.md

Follow-up: removed stack profiles from README open decisions.
