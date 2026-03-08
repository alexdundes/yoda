---
schema_version: '2.00'
status: done
title: Allow one-liner install without explicit version
description: Make the one-liner install flow default to latest when --version is omitted
  and update documentation to remove required version in the quick install command.
priority: 7
created_at: '2026-02-05T12:24:06-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0030 - Allow one-liner install without explicit version

## Summary
The one-liner install should be copy‑paste friendly without requiring `--version`. The installer already defaults to latest when `--version` is omitted, so this task is documentation‑only: update the copyable command to omit `--version` and add an alternative command that includes `--version` plus security guidance.

## Context
The quick install command is intended to be copy‑paste friendly, but it still shows `--version` as required. Users want a simpler first‑run flow that defaults to the latest release when version is omitted, while still recommending pinning for safety.

## Objective
Make the one‑liner install work without specifying `--version`, and update documentation/specs to reflect the simplified command and guidance.

## Scope
- Update README quick install command to remove the required `--version` flag and add a second copyable command with `--version` as a safer alternative.
- Update `project/specs/24-installation-and-upgrade.md` quick install example to omit `--version`, plus add the explicit version alternative.
- Expand the explanatory text and safety guidance around version pinning.

## Out of scope
- Changes to installer code (script already defaults to latest).
- Changing the package format or release workflow.

## Requirements
- Docs show the one‑liner without `--version` and provide a second copyable command with `--version`.
- Safety guidance recommends pinning a version for production/regulated environments.

## Acceptance criteria
- [ ] README quick install block includes a copyable command without `--version`.
- [ ] README includes a second copyable command with `--version`.
- [ ] Spec quick install section mirrors the same two commands and guidance.
- [ ] Safety guidance still recommends pinning a version for production.


## Entry points
- `docs/install/yoda-install.sh`
- `README.md`
- `project/specs/24-installation-and-upgrade.md`

## Implementation notes
- Installer behavior already defaults to latest; only documentation changes are required.

## Tests
Manual validation: run the installer without `--version` and confirm it uses latest.json.

## Risks and edge cases
- Users may install unpinned versions without noticing; keep warnings clear.

## Result log
- Updated README quick install to show a versionless command plus a pinned alternative and clearer safety guidance.
- Updated `project/specs/24-installation-and-upgrade.md` to mirror the two one‑liner options and warnings.

Commit message:
docs(install): simplify one-liner and add pinned alternative

Issue: yoda-0030
Path: yoda/project/issues/yoda-0030-allow-one-liner-install-without-explicit-version.md

## Flow log
2026-02-05T12:24:06-03:00 | [yoda-0030] issue_add created | title: Allow one-liner install without explicit version | description: Make the one-liner install flow default to latest when --version is omitted and update documentation to remove required version in the quick install command. | slug: allow-one-liner-install-without-explicit-version | priority: 7 | entrypoints: docs/install/yoda-install.sh:code, README.md:doc, project/specs/24-installation-and-upgrade.md:doc
2026-02-06T08:54:31-03:00 | [yoda-0030] todo_update | status: to-do -> doing
2026-02-06T08:58:24-03:00 | [yoda-0030] Updated quick install docs to remove required --version and add pinned alternative with safety guidance.
2026-02-06T08:58:28-03:00 | [yoda-0030] todo_update | status: doing -> done