# issue_add.py specification

## Objective

Define the required behavior for `issue_add.py`, the script that creates a new markdown issue file in `yoda/project/issues/`.

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
- Canonical issue path: `yoda/project/issues/<dev>-<NNNN>-<slug>.md`
- Templates:
  - Standard: `yoda/templates/issue.md`
- Flow log path: section `## Flow log` in the issue markdown file.

## CLI

The script follows the global CLI contract in `project/specs/13-yoda-scripts-v1.md`.

Required inputs:
- `--title <text>`: issue title.
- `--description <text>`: short description used in issue front matter.

Optional inputs:
- `--summary <text>`: alias for description (if provided, it overrides `--description`).
- `--slug <slug>`: explicit slug for the issue. If omitted, the slug is generated from the title.
- `--priority <0..10>`: integer priority (default 5 baseline).
- `--extern-issue <NNN>`: generate `extern_issue_file` pointing to `../extern_issues/<provider>-<NNN>.json`.

Global flags:
- `--dev <slug>`
- `--format md|json`
- `--json`
- `--dry-run`
- `--verbose`

## ID generation

- The canonical ID is `<dev>-<NNNN>` where `NNNN` is a zero-padded 4-digit number.
- The next ID is computed by scanning existing issue filenames for the same `<dev>` and incrementing the highest value.
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

- Use `yoda/templates/issue.md`.

## Behavior

1) Resolve developer slug from `--dev`.
   - If missing, return guidance instructing the agent to ask the human for the slug and rerun with `--dev <slug>`.
2) Acquire an external lock file scoped by `--dev` before reading/writing issue artifacts.
   - Retry lock acquisition up to 3 attempts with increasing wait between attempts.
   - If lock acquisition fails after retries, exit with code 4 and an explicit message.
3) Validate inputs and template availability. If validation fails, exit with code 2.
5) Generate the next canonical ID and slug.
6) Construct the issue path.
7) Check for conflicts:
   - If the issue file already exists, exit with code 4.
8) Load the selected template. If missing, exit with code 3.
9) Populate issue front matter fields using canonical metadata.
10) Create the issue Markdown file from the template with the populated fields.
    - The generated issue file must not include the opening template instruction comment that asks to replace `[ID]` and `[TITLE]`.
11) Append an initial creation entry to `## Flow log` in the issue file.
12) File writes during creation MUST be atomic per file (temporary file + replace).
13) If `--dry-run` is set, perform all steps except file writes. Output a summary and exit 0.

Failure policy:
- If a write step fails after lock acquisition, return explicit error and abort.
- No automatic rollback is required for files written before the failure.

## Metadata population

The issue front matter must include:
- `schema_version: "2.00"`
- `id`, `title`, `description`
- `status: to-do`
- `priority`
- `created_at`, `updated_at` (same timestamp)
- `extern_issue_file`:
  - when `--extern-issue` is provided, MUST be set to a relative path from `yoda/project/issues/` to `yoda/project/extern_issues/<provider>-<NNN>.json`;
  - example: `../extern_issues/github-2.json`.

Metadata policy:
- `slug` is represented by the issue filename (`<id>-<slug>.md`) and must not be persisted in front matter.
- Optional empty fields (`depends_on`, `pending_reason`, `extern_issue_file`) must be omitted.
- `depends_on` starts empty by default and is written only when non-empty.

Priority policy for issue creation:
- If `--priority` is omitted, the created issue must use `5` (baseline).
- In YODA Intake, values different from `5` should be used only with explicit comparative justification in the issue Markdown.

Timestamps:
- Use the timezone defined in the TODO root field `timezone`.
- Format timestamps as ISO 8601 with explicit offset.

## Logging

- The script must append a line in the issue `## Flow log` section on successful creation.
- The initial message should mention issue creation, title, and priority.
- `--dry-run` must not append flow log entries.

## Output

On success, the script outputs a short summary in the chosen format, including:
- Issue ID
- Issue path
- Template used

## Error handling

- Exit codes must follow the global contract:
  - `0`: success
  - `1`: general error
  - `2`: validation error
  - `3`: not found (missing template)
  - `4`: conflict (ID or issue file already exists)
- Errors must be written to stderr and include an actionable message.
