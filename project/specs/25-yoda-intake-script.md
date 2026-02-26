# yoda_intake.py specification

## Objective

Define the required behavior for `yoda_intake.py`, the script that returns AGENT runbooks for YODA Intake.

## Scope

- Define CLI modes and outputs for initial intake, local-only intake, and external-source intake.
- Define behavior when developer slug is missing.
- Define behavior when external source file is missing.
- Define output contract for markdown/json responses.

Out of scope:
- Fetching external issues from provider APIs (handled by `get_extern_issue.py`).
- Creating issues in TODO directly (handled by `issue_add.py`).

## Location

- Script path: `yoda/scripts/yoda_intake.py`
- External source folder: `yoda/project/extern-issues/`

## CLI

The script follows the global CLI contract in `project/specs/13-yoda-scripts-v1.md`.

Inputs:
- `--dev <slug>` (optional for initial guidance mode)
- `--extern-issue <NNN>` (optional; mutually exclusive with `--no-extern-issue`)
- `--no-extern-issue` (optional; mutually exclusive with `--extern-issue`)

Global flags:
- `--format md|json`
- `--json`
- `--dry-run`
- `--verbose`

## Behavior

### Mode A: missing developer slug

When `--dev` is not provided and `YODA_DEV` is not set:
- Return a runbook that instructs the agent to ask the human exactly:
  - `What is your YODA slug?`
- Do not prompt interactively.
- Exit with success.

### Mode B: initial intake (`--dev` only)

When only `--dev` is provided:
- Return initial runbook that branches to:
  - external path: `--extern-issue <NNN>`
  - local path: `--no-extern-issue`
- Exit with success.

### Mode C: local-only intake (`--dev --no-extern-issue`)

- Return full intake runbook for local-only flow.
- Runbook should include:
  - backlog review,
  - human demand collection,
  - issue creation guidance,
  - instruction to check `issue_add.py --help`.
- Exit with success.

### Mode D: external intake (`--dev --extern-issue <NNN>`)

- Validate `<NNN>` as numeric.
- Attempt to load local file from `yoda/project/extern-issues/<provider>-<NNN>.json`:
  - provider is inferred from git `origin` when possible;
  - fallback: first matching `*-<NNN>.json`.
- If file is missing:
  - return runbook instructing the agent to ask the human to run `get_extern_issue.py`.
  - include rerun instruction for `yoda_intake.py --extern-issue <NNN>`.
  - exit with success.
- If file exists:
  - return full external intake runbook.
  - include external issue summary metadata (without dumping full external body).
  - include `File: <absolute path>` in the summary.
  - exit with success.

## Output

Markdown mode (default):
- Human-readable runbook text.
- External summary block in Mode D when source file exists.

JSON mode:
- `mode`
- `dev` (when available)
- `runbook`
- `external_issue` (when available)
- `external_markdown` (when available)
- `external_file` (when available)

## Error handling

- Mutually exclusive violation (`--extern-issue` + `--no-extern-issue`) must return validation error (exit code 2).
- Non-numeric `--extern-issue` must return validation error (exit code 2).
- Unexpected runtime failures must return exit code 1.

