# todo_update.py specification

## Objective

Define behavior for `todo_update.py`, a permanent script for semantic corrections and metadata adjustments.

## Location

- Script path: `yoda/scripts/todo_update.py`

## CLI

Core update inputs include:

- `--issue <id>`
- `--status <status>`
- `--priority <0..10>`
- `--title <text>`
- `--description <text>`
- `--depends-on <csv>`
- `--pending-reason <text>`
- `--extern-issue-file <path>` / `--extern-issue <NNN>`
- `--phase <study|document|implement|evaluate>`

## Help behavior

- `--help` MUST provide short, direct instructions for agents/operators.
- Invocation without required parameters MUST return actionable usage guidance.

## Phase rules

- `phase` may be set only when resulting `status=doing`.
- `phase` MUST be omitted/cleared for statuses `to-do`, `pending`, `done`.

## Behavior

1) Resolve target issue deterministically.
2) Validate requested changes.
3) Apply updates to canonical metadata.
4) Keep metadata consistent with filename-derived id contract.
5) Append compact one-line log describing the update.

## Logging format

- Exactly one line per update action.
- Direct and compact message.

## Output

On success, return issue id, updated fields, target path(s), and timestamp.
