# log_add.py specification

## Objective

Define behavior for `log_add.py`, a permanent script used to append compact issue logs outside normal YODA Flow transitions.

## Location

- Script path: `yoda/scripts/log_add.py`

## CLI

Required operational inputs:

- `--issue <id>`
- `--message <text>`

Optional:

- `--timestamp <iso-8601>`
- global flags from script contract

## Help behavior

- `--help` MUST provide short, direct instructions for agents/operators.
- Invocation without required parameters MUST return actionable usage guidance.

## Behavior

1) Resolve issue target deterministically by issue id.
2) Validate issue id and message.
3) Append log entry.
4) Persist a compact single-line message.

## Logging format

- Message MUST be one line.
- Message SHOULD be short and directly describe the action/context.

## Output

On success, return issue id, log path, and timestamp.
