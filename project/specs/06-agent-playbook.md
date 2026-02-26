# Agent playbook

## Objective

Define how the AI acts in the YODA Framework at each stage of the flow.

## Entry and selection (script-backed)

When the human signals intent to start YODA Flow (example phrases: "Let's do YODA Flow", "YODA Flow, here we go", "YODA Flow, next issue"), the agent assumes the **Flow skin** and must:

1) Resolve developer slug (flag, env, or ask).
2) Call `todo_next.py` to select the next issue.
3) If `todo_next.py` returns conflict (any `doing` issues), stop and ask the human to resolve/close the `doing` issue.
4) Always surface pending hints (if any). If `todo_next.py` returns not found, also surface blocked hints and ask the human what to do next.
5) If a selectable issue is returned, ask for confirmation: “Start YODA Flow for issue dev-0001?” (translate to the human's language if needed).
6) If approved, set status to `doing` with `todo_update.py` and enter Study.

## Phases

Deliverables per phase are defined in `project/specs/02-yoda-flow-process.md` and must be followed.

### Study

- Ask questions and understand context.
- Do not generate code or edit files.
- Produce summaries when requested.
- Deliverable: summary in developer language, plus pending questions/decisions.
- Wait for explicit human instruction before moving to the next step.
- If the human requests `pending`, set status to pending via `todo_update.py` and record the pending reason; then pause the flow.
- If Study discovers dependencies, update `depends_on` (and priority if needed) via `todo_update.py`, set status back to `to-do`, and end the cycle.

### Document

- Create or update the issue Markdown file.
- Prioritize clarity, scope, and criteria.
- Deliverable: issue updated with Study details and acceptance criteria checkboxes.
- Ask the human to approve the issue text; if rejected, return to Study.
- Log key decisions and issue edits with `log_add.py`.

### Implement

- Read the issue Markdown file and existing code.
- Implement only what is documented.
- Deliverable: code changes and tests updated (or marked not applicable).
- Mark acceptance criteria checkboxes when satisfied.
- If new decisions arise outside the spec/issue, log them with `log_add.py`.

### Evaluate

- Receive human feedback.
- Fix code and update the issue Markdown file.
- Suggest a commit message at the end.
- Include the commit text in the issue and show it to the user.
- Commit format must be:
- First line: conventional commit message.
- Body:
  - Issue: `<ID>`
  - Path: `<issue path>`
- Record the cycle log at `yoda/logs/<id>-<slug>.yaml`.
- If a blocker arises, mark status as pending and record the reason in `yoda/todos/TODO.<dev>.yaml`; use the pending resolution script when unblocked.
- Deliverable: result log updated, commit suggestion written, TODO status updated, log entry recorded.
- If the human approves, set status to `done` with `todo_update.py`. If the human rejects, return to Study.
- After completion, call `todo_next.py` and offer to start the next YODA Flow or exit to non-YODA work.

## General rules

- Always keep the issue (Markdown file) as the source of truth.
- Never edit `yoda/todos/TODO.<dev>.yaml` directly.
- Prefer questions when there is ambiguity.
- If the issue is ambiguous, return to Document before coding.
- Do not invent files or paths; verify the repo structure first.
- Any change to `project/specs/` must be tracked by an issue.
- When scripts are available, use them for metadata changes.
- Ensure validation passes before marking issues as done; resolve validation errors first.
- Issue creation (`issue_add.py`) is out of scope for YODA Flow and defined elsewhere.

## YODA Intake (backlog cycle)

When the human signals intent to create issues or explicitly says “YODA Intake”, the agent assumes the **Intake skin** and must:

1) Enter YODA Intake and confirm intent.
2) Run `yoda_intake.py --dev <slug>` and follow the returned AGENT runbook.
3) If the runbook asks for external source:
   - with external issue: ask human to run `get_extern_issue.py --dev <slug> --extern-issue <NNN>`, then run `yoda_intake.py --dev <slug> --extern-issue <NNN>`.
   - without external issue: run `yoda_intake.py --dev <slug> --no-extern-issue`.
4) Consult `todo_list.py` to review existing backlog and avoid duplicates.
5) Ask for a free-form description from the human and collect requirements from this plain-text input.
6) Translate the free-form input into structured issue content until it meets the Definition of Ready (DoR).
7) Create issues via `issue_add.py` and fill/update issue Markdown sections from the same structured translation.
8) Review order (optionally use `todo_reorder.py`) and propose the next YODA Flow issue.
9) Exit Intake explicitly and ask whether to start YODA Flow.

Agent rules for Intake:
- Do not create issues without passing DoR.
- Keep Intake and Flow distinct; Intake prepares issues, Flow executes them.
- In external mode, `get_extern_issue.py` detects provider from `origin` and uses provider-specific CLI (`glab`/`gh`).
- If required CLI is missing, `get_extern_issue.py` should provide actionable install instructions to the human.
- When referencing external issue in commit suggestions, use `#NNN` only (no auto-close keywords).
- Use `priority: 5` as the default baseline for new issues.
- Only assign priority different from `5` when there is explicit comparative importance versus other open issues, and record that rationale in the issue text.
- Treat human free-form text as source input; the agent owns the conversion into structured issue fields and issue Markdown.
