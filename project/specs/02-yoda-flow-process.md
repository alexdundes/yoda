# YODA Flow (process)

## Base cycle

YODA Flow is the standard deterministic cycle:

1) study
2) document
3) implement
4) evaluate

## Flow driver

- `yoda_flow_next.py` is the flow entry and progression driver.
- The command is implicit (no subcommands).
- Each execution resolves only the next deterministic step.

## Phase transitions

- `to-do -> doing` starts the cycle with `phase=study`.
- While `status=doing`, phase advances one step per execution:
  - `study -> document -> implement -> evaluate`
- Completion after `evaluate` transitions to `done` and removes `phase`.
- `pending` requires `pending_reason` and hides `phase`.

## Blocking policy

- On blockers, `yoda_flow_next.py` MUST NOT mutate metadata.
- It MUST return a deterministic blocked response and instruct `todo_update.py`.

## Deliverables per phase

| Phase | Deliverable |
|---|---|
| study | clarified scope, open decisions, and next deterministic action |
| document | issue text approved and unambiguous |
| implement | changes aligned with issue contract |
| evaluate | acceptance validated and result log completed |

## Output contract for yoda_flow_next.py

Both `md` and `json` outputs MUST include:

- `issue_path`
- `status`
- `phase` (when applicable)
- `next_step`
- `blocked_reason` (when blocked)
- `runbook_line`

`runbook_line` MUST be compact (single line).
