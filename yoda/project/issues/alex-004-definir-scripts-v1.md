# alex-004 - Definir comandos e scripts v1 (especificacao)

## Summary
Define the v1 script interface for YODA: names, purpose, and expected behavior for each command.

## Context
The specs require scripts to manage TODO.dev.yaml, logs, and initialization. We need a concrete list of v1 commands and their responsibilities to guide future implementation.

## Objective
Document the v1 script interface: required commands, inputs, outputs, and the minimal behavior expected from each.

## Scope
- Define the mandatory scripts and their roles.
- Describe expected inputs/outputs at a high level.
- Keep it language-agnostic but aligned with Python naming.

## Out of scope
- Implementing scripts.
- Wiring to MCP or other tooling.

## Requirements
- Include init.py and TODO maintenance commands.
- Include pending resolution command.
- Include log command(s).
- Match the specs under project/specs.

## Acceptance criteria
- [ ] Script list is complete and consistent with specs.
- [ ] Each script has a clear, minimal description of behavior.

## Dependencies
- alex-001

## Entry points
- path: project/specs/05-scripts-and-automation.md
  type: issue
- path: project/specs/04-todo-dev-yaml-issues.md
  type: issue
- path: project/specs/06-agent-playbook.md
  type: issue

## Implementation notes
- Keep naming consistent with file name = command.
- Prefer simple CLI-style interfaces.

## Tests
Not applicable.

## Risks and edge cases
- Undefined interfaces may block implementation later.

## Result log
Created project/specs/13-yoda-scripts-v1.md with the v1 script interface and expected behavior.

Commit:
docs(yoda): specify scripts v1 interface

Issue: alex-004
Path: yoda/project/issues/alex-004-definir-scripts-v1.md
