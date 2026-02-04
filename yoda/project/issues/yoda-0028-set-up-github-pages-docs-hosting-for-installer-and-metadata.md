---
agent: Human
created_at: '2026-02-04T18:39:41-03:00'
depends_on:
- yoda-0026
description: Create the docs/install structure and publish yoda-install.sh and latest.json
  via GitHub Pages (/docs). Document the base URL and ensure latest.json points to
  GitHub Releases assets. Include a simple checklist for updating latest.json per
  release.
entrypoints:
- path: project/specs/24-installation-and-upgrade.md
  type: doc
- path: README.md
  type: doc
id: yoda-0028
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: set-up-github-pages-docs-hosting-for-installer-and-metadata
status: to-do
tags: []
title: Set up GitHub Pages /docs hosting for installer and metadata
updated_at: '2026-02-04T18:39:57-03:00'
---

# yoda-0028 - Set up GitHub Pages /docs hosting for installer and metadata
<!-- AGENT: Replace yoda-0028 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Set up GitHub Pages /docs hosting for installer and metadata with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Set up GitHub Pages hosting from `/docs` to serve the installer script and metadata. This creates the public endpoints required by the one-liner install flow and documents the update routine for `latest.json`. The outcome is a minimal, working hosting setup aligned with the spec.

## Context
The spec now defines Pages hosting (`/docs`) and explicit endpoints, but the repository does not yet include the public files or Pages configuration. Without this, the one-liner install cannot work. We need to add the docs/install assets and document the release update routine.

## Objective
Publish `yoda-install.sh` and `latest.json` under `/docs/install`, and ensure GitHub Pages serves them from `https://alexdundes.github.io/yoda/`.

## Scope
<!-- AGENT: List what is in scope for this issue. -->
- Create `docs/install/` in the repo.
- Add `yoda-install.sh` and `latest.json` (initial version or placeholder content).
- Ensure URLs match the spec and README.
- Document the steps to update `latest.json` per release.
- Validate that Pages is enabled for `/docs`.

## Out of scope
<!-- AGENT: List what is explicitly NOT part of this issue. -->
- Implementing the update command (`update.py`).
- Changing the package format or release pipeline.

## Requirements
<!-- AGENT: List functional requirements as bullet points. -->
- `docs/install/yoda-install.sh` exists and matches the spec contract.
- `docs/install/latest.json` exists with the required schema.
- GitHub Pages is configured for `/docs` on `main`.
- README and spec URLs remain consistent.

## Acceptance criteria
<!-- AGENT: List testable acceptance criteria. Use checkboxes. -->
- [ ] `docs/install/` contains `yoda-install.sh` and `latest.json`.
- [ ] Pages is enabled and endpoints resolve under `https://alexdundes.github.io/yoda/`.
- [ ] A documented checklist exists for updating `latest.json` on new releases.

## Dependencies
<!-- AGENT: List dependencies and related issues (IDs). If none, write "None". -->
Depends on: yoda-0026.

## Entry points
<!-- AGENT: List relevant files or artifacts used as references for implementation. -->
- path: project/specs/24-installation-and-upgrade.md
  type: doc
- path: README.md
  type: doc

## Implementation notes
<!-- AGENT: Add technical notes, constraints, or decisions needed to implement. -->
- Use the base URL `https://alexdundes.github.io/yoda/` and serve assets from `/docs/install/`.
- `latest.json` should point to GitHub Releases assets and include `sha256`.
- Keep `yoda-install.sh` stable; only update when behavior changes.

## Tests
<!-- AGENT: Describe tests to be added or updated. If not applicable, write \"Not applicable\". -->
Not applicable (hosting/manual validation).

## Risks and edge cases
<!-- AGENT: List risks, edge cases, or failure scenarios to consider. -->
- Pages build delays or misconfiguration.
- Stale `latest.json` causing failed installs.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
