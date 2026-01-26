# YODA Framework - Decision Summary

This file records decisions and known open points captured so far.

## Decisions captured so far

- Scope: YODA Framework is not just documentation. It is a document-first way of working plus scripts that operationalize the flow (generate, consult, validate docs and tasks).
- Documentation structure: prefer more YAML metadata and use scripts (Python) that generate Markdown optimized for AI consumption and human review.
- YODA Flow: the core cycle is Study -> Document -> Implement -> Evaluate.
- Artifacts direction: one TODO per developer (`yoda/todos/TODO.<dev>.yaml`) and one Markdown file per issue for richer free-form descriptions, with scripts generating the issue skeleton.
- Issues location and naming: issues live in yoda/project/issues/ and follow `<id>-<slug>.md`.
- Slug format (dev and issue): lowercase ASCII, digits, and hyphens only; must start with a letter; no spaces.
- Issue identification: ID appears in the Markdown title.
- Metadata schema basics: id, title, slug, description, status, priority, lightweight, tags, agent, depends_on, pending_reason, created_at, updated_at (entrypoints and origin are optional).
- Issue metadata in Markdown: issue files must include YAML front matter that mirrors the TODO fields.
- Status values: to-do, doing, done, pending (pending = blocker recorded in pending_reason).
- Agent entry file: yoda/yoda.md, with AGENTS.md or gemini.md pointing to it.
- Entry trigger phrase: must mention "YODA Flow" (or "YODA") and intent to take the highest-priority issue without dependencies.
- Process light: skip the Study step and follow the preliminary issue, only when the issue is already clear with explicit acceptance criteria and no open questions.
- Simplicity: keep the flow scriptable and avoid unnecessary complexity in formats.
- Name: use "YODA Framework" as the primary name (with the Y linked to YAML).
- Brand voice and terminology: clear, technical, pragmatic; English for canonical specs; standardized terms (YODA Framework, YODA Flow, issue, `yoda/todos/TODO.<dev>.yaml`, agent, script).
- Stack profiles: YODA v1 is stack-agnostic; profiles are optional, future extensions outside the core.
- Tooling policy: scripts are mandatory when available; bootstrap is the only exception.
- Audience and positioning: primary audience is solo developers (one human + one agent); general-purpose framework for tighter control of agent-assisted development.
- Scope boundaries: out-of-scope items are defined in the v1 list.
- Flow deliverables: Study/Document/Implement/Evaluate minimums defined, with explicit lightweight rule.
- Scripts: live in yoda/scripts, written in Python, file name is the command; init.py is mandatory.
- Scripts v1 include issue_add.py to create TODO entries and issue Markdown from templates using basic fields, and issue_render.py to re-render issue Markdown from templates.
- Logs: one YAML log per issue at `yoda/logs/<id>-<slug>.yaml`.
- Bootstrap exception: while scripts do not exist, use `yoda/todos/TODO.<dev>.md` and Markdown logs at `yoda/logs/<id>-<slug>.md`; bootstrap is temporary.
- Commit: include the commit message text inside the issue and show it to the user using this format:
  - First line: conventional commit message.
  - Body:
    - Issue: `<ID>`
    - Path: `<issue path>`

## Open decisions (not finalized)

None.
