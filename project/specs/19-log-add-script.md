# log_add.py specification

## Objective

Define the required behavior for `log_add.py`, the script that appends entries to issue logs.

## Scope

- Define CLI inputs and outputs for `log_add.py`.
- Define how to resolve log paths from issue ids.
- Define append behavior, log creation rules, and validation.
- Define error handling and output format.

Out of scope:
- Implementing `log_add.py`.
- Changing schemas outside this spec.

## Location

- Script path: `yoda/scripts/log_add.py`
- TODO path: `yoda/todos/TODO.<dev>.yaml`
- Issue path: `yoda/project/issues/<id>-<slug>.md`
- Log path: `yoda/logs/<id>-<slug>.yaml`

## CLI

The script follows the global CLI contract in `project/specs/13-yoda-scripts-v1.md`.

Required inputs:
- `--issue <id>`: canonical issue id (dev-####).
- `--message <text>`: log message text.

Optional inputs:
- `--timestamp <iso8601>`: override timestamp (default: now in TODO timezone).
Note: `log_add.py` does not accept a slug input; it resolves the slug from the TODO item identified by `--issue`.

Global flags:
- `--dev <slug>`
- `--format md|json`
- `--json`
- `--dry-run`
- `--verbose`

## Behavior

1) Resolve developer slug using the standard order: `--dev`, `YODA_DEV`, interactive prompt.
2) Load `yoda/todos/TODO.<dev>.yaml`. If missing, exit with code 3.
3) Validate the TODO schema and inputs. If validation fails, exit with code 2.
4) Find the issue item by id. If not found, exit with code 3.
5) Resolve slug from the TODO issue item and construct issue/log paths.
6) Ensure the issue Markdown file exists. If missing, exit with code 3.
7) Load the log file if it exists; otherwise, create a new log document with the required schema fields.
8) Append a log entry with timestamp and message.
9) Update the log `status` to match the current TODO issue status.
10) Validate the resulting log document. If validation fails, exit with code 2.
11) If `--dry-run` is set, perform all steps except file writes. Output a summary and exit 0.

## Log creation

If the log file does not exist, `log_add.py` must create it with:
- `schema_version: "1.0"`
- `issue_id`: from input
- `issue_path`: resolved from TODO slug
- `todo_id`: same as issue_id
- `status`: current issue status from TODO
- `entries`: empty list (before append)

## Timestamp

- Default timestamp uses the timezone defined in the TODO root field `timezone`.
- The timestamp must be ISO 8601 with explicit offset.
- If `--timestamp` is provided, it must be validated as ISO 8601 with offset.

## Validation

Before writing:
- TODO schema is valid.
- Issue id exists in TODO.
- Issue Markdown file exists.
- Log schema is valid after append (required fields and entry types).
- Log entry timestamp has timezone and message is non-empty.

Validation failures must exit with code 2 and write no files.

## Output

On success, the script outputs a short summary in the chosen format, including:
- Issue ID
- Log path
- Timestamp used
- Dry-run indicator (if applicable)

## Message format

- Messages should be multi-line when detailing updates.
- For updates, use one field per line in the format `field: old -> new`.
- For creation logs, list only the initial values provided (omit fields not supplied).

## Error handling

- Exit codes must follow the global contract:
  - `0`: success
  - `1`: general error
  - `2`: validation error
  - `3`: not found (missing TODO, issue id, or issue file)
  - `4`: conflict (unused by log_add in v1)
- Errors must be written to stderr and include an actionable message.
