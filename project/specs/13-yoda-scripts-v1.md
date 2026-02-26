# YODA Framework - Scripts v1 Specification

This document defines the minimum script interface for YODA v1. Scripts live in `yoda/scripts/` and are executed by their file name (file name = command).

## Naming

- Script path: `yoda/scripts/<name>.py`
- Command name: `<name>.py`

## Developer selection

Scripts that read TODO files MUST resolve the developer slug using:

1) --dev `<slug>` flag
2) YODA_DEV environment variable
3) Interactive prompt when not defined

Slug format:
- Lowercase ASCII, digits, and hyphens only.
- Must start with a letter and contain no spaces.

## CLI contract (all scripts)

Default output is Markdown for human readability. JSON output is available when explicitly requested.

Global flags:
- `--dev <slug>`: target developer slug (see Developer selection).
- `--format md|json`: output format (default: `md`).
- `--json`: shorthand for `--format json`.
- `--dry-run`: simulate changes without writing files.
- `--verbose`: include extra diagnostic details in output.

Exit codes:
- `0`: success.
- `1`: general error (unexpected failure).
- `2`: validation error (invalid inputs or schema).
- `3`: not found (missing file or issue id).
- `4`: conflict (state prevents action).

Error handling:
- Errors must be written to stderr.
- Scripts must include a short, actionable error message.

Agent guidance:
- Agents may inspect the script source code in `yoda/scripts/` to understand behavior, flags, and edge cases.

Validation:
- Any script that mutates metadata MUST run validation before writing changes.
- Validation failures must return exit code 2 and must not write changes.

## JSON output contract (minimum)

When `--format json` (or `--json`) is used, scripts must emit a JSON object with the following minimum keys. Consumers MUST ignore unknown keys for forward compatibility.

- `issue_add.py`:
  - `issue_id`
  - `issue_path`
  - `todo_path`
  - `log_path`
  - `template`
  - `dry_run`
- `todo_update.py`:
  - `issue_id`
  - `updated_fields`
  - `todo_path`
  - `dry_run`
- `log_add.py`:
  - `issue_id`
  - `log_path`
  - `timestamp`
  - `dry_run`
- `todo_next.py`:
  - `issue_id`
  - `issue_path`
  - `todo_path`
  - `pending`
  - `blocked`
  - `doing`
- `todo_list.py`:
  - `issues` (full issue items)
- `todo_reorder.py`:
  - `todo_path`
  - `reordered`
  - `priority_updated`
  - `issue_id`
  - `dry_run`
- `yoda_intake.py`:
  - `mode`
  - `dev`
  - `runbook`
  - `external_issue` (when `--extern-issue` is used)
- `get_extern_issue.py`:
  - `dev`
  - `provider`
  - `issue_number`
  - `saved_file`

## Required scripts

### issue_add.py

Purpose:
- Create a new issue entry in `yoda/todos/TODO.<dev>.yaml` and generate the issue Markdown from the template.

Behavior (minimum):
- Generate the next sequential id.
- Create `yoda/todos/TODO.<dev>.yaml` entry with basic fields.
- Create the issue Markdown file from the template.
- Fill basic fields in the template (id, title, summary) based on provided inputs.

Inputs:
- Title, description or summary, priority.
- Optional external origin linkage via `--extern-issue`, `--origin-system`, `--origin-requester`.

Outputs:
- Updated `yoda/todos/TODO.<dev>.yaml` and new issue Markdown file named `<id>-<slug>.md` in `yoda/project/issues/`.

---

### todo_list.py

Purpose:
- List TODO items from `yoda/todos/TODO.<dev>.yaml`.

Behavior (minimum):
- Filter by status or priority.
- Output a human-readable summary and a machine-friendly list.

Inputs:
- TODO file path (default: `yoda/todos/TODO.<dev>.yaml`).
- --dev `<slug>` (optional, see Developer selection).
- Optional filters.

