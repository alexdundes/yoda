# alex-024 - Define stack profiles policy

## Summary
Decide whether YODA v1 should stay generic or include stack-specific profiles (web, data, backend). The decision should clarify if profiles are part of v1 or deferred. This removes ambiguity about intended extensibility.

## Context
Stack profiles are listed as an open decision in the summary. Current specs are generic and do not define profile behavior.

## Objective
Decide the stack profile policy and record it in the canonical specs and summary.

## Scope
- Decide whether profiles exist in v1 or are deferred.
- Document the policy in canonical specs.
- Update the summary to close the decision.

## Out of scope
- Designing or implementing specific profiles.
- Changing the core YODA Flow.

## Requirements
- The policy is explicit and consistent across specs.
- The decision is recorded in canonical spec file(s).
- project/specs/summary.md reflects the closure.

## Acceptance criteria
- [ ] Stack profile policy is documented in canonical specs.
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
- Ensure the decision aligns with the simplicity goals and scriptability.

## Tests
Not applicable.

## Risks and edge cases
- Introducing profiles too early may add complexity without clear value.

## Result log
