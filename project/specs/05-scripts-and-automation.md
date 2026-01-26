# Scripts and automation

## Objective

Standardize repetitive tasks and reduce the need for manual edits.

## Location and language

- Folder: yoda/scripts
- Language: Python
- Rule: the .py file name is the command name

## Minimum scripts (v1)

- init.py: creates the minimum YODA Framework structure
- issue_add.py: adds an issue to `yoda/todos/TODO.<dev>.yaml` and generates the issue Markdown from the template using basic fields provided by the agent
- `yoda/todos/TODO.<dev>.yaml` maintenance scripts (list, update, reorder, etc.)
- scripts to present `yoda/todos/TODO.<dev>.yaml` in a human-readable format for humans and agents
- log scripts to record flow events
- pending resolution script (sets status from pending and clears pending_reason)

## Logs

- One log per issue at `yoda/logs/<id>-<slug>.yaml`

## Log schema (YAML)

Required fields:

- issue_id: canonical id (dev-####).
- issue_path: path to the issue Markdown file.
- todo_id: same as issue_id.
- status: to-do | doing | done | pending.
- entries: list of log entries.

Each entry must contain:

- timestamp: ISO 8601 with offset.
- message: log message text.

Rules:

- Log files are append-only; new entries are added at the end.
- Any script action must append a log entry.
- Manual log entries are allowed through the log_add.py script.

## Minimal validation (baseline)

Validation runs whenever scripts update metadata or change issue status to done.

Checks:
- TODO schema is valid (root + issue items).
- developer_slug follows slug rules; issues list exists (can be empty).
- timezone is present and valid (`UTC` or IANA TZ database name compatible with Python `zoneinfo`).
- Issue IDs are unique and match dev-#### format.
- status enum is valid; pending_reason required when status = pending.
- priority is 0..10 (default 5); lightweight is required boolean.
- depends_on references existing IDs.
- created_at and updated_at use ISO 8601 with offset.
- Issue front matter exists and mirrors TODO fields.
- Issue id matches filename and title.
- Log file exists per issue; log status enum is valid.
- Log entries use ISO 8601 with offset and mention the issue id.
- schema_version is present and supported; major mismatches are errors.

Failure behavior:
- Exit with code 2 (validation error).
- Write errors to stderr.
- Do not write changes when validation fails.

## Schema versioning and migrations

- TODO and issue metadata use `schema_version` (current: "1.0").
- Versions follow semantic versioning (major.minor).
- Major version changes are breaking and must be rejected by scripts.
- Minor version changes are backward compatible and accepted.
- A migration script is required to upgrade schema versions when needed.

## Principles

- Scripts are the official way to change metadata.
- The human or orchestrator executes the commands.
- When scripts are available, they are mandatory for metadata changes; bootstrap is the only exception.

## Benefits

- Consistent structure.
- Fewer errors when handling metadata.
- Easier auditing and reproducibility.
