# get_extern_issue.py specification

## Objective

Define the required behavior for `get_extern_issue.py`, the script that fetches an external issue and stores it as local JSON for YODA Intake.

## Scope

- Define provider detection via git `origin`.
- Define authenticated and public transport selection and API fetch behavior.
- Define local file output path and naming.
- Define next-step guidance output for intake continuation.

Out of scope:
- Running intake decomposition itself (handled by `yoda_intake.py`).
- Issue creation in TODO (handled by `issue_add.py`).

## Location

- Script path: `yoda/scripts/get_extern_issue.py`
- Output folder: `yoda/project/extern_issues/`
- Output file pattern:
  - GitHub: `github-<NNN>.json`
  - GitLab: `gitlab-<NNN>.json`

## CLI

The script follows the global CLI contract in `project/specs/13-yoda-scripts-v1.md`.

Required inputs:
- `--dev <developer-slug>`
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
5) Select transport:
   - GitLab and GitHub Enterprise require their authenticated provider CLI.
   - For `github.com`, prefer authenticated `gh api` when `gh auth status` is
     ready.
   - For `github.com`, fall back to unauthenticated public HTTP when `gh` is
     absent, authentication is not ready, or an authenticated request fails
     specifically because of authentication/permission.
   - Do not turn network, invalid-payload, or rate-limit failures from the
     authenticated transport into a silent public fallback.
6) Fetch external issue data via provider API helper, including activity log:
   - GitHub: issue details + comments + timeline/events.
   - GitLab: issue details + notes.
   - Both GitHub transports share normalization, deterministic ordering and
     deduplication.
   - Each activity endpoint is limited to `per_page=100`; pagination beyond
     that limit is not part of this contract.
7) For public GitHub HTTP, use the standard-library client with a timeout and
   send `User-Agent`, `Accept: application/vnd.github+json`, and an explicit
   GitHub API version. Do not send a token.
8) Persist JSON to `yoda/project/extern_issues/<provider>-<NNN>.json`.
9) Report transport as `authenticated-cli` or `public-http` in command output,
   but do not add transport metadata to the stored external-issue JSON.
10) Output one explicit continuation command:
   - `python3 yoda/scripts/yoda_intake.py --dev <developer-slug> --extern-issue <NNN>`

For GitHub timeline collection, failure of the timeline endpoint may fall back
to the events endpoint only when that endpoint is specifically unavailable.
Network, authentication, permission, invalid-payload, and rate-limit errors
must remain visible.

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
- `log`

`log` entry minimum keys:
- `type`
- `id`
- `author`
- `created_at`
- `updated_at`
- `body`
- `url`

## Output

Markdown mode (default):
- provider
- external issue number
- transport
- saved file path
- next-step command line

JSON mode:
- `dev`
- `provider`
- `issue_number`
- `origin_url`
- `repo_slug`
- `transport`
- `external_issue`
- `saved_file`
- `dry_run`

## Error handling

- Missing required flags must return validation error (exit code 2).
- Non-numeric external id must return validation error (exit code 2).
- Missing/unsupported origin or provider must return not-found (exit code 3).
- Missing CLI or invalid auth must return not-found (exit code 3) with an
  actionable message when no public fallback applies.
- A public `401`, `403`, or `404` must not claim that a resource is certainly
  absent. It must explain that the resource was not found or is not publicly
  accessible and instruct the operator to authenticate `gh` for private data.
- Public rate limit must be distinguished from ordinary access and network
  failures, using available rate-limit/retry headers in actionable guidance.
- API, network, invalid-payload, or unexpected runtime failures must return
  general error (exit code 1).
- Errors and outputs must not reveal or persist credentials.
