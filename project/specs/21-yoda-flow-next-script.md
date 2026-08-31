# yoda_flow_next.py specification

## Objective

Define behavior for `yoda_flow_next.py`, the deterministic YODA Flow driver in 0.4.0.

## Location

- Script path: `yoda/scripts/yoda_flow_next.py`

## Command model

- Implicit command model (no subcommands, no `--action`).
- Each execution resolves exactly one next deterministic step. This is a
  technical property of the command and is subordinate to the process boundary
  in `project/specs/02-yoda-flow-process.md`: one phase per human interaction.
  Chaining several executions into one interaction is invalid even though each
  execution is individually well formed.
- The execution starts a phase; it MUST precede the work of that phase.

## Inputs

- `--dev <developer-slug>` (required)
- `--log-message "<summary>"` (optional)
- shared global flags

## Core behavior

1) Resolve execution context and current issue state.
2) Determine the next deterministic step.
3) If blocked, do not mutate state and return deterministic blocked instruction for `todo_update.py`.
4) If not blocked, perform only the single next progression action.

Flow log behavior:
- Transition entries MUST use single-line format: `- <ISO8601> transition <de->para>`.
- For new entries, transition messages MUST NOT repeat issue id as prefix.
- When `--log-message` is provided, append ` | <summary>` to the transition line.

## State progression

- `to-do -> doing` starts with `phase=study` when the issue was not prepared.
- `to-do + flow_prepared_until=document -> doing/implement` resumes an issue
  prepared through YODA Prep Flow.
- `to-do + flow_prepared_until=study -> doing/study`; the normal Flow repeats
  Study because preparation has not completed Document.
- While `status=doing`, progress is unitary:
  - `study -> document -> implement -> evaluate`
- After `evaluate`, transition to `done` and remove `phase`.
- Readers accept schema 2.00/2.01 during rollout; a front-matter transition
  persists schema 2.01.

## Output contract (md/json)

Both formats MUST include:

- `issue_path`
- `status`
- `phase` (when applicable)
- `next_step`
- `blocked_reason` (when blocked)
- `runbook_line`

`runbook_line` requirements:

- mandatory
- imperative
- as compact as the instruction allows; MAY span more than one line when a
  single line cannot carry it
- presented to the human, never discarded or silenced

## Error handling

- Invalid issue filename must fail with:
  - `INVALID_ISSUE_FILENAME: expected <dev>-<NNNN>-<slug>.md; got <filename>`
- Use shared exit code contract.
