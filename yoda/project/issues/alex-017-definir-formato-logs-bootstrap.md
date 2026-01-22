# alex-017 - Definir formato de logs no bootstrap vs framework

## Summary
Document the log format difference between the bootstrap meta-implementation (Markdown) and the future framework (YAML).

## Context
Specs currently describe logs as YAML, while the meta-implementation uses Markdown until scripts exist. This should be explicitly stated in the specs to avoid confusion.

## Objective
Update specs to clarify the bootstrap log format and the transition to YAML logs when scripts are available.

## Scope
- Add an explicit bootstrap exception for logs in the relevant specs.
- Keep the canonical future behavior as YAML logs.

## Out of scope
- Implementing log scripts.
- Changing log schemas.

## Requirements
- Specs mention that bootstrap logs are Markdown until scripts exist.
- Canonical framework behavior remains YAML logs.

## Acceptance criteria
- [ ] project/specs/05-scripts-and-automation.md mentions the bootstrap Markdown log exception.
- [ ] project/specs/06-agent-playbook.md reflects the bootstrap log format.

## Dependencies
None

## Entry points
- path: project/specs/05-scripts-and-automation.md
  type: issue
- path: project/specs/06-agent-playbook.md
  type: issue
- path: project/specs/12-yoda-structure.md
  type: issue

## Implementation notes
- Keep the exception scoped to the meta-implementation.

## Tests
Not applicable.

## Risks and edge cases
- Agents may write logs in the wrong format if the exception is not explicit.

## Result log
