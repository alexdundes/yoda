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

1) Update from previous package/version.
2) Keep backup before replacement.
3) Run updated `init.py` to finalize sync and migration checks.

## check/apply rule (0.3.0)

- `--check` and `--apply` are defined on updated `init.py` after update.
- Legacy `update.py` remains responsible for version-to-version update orchestration from the previous version.
- Backup is mandatory before apply operations.

## Rollback

- Restore from backup snapshot.
- Do not auto-delete previous backup.

## Security baseline

- Verify package integrity/checksum before applying updates.
