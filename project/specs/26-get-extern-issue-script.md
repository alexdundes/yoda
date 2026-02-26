# get_extern_issue.py specification

## Objective

Define the required behavior for `get_extern_issue.py`, the script that fetches an external issue and stores it as local JSON for YODA Intake.

## Scope

- Define provider detection via git `origin`.
- Define provider CLI/auth checks and API fetch behavior.
- Define local file output path and naming.
- Define next-step guidance output for intake continuation.

Out of scope:
- Running intake decomposition itself (handled by `yoda_intake.py`).
- Issue creation in TODO (handled by `issue_add.py`).

## Location

- Script path: `yoda/scripts/get_extern_issue.py`
- Output folder: `yoda/project/extern-issues/`
- Output file pattern:
  - GitHub: `github-<NNN>.json`
  - GitLab: `gitlab-<NNN>.json`

## CLI

The script follows the global CLI contract in `project/specs/13-yoda-scripts-v1.md`.

Required inputs:
- `--dev <slug>`
- `--extern-issue <NNN>`

Global flags:
- `--format md|json`
- `--json`
- `--dry-run`
- `--verbose`

## Behavior

1) Validate `--dev` slug.
2) Validate `--extern-issue` as numeric.
3) Detect `origin` URL from git config (`remote.origin.url`) unless override is provided by env.
4) Infer provider from host:
   - host containing `github` => GitHub
   - host containing `gitlab` => GitLab
   - otherwise: explicit not-found error.
5) Ensure required CLI exists:
   - GitHub: `gh`
   - GitLab: `glab`
6) Ensure CLI authentication is ready (`auth status`).
7) Fetch external issue data via provider API helper.
8) Persist JSON to `yoda/project/extern-issues/<provider>-<NNN>.json`.
9) Output concise summary plus one explicit continuation command:
   - `python3 yoda/scripts/yoda_intake.py --dev <slug> --extern-issue <NNN>`

## Stored JSON shape

Minimum keys:
- `provider`
- `number`
- `title`
- `description`
- `state`
- `author`
- `url`
- `labels`

## Output

Markdown mode (default):
- provider
- external issue number
- saved file path
- next-step command line

JSON mode:
- `dev`
- `provider`
- `issue_number`
- `origin_url`
- `repo_slug`
- `external_issue`
- `saved_file`
- `dry_run`

## Error handling

- Missing required flags must return validation error (exit code 2).
- Non-numeric external id must return validation error (exit code 2).
- Missing/unsupported origin or provider must return not-found (exit code 3).
- Missing CLI or invalid auth must return not-found (exit code 3) with actionable message.
- API or unexpected runtime failures must return general error (exit code 1).

