# YODA Framework - Decision Summary

This file records decisions and known open points captured so far.

## Decisions captured so far

- Scope: YODA Framework is not just documentation. It is a document-first way of working plus scripts that operationalize the flow (generate, consult, validate docs and tasks).
- Documentation structure: prefer more YAML metadata and use scripts (Python) that generate Markdown optimized for AI consumption and human review.
- YODA Flow: the core cycle is study -> document -> implement -> evaluate/iterate.
- Artifacts direction: one TODO per developer (TODO.dev.yaml) and one Markdown file per issue for richer free-form descriptions, with scripts generating the issue skeleton.
- Issues location and naming: issues live in yoda/project/issues/ and follow dev-id-slug.md.
- Issue identification: ID appears in the Markdown title.
- Metadata schema basics: id, title, slug, description, entrypoints, status, priority, labels, agent, depends_on, pending_reason, created_at, updated_at.
- Status values: to-do, doing, do-it, pending (pending = blocker recorded in pending_reason).
- Agent entry file: yoda/yoda.md, with AGENTS.md or gemini.md pointing to it.
- Process light: skip the Study step and follow the preliminary issue.
- Simplicity: keep the flow scriptable and avoid unnecessary complexity in formats.
- Name: use "YODA Framework" as the primary name (with the Y linked to YAML).
- Scripts: live in yoda/scripts, written in Python, file name is the command; init.py is mandatory.
- Scripts v1 include issue_add.py to create TODO entries and issue Markdown from templates using basic fields.
- Logs: one YAML log per issue at yoda/logs/dev-id-slug.yaml.
- Commit: include the commit message text inside the issue and show it to the user using this format:
  - First line: conventional commit message.
  - Body:
    - Issue: <ID>
    - Path: <issue path>

## Open decisions (not finalized)

- Tooling policy: is tooling mandatory (prescriptive) or recommended (optional)?
- Audience: official positioning (solo devs vs teams/consultancies vs SaaS/multi-tenant).
- Flow deliverables: minimum required artifacts per phase.
- Metadata schema: any additional required fields beyond the basics.
- Scripts v1: exact CLI interface and command list beyond init.py and TODO maintenance/display.
- Scope boundaries: explicit out-of-scope items (CI/CD, architecture standards, PM, HR, etc.).
- Stack profiles: generic-only or profiles per stack (web/data/backend).
- Brand voice: guideline for tone and terminology.
- Issue template: file location and required sections.
