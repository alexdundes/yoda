# YODA Framework - Decision Summary

This file records decisions and known open points captured so far.

## Decisions captured so far

- Conventions: RFC 2119 keywords govern requirements; timestamps must be ISO 8601 with explicit timezone; UTC is preferred; text files are UTF-8; paths are repo-relative; slugs are immutable once created.
- Source of truth precedence: `project/specs/` defines the framework; for work execution the issue Markdown file is the source of truth; specs override templates on conflict.
- Voice and terminology: clear/technical/pragmatic English for canonical specs; key terms in English; YODA Framework/YODA Flow naming; use “issue” for work units; `yoda/todos/TODO.<dev>.yaml` is the canonical TODO.
- Framework definition: document-first approach (YAML metadata + Markdown narrative), agents/scripts execute what is documented; README is the human entrypoint; `yoda/yoda.md` is the agent entrypoint.
- YODA Flow: Study → Document → Implement → Evaluate with explicit deliverables; lightweight flow can skip Study/Document only when issue is already clear and marked `lightweight: true`; otherwise return to Study.
- Repository structure: required folders under `yoda/` (templates, scripts, logs, todos, project/issues) plus `project/specs/` as source of truth.
- TODO + issue model: one TODO per developer at `yoda/todos/TODO.<dev>.yaml`; one issue Markdown file per issue at `yoda/project/issues/<id>-<slug>.md`.
- IDs and slugs: canonical id `<dev>-<NNNN>`; slug is lowercase ASCII, digits, hyphen, starts with letter; slugs are immutable and renames require migration.
- TODO schema: required root fields include schema_version, developer name/slug, timezone, updated_at, issues; issue items include id/title/slug/description/status/priority/lightweight/agent/depends_on/pending_reason/created_at/updated_at with optional entrypoints/tags/origin.
- Status/state machine: to-do → doing → done; any state can go pending; pending requires pending_reason and is resolved via todo_update.
- Dependencies: `depends_on` uses canonical ids within the same TODO (no cross-dev); selection must ensure dependencies are done.
- Deterministic selection: `todo_next.py` selects highest priority then list order; blocks if any issue is doing; reports pending/blocked hints.
- Issue metadata in Markdown: YAML front matter mirrors TODO fields; issue title must include the ID.
- Logs: one YAML log per issue in `yoda/logs/<id>-<slug>.yaml`; append-only; entries include timestamp + message; log status mirrors TODO; update logs on script actions.
- Scripts policy: scripts are mandatory for metadata changes when available; scripts live in `yoda/scripts/`, Python, file name = command name.
- CLI contract: global flags (`--dev`, `--format`, `--json`, `--dry-run`, `--verbose`); exit codes 0/1/2/3/4; errors to stderr with actionable messages.
- JSON output minimums defined for `issue_add.py`, `todo_update.py`, `log_add.py`, `todo_next.py`.
- `todo_list.py` JSON output uses full issue items.
- Required scripts (v1): issue_add, todo_list, todo_update, todo_next, todo_reorder, log_add.
- Script behavior specs defined for: todo_list, todo_reorder, issue_add, todo_update, log_add, todo_next (validation, conflicts, output, and log rules).
- Python structure: shared helpers in `yoda/scripts/lib/`, pytest for tests, dependencies in `yoda/scripts/requirements.txt`.
- Issue templates: standard vs lightweight, required fill-in rules, and commit text format embedded in the issue result log.
- Agent entry: `AGENTS.md`/`gemini.md` route to `yoda/yoda.md`; entry phrase must mention YODA Flow and intent to take highest-priority selectable issue; resolve dev via flag/env/prompt.
- Out of scope (v1) is defined in `project/specs/22-out-of-scope.md`.
- Visual identity: monochrome document icon with Y; simple lines, no extra elements.
- MCP: future v2 direction (minimal tools: todos.list/docs.read/workspace.apply_patch), with noted risks and benefits.
- Influences: DocDD/RDD/Docs-as-Code/Design-first/ADRs/Literate Programming/Agentic Design Patterns inform guidance and vocabulary.
- Distribution and packaging: default artefact `tar.gz` named `yoda-framework-<semver+build>`, manifest `yoda/PACKAGE_MANIFEST.yaml`, structured changelog `CHANGELOG.yaml`, excludes `project/specs` and runtime data; `package`/`init` must follow this contract. (see `23-distribution-and-packaging.md`)
- Installation and upgrade: install via one-liner (with warnings) or manual flow; updates use `latest.json` metadata + checksum; preserve YODA data folders; rollback to `yoda/_previous/<version>`; license lives at `yoda/LICENSE`. (see `24-installation-and-upgrade.md`)

## Open decisions (not finalized)

None.
