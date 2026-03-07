# Issue template usage

## Objective

Define how issue templates are filled and maintained under 0.3.0.

## Rules

1) Issue file name follows `<dev>-<NNNN>-<slug>.md`.
2) Front matter follows the 0.3.0 canonical order.
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
- `depends_on` omitted when empty.
- `extern_issue_file` omitted when empty.

## Migration and normalization

- Existing issues are normalized by `init.py` (`--check`/`--apply`) according to 0.3.0.
- Do not rely on manual bulk edits to enforce template shape across existing issues.
