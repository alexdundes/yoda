# Document-first, YAML, and Markdown

## Document-first principle

- Documentation comes before implementation.
- Code and script behavior are consequences of the documented contract.
- Agents MUST follow documented contracts, not informal assumptions.

## Role of Markdown

- Issue Markdown files are the primary execution contract for YODA Flow.
- Narrative, scope, acceptance criteria, and result context live in Markdown.

## Role of YAML

- YAML front matter carries machine-readable issue metadata.
- Metadata must remain minimal, deterministic, and schema-driven.

## 0.3.0 direction

- Source of truth for flow execution is the issue `.md` file.
- Front matter no longer stores `id`; ID is derived from filename.
- `depends_on` remains only in front matter (no duplicate section in body).
- `phase` is conditional and only serialized when `status=doing`.

## Guardrails

- If issue text is ambiguous, return to document phase before implementing.
- Do not invent paths or files; verify repository structure first.
- Any spec change must be tracked by an issue.
