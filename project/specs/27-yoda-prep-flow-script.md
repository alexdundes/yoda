# yoda_prep_flow.py specification

## Objective

Define the preparation-only YODA Prep Flow that executes Study and Document for
one explicit issue without entering Implement or Evaluate.

## Location and entry

- Script path: `yoda/scripts/yoda_prep_flow.py`
- Invocation: `python3 yoda/scripts/yoda_prep_flow.py --dev <slug> --issue <id>`
- YODA Prep Flow MUST be entered only from explicit human intent.
- Agents MUST read the command `--help` before using the flow.

## Inputs

- `--dev <slug>` (required)
- `--issue <dev-NNNN>` (required)
- shared `--format md|json`, `--json`, `--dry-run`, and `--verbose` flags

The command operates on the explicit issue regardless of backlog priority or
unresolved dependencies. This exception applies only to documentation
preparation and does not make the issue selectable for implementation.

## State contract

YODA Prep Flow advances one step per call and requires explicit human approval
between calls:

1. No `flow_prepared_until` -> `flow_prepared_until: study`
2. `flow_prepared_until: study` -> `flow_prepared_until: document`
3. `flow_prepared_until: document` remains document-prepared

Every prep transition:

- keeps `status: to-do`
- removes `phase`
- updates `updated_at`
- persists schema 2.01 when front matter is written
- appends one compact `## Flow log` entry

`flow_prepared_until` is optional. Accepted values are `study` and `document`;
an absent value means normal YODA Flow behavior.

## Runbooks

- Study: gather context, list open decisions, do not implement, and wait for
  approval.
- Document: update issue text with approved decisions, do not implement, and
  wait for approval.
- After Document, the issue remains `to-do` until selected by normal YODA Flow.
- `yoda_flow_next.py` MUST start a selected `to-do` issue with
  `flow_prepared_until: document` at `doing/implement`.

## Output contract

Markdown and JSON outputs include:

- `issue_id`
- `issue_path`
- `status`
- `phase` (empty during Prep Flow)
- `flow_prepared_until`
- `next_step`
- `runbook_line`
- `log_timestamp`
- `dry_run`

`runbook_line` is a compact, single-line imperative instruction.

## Validation and errors

- Issue ID MUST match the provided developer slug.
- Issue file MUST exist and use compatible schema 2.00 or 2.01.
- `flow_prepared_until` outside `study|document` is a validation error.
- A `done` issue cannot enter YODA Prep Flow.
- Missing flags and invalid metadata return the shared validation exit code.
- Missing issue files return the shared not-found exit code.

## Dry-run

`--dry-run` resolves and validates the transition and returns the simulated
payload without changing front matter or appending Flow log entries.
