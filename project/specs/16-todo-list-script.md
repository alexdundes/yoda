# todo_list.py specification

## Objective

Define the required behavior for `todo_list.py`, the script that lists and filters issues from `yoda/todos/TODO.<dev>.yaml`.

## Scope

- Define CLI inputs and outputs for `todo_list.py`.
- Define default selection and ordering rules.
- Define optional filters and alternate ordering modes.
- Define text/regex search behavior across issue Markdown files.

Out of scope:
- Implementing `todo_list.py`.
- Changing schemas outside this spec.

## Location

- Script path: `yoda/scripts/todo_list.py`
- TODO path: `yoda/todos/TODO.<dev>.yaml`
- Issue path: `yoda/project/issues/<id>-<slug>.md`

## CLI

The script follows the global CLI contract in `project/specs/13-yoda-scripts-v1.md`.

Optional inputs:
- `--dev <slug>`
- `--status <csv>`: filter by status (comma-separated).
- `--tags <csv>`: filter by tags (comma-separated).
- `--agent <text>`: filter by agent name (exact match).
- `--priority-min <n>`: minimum priority (0..10).
- `--priority-max <n>`: maximum priority (0..10).
- `--depends-on <id>`: include issues that list this id in `depends_on`.
- `--lightweight <true|false>`: filter by lightweight value.
- `--created-from <iso8601>`: inclusive lower bound for `created_at`.
- `--created-to <iso8601>`: inclusive upper bound for `created_at`.
- `--updated-from <iso8601>`: inclusive lower bound for `updated_at`.
- `--updated-to <iso8601>`: inclusive upper bound for `updated_at`.
- `--order <mode>`: override ordering (see Ordering).
- `--grep <pattern>`: search in selected issue Markdown files using a regex pattern.
- `--case-sensitive`: make `--grep` search case-sensitive (default is case-insensitive).

Global flags:
- `--format md|json`
- `--json`
- `--dry-run`
- `--verbose`

## Behavior

1) Resolve developer slug using the standard order: `--dev`, `YODA_DEV`, interactive prompt.
2) Load `yoda/todos/TODO.<dev>.yaml`. If missing, exit with code 3.
3) Validate the TODO schema. If validation fails, exit with code 2.
4) Apply filters (see Filters).
5) Apply ordering (see Ordering).
6) If `--grep` is provided, apply text search to the selected issues (see Text search).
7) Output the results in the selected format.

## Filters

Defaults:
- If `--status` is not provided, include only issues with status != `done` and exclude `pending` from the table list.

Filter rules:
- `--status`: include issues whose status is in the list.
- `--tags`: include issues that have **all** of the provided tags.
- `--agent`: include issues whose `agent` matches exactly.
- `--priority-min` / `--priority-max`: include issues within the inclusive range.
- `--depends-on`: include issues where `depends_on` contains the provided id.
- `--lightweight`: include issues whose `lightweight` matches the provided value.
- `--created-from` / `--created-to`: include issues whose `created_at` is within the inclusive range.
- `--updated-from` / `--updated-to`: include issues whose `updated_at` is within the inclusive range.

Date filters:
- Input timestamps must be ISO 8601 with explicit timezone.
- Invalid timestamps must return validation error (exit code 2).

## Ordering

### Default (execution order)

- Primary: priority (descending).
- Tie-breaker: order in the YAML list (top to bottom).
- Dependency adjustment: if an issue depends on another issue that is not `done`, the dependent issue must appear **after** that dependency.

Dependency adjustment must be stable and deterministic:
- Start from the priority/YAML ordered list.
- For each issue, if it depends on any issue not `done`, move it after its unresolved dependencies while preserving relative order as much as possible.
- If cycles exist, keep YAML order and do not error.

### Alternate ordering (`--order`)

Supported modes:
- `created-asc`: `created_at` ascending, tie-breaker YAML order.
- `created-desc`: `created_at` descending, tie-breaker YAML order.
- `updated-asc`: `updated_at` ascending, tie-breaker YAML order.
- `updated-desc`: `updated_at` descending, tie-breaker YAML order.

## Text search

When `--grep <pattern>` is provided:
- Apply filters and ordering first.
- Search **only** the selected issues’ Markdown files.
- Treat `<pattern>` as a regular expression.
- Search is **case-insensitive by default**; `--case-sensitive` enables case-sensitive matching.
- If the regex is invalid, exit with code 2 (validation error).
- If an issue Markdown file does not exist, skip it silently.

Output when `--grep` is used (Markdown format):
- Do not render a table.
- Render a readable, flowing Markdown output:
  - Issue header line with id, title, and relative path.
  - One line per match showing the full matching line (optionally prefixed with line number).

## Output

### Markdown (default, no `--grep`)

- If there are `pending` issues in the selection, render a **pending alert block** before the table:
  - A clear alert-style header.
  - Issue id, title, status, and `pending_reason`.
  - These pending issues are **not** included in the table list.
- Render a table with concise columns for readability by humans and agents.
- Columns should include at least: `id`, `status`, `priority`, `title`.
- The table must respect reasonable column widths for typical terminal widths.

### Markdown (with `--grep`)

- Use flowing text format as described in Text search.

### JSON (`--format json` or `--json`)

- The JSON output should include an array of issues with **all issue fields** from the TODO item (including `pending_reason`).

## Error handling

- Exit codes follow the global contract:
  - `0`: success
  - `1`: general error
  - `2`: validation error
  - `3`: not found (missing TODO)
  - `4`: conflict (unused by todo_list in v1)
- Errors must be written to stderr and include an actionable message.
