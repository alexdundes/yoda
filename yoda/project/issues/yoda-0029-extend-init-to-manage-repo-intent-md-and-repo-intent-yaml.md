---
agent: Human
created_at: '2026-02-04T20:16:53-03:00'
depends_on: []
description: Update init.py to create REPO_INTENT.md when missing and append a YODA
  block when present; apply the same concept to repo.intent.yaml without overwriting
  existing content.
entrypoints:
- path: yoda/scripts/init.py
  type: code
- path: REPO_INTENT.md
  type: doc
- path: repo.intent.yaml
  type: config
id: yoda-0029
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 6
schema_version: '1.0'
slug: extend-init-to-manage-repo-intent-md-and-repo-intent-yaml
status: done
tags: []
title: Extend init to manage REPO_INTENT.md and repo.intent.yaml
updated_at: '2026-02-06T09:06:04-03:00'
---

# yoda-0029 - Extend init to manage REPO_INTENT.md and repo.intent.yaml
<!-- AGENT: Replace yoda-0029 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Extend init to manage REPO_INTENT.md and repo.intent.yaml with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Extend `init.py` to manage repository intent files in embedded projects. When `REPO_INTENT.md` or `repo.intent.yaml` are missing, init should create them; when they exist, init should append/merge YODA information without overwriting existing content. This keeps agent onboarding consistent with the YODA entry points.

## Context
After installation, agent files reference `REPO_INTENT.md`, but host projects often lack it. This creates broken onboarding instructions for new agents. There is also a `repo.intent.yaml` convention that should capture YODA’s embedded context; init does not populate it today.

## Objective
Ensure `init.py` creates or updates `REPO_INTENT.md` and `repo.intent.yaml` in a safe, idempotent, and non-destructive way.

## Scope
<!-- AGENT: List what is in scope for this issue. -->
- Update `yoda/scripts/init.py` to create `REPO_INTENT.md` if missing.
- When `REPO_INTENT.md` exists, append or update a YODA block using markers (no destructive overwrite).
- Create `repo.intent.yaml` if missing with a minimal YODA section.
- When `repo.intent.yaml` exists, merge in a YODA section without removing existing keys.
- Ensure `--dry-run` reports planned changes without writing.
- Add pytest coverage in `yoda/scripts/tests/test_init.py` for the new behaviors.

## Out of scope
<!-- AGENT: List what is explicitly NOT part of this issue. -->
- Rewriting or reformatting the host project’s existing intent content.
- Migrating other metadata formats or custom repository files.

## Requirements
<!-- AGENT: List functional requirements as bullet points. -->
- Idempotent behavior: re-running init does not duplicate blocks.
- No destructive overwrite of existing `REPO_INTENT.md` or `repo.intent.yaml` content.
- If YAML parsing fails for `repo.intent.yaml`, do not modify the file and report a conflict.
- REPO_INTENT.md block should include the YODA entry guidance and point to `yoda/yoda.md`.

## Acceptance criteria
<!-- AGENT: List testable acceptance criteria. Use checkboxes. -->
- [ ] `init.py` creates `REPO_INTENT.md` when missing and includes a YODA block.
- [ ] `init.py` appends/updates the YODA block in existing `REPO_INTENT.md` without overwriting prior content.
- [ ] `init.py` creates `repo.intent.yaml` when missing with a YODA section.
- [ ] `init.py` merges a YODA section into existing `repo.intent.yaml` while preserving other keys.
- [ ] `--dry-run` does not write changes.
- [ ] Tests cover create + idempotent + preserve behaviors.

## Dependencies
<!-- AGENT: List dependencies and related issues (IDs). If none, write "None". -->
None.

## Entry points
<!-- AGENT: List relevant files or artifacts used as references for implementation. -->
- path: yoda/scripts/init.py
  type: code
- path: REPO_INTENT.md
  type: doc
- path: repo.intent.yaml
  type: config

## Implementation notes
<!-- AGENT: Add technical notes, constraints, or decisions needed to implement. -->
- Reuse the existing YODA block markers for `REPO_INTENT.md` (or introduce a similar marker) to keep updates idempotent.
- For `repo.intent.yaml`, add a top-level `yoda` section (e.g., `embedded: true`, `manual: yoda/yoda.md`, `agent_entry_order`) without altering existing keys.
- Preserve formatting where possible; when re-serializing YAML, use safe_dump with stable ordering.

## Tests
<!-- AGENT: Describe tests to be added or updated. If not applicable, write \"Not applicable\". -->
Update `yoda/scripts/tests/test_init.py` to cover:
- Creating `REPO_INTENT.md` and `repo.intent.yaml`.
- Appending/merging without overwriting.
- Idempotency on re-run.

## Risks and edge cases
<!-- AGENT: List risks, edge cases, or failure scenarios to consider. -->
- Existing files with incompatible formatting (invalid YAML or missing markers).
- Projects with strict formatting expectations for intent files.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
- Added REPO_INTENT.md creation/upsert with YODA markers and default content.
- Added repo.intent.yaml creation and merge behavior for a YODA section.
- Extended init tests to cover repo intent creation, merge, and idempotency.
- Tests: `python3 -m pytest yoda/scripts/tests/test_init.py`

Commit message:
feat(init): manage repo intent files

Issue: yoda-0029
Path: yoda/project/issues/yoda-0029-extend-init-to-manage-repo-intent-md-and-repo-intent-yaml.md