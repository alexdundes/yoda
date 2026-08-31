# Issue template usage

## Objective

Define how issue templates are filled and maintained under the current 0.4.0 contract.

## Rules

1) Issue file name follows `<dev>-<NNNN>-<slug>.md`.
2) Front matter follows the schema 2.01 canonical order.
3) Do not include `id` in front matter.
4) Do not include `## Dependencies` section in body.
5) `## Entry points` must be simple list items:
   - `- <entry point>`
6) Include `## Flow log` and keep it empty in template.
7) `## Flow log` entries must follow:
   - `- <ISO8601> <short-message>`
   - For new entries, `<short-message>` must not start with issue id (`<dev>-<NNNN>`).
8) Keep `## Result log` empty in template; fill only during Evaluate.

## Metadata constraints

- `phase` only when `status=doing`.
- `flow_prepared_until` omitted when empty; accepted values are `study` and
  `document`.
- `pending_reason` required only for `status=pending` and omitted otherwise.
- `depends_on` omitted when empty.
- `extern_issue_file` omitted when empty.

## Migration and normalization

- Existing schema 2.00 issues are migrated by `init.py` to 2.01; package
  `--check`/`--apply` modes belong to `update.py`.
- Do not rely on manual bulk edits to enforce template shape across existing issues.
