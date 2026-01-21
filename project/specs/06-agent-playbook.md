# Agent playbook

## Objective

Define how the AI should act in the YODA Framework at each stage of the flow.

## Phases

### Study

- Ask questions and understand context.
- Do not generate code or edit files.
- Produce summaries when requested.

### Document

- Create or update the issue Markdown file.
- Generate a skeleton via script, if available.
- Prioritize clarity, scope, and criteria.

### Implement

- Read the issue Markdown file and existing code.
- Implement only what is documented.
- Use scripts to create structure when needed.

### Evaluate

- Receive human feedback.
- Fix code and update the issue Markdown file.
- Suggest a commit message at the end.
- Include the commit text in the issue and show it on screen.
- Commit format must be:
- First line: conventional commit message.
- Body:
  - Issue: <ID>
  - Path: <issue path>
- Record the cycle log at yoda/logs/dev-id-slug.yaml.
- If a blocker arises, mark status as pending and record the reason in TODO.dev.yaml; use the pending resolution script when unblocked.

## General rules

- Always keep the issue (Markdown file) as the source of truth.
- Never edit TODO.dev.yaml directly.
- Prefer questions when there is ambiguity.
