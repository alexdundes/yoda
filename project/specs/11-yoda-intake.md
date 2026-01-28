# YODA Intake (cycle)

## Objective

Define the YODA Intake cycle, the discovery/triage loop that turns human demands into ready-to-execute issues.

## Positioning

- **YODA Intake** is backlog-centric: it shapes and prepares issues.
- **YODA Flow** is issue-centric: it executes a ready issue.
- Intake precedes Flow and hands off issues to Flow explicitly.

## Entry trigger

The human signals intent to create one or more issues, or explicitly says “YODA Intake”.

Examples (translate to the human's language if needed):
- “I want to create an issue.”
- “I want to create several issues.”
- “Enter YODA Intake.”

## Cycle steps

1) **Collect**
   - Gather the initial request, goals, constraints, and context.
2) **Triage**
   - Use `todo_list.py` to review the backlog and avoid duplicates.
   - Identify conflicts, dependencies, or candidates for merge/split.
3) **Shape**
   - Decompose into well-sized issues (epic vs tasks).
   - Define scope, out of scope, acceptance criteria, and risks.
4) **Definition of Ready (DoR)**
   - Ensure each issue meets the minimal readiness criteria (see below).
5) **Create**
   - Use `issue_add.py` to create issues and add them to the TODO.
   - Edit the issue Markdown to remove placeholders and complete sections.
6) **Order**
   - Review ordering; optionally use `todo_reorder.py`.
7) **Handoff**
   - Explicitly close Intake and propose the next YODA Flow issue.

## Definition of Ready (DoR)

Each issue must include at minimum:
- Clear title and short summary.
- Context and objective.
- Scope and out-of-scope.
- Acceptance criteria (testable).
- Dependencies and risks.

## Agent rules (Intake)

- Do not create issues without passing the DoR gate.
- Always consult `todo_list.py` before proposing new issues.
- Keep the cycle explicit: enter Intake, exit Intake, then offer YODA Flow.
- Use clear, analyst-style language.

## Outputs

- One or more issues created and added to `TODO.<dev>.yaml`.
- Updated issue Markdown files (placeholders resolved).
- Backlog order reviewed and coherent.

## Exit criteria

- Issues are ready for YODA Flow.
- Agent states that Intake is complete and proposes the next issue to execute.
