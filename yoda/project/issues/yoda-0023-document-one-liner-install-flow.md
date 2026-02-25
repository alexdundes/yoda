---
agent: Human
created_at: '2026-02-04T08:07:08-03:00'
depends_on:
- yoda-0024
description: Define and document the one-liner install script (yoda-install.sh), hosting
  URLs, and latest.json metadata. Include security guidance and update README.md placeholders
  once URLs are defined.
entrypoints:
- path: README.md
  type: doc
- path: project/specs/24-installation-and-upgrade.md
  type: doc
id: yoda-0023
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: document-one-liner-install-flow
status: done
tags: []
title: Document one-liner install flow
updated_at: '2026-02-04T11:10:48-03:00'
---

# yoda-0023 - Document one-liner install flow
<!-- AGENT: Replace yoda-0023 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Document one-liner install flow with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Define the one-liner install flow as a documented, spec-first process, including hosting on GitHub Pages (`/docs`) and metadata via `latest.json`. Provide a clear, human-operated setup checklist for enabling GitHub Pages on the repo. This issue updates specs and documentation only; implementation of scripts or release automation is explicitly out of scope.

## Context
The package README now emphasizes a one-liner install, but the hosting model and URL structure are not defined yet. We need an explicit contract for where `yoda-install.sh` and `latest.json` live, how they point to the release tarball, and how users configure GitHub Pages. This should be captured in specs before any implementation work.

## Objective
Document the one-liner install hosting strategy, metadata contract, and setup steps in the specs, then update README placeholders once the base URL is established. Ensure the documentation aligns with yoda-0024 and the install/upgrade spec.

## Scope
<!-- AGENT: List what is in scope for this issue. -->
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
<!-- AGENT: List what is explicitly NOT part of this issue. -->
- Implementing `yoda-install.sh` or `update.py`.
- Publishing artefacts or automating release pipelines.
- Adding signature-based verification (PGP/Minisign).

## Requirements
<!-- AGENT: List functional requirements as bullet points. -->
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
<!-- AGENT: List testable acceptance criteria. Use checkboxes. -->
- [ ] Specs updated to document Pages hosting, endpoints, and `latest.json` schema.
- [ ] Human setup checklist for GitHub Pages is included in the issue or spec text.
- [ ] README placeholders are updated after yoda-0024 to use the defined base URL.
- [ ] The issue explicitly states spec-first and no implementation.

## Dependencies
<!-- AGENT: List dependencies and related issues (IDs). If none, write "None". -->
Depends on: yoda-0024.

## Entry points
<!-- AGENT: List relevant files or artifacts used as references for implementation. -->
- path: README.md
  type: doc
- path: project/specs/24-installation-and-upgrade.md
  type: doc
- path: project/specs/23-distribution-and-packaging.md
  type: doc

## Implementation notes
<!-- AGENT: Add technical notes, constraints, or decisions needed to implement. -->
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
<!-- AGENT: Describe tests to be added or updated. If not applicable, write \"Not applicable\". -->
Not applicable (documentation-only).

## Risks and edge cases
<!-- AGENT: List risks, edge cases, or failure scenarios to consider. -->
- Pages misconfiguration or delays can break one-liner installs.
- Inconsistent URLs between specs and README.
- Stale `latest.json` pointing to missing release assets.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
- Updated installation/upgrade spec with GitHub Pages `/docs` hosting, explicit endpoints, and base URL; aligned README one-liner with the final URL and added a confirmation TODO.

Commit suggestion:
```
docs: define one-liner install hosting

Issue: yoda-0023
Path: yoda/project/issues/yoda-0023-document-one-liner-install-flow.md
```