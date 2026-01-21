# alex-002 - Formalizar template de issue (normal e lightweight)

## Summary
Align the issue templates in yoda/templates/ with the current specs and usage rules, ensuring they are ready for agents to use.

## Context
The framework now defines two templates: a standard issue template and a lightweight process template. We need to confirm both match the English specs, include direct agent instructions, and reflect the meta-implementation exception where logs are Markdown. The templates already exist but must be verified against the specs and adjusted if needed.

## Objective
Review, adjust, and finalize the issue templates to match the YODA specs and provide clear instructions to agents.

## Scope
- Review yoda/templates/issue.md and yoda/templates/issue-lightweight-process.md.
- Align wording and required sections with project/specs.
- Ensure templates include direct agent instructions in HTML comments.
- Confirm templates mention commit text requirement in the result section.

## Out of scope
- Implementing scripts to generate issues.
- Creating new templates beyond the two defined.
- Editing TODO metadata beyond this issue.

## Requirements
- Templates must be consistent with project/specs/04-todo-dev-yaml-issues.md.
- Result section must instruct the agent to include the final commit message.
- Lightweight template must be short and direct.
- Keep ASCII-only content.

## Acceptance criteria
- [ ] Both templates are reviewed and updated as needed.
- [ ] Instructions are clear for an agent with zero context.
- [ ] No conflicts with current specs.

## Dependencies
- alex-001

## Entry points
- path: yoda/templates/issue.md
  type: issue
- path: yoda/templates/issue-lightweight-process.md
  type: issue
- path: project/specs/04-todo-dev-yaml-issues.md
  type: issue
- path: project/specs/05-scripts-and-automation.md
  type: issue
- path: project/specs/06-agent-playbook.md
  type: issue

## Implementation notes
- Keep the structure concise and practical for agents.
- Use language consistent with the English specs.

## Tests
Not applicable.

## Risks and edge cases
- If templates diverge from specs, agents may follow inconsistent rules.

## Result log
Updated yoda/templates/issue.md and yoda/templates/issue-lightweight-process.md to align with specs, including explicit commit formatting and test notes. Added the commit format requirement in yoda/yoda.md and specs.

Commit:
docs(templates): standardize commit format instructions

Issue: alex-002
Path: yoda/project/issues/alex-002-template-issue.md
