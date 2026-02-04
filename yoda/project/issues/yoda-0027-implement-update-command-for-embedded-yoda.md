---
agent: Human
created_at: '2026-02-04T18:39:33-03:00'
depends_on:
- yoda-0025
description: Implement yoda/scripts/update.py with --check, --apply, --source to handle
  upgrades. It must fetch latest.json, validate sha256, back up to yoda/_previous/<version>,
  replace framework files only, preserve data, and re-run init. Provide dry-run and
  clear output.
entrypoints:
- path: project/specs/24-installation-and-upgrade.md
  type: doc
- path: yoda/scripts/init.py
  type: code
id: yoda-0027
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 6
schema_version: '1.0'
slug: implement-update-command-for-embedded-yoda
status: done
tags: []
title: Implement update command for embedded YODA
updated_at: '2026-02-04T19:18:59-03:00'
---

# yoda-0027 - Implement update command for embedded YODA
<!-- AGENT: Replace yoda-0027 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Implement update command for embedded YODA with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Implement a dedicated update command for embedded YODA (`yoda/scripts/update.py`). It should check for updates, validate package integrity, perform safe in-place upgrades, and support rollback via backups. This delivers the upgrade path defined in the install/upgrade spec.

## Context
We have install and packaging capabilities but no automated upgrade path for embedded projects. The spec requires a safe update flow that preserves project data, verifies checksums, and creates backups. This command will operationalize that flow.

## Objective
Create `yoda/scripts/update.py` with `--check`, `--apply`, and `--source`, aligned with `project/specs/24-installation-and-upgrade.md`.

## Scope
<!-- AGENT: List what is in scope for this issue. -->
- Implement `yoda/scripts/update.py` with CLI flags `--check`, `--apply`, `--source`, `--root`, and `--version` (optional).
- Allow overriding metadata source via `--latest` or `YODA_LATEST_URL` to support tests/private forks.
- Fetch `latest.json`, validate `sha256`, and download the tarball.
- Back up current `yoda/` subtree to `yoda/_previous/<version>`.
- Replace framework files only (scripts/templates/manual/manifest/changelog/license).
- Preserve `yoda/todos/`, `yoda/logs/`, `yoda/project/issues/`.
- Re-run `init.py` to update agent entry blocks.
- Provide dry-run behavior and clear output.

## Out of scope
<!-- AGENT: List what is explicitly NOT part of this issue. -->
- Publishing artefacts or defining release pipelines.
- Signature verification (PGP/Minisign).
- Windows installers.

## Requirements
<!-- AGENT: List functional requirements as bullet points. -->
- Must validate checksum against `latest.json`.
- Must not overwrite host root `README.md` or root `LICENSE`.
- Must preserve YODA data directories.
- Must create backup at `yoda/_previous/<version>`.
- Must support `--source` for local tarball path or URL.
- If `--source` is provided, allow applying a different version than `latest.json`.
- Must be safe to run multiple times.

## Acceptance criteria
<!-- AGENT: List testable acceptance criteria. Use checkboxes. -->
- [ ] `yoda/scripts/update.py` exists and supports `--check` and `--apply`.
- [ ] Update creates backup and preserves data directories.
- [ ] Checksum mismatches abort the update.
- [ ] `--source` works for a local tarball.
- [ ] Re-running update does not corrupt state.

## Dependencies
<!-- AGENT: List dependencies and related issues (IDs). If none, write "None". -->
Depends on: yoda-0025.

## Entry points
<!-- AGENT: List relevant files or artifacts used as references for implementation. -->
- path: project/specs/24-installation-and-upgrade.md
  type: doc
- path: yoda/scripts/init.py
  type: code
- path: yoda/scripts/package.py
  type: code

## Implementation notes
<!-- AGENT: Add technical notes, constraints, or decisions needed to implement. -->
- Reuse shared helpers from `yoda/scripts/lib` for output, validation, and paths.
- Consider supporting `--dry-run` consistent with other scripts.
- File ordering should remain deterministic when copying from the extracted package.
- Backup directory should use `version+build` to avoid collisions.
- `--check` should return exit code 0 even when updates are available.
- `--dry-run` should still download and validate the tarball.
- `--dev` is optional; skip init if not provided.

## Tests
<!-- AGENT: Describe tests to be added or updated. If not applicable, write \"Not applicable\". -->
- Add pytest coverage for `--check` and `--apply` using temp dirs and dummy tarballs.

## Risks and edge cases
<!-- AGENT: List risks, edge cases, or failure scenarios to consider. -->
- Partial updates if copy fails mid-way.
- Missing `latest.json` or invalid schema.
- Backup directory already exists for the same version.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
- Added `yoda/scripts/update.py` with `--check`/`--apply`, metadata overrides, checksum validation, backup, and selective framework replacement.
- Implemented preservation rules for YODA data dirs and optional init execution.
- Added pytest coverage for `--check` and `--apply`.
- Tests: `python3 -m pytest yoda/scripts/tests/test_update.py`

Commit message:
feat(update): add update command for embedded yoda

Issue: yoda-0027
Path: yoda/project/issues/yoda-0027-implement-update-command-for-embedded-yoda.md