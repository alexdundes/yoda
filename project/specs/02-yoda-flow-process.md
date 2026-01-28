# YODA Flow (process)

## Base cycle

YODA Flow is the standard work cycle of the framework:

1) Study
2) Document
3) Implement
4) Evaluate

## Step details

### 1) Study

- Open conversation between human and AI.
- Focus on understanding context, rules, and constraints.
- No repository artifacts are produced in this step.
- Deliverable is the conversation summary plus pending questions/decisions.
- At the end, the AI is ready to document an issue (Markdown file).

### 2) Document

- The AI creates or updates the issue Markdown file based on what was discussed.
- The human reviews and corrects the text to remove ambiguity.
- The issue (Markdown file) becomes the official contract for implementation.

### 3) Implement

- The AI implements only what is defined in the issue Markdown file.
- If something changes, return to the Document step and update the issue Markdown file.

### 4) Evaluate

- The human validates the result.
- The AI fixes code and documentation based on feedback.
- At the end, the issue receives a summary of what was done and a suggested commit message.

## Notes

- The cycle is designed to be iterative and not waterfall.
  - Next issue selection must follow deterministic rules defined in specs (priority, order, pending, dependencies, and no issue in `doing`).
- YODA Flow is issue-centric and starts only after issues are ready (see YODA Intake for the discovery/triage cycle).
- - Lightweight process: it does not include the Study step; the AI follows the preliminary issue directly.
  - Use lightweight only when the issue is already clear, has explicit acceptance criteria, and no open questions remain.
  - If there is ambiguity, new requirements, or non-trivial risk, include Study.
  - Lightweight must be explicitly marked in the issue or TODO (example: lightweight: true).

## Deliverables per phase

| Phase     | Deliverables |
|-----------|--------------|
| Study     | Chat summary in developer language; questions and pending decisions list; explicit human confirmation to proceed. |
| Document  | Issue Markdown updated with Study details; human confirmation that the issue text is OK. |
| Implement | Changes match the issue; tests updated or marked not applicable; acceptance criteria checked when satisfied. |
| Evaluate  | Result log updated; commit suggestion written (required format); TODO status updated; log entry recorded. |

## Study requirements

- The agent must summarize the issue in developer language.
- If the issue is incomplete, the agent must ask for missing information.
- If the issue exists, the agent must ask about remaining decisions until none remain.
- The agent must wait for an explicit human instruction before moving to the next step.

## Document requirements

- The agent must update the issue file with all Study outcomes.
- The agent must ask the human to approve the issue text.
- If the human rejects the text, return to Study.

## Implement requirements

- Implement only what the issue specifies.
- If tests are required, they must be implemented.
- If the project expects unit tests, they must be added.
- Acceptance criteria checkboxes must be marked when satisfied.

## Lightweight rule

- Lightweight must be explicit in the issue or TODO (example: lightweight: true).
- When lightweight is true and the issue is sufficient, Study and Document may be skipped.
- If the issue is not sufficient, return to Study and Document.
