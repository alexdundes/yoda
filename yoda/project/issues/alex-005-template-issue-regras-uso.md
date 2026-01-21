# A-005 - Template de issue (regras e uso)

## Summary
Document how agents should create and fill issues using the templates under yoda/templates/.

## Context
We have two templates (standard and lightweight) and a commit format requirement. We need a short guide describing when to use each template, how to fill sections, and how to record results.

## Objective
Create a usage guide for the issue templates that is aligned with the specs and the YODA Flow.

## Scope
- Define when to use standard vs lightweight template.
- Define how to fill required sections.
- Define how to write the commit block in Result log.

## Out of scope
- Script implementation.
- Changes to template files themselves.

## Requirements
- Use clear, operational language.
- Reference yoda/templates paths.
- Include the commit format rules.
- Explain that the add-issue script creates the Markdown from the template using basic fields provided by the agent, then the agent completes the remaining sections.

## Acceptance criteria
- [ ] Usage guide exists and is consistent with specs.
- [ ] Guidance is actionable for agents.

## Dependencies
- A-002

## Entry points
- path: yoda/templates/issue.md
  type: issue
- path: yoda/templates/issue-lightweight-process.md
  type: issue
- path: project/specs/06-agent-playbook.md
  type: issue

## Implementation notes
- Keep it concise and practical.

## Tests
Not applicable.

## Risks and edge cases
- Incorrect use of templates can lead to inconsistent issues.

## Result log
Created yoda/project/specs/issue-templates-usage.md with rules for template selection, script-driven creation, and commit format.

Commit:
docs(yoda): add issue template usage guide

Issue: A-005
Path: yoda/project/issues/alex-005-template-issue-regras-uso.md
