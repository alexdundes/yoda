# Conventions

This file defines normative language and common conventions for the YODA Framework specs.

## Normative keywords

The following keywords are to be interpreted as in RFC 2119:

- MUST: absolute requirement
- SHOULD: strong recommendation
- MAY: optional

## Formats

- Dates and timestamps MUST use ISO 8601.
- Timezone MUST be explicit and use Brasilia time (America/Sao_Paulo) with offset.
- Text files MUST be UTF-8.

## Paths

- All paths MUST be relative to the repository root.

## Source of truth precedence

- For framework definition, project/specs is the source of truth.
- For a unit of work, the issue Markdown file is the source of truth over conversation.
- If templates conflict with specs, specs MUST win.

## Brand voice and terminology

Voice guidelines:

- Be clear, technical, and pragmatic.
- Prefer short sentences and active voice.
- Avoid marketing language, hype, or vague adjectives.
- Use normative keywords only for true requirements.
- Canonical specs and issue templates are written in English.
- Localized docs are allowed, but keep key terms in English.

Terminology rules:

- "YODA Framework" is the primary name; "YODA" is allowed after first mention.
- "YODA Flow" is the official name of the cycle; phases are Study, Document, Implement, Evaluate.
- Use "issue" for a unit of work; avoid "ticket" or "task" as the primary label.
- `TODO.<dev>.yaml` is the canonical TODO file; mention `TODO.<dev>.md` only as a bootstrap exception.
- Use "agent" for automated/AI actors and "script" for CLI automation in yoda/scripts.
- Tokens with angle brackets (example: `TODO.<dev>.yaml`) must use inline code in prose to avoid Markdown tag parsing.

## Notes

- When in doubt, prefer explicitness over inference.
