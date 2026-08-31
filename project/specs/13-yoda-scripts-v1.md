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

## Script set (0.4.0)

- `issue_add.py`
- `yoda_intake.py`
- `get_extern_issue.py`
- `todo_list.py`
- `todo_update.py` (permanent)
- `log_add.py` (permanent)
- `yoda_flow_next.py`
- `yoda_prep_flow.py`
- `todo_next.py` (inspection helper)
- `init.py`
- `update.py`

## Flow ownership

- `yoda_flow_next.py` owns deterministic issue selection and phase transitions.
- `yoda_prep_flow.py` owns explicit Study/Document preparation for one issue.
- `todo_next.py` and `todo_list.py` are read/inspection helpers and do not own
  Flow phase transitions.

## yoda_flow_next.py

- implicit command model
- resolves only the next deterministic step
- supports optional `--log-message "<summary>"` to append a compact action summary to the transition log line
- outputs `issue_path`, `status`, `phase` (if applicable), `next_step`, `blocked_reason` (if blocked), `runbook_line`
- `runbook_line` is mandatory in `md` and `json`
- on block, no mutation; instruct `todo_update.py`
- issues prepared through Document start at `doing/implement`

## yoda_prep_flow.py

- requires explicit `--issue`
- ignores backlog order/dependencies for preparation only
- advances one authorized Study/Document step per call
- keeps issue `to-do` and persists `flow_prepared_until`
- never enters Implement or Evaluate

## todo_update.py

- permanent semantic/metadata adjustment tool
- supports `phase` updates when valid
- logs are one-line, concise
- `--help` and empty invocation should provide direct operator guidance

## log_add.py

- permanent tool for issue logging outside normal flow progression
- log message must be one-line and concise
- `--help` and empty invocation should provide direct operator guidance
