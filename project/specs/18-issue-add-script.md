# issue_add.py specification

## Objective

Define the required behavior for `issue_add.py`, the script that creates a new issue entry in `yoda/todos/TODO.<dev>.yaml` and generates the corresponding issue Markdown file.

## Scope

- Define CLI inputs and outputs for `issue_add.py`.
- Define ID and slug generation rules.
- Define template selection and file creation behavior.
- Define validation, error handling, and conflict rules.
- Define logging behavior for issue creation.

Out of scope:
- Implementing `issue_add.py`.
- Changing schemas outside this spec.

## Location

- Script path: `yoda/scripts/issue_add.py`
- TODO path: `yoda/todos/TODO.<dev>.yaml`
- Issue path: `yoda/project/issues/<id>-<slug>.md`
- Templates:
  - Standard: `yoda/templates/issue.md`
  - Lightweight: `yoda/templates/issue-lightweight-process.md`
- Log path: `yoda/logs/<id>-<slug>.yaml`

## CLI

The script follows the global CLI contract in `project/specs/13-yoda-scripts-v1.md`.

Required inputs:
- `--title <text>`: issue title.
- `--description <text>`: short description used as the TODO description and issue front matter description.

Optional inputs:
- `--summary <text>`: alias for description (if provided, it overrides `--description`).
- `--slug <slug>`: explicit slug for the issue. If omitted, the slug is generated from the title.
- `--priority <0..10>`: integer priority (default 5).
- `--lightweight`: use the lightweight template and set `lightweight: true`.
- `--agent <text>`: agent name (default `Human`).
- `--tags <csv>`: comma-separated tags.
- `--entrypoint <path>:<type>`: entrypoint item, repeatable. Allowed types: `doc`, `code`, `config`, `schema`, `data`, `asset`, `other`.

Global flags:
- `--dev <slug>`
- `--format md|json`
- `--json`
- `--dry-run`
- `--verbose`

## ID generation

- The canonical ID is `<dev>-<NNNN>` where `NNNN` is a zero-padded 4-digit number.
- The next ID is computed by scanning existing issue IDs in the target TODO and incrementing the highest value.
- If no issues exist, start at `0001`.

## Slug generation

- Slug rules must follow `project/specs/04-todo-dev-yaml-issues.md`.
- If `--slug` is provided, validate it and use it as-is.
- If `--slug` is not provided, generate a slug from the title using these rules:
  - Lowercase.
  - Replace any non-alphanumeric sequence with a single hyphen.
  - Trim leading and trailing hyphens.
  - If the result does not start with a letter, prefix with `issue-`.

## Template selection

- Default template is `yoda/templates/issue.md`.
- If `--lightweight` is provided, use `yoda/templates/issue-lightweight-process.md`.

## Behavior

1) Resolve developer slug using the standard order: `--dev`, `YODA_DEV`, interactive prompt.
2) Load `yoda/todos/TODO.<dev>.yaml`. If it does not exist, create a new TODO file with default root fields (see "TODO file creation") before continuing.
3) Validate the TODO schema and inputs. If validation fails, exit with code 2.
4) Generate the next canonical ID and slug.
5) Construct the issue path and log path.
6) Check for conflicts:
   - If the ID already exists in the TODO, exit with code 4.
   - If the issue file already exists, exit with code 4.
   - If the log file already exists, exit with code 4.
7) Load the selected template. If missing, exit with code 3.
8) Populate the issue front matter fields to mirror the TODO item fields.
9) Create or update the TODO entry (append to the end of the issues list).
10) Create the issue Markdown file from the template with the populated fields.
    - The generated issue file must not include the opening template instruction comment that asks to replace `[ID]` and `[TITLE]`.
11) Create the log file with a single entry describing the issue creation.
12) If `--dry-run` is set, perform all steps except file writes. Output a summary and exit 0.

## Metadata population

The TODO issue item and issue front matter must include:
- `schema_version: "1.0"`
- `id`, `title`, `slug`, `description`
- `status: to-do`
- `priority`
- `lightweight`
- `agent`
- `depends_on: []`
- `pending_reason: ""`
- `created_at`, `updated_at` (same timestamp)
- `entrypoints` (from flags)
- `tags` (from flags)
- `origin` (default empty values)

Timestamps:
- Use the timezone defined in the TODO root field `timezone`.
- Format timestamps as ISO 8601 with explicit offset.

## TODO file creation

If `yoda/todos/TODO.<dev>.yaml` does not exist, `issue_add.py` must create it with these defaults before creating the issue:
- `schema_version: "1.0"`
- `developer_name`: derive from `<dev>` by title-casing (example: `dev` -> `Dev`).
- `developer_slug`: `<dev>`
- `timezone`: local machine timezone (IANA TZ name when available)
- `updated_at`: current timestamp
- `issues`: empty array

## Logging

- The script must create `yoda/logs/<id>-<slug>.yaml` if it does not exist.
- The log file must follow the log schema in `project/specs/05-scripts-and-automation.md`.
- The initial log entry message should mention the issue id and include initial values provided (one per line, omit fields not supplied).

## Output

On success, the script outputs a short summary in the chosen format, including:
- Issue ID
- Issue path
- TODO path
- Log path
- Template used

## Error handling

- Exit codes must follow the global contract:
  - `0`: success
  - `1`: general error
  - `2`: validation error
  - `3`: not found (missing TODO or template)
  - `4`: conflict (ID or file already exists)
- Errors must be written to stderr and include an actionable message.
