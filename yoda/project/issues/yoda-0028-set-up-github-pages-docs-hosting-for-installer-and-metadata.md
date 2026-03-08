---
schema_version: '2.00'
status: done
depends_on:
- yoda-0026
title: Set up GitHub Pages /docs hosting for installer and metadata
description: Create the docs/install structure and publish yoda-install.sh and latest.json
  via GitHub Pages (/docs). Document the base URL and ensure latest.json points to
  GitHub Releases assets. Include a simple checklist for updating latest.json per
  release.
priority: 5
created_at: '2026-02-04T18:39:41-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0028 - Set up GitHub Pages /docs hosting for installer and metadata

## Summary
Set up GitHub Pages hosting from `/docs` to serve the installer script and metadata. This creates the public endpoints required by the one-liner install flow and documents the update routine for `latest.json`. The outcome is a minimal, working hosting setup aligned with the spec.

## Context
The spec now defines Pages hosting (`/docs`) and explicit endpoints, but the repository does not yet include the public files or Pages configuration. Without this, the one-liner install cannot work. We need to add the docs/install assets and document the release update routine.

## Objective
Publish `yoda-install.sh` and `latest.json` under `/docs/install`, and ensure GitHub Pages serves them from `https://alexdundes.github.io/yoda/`.

## Scope
- Create `docs/install/` in the repo.
- Add `yoda-install.sh` and `latest.json` (initial version or placeholder content).
- Ensure URLs match the spec and README.
- Document the steps to update `latest.json` per release.
- Validate that Pages is enabled for `/docs`.

## Out of scope
- Implementing the update command (`update.py`).
- Changing the package format or release pipeline.

## Requirements
- `docs/install/yoda-install.sh` exists and matches the spec contract.
- `docs/install/latest.json` exists with the required schema.
- GitHub Pages is configured for `/docs` on `main`.
- README and spec URLs remain consistent.

## Acceptance criteria
- [ ] `docs/install/` contains `yoda-install.sh` and `latest.json`.
- [ ] Pages is enabled and endpoints resolve under `https://alexdundes.github.io/yoda/`.
- [ ] A documented checklist exists for updating `latest.json` on new releases.

## Dependencies
Depends on: yoda-0026.

## Entry points
- path: project/specs/24-installation-and-upgrade.md
  type: doc
- path: README.md
  type: doc

## Implementation notes
- Use the base URL `https://alexdundes.github.io/yoda/` and serve assets from `/docs/install/`.
- `latest.json` should point to GitHub Releases assets and include `sha256`.
- Keep `yoda-install.sh` stable; only update when behavior changes.
- The repo can ship a placeholder `latest.json`, but it must be updated before the first release.

## Tests
Not applicable (hosting/manual validation).

## Risks and edge cases
- Pages build delays or misconfiguration.
- Stale `latest.json` causing failed installs.

## Result log
- Added `docs/install/latest.json` placeholder with required fields alongside the installer.
- Documented GitHub Pages setup and the `latest.json` update checklist in `project/specs/24-installation-and-upgrade.md`.
- Updated README to note Pages configuration for `/docs`.

Commit message:
docs(hosting): add latest.json placeholder and pages checklist

Issue: yoda-0028
Path: yoda/project/issues/yoda-0028-set-up-github-pages-docs-hosting-for-installer-and-metadata.md

## Flow log
2026-02-04T18:39:41-03:00 | [yoda-0028] issue_add created | title: Set up GitHub Pages /docs hosting for installer and metadata | description: Create the docs/install structure and publish yoda-install.sh and latest.json via GitHub Pages (/docs). Document the base URL and ensure latest.json points to GitHub Releases assets. Include a simple checklist for updating latest.json per release. | slug: set-up-github-pages-docs-hosting-for-installer-and-metadata | priority: 5 | entrypoints: project/specs/24-installation-and-upgrade.md:doc, README.md:doc
2026-02-04T18:39:57-03:00 | [yoda-0028] todo_update | depends_on: [] -> yoda-0026
2026-02-04T19:21:25-03:00 | [yoda-0028] todo_update | status: to-do -> doing
2026-02-04T19:23:33-03:00 | [yoda-0028] Added docs/install/latest.json placeholder and documented Pages setup + latest.json checklist.
2026-02-04T19:23:38-03:00 | [yoda-0028] todo_update | status: doing -> done