# YODA Framework - Installation and upgrade

This spec defines how YODA is installed and upgraded in embedded host projects.

## Goals

- keep install/upgrade simple and verifiable
- preserve project data
- support safe rollback

## Required preservation

Upgrade/install processes MUST preserve:

- `yoda/project/issues/`
- `yoda/project/extern_issues/`
- compatibility data folders as applicable (`yoda/todos/`, `yoda/logs/`)

## Update flow

1) Resolve latest metadata from `docs/install/latest.json` or an explicit
   `--latest` override. `update.py --version` is an expected-version guard and
   MUST equal the resolved latest version/build; it does not select historical
   releases.
2) Download/read the package and verify its SHA-256 before extraction.
3) Keep a backup under `yoda/_previous/<version+build>` before replacement.
4) Replace framework-owned files while preserving project data.
5) Run updated `init.py` when `--dev` is provided to finalize schema/layout
   migration.

`init.py` finalization is non-intrusive: it must operate only on YODA-managed
files under `yoda/` and must not create or modify host-root agent or intent
files.

## Installer modes

- Latest one-liner uses `docs/install/yoda-install.sh` without `--version` and
  resolves the current `latest.json` entry.
- Pinned installation passes `--version <semver+build>`.
- Installer `--version` pins the version expected from current latest metadata;
  it does not discover historical release metadata.
- Installer verifies the `latest.json`/package checksum before applying files.

## Update check/apply rule

- `update.py --check` compares current and available version/build metadata
  without applying files.
- `update.py --apply` performs backup, replacement, and optional init.
- Both modes emit non-blocking warnings for a SemVer MAJOR change or a target
  older than the installed version/build.
- Historical version selection is unsupported by `update.py`; `--version` must
  match `latest.json`, and mismatches fail before package download/checksum.
- `init.py` does not expose `--check` or `--apply`; it initializes/reconciles
  the embedded workspace.
- Backup is mandatory before update apply operations.

## Rollback

- Restore from backup snapshot.
- Do not auto-delete previous backup.

## Security baseline

- Verify package integrity/checksum before applying updates.
