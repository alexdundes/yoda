# alex-003 - Estrutura minima do YODA Framework

## Summary
Define and document the minimum folder and file structure for a YODA Framework project.

## Context
The specs define core folders (yoda/, yoda/templates/, yoda/scripts/, yoda/logs/, yoda/project/issues/). We need a clear, consolidated structure description so future scripts and agents know what to create and where.

## Objective
Produce a clear description of the minimum structure, including required paths and their purpose.

## Scope
- Document required folders and files.
- Include the meta-implementation exceptions (logs in Markdown).
- Align with existing specs and current repository layout.

## Out of scope
- Implementing scripts or generators.
- Changing existing structure in the repo.

## Requirements
- Provide a tree-like structure of required paths.
- Describe the purpose of each path.
- Include yoda/yoda.md as root agent file.

## Acceptance criteria
- [ ] Structure is documented and consistent with specs.
- [ ] Paths are explicit and unambiguous.

## Dependencies
- alex-001

## Entry points
- path: project/specs/01-yoda-overview.md
  type: issue
- path: project/specs/05-scripts-and-automation.md
  type: issue
- path: project/specs/06-agent-playbook.md
  type: issue
- path: yoda/yoda.md
  type: issue

## Implementation notes
- Keep the structure minimal and practical.
- Use ASCII-only text.

## Tests
Not applicable.

## Risks and edge cases
- Inconsistent structure may break future scripts.

## Result log
Created project/specs/12-yoda-structure.md with the minimum folder and file structure and path purposes.

Commit:
docs(yoda): document minimum project structure

Issue: alex-003
Path: yoda/project/issues/alex-003-estrutura-minima-yoda-framework.md
