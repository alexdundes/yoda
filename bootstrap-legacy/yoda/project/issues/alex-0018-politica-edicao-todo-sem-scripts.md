# alex-0018 - Definir politica de edicao de TODO sem scripts

## Summary
Clarify how TODO updates are handled when scripts are not yet available in the meta-implementation.

## Context
Specs say agents must never edit `TODO.<dev>.yaml` directly and should use scripts, but the meta-implementation has no scripts yet and uses Markdown TODOs. The spec should define how to proceed during bootstrap.

## Objective
Document the bootstrap rule for TODO updates before scripts exist, while keeping YAML and scripts as the canonical future behavior.

## Scope
- Define a bootstrap exception for manual TODO updates.
- Keep the canonical rule that scripts are required once available.
- Document the exception in the dedicated bootstrap specs file.

## Out of scope
- Implementing the scripts.
- Changing TODO schemas.

## Requirements
- Bootstrap specs describe the exception for manual TODO updates.
- Canonical rule remains script-based updates for YAML.

## Acceptance criteria
- [ ] Bootstrap specs are documented in a separate file that explains the bootstrap concept.
- [ ] Bootstrap specs include the manual TODO update exception.

## Dependencies
None

## Entry points
- path: project/specs/15-bootstrap.md
  type: issue

## Implementation notes
- Keep the exception limited to the meta-implementation phase.

## Tests
Not applicable.

## Risks and edge cases
- Without an explicit exception, agents may be blocked from maintaining the TODO.

## Result log
Documented the manual TODO update exception in the bootstrap specs file.

Commit:
docs(specs): allow manual TODO updates in bootstrap

Issue: alex-0018
Path: yoda/project/issues/alex-0018-politica-edicao-todo-sem-scripts.md
