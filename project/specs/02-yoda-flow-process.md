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
- `to-do + flow_prepared_until=document -> doing/implement` resumes an issue
  already prepared through YODA Prep Flow.
- `to-do + flow_prepared_until=study -> doing/study`: Study is executed again in
  normal YODA Flow because only completed Document authorizes skipping directly
  to Implement.
- While `status=doing`, phase advances one step per execution:
  - `study -> document -> implement -> evaluate`
- Completion after `evaluate` transitions to `done` and removes `phase`.
- `pending` requires `pending_reason` and hides `phase`.

## YODA Prep Flow

YODA Prep Flow is an explicit alternative for preparing one issue through
Study and Document without entering implementation:

- entrypoint: `yoda_prep_flow.py --dev <slug> --issue <id>`
- operates on the explicit issue, independent of backlog order/dependencies
- advances one step per authorized call: `none -> study -> document`
- keeps the issue `to-do` and omits `phase`
- persists `flow_prepared_until: document` after Document
- causes the normal YODA Flow to resume that issue at Implement

Its complete CLI contract is defined in
`project/specs/27-yoda-prep-flow-script.md`.

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