Outputs:
- Structured list of issues.
  - JSON output includes full issue items when `--format json` is used.

---

### todo_update.py

Purpose:
- Update `yoda/todos/TODO.<dev>.yaml` fields.

Behavior (minimum):
- Update status, priority, depends_on, pending_reason.
- Update updated_at.
- Use `todo_update.py` to resolve `pending` issues by setting a new status and clearing `pending_reason`.
- `todo_update.py` is the standard way to re-sync issue front matter with the TODO item.
- If the issue Markdown file is missing, `todo_update.py` must fail (do not recreate the file). If recovery is needed, a human or agent must recreate the Markdown manually (no scripts).

Inputs:
- Issue id.
- Field updates (flags or key=value).
- --dev `<slug>` (optional, see Developer selection).

Outputs:
- Updated `yoda/todos/TODO.<dev>.yaml`.

---

### todo_next.py

Purpose:
- Return the next actionable issue.

Behavior (minimum):
- Select highest priority issue without unresolved dependencies.
- If any issue is `doing`, exit with conflict and report the doing list.
- Only `to-do` issues are selectable.
- Tie-breaker: position in the YAML list (top to bottom).
- Skip issues with pending status.
- If no selectable issues exist, exit with an error and list pending items and blocked dependencies.

Inputs:
- TODO file path (default: `yoda/todos/TODO.<dev>.yaml`).
- --dev `<slug>` (optional, see Developer selection).

Outputs:
- Issue id and path.
 
Notes:
- If any pending issues exist, include a hint listing them and their reasons, even when a selectable issue exists.
- If any `doing` issues exist, return conflict and list them to enforce one-at-a-time execution.

---

### todo_reorder.py

Purpose:
- Reorder TODO items.

Behavior (minimum):
- Apply the default reorder (pending first, active by execution order, done last).
- Optionally apply `--prefer/--over` prioritization before reordering.
- Update updated_at only when a reorder or priority change occurs.

Inputs:
- Optional `--prefer <id-a>` and `--over <id-b>`.
- --dev `<slug>` (optional, see Developer selection).

Outputs:
- Updated `yoda/todos/TODO.<dev>.yaml`.

---

### log_add.py

Purpose:
- Append a log entry for an issue.

Behavior (minimum):
- Add a timestamped entry to the issue log.

Inputs:
- Issue id.
- Message text.

Outputs:
- Updated log file named `<id>-<slug>.yaml` in `yoda/logs/`.

---

### yoda_intake.py

Purpose:
- Provide AGENT runbooks for YODA Intake.

Behavior (minimum):
- `--dev` only: return initial runbook to branch into `--extern-issue` vs `--no-extern-issue`.
- `--no-extern-issue`: return full runbook for local-only intake.
- `--extern-issue <NNN>`:
  - if external file is missing, return runbook asking the human to execute `get_extern_issue.py`;
  - if external file exists, return full runbook and friendly markdown summary of the source issue.

Inputs:
- `--dev <slug>`
- Optional `--extern-issue <NNN>` or `--no-extern-issue` (mutually exclusive).

Outputs:
- Runbook text (markdown by default).
- Source issue summary when external mode is used and local source file exists.

---

### get_extern_issue.py

Purpose:
- Fetch external issue details and persist them locally for later `yoda_intake.py` consumption.

Behavior (minimum):
- Detect provider from git `origin`.
- Use provider CLI (`glab`/`gh`) to fetch issue details.
- Write source JSON to `yoda/project/extern-issues/<provider>-<NNN>.json`.
- Output a one-line next step command to continue intake loop.

Inputs:
- `--dev <slug>`
- `--extern-issue <NNN>`

Outputs:
- Saved JSON file path.
- Next step command: `yoda_intake.py --dev <slug> --extern-issue <NNN>`.

## Notes

- Scripts must avoid destructive actions without explicit user confirmation.
- Scripts should fail loudly on missing paths or invalid data.
- Output formats should be minimal and consistent for agents.
