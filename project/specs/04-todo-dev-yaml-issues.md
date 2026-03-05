# TODO compatibility and issue Markdown contract

## Objective

Define the 0.3.0 issue-centric model and how legacy TODO data coexists during migration.

## Canonical execution model (0.3.0)

- YODA Flow execution is driven by issue Markdown files in `yoda/project/issues/`.
- Canonical issue identifier is derived from filename `<dev>-<NNNN>-<slug>.md`.
- Issue front matter does not include `id`.

## Front matter schema (issue)

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
- `depends_on`: list of issue IDs (omit when empty)
- `pending_reason`: required when `status=pending`
- `extern_issue_file`: path to external issue JSON (omit when empty)

## Body contract

- `## Dependencies` section MUST NOT exist.
- `## Entry points` MUST be a simple list (`- <entry point>`).

## Filename validation

- Filename MUST match `<dev>-<NNNN>-<slug>.md`.
- Invalid filename MUST raise blocking error:
  - `INVALID_ISSUE_FILENAME: expected <dev>-<NNNN>-<slug>.md; got <filename>`

## Legacy TODO compatibility

- `yoda/todos/TODO.<dev>.yaml` may exist during migration and compatibility operations.
- Legacy TODO is not the canonical execution source for YODA Flow in 0.3.0.

## Constraints

- `depends_on` references issues in the same repository scope.
- Empty optional metadata (`depends_on`, `extern_issue_file`, `phase`) MUST be omitted.
- Timestamps use ISO 8601 with explicit timezone.
