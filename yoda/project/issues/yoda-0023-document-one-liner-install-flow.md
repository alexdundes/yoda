---
schema_version: '2.00'
id: yoda-0023
status: done
depends_on:
- yoda-0024
title: Document one-liner install flow
description: Define and document the one-liner install script (yoda-install.sh), hosting
  URLs, and latest.json metadata. Include security guidance and update README.md placeholders
  once URLs are defined.
priority: 5
created_at: '2026-02-04T08:07:08-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0023 - Document one-liner install flow

## Summary
Define the one-liner install flow as a documented, spec-first process, including hosting on GitHub Pages (`/docs`) and metadata via `latest.json`. Provide a clear, human-operated setup checklist for enabling GitHub Pages on the repo. This issue updates specs and documentation only; implementation of scripts or release automation is explicitly out of scope.

## Context
The package README now emphasizes a one-liner install, but the hosting model and URL structure are not defined yet. We need an explicit contract for where `yoda-install.sh` and `latest.json` live, how they point to the release tarball, and how users configure GitHub Pages. This should be captured in specs before any implementation work.

## Objective
Document the one-liner install hosting strategy, metadata contract, and setup steps in the specs, then update README placeholders once the base URL is established. Ensure the documentation aligns with yoda-0024 and the install/upgrade spec.

## Scope
- Specify GitHub Pages hosting from `/docs` in the same repository.
- Define the base URL pattern for Pages and how it maps to install assets.
- Specify `docs/install/yoda-install.sh` and `docs/install/latest.json` as the public endpoints.
- Define `latest.json` schema: `version`, `build`, `package_url`, `sha256`.
- Require package tarballs to be hosted in GitHub Releases; `latest.json` must point to the release asset URL.
- Document checksum-only verification (no signatures for now).
- Provide a human checklist for configuring GitHub Pages in the repo settings.
- Update specs (and related docs) to include the hosting contract.
- After yoda-0024, revise README placeholders to use the defined base URL.

## Out of scope
- Implementing `yoda-install.sh` or `update.py`.
- Publishing artefacts or automating release pipelines.
- Adding signature-based verification (PGP/Minisign).

## Requirements
- Spec-first: update specs before any implementation work.
- Hosting model: GitHub Pages served from `/docs` on `main`.
- Base URL should be `https://alexdundes.github.io/yoda/` (derived from repo).
- Public endpoints:
  - `https://alexdundes.github.io/yoda/install/yoda-install.sh`
  - `https://alexdundes.github.io/yoda/install/latest.json`
- `latest.json` must include `version`, `build`, `package_url`, `sha256`.
- `package_url` must point to a GitHub Releases asset for the tarball.
- Use checksum validation only.
- Include a human-operated setup checklist for GitHub Pages configuration.
- Document the dependency on yoda-0024 and the need to update README placeholders accordingly.

## Acceptance criteria
- [ ] Specs updated to document Pages hosting, endpoints, and `latest.json` schema.
- [ ] Human setup checklist for GitHub Pages is included in the issue or spec text.
- [ ] README placeholders are updated after yoda-0024 to use the defined base URL.
- [ ] The issue explicitly states spec-first and no implementation.

## Dependencies
Depends on: yoda-0024.

## Entry points
- path: README.md
  type: doc
- path: project/specs/24-installation-and-upgrade.md
  type: doc
- path: project/specs/23-distribution-and-packaging.md
  type: doc

## Implementation notes
- GitHub Pages configuration (human checklist):
  1) Open repo settings: `Settings → Pages`.
  2) Source: “Deploy from a branch”.
  3) Branch: `main`, folder: `/docs`.
  4) Save, wait for Pages to build.
  5) Verify base URL `https://alexdundes.github.io/yoda/` is live.
  6) Confirm `install/` files are served from `/docs/install/`.
- `latest.json` should be updated for each release; `yoda-install.sh` should be stable and only change when behavior changes.
- Ensure yoda-0024 README placeholders are revised once URLs are final.

## Tests
Not applicable (documentation-only).

## Risks and edge cases
- Pages misconfiguration or delays can break one-liner installs.
- Inconsistent URLs between specs and README.
- Stale `latest.json` pointing to missing release assets.

## Result log
- Updated installation/upgrade spec with GitHub Pages `/docs` hosting, explicit endpoints, and base URL; aligned README one-liner with the final URL and added a confirmation TODO.

Commit suggestion:
```
docs: define one-liner install hosting

Issue: yoda-0023
Path: yoda/project/issues/yoda-0023-document-one-liner-install-flow.md
```

## Flow log
2026-02-04T08:07:08-03:00 | [yoda-0023] issue_add created | title: Document one-liner install flow | description: Define and document the one-liner install script (yoda-install.sh), hosting URLs, and latest.json metadata. Include security guidance and update README.md placeholders once URLs are defined. | slug: document-one-liner-install-flow | priority: 5 | entrypoints: README.md:doc, project/specs/24-installation-and-upgrade.md:doc
2026-02-04T09:38:26-03:00 | [yoda-0023] todo_update | depends_on: [] -> yoda-0024
2026-02-04T11:09:01-03:00 | [yoda-0023] todo_update | status: to-do -> doing
2026-02-04T11:10:41-03:00 | [yoda-0023] Documented GitHub Pages /docs hosting and endpoints; updated README one-liner URL and placeholder TODO.
2026-02-04T11:10:48-03:00 | [yoda-0023] todo_update | status: doing -> done
