# YODA scripts specification

## Global CLI contract

All scripts follow shared flags:

- `--dev`
- `--format md|json`
- `--json`
- `--dry-run`
- `--verbose`

Developer slug contract:
- `--dev` is the single source of developer slug for YODA commands.
- Missing `--dev` MUST return guidance instructing the agent to ask the human for the slug.
- Exception: `update.py` may run without `--dev`.

Help guidance contract:
- `--help` MUST include direct operator guidance/runbook text with:
  - purpose
  - when to use
  - whether the command mutates state

## Exit codes

- `0`: success
- `1`: general error
- `2`: validation error
- `3`: not found
- `4`: conflict

## Script set (0.3.0)

- `issue_add.py`
- `yoda_intake.py`
- `get_extern_issue.py`
- `todo_list.py`
- `todo_update.py` (permanent)
- `log_add.py` (permanent)
- `yoda_flow_next.py`

## Removed from flow contract

- `todo_next.py`

## yoda_flow_next.py

- implicit command model
- resolves only the next deterministic step
- supports optional `--log-message "<summary>"` to append a compact action summary to the transition log line
- outputs `issue_path`, `status`, `phase` (if applicable), `next_step`, `blocked_reason` (if blocked), `runbook_line`
- `runbook_line` is mandatory in `md` and `json`
- on block, no mutation; instruct `todo_update.py`

## todo_update.py

- permanent semantic/metadata adjustment tool
- supports `phase` updates when valid
- logs are one-line, concise
- `--help` and empty invocation should provide direct operator guidance

## log_add.py

- permanent tool for issue logging outside normal flow progression
- log message must be one-line and concise
- `--help` and empty invocation should provide direct operator guidance
