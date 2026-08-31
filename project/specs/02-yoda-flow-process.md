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

## Phase boundary

A phase boundary is a process rule, not a bookkeeping step. Every phase runs in
this order:

1) The human authorizes the next phase.
2) The agent applies the transition with `yoda_flow_next.py`.
3) The agent presents the returned runbook.
4) The agent executes only the work of that phase.
5) The agent presents the phase deliverable and stops.

- The transition MUST precede the work of the phase it starts. It MUST NOT be
  applied afterwards to stamp work that is already finished.
- One step is one phase per human interaction, not one phase per command call.
  Consecutive calls that chain several phases into a single interaction break
  this rule even when each call is individually valid.
- A generic approval such as "go ahead" authorizes only the next boundary. Every
  later phase requires its own deliverable to be presented first.
- The output of `yoda_flow_next.py` is operational instruction. The agent MUST
  present it and MUST NOT discard, silence, or redirect it.
- Close timestamps in `## Flow log` MAY indicate chaining and justify review, but
  MUST NOT be treated on their own as proof of a violation: a phase can be
  legitimately short.

## Phase transitions

- `to-do -> doing` starts the cycle with `phase=study`.
- `to-do + flow_prepared_until=document -> doing/implement` resumes an issue
  already prepared through YODA Prep Flow.
- `to-do + flow_prepared_until=study -> doing/study`: Study is executed again in
  normal YODA Flow because only completed Document authorizes skipping directly
  to Implement.
- While `status=doing`, phase advances one authorized step at a time:
  - `study -> document -> implement -> evaluate`
- Completion after `evaluate` transitions to `done` and removes `phase`.
- `pending` requires `pending_reason` and hides `phase`.

## YODA Prep Flow

YODA Prep Flow is an explicit alternative for preparing one issue through
Study and Document without entering implementation:

- entrypoint: `yoda_prep_flow.py --dev <developer-slug> --issue <id>`
- operates on the explicit issue, independent of backlog order/dependencies
- advances one preparation stage per human interaction:
  `none -> study -> document`; each stage requires explicit human
  authorization, ends by presenting its deliverable, and stops before another
  stage can begin
- keeps the issue `to-do` and omits `phase`
- persists `flow_prepared_until: document` after Document
- causes the normal YODA Flow to resume that issue at Implement

Its complete CLI contract is defined in
`project/specs/27-yoda-prep-flow-script.md`.

## Blocking policy

- On blockers, `yoda_flow_next.py` MUST NOT mutate metadata.
- It MUST return a deterministic blocked response and instruct `todo_update.py`.

## Deliverables per phase

Each phase ends by presenting its deliverable to the human and stopping. The
deliverable is what the next authorization is granted against; without it, an
approval has no object.

| Phase | Deliverable |
|---|---|
| study | findings, constraints, and the open decisions the human must settle |
| document | the updated issue carrying the approved decisions and a closed document-first contract |
| implement | the code and artifacts of the approved scope, with the verifications that were run |
| evaluate | acceptance criteria checked, remaining findings, and the `Result log` filled in when approved |

## Output contract for yoda_flow_next.py

Both `md` and `json` outputs MUST include:

- `issue_path`
- `status`
- `phase` (when applicable)
- `next_step`
- `blocked_reason` (when blocked)
- `runbook_line`

`runbook_line` MUST be imperative and as compact as the instruction allows. It
MAY span more than one line when a single line cannot carry it; being understood
takes precedence over being short.
