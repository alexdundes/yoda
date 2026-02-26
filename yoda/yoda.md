# YODA Agent Playbook (Embedded)

Primary operational guide for AGENT when YODA is embedded in a project package.

## Core rule

Use script runbooks as the source of truth for operational details.
- This file defines policy and flow boundaries.
- Scripts define step-by-step execution details.
- If there is a conflict, follow script output.

## Entry order

1. Read `REPO_INTENT.md`.
2. Read this file (`yoda/yoda.md`).
3. Resolve developer slug (`--dev` > `YODA_DEV` > ask human).

## Developer slug

- Required by all YODA scripts.
- Format: lowercase ASCII, digits, hyphens; must start with a letter.
- Data path pattern: `yoda/todos/TODO.<dev>.yaml`.

## YODA modes

- `YODA Flow`: execute a selected issue.
- `YODA Intake`: create/refine backlog issues.

Do not mix modes implicitly. Enter and exit each mode explicitly.

## YODA Flow

Entry:
1. Confirm the human intent includes entering YODA Flow.
2. Run `python3 yoda/scripts/todo_next.py --dev <slug>`.
3. Confirm the selected issue with the human.
4. Set `doing` via `todo_update.py`.

Execution phases:
1. Study
2. Document
3. Implement
4. Evaluate

Flow policy:
- Implement only approved issue scope.
- Use scripts to update metadata (do not hand-edit TODO YAML).
- If blocked, set `pending` with explicit reason.
- In Evaluate, validate acceptance criteria, append log (`log_add.py`), and close with `todo_update.py --status done`.

## YODA Intake

Entry:
1. Confirm the human intent includes entering YODA Intake.
2. Run:
```bash
python3 yoda/scripts/yoda_intake.py --dev <slug>
```
3. Follow the returned runbook exactly.

External source path:
1. If the runbook indicates external issue intake, ask the human to run:
```bash
python3 yoda/scripts/get_extern_issue.py --dev <slug> --extern-issue <NNN>
```
2. After the JSON file is created in `yoda/project/extern-issues/`, run:
```bash
python3 yoda/scripts/yoda_intake.py --dev <slug> --extern-issue <NNN>
```
3. Follow the returned runbook and use the referenced JSON file as the external source.

No external source path:
```bash
python3 yoda/scripts/yoda_intake.py --dev <slug> --no-extern-issue
```

Intake policy:
- Review current backlog before adding new issues.
- Translate human free text into structured issue content.
- Priority baseline is `5`; change only with explicit relative justification against open issues.
- Keep `origin` traceability when external source exists.
- Before creating issues, run `python3 yoda/scripts/issue_add.py --help` and follow its runbook.

## Script authority map

- `yoda_intake.py`: Intake decision and AGENT runbook output.
- `get_extern_issue.py`: fetch/store external issue JSON (human-run command).
- `issue_add.py`: issue creation contract and required fields.
- `todo_next.py`: next selectable issue.
- `todo_list.py`: backlog inspection and duplicate checks.
- `todo_update.py`: status/priority/dependency transitions.
- `log_add.py`: issue log append.

## Key paths

- Manual: `yoda/yoda.md`
- TODO: `yoda/todos/TODO.<dev>.yaml`
- Issues: `yoda/project/issues/<id>-<slug>.md`
- Logs: `yoda/logs/<id>-<slug>.yaml`
- External issues: `yoda/project/extern-issues/<provider>-<NNN>.json`
- Scripts: `yoda/scripts/*.py`

## Exit and handoff

- On Intake completion, propose starting YODA Flow.
- On Flow completion, offer next selectable issue or explicit exit.
