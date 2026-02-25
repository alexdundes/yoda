---
agent: Human
created_at: '2026-02-05T12:24:06-03:00'
depends_on: []
description: Make the one-liner install flow default to latest when --version is omitted
  and update documentation to remove required version in the quick install command.
entrypoints:
- path: docs/install/yoda-install.sh
  type: code
- path: README.md
  type: doc
- path: project/specs/24-installation-and-upgrade.md
  type: doc
id: yoda-0030
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 7
schema_version: '1.0'
slug: allow-one-liner-install-without-explicit-version
status: done
tags: []
title: Allow one-liner install without explicit version
updated_at: '2026-02-06T08:58:28-03:00'
---

# yoda-0030 - Allow one-liner install without explicit version
<!-- AGENT: Replace yoda-0030 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Allow one-liner install without explicit version with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
The one-liner install should be copy‑paste friendly without requiring `--version`. The installer already defaults to latest when `--version` is omitted, so this task is documentation‑only: update the copyable command to omit `--version` and add an alternative command that includes `--version` plus security guidance.

## Context
The quick install command is intended to be copy‑paste friendly, but it still shows `--version` as required. Users want a simpler first‑run flow that defaults to the latest release when version is omitted, while still recommending pinning for safety.

## Objective
Make the one‑liner install work without specifying `--version`, and update documentation/specs to reflect the simplified command and guidance.

## Scope
<!-- AGENT: List what is in scope for this issue. -->
- Update README quick install command to remove the required `--version` flag and add a second copyable command with `--version` as a safer alternative.
- Update `project/specs/24-installation-and-upgrade.md` quick install example to omit `--version`, plus add the explicit version alternative.
- Expand the explanatory text and safety guidance around version pinning.

## Out of scope
<!-- AGENT: List what is explicitly NOT part of this issue. -->
- Changes to installer code (script already defaults to latest).
- Changing the package format or release workflow.

## Requirements
<!-- AGENT: List functional requirements as bullet points. -->
- Docs show the one‑liner without `--version` and provide a second copyable command with `--version`.
- Safety guidance recommends pinning a version for production/regulated environments.

## Acceptance criteria
<!-- AGENT: List testable acceptance criteria. Use checkboxes. -->
- [ ] README quick install block includes a copyable command without `--version`.
- [ ] README includes a second copyable command with `--version`.
- [ ] Spec quick install section mirrors the same two commands and guidance.
- [ ] Safety guidance still recommends pinning a version for production.

## Dependencies
<!-- AGENT: List dependencies and related issues (IDs). If none, write "None". -->
None.

## Entry points
<!-- AGENT: List relevant files or artifacts used as references for implementation. -->
- path: docs/install/yoda-install.sh
  type: code
- path: README.md
  type: doc
- path: project/specs/24-installation-and-upgrade.md
  type: doc

## Implementation notes
<!-- AGENT: Add technical notes, constraints, or decisions needed to implement. -->
- Installer behavior already defaults to latest; only documentation changes are required.

## Tests
<!-- AGENT: Describe tests to be added or updated. If not applicable, write \"Not applicable\". -->
Manual validation: run the installer without `--version` and confirm it uses latest.json.

## Risks and edge cases
<!-- AGENT: List risks, edge cases, or failure scenarios to consider. -->
- Users may install unpinned versions without noticing; keep warnings clear.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
- Updated README quick install to show a versionless command plus a pinned alternative and clearer safety guidance.
- Updated `project/specs/24-installation-and-upgrade.md` to mirror the two one‑liner options and warnings.

Commit message:
docs(install): simplify one-liner and add pinned alternative

Issue: yoda-0030
Path: yoda/project/issues/yoda-0030-allow-one-liner-install-without-explicit-version.md