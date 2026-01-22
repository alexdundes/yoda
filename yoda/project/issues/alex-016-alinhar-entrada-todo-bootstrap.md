# alex-016 - Alinhar entrada do agente com TODO no bootstrap

## Summary
Clarify in the specs how agent entry should resolve TODO sources during bootstrap (Markdown) vs the future YAML format.

## Context
The entry flow in project/specs/07-agent-entry-and-root-file.md points to TODO.<dev>.yaml, while the bootstrap structure uses TODO.<dev>.md. The specs should explicitly define the conditional behavior.

## Objective
Update the specs to state how agent entry resolves TODO files in bootstrap mode and when to switch to YAML.

## Scope
- Define the bootstrap fallback behavior for TODO.<dev>.md.
- Keep the canonical rule for TODO.<dev>.yaml as the future framework default.
- Align related specs that describe entry flow and structure.

## Out of scope
- Implementing scripts or tooling.
- Changing the underlying YODA Flow steps.

## Requirements
- Entry flow documents the conditional behavior for bootstrap vs YAML.
- Structure spec reflects the canonical TODO format and the bootstrap exception.

## Acceptance criteria
- [ ] project/specs/07-agent-entry-and-root-file.md documents TODO.<dev>.md fallback in bootstrap.
- [ ] project/specs/12-yoda-structure.md stays consistent with the entry flow.

## Dependencies
None

## Entry points
- path: project/specs/07-agent-entry-and-root-file.md
  type: issue
- path: project/specs/12-yoda-structure.md
  type: issue

## Implementation notes
- Keep the framework default (YAML) as the canonical target.

## Tests
Not applicable.

## Risks and edge cases
- Agents may diverge if the bootstrap rule is not explicit.

## Result log
