# alex-019 - Define tooling policy (mandatory vs optional)

## Summary
Define whether YODA tooling is mandatory or optional and document the rule in the canonical specs. This decision should explain how teams behave before and after scripts exist. The outcome must remove ambiguity from the framework guidance.

## Context
The summary lists an open decision about tooling policy. Without a clear rule, agents and users may disagree on whether scripts are required or merely recommended.

## Objective
Decide the tooling policy and update the relevant spec files so the rule is consistent across the framework.

## Scope
- Decide the official tooling policy for YODA v1.
- Document the rule in the canonical specs.
- Update the summary to reflect the decision.

## Out of scope
- Implementing tooling or scripts.
- Changing unrelated framework concepts.

## Requirements
- The policy is explicit and unambiguous.
- The policy is recorded in the canonical spec file(s).
- project/specs/summary.md reflects the closed decision.

## Acceptance criteria
- [ ] Tooling policy is defined and documented in the appropriate spec file(s).
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
- Consider how bootstrap behavior is described relative to future script-based workflow.

## Tests
Not applicable.

## Risks and edge cases
- If the policy is too strict, it may block bootstrap usage.

## Result log
