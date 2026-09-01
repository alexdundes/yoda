# YODA Agent Playbook (Embedded)

Primary operational guide for AGENT when YODA is embedded in a project package.

## Core rule

Use script runbooks as the source of truth for operational details.
- This file defines policy and flow boundaries.
- Scripts define step-by-step execution details.
- If there is a conflict, follow script output.

## Entry order

1. Read the YODA-local agent entry file when present (`yoda/AGENTS.md`, `yoda/GEMINI.md`, or `yoda/CLAUDE.md`).
2. Read this file (`yoda/yoda.md`).
3. Resolve developer slug from `--dev`; if missing, ask human and rerun with
   `--dev <developer-slug>`.

## Developer slug

- Required by YODA scripts.
- Stable namespace used as the issue ID prefix (`mynick` -> `mynick-0001`).
- Format: lowercase ASCII letters, digits, and hyphens; must start with a letter.
- Valid examples: `mynick`, `fernando`, `time-backend`.
- Invalid examples: `MeuNick`, `123fernando`, `fernando_silva`.
- `<developer-slug>` is a placeholder to replace; do not type the angle brackets.
- Reuse the same developer slug in later YODA commands.

## Source of truth

- Agent entry files: `yoda/AGENTS.md`, `yoda/GEMINI.md`, `yoda/CLAUDE.md`
- Issues markdown: `yoda/project/issues/<id>-<slug>.md`
- Dependencies: front matter `depends_on`
- Flow execution log: section `## Flow log` inside each issue markdown, use `log_add.py --help`

## YODA modes

- `YODA Flow`: execute one issue through phases.
- `YODA Prep Flow`: prepare Study/Document for one issue without implementation.
- `YODA Intake`: create/refine backlog issues.

Do not mix modes implicitly. Enter and exit each mode explicitly.

## YODA Flow

for know runbook: read `python3 yoda/scripts/yoda_flow_next.py --help` 

Entry:
1. Confirm the human intent includes entering YODA Flow.
2. Run `python3 yoda/scripts/yoda_flow_next.py --dev <developer-slug>`.
3. Present the returned runbook to the human, then execute that phase only.

Execution phases:
1. Study
2. Document
3. Implement
4. Evaluate

Phase boundary — run every phase in this order:
1. Wait for the human to authorize the next phase.
2. Run `yoda_flow_next.py` to enter it. Do this BEFORE doing the work.
3. Present the returned runbook to the human.
4. Execute only the work of that phase.
5. Present the phase deliverable and stop.

Flow policy:
- One step is one phase per human interaction, not one phase per command call.
  Never chain phases inside a single interaction.
- Never apply a transition to stamp work already finished. The transition starts
  the phase; it does not record it.
- Never discard, silence, or redirect the output of a YODA command. Do not send
  it to `/dev/null` and do not hide it behind command chaining. The runbook is
  your instruction for the phase, and the human must see it.
- Treat a generic "go ahead" as authorization for the next boundary only. Ask
  again after presenting each deliverable.
- Implement only approved issue scope.
- In `Evaluate`, validate acceptance criteria and fill `## Result log` in the issue markdown.
- Use `todo_update.py --help` for manual semantic/process corrections.
- Use `log_add.py --help` only for issue context outside the normal YODA Flow path.

Phase deliverables — present these before asking to continue:
- `Study`: findings, constraints, and the open decisions the human must settle.
- `Document`: the updated issue with approved decisions and a closed contract.
- `Implement`: the code and artifacts of the approved scope, with the
  verifications you ran.
- `Evaluate`: acceptance criteria checked, remaining findings, and the
  `## Result log` filled in when approved.

Close timestamps in `## Flow log` may indicate chaining and justify review, but
a short phase is not by itself a violation.

Evaluate `Result log` official format:
- `<First line: conventional commit message.>`
- blank line
- `<descricao do que foi feito>`
- blank line
- `- **<GitLab|GitHub> Issue** :   #NNN` (only when `extern_issue_file` exists)
- blank line
- `- **Issue**: \`<ID>\``
- blank line
- `- **Path**: \`<issue path>\``

External issue line rule:
- Emit the line only when the issue front matter contains `extern_issue_file`.
- Derive provider and number from `extern_issue_file` (for example, `../extern_issues/github-2.json` => `GitHub` and `#2`).
- Omit the line when no external association exists.

## YODA Prep Flow

