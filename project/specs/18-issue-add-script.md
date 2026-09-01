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
- `--priority <0..10>`: optional integer priority. Omit it for the normal
  baseline `5`; provide it only for a justified exception to natural order.
- `--extern-issue <NNN>`: generate `extern_issue_file` pointing to `../extern_issues/<provider>-<NNN>.json`.
- `--source-doc <path>`: optional base documentation already present in the consumer project.

Global flags:
- `--dev <developer-slug>`
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
   - If missing, return guidance instructing the agent to ask the human for the developer slug and rerun with `--dev <developer-slug>`.
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
- `schema_version: "2.01"`
- `title`, `description`
- `status: to-do`
- `priority`
- `created_at`, `updated_at` (same timestamp)
- `extern_issue_file`:
  - when `--extern-issue` is provided, MUST be set to a relative path from `yoda/project/issues/` to `yoda/project/extern_issues/<provider>-<NNN>.json`;
  - example: `../extern_issues/github-2.json`.

Metadata policy:
- `id` is derived from the filename and MUST NOT be persisted in front matter.
- `slug` is represented by the issue filename (`<id>-<slug>.md`) and must not be persisted in front matter.
- `source_doc`:
  - when `--source-doc` is provided, MUST be normalized before writing, in this order:
    1) expand `~`; 2) resolve a relative value against the current working directory;
    3) resolve `..` and symlinks; 4) require containment inside the project root;
    5) require the path to exist, as a file or a directory; 6) store the project
    relative form with POSIX separators, without a leading `./` and without a
    trailing slash;
  - a value outside the project root, a value that does not exist, or the project
    root itself MUST fail with the validation exit code and MUST NOT create the issue;
  - the absolute prefix of the developer machine MUST NOT reach the front matter;
  - when the flag is absent, the field MUST be omitted.
- Optional empty fields (`depends_on`, `pending_reason`, `extern_issue_file`, `source_doc`) must be omitted.
- `depends_on` starts empty by default and is written only when non-empty.

Priority policy for issue creation:
- If `--priority` is omitted, the created issue must use `5` (baseline).
- Omitting `--priority` is the normal path. The agent must not rank issues in a
  batch or assign different values to encode their planned sequence.
- Natural order resumes `doing`, defers unresolved real dependencies, and then
  follows stable issue ID order among baseline-priority issues. Create a batch
  in its desired natural order and use `depends_on` only when one issue cannot
  be executed correctly before another.
- Values above `5` anticipate and values below `5` postpone an issue relative to
  natural order. Either direction requires a relative reason recorded in the
  issue Markdown; no new front-matter field is introduced.
- A human request to advance or postpone work is valid justification. Generic
  importance is not.

Valid exception example:

> Use a value above `5` so this issue precedes the available backlog because
> every new capture continues losing data needed for recovery.

Invalid exception example:

> Use priority `9` because this issue is very important.

Timestamps:
- Detect the local system timezone; do not depend on a TODO YAML root.
- Format timestamps as ISO 8601 with explicit offset.

## Logging

- The script must append a line in the issue `## Flow log` section on successful creation.
- The initial message should mention issue creation, title, and priority.
- `--dry-run` must not append flow log entries.

## Output

On success, the script outputs a short summary in the chosen format, including:
- `issue_id`
- `issue_path`
- `template`
- `dry_run`

## Error handling

- Exit codes must follow the global contract:
  - `0`: success
  - `1`: general error
  - `2`: validation error
  - `3`: not found (missing template)
  - `4`: conflict (ID or issue file already exists)
- Errors must be written to stderr and include an actionable message.
