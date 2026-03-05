# Conventions

This file defines normative language and shared conventions for YODA Framework specifications.

## Normative keywords

Keywords are interpreted as RFC 2119:

- MUST: absolute requirement
- SHOULD: strong recommendation
- MAY: optional

## Formats

- Dates and timestamps MUST use ISO 8601 with explicit timezone.
- UTC SHOULD be the default timezone for generated metadata.
- Text files MUST use UTF-8.

## Paths and naming

- All paths MUST be repository-relative.
- Issue file path pattern MUST be `<dev>-<NNNN>-<slug>.md` under `yoda/project/issues/`.
- Issue ID MUST be derived from the file name, not from front matter fields.

## Source of truth precedence

- For framework definition, `project/specs/` is the source of truth.
- For execution in YODA Flow, the issue Markdown file is the source of truth.
- If template text conflicts with specs, specs MUST win.

## Terminology

- Primary name: "YODA Framework" ("YODA" allowed after first mention).
- Official cycle name: "YODA Flow".
- Official phases: `study`, `document`, `implement`, `evaluate`.
- Use "issue" for units of work.
- Use "agent" for AI actor and "script" for CLI automation.

## Metadata conventions

- Issue front matter canonical order for 0.3.0:
  - `schema_version`
  - `status`
  - `phase` (only when `status=doing`)
  - `depends_on` (optional, omitted if empty)
  - `title`
  - `description`
  - `priority`
  - `extern_issue_file` (optional, omitted if empty)
  - `created_at`
  - `updated_at`
- `id` MUST NOT exist in front matter.
- `phase` MUST be omitted unless `status=doing`.

## Logging conventions

- Log entries MUST be compact and single-line.
- `runbook_line` outputs MUST be single-line and imperative.

## Notes

- Prefer explicit requirements over implicit interpretation.
