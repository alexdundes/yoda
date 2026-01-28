# todo_reorder.py specification

## Objective

Define the required behavior for `todo_reorder.py`, the script that reorders the issues in `yoda/todos/TODO.<dev>.yaml` to match the desired visual and execution order.

## Scope

- Define CLI inputs and outputs for `todo_reorder.py`.
- Define default reordering rules.
- Define the `--prefer/--over` prioritization behavior.
- Define validation and error handling.

Out of scope:
- Implementing `todo_reorder.py`.
- Changing schemas outside this spec.

## Location

- Script path: `yoda/scripts/todo_reorder.py`
- TODO path: `yoda/todos/TODO.<dev>.yaml`

## CLI

The script follows the global CLI contract in `project/specs/13-yoda-scripts-v1.md`.

Optional inputs:
- `--dev <slug>`
- `--prefer <id-a>`: prioritize issue A relative to B (see Behavior).
- `--over <id-b>`: required with `--prefer`.

Global flags:
- `--format md|json`
- `--json`
- `--dry-run`
- `--verbose`

## Behavior

1) Resolve developer slug using the standard order: `--dev`, `YODA_DEV`, interactive prompt.
2) Load `yoda/todos/TODO.<dev>.yaml`. If missing, exit with code 3.
3) Validate the TODO schema. If validation fails, exit with code 2.
4) If `--prefer` is provided, apply the prioritization rule (see below).
5) Reorder the issues with the default ordering rules (see Ordering).
6) If a reorder occurred or a priority was updated, update `updated_at` for the TODO root and any issue whose priority changed.
7) Write changes unless `--dry-run` is set.
8) Output a summary in the chosen format.

## Ordering (default)

Reorder the YAML list to present the desired visual order:

1) `pending` issues first, ordered by `updated_at` ascending.
2) Active issues (status not `done` and not `pending`) next, ordered by execution order:
   - priority descending,
   - YAML order as tie-breaker,
   - dependencies not yet `done` must appear before their dependents (stable/deterministic).
3) `done` issues last, ordered by `updated_at` descending.

If dependency cycles exist, keep YAML order for the active segment and do not error.

## Prioritization (`--prefer` / `--over`)

When `--prefer <id-a> --over <id-b>` is provided:

- Both ids must exist in the TODO; otherwise exit with code 2.
- Both issues must have status `to-do`; otherwise exit with code 2.
- If `id-a` depends on `id-b`, exit with code 2 (cannot prioritize a dependent over its dependency).
- If `id-a` has lower priority than `id-b`, set `id-a` priority to match `id-b`.
- Apply the standard reorder after any priority adjustments (no additional forced position beyond the ordering rules).
- After applying prioritization, perform the default reordering.

`--prefer` and `--over` are not exclusive with default reordering; they are applied first and then the full reorder is executed.

## Output

### Markdown (default)

Return a short summary of actions:
- Whether reorder occurred.
- Whether a priority change was applied (and which issue).

### JSON (`--format json` or `--json`)

Minimum keys:
- `todo_path`
- `reordered` (boolean)
- `priority_updated` (boolean)
- `issue_id` (when `--prefer` is used)
- `dry_run`

Additional keys are allowed.

## Validation

- `--prefer` must be used together with `--over`.
- `--prefer` and `--over` must be valid issue ids present in the TODO.
- If `--prefer` equals `--over`, return exit code 2.

## Error handling

- Exit codes follow the global contract:
  - `0`: success
  - `1`: general error
  - `2`: validation error
  - `3`: not found (missing TODO)
  - `4`: conflict (unused by todo_reorder in v1)
- Errors must be written to stderr and include an actionable message.
