# YODA Agent Manual (Embedded)

Single-file guide for agents when the packaged YODA Framework is embedded in another project. Use this as the operative source; it does not rely on `project/specs/`.

## Table of contents
- Quick start
- Developer slug resolution
- Entering YODA Flow
- YODA Flow playbook (Study, Document, Implement, Evaluate, Lightweight)
- Blocking and pending
- Entering YODA Intake
- Scripts quick reference
- Files and paths in the package
- Exit and handoff

## Quick start
1) Confirm intent: user must say “YODA Flow” (or “YODA Intake” for backlog work).
2) Resolve developer slug (`--dev` > `YODA_DEV` env > ask user).
3) Run `python3 yoda/scripts/todo_next.py --dev <slug>` to pick the next selectable issue.
4) Ask: “Start YODA Flow for issue <id>?” If yes, set status to `doing` with `todo_update.py`.
5) Follow the playbook below; use only documented issue scope.

## Developer slug resolution
- Order: CLI `--dev` flag → `YODA_DEV` env var → prompt the user.
- Slug rules: lowercase ASCII, digits, hyphens; starts with a letter; no spaces.
- All TODO/issue paths depend on the slug (`yoda/todos/TODO.<dev>.yaml`).

## Entering YODA Flow
1) Confirm entry phrase includes “YODA Flow” and intent to take the highest-priority selectable issue.
   - When entering YODA Flow, the agent assumes the **Flow skin**.
2) Ensure no issue is already `doing`; if there is, pause and ask the user to resolve.
3) Run `todo_next.py`; surface pending/blocked info if present.
4) Ask for confirmation; if approved, mark the issue `doing` via `todo_update.py`.

## YODA Flow playbook
### Study
- Goal: understand the issue, constraints, and open questions.
- Deliverable: short chat summary + questions/decisions; wait for approval before Document.

### Document
- Update the issue Markdown (`yoda/project/issues/<id>-<slug>.md`) to reflect Study outcomes.
- Ensure acceptance criteria are clear and testable.
- Get human confirmation before coding.

### Implement
- Execute only what the issue states.
- Use scripts to update metadata; do not edit TODO files directly.
- Add/adjust tests if required by acceptance criteria or project norms.

### Evaluate
- Validate against acceptance criteria.
- Record a result log entry via `log_add.py`.
- Suggest a commit message (conventional): first line = message; body lines `Issue: <ID>`, `Path: <issue path>`.
- Update TODO status to `done` with `todo_update.py`; offer next issue via `todo_next.py`.

### Lightweight rule
- Allowed only if `lightweight: true` in the issue/TODO and scope is already clear.
- If ambiguity or risk appears, fall back to full flow (Study → Document).

## Blocking and pending
- If a blocker appears during Implement/Evaluate, set status `pending` with `todo_update.py --pending-reason "<reason>"`.
- Surface dependencies explicitly; do not proceed until resolved.
- When dependency is cleared, move back to `to-do` or `doing` as appropriate.

## Entering YODA Intake (backlog cycle)
Trigger: user wants to create/refine issues (e.g., “YODA Intake”).
Steps:
1) Confirm Intake entry.
   - When entering YODA Intake, the agent assumes the **Intake skin**.
2) Review backlog with `todo_list.py` to avoid duplicates.
3) Collect goals/constraints; shape issues until they meet Definition of Ready (clear title, context/objective, scope/out-of-scope, acceptance criteria, dependencies/risks).
4) Assign priority using baseline `5` by default; only use another value with explicit comparative justification versus open issues.
5) Create issues via `issue_add.py`; fill Markdown sections.
6) If priority is different from `5`, record a short rationale in the issue Markdown.
7) Review ordering (optionally `todo_reorder.py`).
8) Exit Intake explicitly and offer to start YODA Flow on the top selectable issue.

## Scripts quick reference
- `todo_list.py [--status ...] [--grep ...]`: list/filter issues; excludes `done` by default.
- `todo_next.py`: select highest-priority selectable issue; reports blockers/pending.
- `todo_update.py --issue <id> --status <status> [--priority ...] [--depends-on ...] [--pending-reason ...]`.
- `todo_reorder.py`: reorder TODO entries (if needed during Intake).
- `issue_add.py --title --description [--priority ...] [--tags ...] [--entrypoint ...]`: create new issue + log + TODO entry (default priority baseline is `5`).
- `log_add.py --issue <id> --message "<msg including id>" [--timestamp ...]`: append to issue log.
Notes:
- Always include the issue id in log messages (`[yoda-0001] ...`).
- Use `--dev <slug>` on all commands unless `YODA_DEV` is set.
- All scripts live in `yoda/scripts/`; run from repo root.
- During Intake, use priority `5` unless there is a clear relative reason to set another value.

## Files and paths in the package
- Manual: `yoda/yoda.md` (this file).
- TODO: `yoda/todos/TODO.<dev>.yaml` (one per developer).
- Issues: `yoda/project/issues/<id>-<slug>.md`.
- Logs: `yoda/logs/<id>-<slug>.yaml`.
- Templates: `yoda/templates/issue.md`, `yoda/templates/issue-lightweight-process.md`.
- Scripts: `yoda/scripts/*.py`.
- Package metadata: `yoda/PACKAGE_MANIFEST.yaml`, `CHANGELOG.yaml`, plus root `LICENSE` and `README`.

## Exit and handoff
- After Evaluate, propose the next issue via `todo_next.py` or exit Flow if the user prefers.
- If Intake just completed, explicitly close it and offer YODA Flow.
- Keep conversation concise; default language is English unless user prefers otherwise.
