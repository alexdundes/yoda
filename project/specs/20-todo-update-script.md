# todo_update.py specification

## Objective

Define the required behavior for `todo_update.py`, the script that updates fields in `yoda/todos/TODO.<dev>.yaml`.

## Scope

- Define CLI inputs and outputs for `todo_update.py`.
- Define allowed field updates and validation rules.
- Define behavior for status transitions and pending_reason.
- Define error handling and output format.

Out of scope:
- Implementing `todo_update.py`.
- Changing schemas outside this spec.

## Location

- Script path: `yoda/scripts/todo_update.py`
- TODO path: `yoda/todos/TODO.<dev>.yaml`
- Issue path: `yoda/project/issues/<id>-<slug>.md`

## CLI

The script follows the global CLI contract in `project/specs/13-yoda-scripts-v1.md`.

Required inputs:
- `--issue <id>`: canonical issue id (dev-####).

Updatable fields (flags):
- `--status <to-do|doing|done|pending>`
- `--priority <0..10>`
- `--title <text>`
- `--description <text>`
- `--slug <slug>`: filename slug override used for issue/log rename.
- `--depends-on <csv>`: comma-separated issue ids.
- `--pending-reason <text>`
- `--extern-issue <NNN>`: infer provider from git `origin` and generate `extern_issue_file` as `../extern_issues/<provider>-<NNN>.json`.
- `--extern-issue-file <path>`: relative path from `yoda/project/issues/` to external JSON (example: `../extern_issues/github-2.json`).

Optional inputs:
- `--clear-depends-on`: remove all dependencies.
- `--clear-extern-issue-file`: clear external source linkage (`extern_issue_file: ""`).

Global flags:
- `--dev <slug>`
- `--format md|json`
- `--json`
- `--dry-run`
- `--verbose`

## Behavior

1) Resolve developer slug using the standard order: `--dev`, `YODA_DEV`, interactive prompt.
2) Load `yoda/todos/TODO.<dev>.yaml`. If missing, exit with code 3.
3) Validate the TODO schema. If validation fails, exit with code 2.
4) Find the issue item by id. If not found, exit with code 3.
5) Resolve current issue file by id (`yoda/project/issues/<id>-*.md`); if missing, exit with code 3; if multiple matches, exit with code 4.
6) Apply provided updates to the issue item.
7) Enforce pending rules:
   - If status is set to `pending`, `pending_reason` must be provided (or already present).
   - If status is set to any non-pending value, `pending_reason` must be cleared unless explicitly provided.
8) Resolve target filename slug:
   - use `--slug` when provided;
   - else, if `--title` changed, derive slug from the new title;
   - else keep current filename slug.
9) If target slug differs, rename issue and log files to `<id>-<target-slug>.*` (conflict => exit 4).
10) Update issue `updated_at` and root `updated_at` with the current timestamp in TODO timezone.
11) Validate the resulting TODO. If validation fails, exit with code 2.
12) Update the issue Markdown front matter to mirror the TODO item.
13) Append a log entry for the updated issue via `log_add.py` (or shared helper) unless `--dry-run` is set.
14) If `--dry-run` is set, perform all steps except file writes. Output a summary and exit 0.

## Updates

- Only the fields listed above may be updated by `todo_update.py`.
- Fields not specified by flags must remain unchanged.
- `depends_on` must be a list after processing.
- `priority` must remain within 0..10.
- `status` must match the allowed enum.
- `depends_on` ids must exist within the same TODO.
- `extern_issue_file`, when provided and non-empty, must match the schema/validation pattern.
- `--extern-issue` and `--extern-issue-file` are mutually exclusive.
- `slug` must not be persisted in TODO/front matter; it is a filename concern.
- `--clear-extern-issue-file` removes external linkage from persisted metadata.

## Timestamp

- Use the timezone defined in the TODO root field `timezone`.
- Format timestamps as ISO 8601 with explicit offset.

## Validation

Before writing:
- TODO schema is valid.
- Issue id exists in TODO.
- Issue Markdown file exists and can be updated.
- Updated fields are valid per schema constraints.
- `pending_reason` rules are satisfied.
- `depends_on` references existing IDs.

Validation failures must exit with code 2 and write no files.

## Output

On success, the script outputs a short summary in the chosen format, including:
- Issue ID
- Updated fields list
- TODO path
- Dry-run indicator (if applicable)

## Log message

- Log messages must include one line per changed field in the format `field: old -> new`.
- Only fields that actually changed should be logged.

## Error handling

- Exit codes must follow the global contract:
  - `0`: success
  - `1`: general error
  - `2`: validation error
  - `3`: not found (missing TODO or issue id)
  - `4`: conflict (rename target exists or multiple files found for same id)
- Errors must be written to stderr and include an actionable message.
