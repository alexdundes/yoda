# Scripts and automation

## Objective

Standardize deterministic operations and reduce manual metadata drift.

## Location and language

- Folder: `yoda/scripts/`
- Language: Python
- File name equals command name.

## Core scripts in 0.4.0

- `issue_add.py`: create issue artifacts.
- `yoda_intake.py`: intake orchestration.
- `get_extern_issue.py`: fetch external issue JSON.
- `todo_list.py`: list/filter the Markdown issue index.
- `todo_next.py`: report the next selectable issue for inspection.
- `todo_update.py`: permanent metadata correction/update tool.
- `log_add.py`: permanent one-line contextual log tool (outside flow).
- `yoda_flow_next.py`: deterministic flow progression driver.
- `yoda_prep_flow.py`: explicit Study/Document preparation for one issue.
- `init.py`: initialize/reconcile embedded YODA data.
- `update.py`: check/apply embedded package updates.

## Flow ownership and helpers

- `yoda_flow_next.py` is the canonical Flow driver.
- `todo_next.py` and `todo_list.py` inspect the Markdown index but do not drive
  phase transitions.

## Logging policy

- Logs MUST be compact single-line entries.
- Flow and helper scripts MUST emit concise, deterministic logs.
- `log_add.py` remains available for work performed outside YODA Flow while still related to an issue.

## Write validation

Scripts that mutate metadata MUST validate:

- filename-derived issue ID format
- status enum validity
- `pending_reason` required when `status=pending`
- timestamps format validity
- schema compatibility before mutation

## Markdown-index read validation

- Schema 2.00 and 2.01 are accepted only when their metadata passes current
  validation.
- `created_at` and `updated_at` require ISO 8601 with an explicit timezone.
- `pending` requires a non-empty `pending_reason`.
- `flow_prepared_until` accepts only `study` or `document`.
- By explicit yoda-0049 decisions, `phase` outside `doing` is ignored and a
  missing dependency target is treated as resolved.
- Index loading is fail-fast: one invalid issue prevents `todo_list.py`,
  `todo_next.py`, and `yoda_flow_next.py` from operating for that developer.
- Remediation: set a missing pending reason with `todo_update.py --status
  pending --pending-reason <reason>`; repair invalid timestamps in issue front
  matter to ISO 8601 with offset before rerunning the index command.

## Versioning and migrations

- Historical context: 0.3.0 introduced the breaking Markdown-first model.
- The optional `flow_prepared_until` field is a backward-compatible minor
  layout change in schema 2.01. The same rollout also begins enforcing
  pre-existing normative timestamp and pending-reason rules that older readers
  tolerated.
- Readers accept conforming 2.00/2.01 data during rollout; front-matter writers
  persist 2.01. `init.py` bumps compatible schema versions but does not invent a
  missing pending reason or repair invalid timestamps.
- `update.py --apply` keeps backup behavior and runs `init.py` when `--dev` is
  available.
- `--check` and `--apply` belong to `update.py`, not `init.py`.

## Principles

- Scripts are mandatory for metadata changes when available.
- Human/agent should avoid direct manual metadata mutation when script coverage exists.
