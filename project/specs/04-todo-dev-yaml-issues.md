# TODO compatibility and issue Markdown contract

## Objective

Define the current issue-centric model and how legacy TODO data coexists during migration.

## Canonical execution model (0.4.0)

- YODA Flow execution is driven by issue Markdown files in `yoda/project/issues/`.
- Canonical issue identifier is derived from filename `<dev>-<NNNN>-<slug>.md`.
- Issue front matter does not include `id`.

## Front matter schema (issue)

Canonical order:

- `schema_version`
- `status`: `to-do | doing | pending | done`
- `phase`: `study | document | implement | evaluate` (only when `status=doing`)
- `flow_prepared_until`: `study | document` (omit when empty)
- `pending_reason`: required when `status=pending` (omit otherwise)
- `depends_on`: list of issue IDs (omit when empty)
- `title`
- `description`
- `priority`: integer `0..10`
- `extern_issue_file`: path to external issue JSON (omit when empty)
- `created_at`
- `updated_at`

Required fields:

- `schema_version`
- `status`: `to-do | doing | pending | done`
- `title`
- `description`
- `priority`: integer `0..10`
- `created_at`
- `updated_at`

Conditional/optional fields:

- `phase`: `study | document | implement | evaluate` (only when `status=doing`)
- `flow_prepared_until`: `study | document` (omit when empty)
- `depends_on`: list of issue IDs (omit when empty)
- `pending_reason`: required when `status=pending`
- `extern_issue_file`: path to external issue JSON (omit when empty)

## Body contract

- `## Dependencies` section MUST NOT exist.
- `## Entry points` MUST be a simple list (`- <entry point>`).
- `## Flow log` MUST exist and use append-only single-line entries:
  - `- <ISO8601> <short-message>`
  - For new entries, `<short-message>` MUST NOT repeat the issue id (`<dev>-<NNNN>`) as a prefix.

## Filename validation

- Filename MUST match `<dev>-<NNNN>-<slug>.md`.
- Invalid filename MUST raise blocking error:
  - `INVALID_ISSUE_FILENAME: expected <dev>-<NNNN>-<slug>.md; got <filename>`

## Legacy TODO compatibility

- `yoda/todos/TODO.<dev>.yaml` may exist during migration and compatibility operations.
- Legacy TODO is not the canonical execution source for YODA Flow.
- Structural normalization is centralized in `init.py`:
  - normal init/update finalization migrates supported issue schemas
  - `--reconcile-layout` performs explicit layout reconciliation
- Package update modes belong to `update.py`:
  - `--check`: audit package updates without applying them
  - `--apply`: apply a package update, preserve project data, and run init when
    `--dev` is provided
- During transition, scripts may read legacy and new formats; structural conversion must not be implicit in helper scripts.

## Constraints

- `depends_on` references issues in the same repository scope.
- Empty optional metadata (`flow_prepared_until`, `depends_on`,
  `pending_reason`, `extern_issue_file`, `phase`) MUST be omitted.
- Timestamps use ISO 8601 with explicit timezone.
