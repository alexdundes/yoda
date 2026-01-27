# todo_next.py specification

## Objective

Define the required behavior for `todo_next.py`, the script that selects the next actionable issue from `yoda/todos/TODO.<dev>.yaml`.

## Scope

- Define CLI inputs and outputs for `todo_next.py`.
- Define deterministic selection rules and dependency handling.
- Define hinting behavior for pending issues (even on success).
- Define error handling and output format.

Out of scope:
- Implementing `todo_next.py`.
- Changing schemas outside this spec.

## Location

- Script path: `yoda/scripts/todo_next.py`
- TODO path: `yoda/todos/TODO.<dev>.yaml`
- Issue path: `yoda/project/issues/<id>-<slug>.md`

## CLI

The script follows the global CLI contract in `project/specs/13-yoda-scripts-v1.md`.

Optional inputs:
- `--dev <slug>`
- `--todo <path>`: override TODO path (default: `yoda/todos/TODO.<dev>.yaml`).

Global flags:
- `--format md|json`
- `--json`
- `--dry-run`
- `--verbose`

## Behavior

1) Resolve developer slug using the standard order: `--dev`, `YODA_DEV`, interactive prompt.
2) Resolve TODO path (default or `--todo`). If missing, exit with code 3.
3) Load the TODO and validate the schema. If validation fails, exit with code 2.
4) If any issue has status `doing`, exit with code 4 (conflict) and include the list of doing issues in the output.
5) Build a list of selectable issues:
   - status is `to-do` only.
   - all `depends_on` ids are present and have status `done`.
6) Select the next issue using deterministic rules:
   - highest priority first (desc).
   - tie-breaker: order in the YAML list (top to bottom).
7) Collect pending issues (status = `pending`) with their `pending_reason`.
8) Collect blocked issues (unresolved `depends_on`) with the blocking ids.
9) If no selectable issues exist, exit with code 3 and include pending/blocked lists in the output.
10) If a selectable issue exists, output the selected issue plus a pending hint whenever pending issues exist.
11) If `--dry-run` is set, perform all steps except file writes. Output a summary and exit 0.

## Output

On success, the script outputs a short summary in the chosen format, including:
- Issue ID
- Issue path
- TODO path
- Pending hint (if any pending issues exist)

On failure (no selectable issues), the script outputs:
- Error message (not found)
- Pending list (if any)
- Blocked list (if any)

On conflict (doing issues exist), the script outputs:
- Error message (conflict)
- Doing list
- Pending list (if any)

## Pending hint (always-on)

If any issues are `pending`, the script MUST include a hint in the output even when a selectable issue is returned. This hint must list each pending issue id and its `pending_reason`.

## Validation

Before returning success:
- TODO schema is valid.
- Selected issue id exists in TODO.
- Issue path can be resolved from id + slug.

Validation failures must exit with code 2 and write no files.

## Error handling

- Exit codes must follow the global contract:
  - `0`: success
  - `1`: general error
  - `2`: validation error
  - `3`: not found (missing TODO or no selectable issues)
  - `4`: conflict (one or more issues are already `doing`)
- Errors must be written to stderr and include an actionable message.
