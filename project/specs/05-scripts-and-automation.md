# Scripts and automation

## Objective

Standardize repetitive tasks and reduce the need for manual edits.

## Location and language

- Folder: yoda/scripts
- Language: Python
- Rule: the .py file name is the command name

## Minimum scripts (v1)

- init.py: creates the minimum YODA Framework structure
- issue_add.py: adds an issue to `TODO.<dev>.yaml` and generates the issue Markdown from the template using basic fields provided by the agent
- `TODO.<dev>.yaml` maintenance scripts (list, update, reorder, etc.)
- scripts to present `TODO.<dev>.yaml` in a human-readable format for humans and agents
- log scripts to record flow events
- pending resolution script (sets status from pending and clears pending_reason)

## Logs

- One log per issue at yoda/logs/dev-id-slug.yaml

## Minimal validation (baseline)

Validation runs whenever scripts update metadata or change issue status to done.

Checks:
- TODO schema is valid (root + issue items).
- developer_slug follows slug rules; issues list exists (can be empty).
- Issue IDs are unique and match dev-#### format.
- status enum is valid; pending_reason required when status = pending.
- priority is 0..10 (default 5); lightweight is required boolean.
- depends_on references existing IDs.
- created_at and updated_at use ISO 8601 with offset.
- Issue front matter exists and mirrors TODO fields.
- Issue id matches filename and title.
- Log file exists per issue; log status enum is valid.
- Log entries use ISO 8601 with offset and mention the issue id.

Failure behavior:
- Exit with code 2 (validation error).
- Write errors to stderr.
- Do not write changes when validation fails.

## Principles

- Scripts are the official way to change metadata.
- The human or orchestrator executes the commands.
- When scripts are available, they are mandatory for metadata changes; bootstrap is the only exception.

## Benefits

- Consistent structure.
- Fewer errors when handling metadata.
- Easier auditing and reproducibility.
