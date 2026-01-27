# alex-0008 - Define issue metadata schema

## Summary
Define a formal schema for issue metadata (front matter or equivalent) and document where it lives. The schema must specify required fields, types, and constraints. This removes ambiguity for issue creation and validation.

## Context
Issues are stored as Markdown with metadata, but the schema for that metadata is not defined. Without a schema, issue files may diverge across agents.

## Objective
Specify the issue metadata schema and document it in the canonical specs.

## Scope
- Define required metadata fields and constraints.
- Clarify the canonical location/format for metadata (front matter or other).
- Update canonical specs and templates accordingly.

## Out of scope
- Implementing schema validation tooling.
- Changing the issue workflow beyond metadata definition.

## Requirements
- Schema is explicit and unambiguous.
- Metadata location and format are clearly defined.
- Canonical specs reflect the finalized schema.

## Acceptance criteria
- [ ] Issue metadata schema is documented in canonical specs.
- [ ] Metadata location and format are explicitly defined.

## Dependencies
None

## Entry points
- path: project/specs/03-document-first-yaml-markdown.md
  type: issue
- path: project/specs/04-todo-dev-yaml-issues.md
  type: issue
- path: yoda/templates/issue.md
  type: issue

## Implementation notes
- Keep the schema consistent with `TODO.<dev>.yaml` metadata expectations.

## Tests
Not applicable.

## Risks and edge cases
- Too many required fields could make issue creation heavy.

## Result log
Defined issue metadata as YAML front matter mirroring TODO fields, including required lightweight, and updated templates/specs.

Commit:
docs(specs): define issue metadata schema

Issue: alex-0008
Path: yoda/project/issues/alex-0008-schema-formal-metadata-issue.md
