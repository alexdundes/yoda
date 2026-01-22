# alex-018 - Definir politica de edicao de TODO sem scripts

## Summary
Clarify how TODO updates are handled when scripts are not yet available in the meta-implementation.

## Context
Specs say agents must never edit `TODO.<dev>.yaml` directly and should use scripts, but the meta-implementation has no scripts yet and uses Markdown TODOs. The spec should define how to proceed during bootstrap.

## Objective
Document the bootstrap rule for TODO updates before scripts exist, while keeping YAML and scripts as the canonical future behavior.

## Scope
- Define a bootstrap exception for manual TODO updates.
- Keep the canonical rule that scripts are required once available.

## Out of scope
- Implementing the scripts.
- Changing TODO schemas.

## Requirements
- Specs describe the bootstrap exception for TODO updates.
- Canonical rule remains script-based updates for YAML.

## Acceptance criteria
- [ ] project/specs/06-agent-playbook.md mentions the bootstrap TODO update exception.
- [ ] project/specs/04-todo-dev-yaml-issues.md clarifies the bootstrap constraint.

## Dependencies
None

## Entry points
- path: project/specs/06-agent-playbook.md
  type: issue
- path: project/specs/04-todo-dev-yaml-issues.md
  type: issue

## Implementation notes
- Keep the exception limited to the meta-implementation phase.

## Tests
Not applicable.

## Risks and edge cases
- Without an explicit exception, agents may be blocked from maintaining the TODO.

## Result log
