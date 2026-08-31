# YODA Intake (cycle)

## Objective

Define the YODA Intake cycle, the discovery/triage loop that turns human demands into ready-to-execute issues.

## Positioning

- **YODA Intake** is backlog-centric: it shapes and prepares issues.
- **YODA Flow** is issue-centric: it executes a ready issue.
- Intake precedes Flow and hands off issues to Flow explicitly.
- When the agent enters YODA Intake, it assumes the **Intake skin**.

## Entry trigger

The human signals intent to create one or more issues, or explicitly says “YODA Intake”.

Examples (translate to the human's language if needed):
- “I want to create an issue.”
- “I want to create several issues.”
- “Enter YODA Intake.”

## Cycle steps

1) **Start via script**
   - Call `yoda_intake.py --dev <developer-slug>` when entering Intake.
   - Follow the returned initial runbook to decide:
     - external issue path (`--extern-issue <NNN>`)
     - no external issue path (`--no-extern-issue`)
2) **Collect**
   - Ask the human for a free-form description (plain text) of the issue or demand.
   - Gather goals, constraints, and context from that same free-form input.
3) **Triage**
   - Use `todo_list.py` to review the backlog and avoid duplicates.
   - Identify conflicts, dependencies, or candidates for merge/split.
4) **Shape**
   - Translate the free-form input into structured issue content.
   - Decompose into well-sized issues (epic vs tasks).
   - Define scope, out of scope, acceptance criteria, and risks.
   - Apply the priority policy below; do not rank a batch or encode its planned
     sequence with priority values.
5) **Definition of Ready (DoR)**
   - Ensure each issue meets the minimal readiness criteria (see below).
6) **Create**
   - Use `issue_add.py` to create markdown issues.
   - Fill/update the issue Markdown from the same structured translation generated from the human free-form input.
   - Remove placeholders and complete sections.
7) **Handoff**
   - Explicitly close Intake and propose the next YODA Flow issue.

## Natural order, dependencies, and priority

Natural order is determined by the execution model:

1. Resume the current `doing` issue before starting another issue.
2. Defer an issue while any real dependency is unresolved.
3. Among the remaining issues at baseline `priority: 5`, use stable issue ID
   order.

`depends_on` expresses real precedence: an issue cannot be executed correctly
before its dependency is complete. It must not be created merely to arrange the
backlog. `priority` expresses a deliberate exception for work that could follow
natural order but has a concrete reason to run earlier or later. The two fields
must not substitute for each other.

Intake rules:

- Keep `priority: 5` by default. Omitting `--priority` in `issue_add.py` is the
  normal creation path.
- Do not rank issues in a batch or use priority as an ordinal plan.
- Create batch issues in the desired natural order. Add `depends_on` only for
  real precedence.
- Values above `5` move an issue before natural order; values below `5` move it
  after natural order. Both are exceptions and require a relative reason in the
  issue Markdown explaining why natural order is unsuitable.
- An explicit human request to advance or postpone work is a valid reason. A
  generic statement that work is important is not.

Valid exception example:

> Raise the priority so this issue precedes the available backlog because each
> additional capture continues losing data required for recovery.

Invalid exception example:

> This issue is very important to the project.

External source path (when `--extern-issue <NNN>` is used):
- Ask the human to run `get_extern_issue.py --dev <developer-slug> --extern-issue <NNN>`.
- `get_extern_issue.py` stores source data at `yoda/project/extern_issues/<provider>-<NNN>.json`.
- Re-run `yoda_intake.py --dev <developer-slug> --extern-issue <NNN>` to continue with local source file.
- Associate commits with external issue using `#NNN` only; do not auto-close external issues.

External log usage (from `extern_issues/<provider>-<NNN>.json`):
- Treat `log` as auxiliary context for Intake decisions, not as the single source of truth.
- Use `log` events to detect recency and state changes (for example: reopened, closed, referenced commits, project moves).
- Use these signals to refine triage. Change priority only when a signal provides
  a relative reason to depart from natural order, such as continuing data loss
  or an explicit request to postpone reopened work.
- Keep issue shaping anchored in human intent and external issue description;
  use `log` to refine scope and identify justified ordering exceptions.
- When relevant, reference meaningful `log` events in the Intake rationale for traceability.

## Definition of Ready (DoR)

Each issue must include at minimum:
- Clear title and short summary.
- Context and objective.
- Scope and out-of-scope.
- Acceptance criteria (testable).
- Dependencies and risks.
- Priority set to baseline `5`, or a relative justification recorded in the
  issue Markdown when different from `5`.

## Agent rules (Intake)

- Do not create issues without passing the DoR gate.
- Enter Intake through `yoda_intake.py` and follow the returned runbook.
- Always consult `todo_list.py` before proposing new issues.
- Keep the cycle explicit: enter Intake, exit Intake, then offer YODA Flow.
- Use clear, analyst-style language.
- Keep priority `5` by default. Do not rank a batch or encode planned sequence
  with priority. When using another value, record why this issue must run before
  or after the natural order.
- The agent is responsible for converting free-form human input into structured issue fields and Markdown updates.

## Outputs

- One or more markdown issues created in `yoda/project/issues/`.
- Updated issue Markdown files derived from the same structured Intake translation (placeholders resolved).
- Backlog reviewed and coherent.

## Exit criteria

- Issues are ready for YODA Flow.
- Agent states that Intake is complete and proposes the next issue to execute.
