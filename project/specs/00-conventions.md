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

## Independence and self-containment

- `project/specs/` is a portable unit: a normative rule MUST be interpretable
  from the specification set alone, without an issue backlog, Flow logs, or Git
  history.
- A concrete issue identifier, an issue file link, or a commit MUST NOT be used
  as normative authority; the rule and its rationale belong in the spec.
- Generic references to the issue model the product implements, such as
  `yoda/project/issues/<dev>-<NNNN>-<slug>.md`, remain part of the contract.
- Traceability runs `issue -> spec`, never `spec -> issue`.
- Full rules in `project/specs/28-spec-independence-and-portability.md`.

## Terminology

- Primary name: "YODA Framework" ("YODA" allowed after first mention).
- Official cycle name: "YODA Flow".
- Official phases: `study`, `document`, `implement`, `evaluate`.
- Use "issue" for units of work.
- Use "agent" for AI actor and "script" for CLI automation.

## Metadata conventions

- Operational baseline: YODA Framework 0.4.0.
- Current issue schema: `2.01`.
- Readers MUST accept conforming `2.00` data during the 2.01 migration window;
  writers that mutate issue front matter MUST persist `2.01`.
- Issue front matter canonical order:
  - `schema_version`
  - `status`
  - `phase` (only when `status=doing`)
  - `flow_prepared_until` (optional, omitted if empty)
  - `pending_reason` (required when `status=pending`, omitted otherwise)
  - `depends_on` (optional, omitted if empty)
  - `title`
  - `description`
  - `priority`
  - `extern_issue_file` (optional, omitted if empty)
  - `created_at`
  - `updated_at`
- `id` MUST NOT exist in front matter.
- `phase` MUST be omitted unless `status=doing`.
- `flow_prepared_until` accepts only `study` or `document`.

Schema 2.01 adds an optional field but also enforces existing normative rules
that schema 2.00 readers previously tolerated: `pending` requires a non-empty
`pending_reason`, and timestamps require ISO 8601 with an explicit offset.
Index loading is fail-fast across a developer's issue set. Use
`todo_update.py --status pending --pending-reason <reason>` for a missing reason;
repair invalid timestamps in the issue front matter before retrying. `init.py`
updates the schema marker but does not invent these values.

## Logging conventions

- Log entries MUST be compact and single-line.
- `runbook_line` outputs MUST be imperative and as compact as the instruction
  allows; they MAY span more than one line. This does not relax the single-line
  rule for log entries above.

## Notes

- Prefer explicit requirements over implicit interpretation.