Use YODA Prep Flow only when the human explicitly wants to prepare an issue's
Study/Document work without entering implementation.

Before using it, read the script runbook:
```bash
python3 yoda/scripts/yoda_prep_flow.py --help
```

Entry:
1. Confirm the human intent includes entering YODA Prep Flow.
2. Run `python3 yoda/scripts/yoda_prep_flow.py --dev <developer-slug> --issue <id>`.
3. Follow the returned runbook for the selected prep step.

Prep policy:
- YODA Prep Flow works on the explicit `--issue`; it does not select by backlog order.
- It is allowed to prepare documentation independent of dependencies, but it does not authorize implementation.
- When prep reaches Document, the issue remains `to-do` and YODA Flow later starts it at Implement.

## YODA Intake

Entry:
1. Confirm the human intent includes entering YODA Intake.
2. Run:
```bash
python3 yoda/scripts/yoda_intake.py --dev <developer-slug>
```
3. Follow the returned runbook exactly.

External source path:
1. If the runbook indicates external issue intake, run:
```bash
python3 yoda/scripts/get_extern_issue.py --dev <developer-slug> --extern-issue <NNN>
```
2. On success, present the reported transport and the saved file path to the
   human. The transport is `authenticated-cli` or `public-http`, and it tells
   the human whether their authenticated CLI session was used: the collector
   prefers that session whenever it is available, and only falls back to
   unauthenticated HTTP for public `github.com` issues. Private repositories,
   GitHub Enterprise, and GitLab always need the authenticated CLI. The stored
   external issue JSON is the same either way.
3. On any failure, present the returned error and hand execution to the human,
   offering the same command to run locally. Do not work around the failure by
   another route and do not try to determine repository visibility beforehand.
   The human may also run the command themselves at any point.
4. After the JSON file is created in `yoda/project/extern_issues/`, run:
```bash
python3 yoda/scripts/yoda_intake.py --dev <developer-slug> --extern-issue <NNN>
```
5. Follow the returned runbook and use the referenced JSON file as the external source.

No external source path:
```bash
python3 yoda/scripts/yoda_intake.py --dev <developer-slug> --no-extern-issue
```

Intake policy:
- Review current backlog before adding new issues.
- Translate human free text into structured issue content.
- Keep `priority: 5` by default; omitting `--priority` is the normal path.
- Do not rank issues in a batch or use priority to encode planned sequence.
- Natural order resumes the current `doing` issue, defers unresolved real
  dependencies, then follows stable issue ID order. Create batch issues in that
  desired natural order.
- Use `depends_on` only when one issue cannot be executed correctly before
  another. Do not create artificial dependencies to organize the backlog.
- Change priority only as a justified exception: above `5` runs before and below
  `5` runs after natural order. Record the relative reason in the issue Markdown;
  generic importance is insufficient.
- Keep `extern_issue_file` traceability when external source exists.
- Before creating issues, run `python3 yoda/scripts/issue_add.py --help` and follow its runbook.

## Script authority map

- `yoda_flow_next.py`: deterministic next-step selection + flow transition/runbook.
- `yoda_prep_flow.py`: explicit issue Study/Document preparation without implementation.
- `todo_update.py`: manual status/phase/metadata corrections.
- `log_add.py`: compact one-line issue log outside normal flow path.
- `todo_next.py`: inspect the issue that would be resumed/selected; no transition.
- `todo_list.py`: ordered backlog view for inspection/filtering, not an execution plan.
- `issue_add.py`: issue creation contract and required fields.
- `yoda_intake.py`: Intake decision and AGENT runbook output.
- `get_extern_issue.py`: fetch/store external issue JSON.

## Compatibility notes

- Default YODA Flow path: `yoda_flow_next.py`.
- `todo_list.py` displays a backlog view, `todo_next.py` inspects the next
  selection, and `yoda_flow_next.py` owns selection and phase transitions.
- `todo_update.py` and `log_add.py` are auxiliary commands for manual adjustments outside the default automated flow step.

## Key paths

- Manual: `yoda/yoda.md`
- Issues: `yoda/project/issues/<id>-<slug>.md`
- External issues: `yoda/project/extern_issues/<provider>-<NNN>.json`
- Scripts: `yoda/scripts/*.py`

## Exit and handoff

- On Intake completion, propose starting YODA Flow.
- On Flow completion, offer next selectable issue or explicit exit.
