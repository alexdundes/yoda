# Scripts and automation

## Objective

Standardize deterministic operations and reduce manual metadata drift.

## Location and language

- Folder: `yoda/scripts/`
- Language: Python
- File name equals command name.

## Core scripts in 0.3.0

- `issue_add.py`: create issue artifacts.
- `yoda_intake.py`: intake orchestration.
- `get_extern_issue.py`: fetch external issue JSON.
- `todo_list.py`: compatibility/backlog listing.
- `todo_update.py`: permanent metadata correction/update tool.
- `log_add.py`: permanent one-line contextual log tool (outside flow).
- `yoda_flow_next.py`: deterministic flow progression driver.

## Deprecated/removed script

- `todo_next.py` is removed from 0.3.0 flow contract.

## Logging policy

- Logs MUST be compact single-line entries.
- Flow and helper scripts MUST emit concise, deterministic logs.
- `log_add.py` remains available for work performed outside YODA Flow while still related to an issue.

## Validation baseline

Scripts that mutate metadata MUST validate:

- filename-derived issue ID format
- status enum validity
- `phase` only when `status=doing`
- `pending_reason` required when `status=pending`
- `depends_on` references valid issue IDs
- timestamps format validity

## Versioning and migrations

- 0.3.0 introduces breaking model updates.
- Legacy update flow keeps backup behavior.
- `--check` and `--apply` are defined on updated `init.py` after update completion.

## Principles

- Scripts are mandatory for metadata changes when available.
- Human/agent should avoid direct manual metadata mutation when script coverage exists.
