---
schema_version: '2.00'
id: yoda-0026
status: done
depends_on:
- yoda-0025
title: Implement yoda-install.sh one-liner installer
description: Create the yoda-install.sh script to support the one-liner install flow.
  The script downloads the tarball, verifies sha256 via latest.json, extracts, copies
  the yoda/ subtree per spec, and runs init. Include security warnings and support
  --version/--root/--source.
priority: 6
created_at: '2026-02-04T18:39:27-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0026 - Implement yoda-install.sh one-liner installer

## Summary
Implement the `yoda-install.sh` script to power the one-liner install flow defined in the spec. The script must download the package, verify checksum via `latest.json`, install the `yoda/` subtree, and run init. This enables fast onboarding while preserving safety constraints.

## Context
The README and install spec describe a one-liner install, but there is no installer script yet. We need a stable shell script that follows the spec rules (checksum verification, preserve data, no host README overwrite) and supports both pinned versions and custom sources.

## Objective
Deliver `docs/install/yoda-install.sh` with a clear, safe, repeatable install flow aligned to `project/specs/24-installation-and-upgrade.md`.

## Scope
- Create `docs/install/yoda-install.sh` in the repository.
- Support flags: `--version`, `--root`, `--source`.
- Add `--dev` (optional) and `--dry-run`.
- Fetch `latest.json`, resolve `package_url`, and verify `sha256`.
- Extract tarball to temp, copy the `yoda/` subtree into the host root.
- Preserve `yoda/todos/`, `yoda/logs/`, `yoda/project/issues/` if they exist.
- Run `python yoda/scripts/init.py --dev <slug> --root <root>` if a dev slug is provided.
- Provide clear stdout messages and non-zero exits on failure.

## Out of scope
- Implementing `update.py` or release automation.
- Cryptographic signatures (PGP/Minisign).
- Windows-specific installers.

## Requirements
- Must use checksum validation from `latest.json` (checksum-only).
- Must not overwrite host root `README.md` or root `LICENSE`.
- Must overwrite framework files under `yoda/` per spec (scripts/templates/manual/manifest/changelog/license).
- Must preserve YODA data dirs (`yoda/todos`, `yoda/logs`, `yoda/project/issues`).
- Must accept `--source` to override `package_url` (file path or URL).
- If `--version` is omitted, install the version from `latest.json`.
- `--dev` is optional; init runs only when provided.
- `--dry-run` shows planned actions without writing.
- Should be idempotent when run multiple times with the same version.

## Acceptance criteria
- [ ] `docs/install/yoda-install.sh` exists and is executable.
- [ ] Script installs the package and runs init without touching host `README.md`.
- [ ] Checksum verification fails on mismatch.
- [ ] `--source` override works for local tarball path.
- [ ] YODA data directories are preserved.
- [ ] `--version` optional (defaults to latest) and `--dry-run` works.

## Dependencies
Depends on: yoda-0025.

## Entry points
- path: project/specs/24-installation-and-upgrade.md
  type: doc
- path: README.md
  type: doc
- path: yoda/scripts/init.py
  type: code

## Implementation notes
- Use `/bin/sh` or bash with `set -euo pipefail`.
- Prefer `curl -fsSL` (or `wget` fallback if needed).
- Use `sha256sum` on Linux and `shasum -a 256` on macOS.
- Allow `--dev` to trigger `init.py`; omit if not set.
- Provide clear `--dry-run` output for each step.
- Keep the script stable; changes should be rare and versioned.

## Tests
- Add a minimal shell test or manual validation steps; unit tests in pytest are optional.

## Risks and edge cases
- Missing curl/shasum tooling on target machines.
- Users running the script without pinning `--version`.
- Partial installs if filesystem permissions block copy operations.

## Result log
- Implemented `docs/install/yoda-install.sh` with flag parsing, latest.json resolution, checksum verification, selective YODA subtree install, and optional init.
- Added `--dry-run` messaging and preservation rules for `yoda/todos`, `yoda/logs`, and `yoda/project/issues`.
- Verified shell syntax with `sh -n docs/install/yoda-install.sh`.

Commit message:
feat(install): add yoda-install.sh one-liner installer

Issue: yoda-0026
Path: yoda/project/issues/yoda-0026-implement-yoda-install-sh-one-liner-installer.md

## Flow log
2026-02-04T18:39:27-03:00 | [yoda-0026] issue_add created | title: Implement yoda-install.sh one-liner installer | description: Create the yoda-install.sh script to support the one-liner install flow. The script downloads the tarball, verifies sha256 via latest.json, extracts, copies the yoda/ subtree per spec, and runs init. Include security warnings and support --version/--root/--source. | slug: implement-yoda-install-sh-one-liner-installer | priority: 6 | entrypoints: project/specs/24-installation-and-upgrade.md:doc, README.md:doc
2026-02-04T18:39:46-03:00 | [yoda-0026] todo_update | depends_on: [] -> yoda-0025
2026-02-04T18:53:11-03:00 | [yoda-0026] todo_update | status: to-do -> doing
2026-02-04T19:01:07-03:00 | [yoda-0026] Implemented docs/install/yoda-install.sh with checksum validation, preserve rules, and dry-run support.
2026-02-04T19:01:10-03:00 | [yoda-0026] todo_update | status: doing -> done
