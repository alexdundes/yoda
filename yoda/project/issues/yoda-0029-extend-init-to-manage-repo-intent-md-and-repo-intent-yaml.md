---
schema_version: '2.00'
status: done
title: Extend init to manage REPO_INTENT.md and repo.intent.yaml
description: Update init.py to create REPO_INTENT.md when missing and append a YODA
  block when present; apply the same concept to repo.intent.yaml without overwriting
  existing content.
priority: 6
created_at: '2026-02-04T20:16:53-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0029 - Extend init to manage REPO_INTENT.md and repo.intent.yaml

## Summary
Extend `init.py` to manage repository intent files in embedded projects. When `REPO_INTENT.md` or `repo.intent.yaml` are missing, init should create them; when they exist, init should append/merge YODA information without overwriting existing content. This keeps agent onboarding consistent with the YODA entry points.

## Context
After installation, agent files reference `REPO_INTENT.md`, but host projects often lack it. This creates broken onboarding instructions for new agents. There is also a `repo.intent.yaml` convention that should capture YODA’s embedded context; init does not populate it today.

## Objective
Ensure `init.py` creates or updates `REPO_INTENT.md` and `repo.intent.yaml` in a safe, idempotent, and non-destructive way.

## Scope
- Update `yoda/scripts/init.py` to create `REPO_INTENT.md` if missing.
- When `REPO_INTENT.md` exists, append or update a YODA block using markers (no destructive overwrite).
- Create `repo.intent.yaml` if missing with a minimal YODA section.
- When `repo.intent.yaml` exists, merge in a YODA section without removing existing keys.
- Ensure `--dry-run` reports planned changes without writing.
- Add pytest coverage in `yoda/scripts/tests/test_init.py` for the new behaviors.

## Out of scope
- Rewriting or reformatting the host project’s existing intent content.
- Migrating other metadata formats or custom repository files.

## Requirements
- Idempotent behavior: re-running init does not duplicate blocks.
- No destructive overwrite of existing `REPO_INTENT.md` or `repo.intent.yaml` content.
- If YAML parsing fails for `repo.intent.yaml`, do not modify the file and report a conflict.
- REPO_INTENT.md block should include the YODA entry guidance and point to `yoda/yoda.md`.

## Acceptance criteria
- [ ] `init.py` creates `REPO_INTENT.md` when missing and includes a YODA block.
- [ ] `init.py` appends/updates the YODA block in existing `REPO_INTENT.md` without overwriting prior content.
- [ ] `init.py` creates `repo.intent.yaml` when missing with a YODA section.
- [ ] `init.py` merges a YODA section into existing `repo.intent.yaml` while preserving other keys.
- [ ] `--dry-run` does not write changes.
- [ ] Tests cover create + idempotent + preserve behaviors.


## Entry points
- `yoda/scripts/init.py`
- `REPO_INTENT.md`
- `repo.intent.yaml`

## Implementation notes
- Reuse the existing YODA block markers for `REPO_INTENT.md` (or introduce a similar marker) to keep updates idempotent.
- For `repo.intent.yaml`, add a top-level `yoda` section (e.g., `embedded: true`, `manual: yoda/yoda.md`, `agent_entry_order`) without altering existing keys.
- Preserve formatting where possible; when re-serializing YAML, use safe_dump with stable ordering.

## Tests
Update `yoda/scripts/tests/test_init.py` to cover:
- Creating `REPO_INTENT.md` and `repo.intent.yaml`.
- Appending/merging without overwriting.
- Idempotency on re-run.

## Risks and edge cases
- Existing files with incompatible formatting (invalid YAML or missing markers).
- Projects with strict formatting expectations for intent files.

## Result log
- Added REPO_INTENT.md creation/upsert with YODA markers and default content.
- Added repo.intent.yaml creation and merge behavior for a YODA section.
- Extended init tests to cover repo intent creation, merge, and idempotency.
- Tests: `python3 -m pytest yoda/scripts/tests/test_init.py`

Commit message:
feat(init): manage repo intent files

Issue: yoda-0029
Path: yoda/project/issues/yoda-0029-extend-init-to-manage-repo-intent-md-and-repo-intent-yaml.md

## Flow log
- 2026-02-04T20:16:53-03:00 issue_add created | title: Extend init to manage REPO_INTENT.md and repo.intent.yaml | description: Update init.py to create REPO_INTENT.md when missing and append a YODA block when present; apply the same concept to repo.intent.yaml without overwriting existing content. | slug: extend-init-to-manage-repo-intent-md-and-repo-intent-yaml | priority: 6 | entrypoints: yoda/scripts/init.py:code, REPO_INTENT.md:doc, repo.intent.yaml:config
- 2026-02-06T09:00:53-03:00 todo_update | status: to-do -> doing
- 2026-02-06T09:06:00-03:00 Extended init to create/update REPO_INTENT.md and repo.intent.yaml with YODA data; added tests.
- 2026-02-06T09:06:04-03:00 todo_update | status: doing -> done
