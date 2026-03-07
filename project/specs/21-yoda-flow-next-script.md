# yoda_flow_next.py specification

## Objective

Define behavior for `yoda_flow_next.py`, the deterministic YODA Flow driver in 0.3.0.

## Location

- Script path: `yoda/scripts/yoda_flow_next.py`

## Command model

- Implicit command model (no subcommands, no `--action`).
- Each execution resolves exactly one next deterministic step.

## Inputs

- `--dev <slug>` (required)
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

- `to-do -> doing` starts with `phase=study`.
- While `status=doing`, progress is unitary:
  - `study -> document -> implement -> evaluate`
- After `evaluate`, transition to `done` and remove `phase`.

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
- compact
- single-line imperative instruction

## Error handling

- Invalid issue filename must fail with:
  - `INVALID_ISSUE_FILENAME: expected <dev>-<NNNN>-<slug>.md; got <filename>`
- Use shared exit code contract.
