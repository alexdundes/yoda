---
agent: Human
created_at: '2026-01-29T06:31:15-03:00'
depends_on:
- yoda-0016
description: Definir e redigir arquivo LICENSE curto a ser incluído no artefato distribuível,
  alinhado às decisões de empacote e licença do projeto.
entrypoints: []
id: yoda-0021
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 6
schema_version: '1.0'
slug: license-curta-para-pacote-yoda
status: done
tags: []
title: LICENSE curta para pacote YODA
updated_at: '2026-02-04T07:58:07-03:00'
---

# yoda-0021 - LICENSE curta para pacote YODA
<!-- AGENT: Replace yoda-0021 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and LICENSE curta para pacote YODA with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Produce a short, explicit LICENSE file to ship inside the YODA package, aligned with the packaging spec (yoda-0016) and the project’s chosen licensing model. The license text must be lightweight and clear for consumers embedding the framework.

## Context
The distributable package defined in `23-distribution-and-packaging.md` requires a bundled `LICENSE`. The repository currently has no top-level license file, so consumers would lack clarity on usage rights when receiving the packaged artefact.

## Objective
Create a concise LICENSE file (English) suitable for inclusion in the packaged artefact, reflecting the selected license (e.g., MIT/Apache-2.0) and ownership details, and ensure the packaging manifest references it.

## Scope
- Select the license type (MIT or Apache-2.0) consistent with project intent (confirm with requester if needed).
- Draft `LICENSE` text in English, short but legally sound (SPDX-aligned).
- Place the file where the `package` command will pick it up (repo root) and ensure inclusion in the artefact.
- Add `yoda/LICENSE` for embedded use; keep it identical to root `LICENSE`.
- Note the chosen license and path in the packaging spec/manifest if required.

## Out of scope
- Legal review beyond standard open-source text.
- Multi-language licensing.
- Updating third-party dependency licenses.

## Requirements
- LICENSE must be in English and include project name, copyright holder, and year.
- Use standard, unmodified SPDX license text (MIT or Apache-2.0); if any customization is required, get approval.
- File path MUST match packaging include list (root `LICENSE`).
- Add `yoda/LICENSE` (same text as root) for embedded installs.
- Update `yoda/PACKAGE_MANIFEST.yaml` template or notes if needed to mention the license file.
- Keep wording concise (no extra boilerplate beyond the standard text).

## Acceptance criteria
- [ ] `LICENSE` file exists in the repo root with the agreed license (MIT) in English.
- [ ] `yoda/LICENSE` exists and matches the root `LICENSE`.
- [ ] File is referenced/included by the packaging rules (23-distribution-and-packaging) without extra exclusions.
- [ ] Ownership/year fields are filled and accurate.
- [ ] No other repo files need modification to distribute the license.

## Dependencies
yoda-0016

## Entry points
- path: project/specs/23-distribution-and-packaging.md
  type: doc
- path: project/specs/summary.md
  type: doc

## Implementation notes
- Confirm license choice with requester if unspecified; default recommendation: MIT for simplicity or Apache-2.0 if patent grant desired.
- Keep file ASCII/UTF-8, no BOM.
- Consider adding SPDX identifier on the first line if MIT is chosen (`SPDX-License-Identifier: MIT`).
  - For this issue, use MIT with copyright: 2026 Alex Sandre Dundes Rodrigues.
  - Include project name as part of the copyright line to satisfy the requirement.

## Tests
- Not applicable (documentation); manual check that packaging include rules capture the file.

## Risks and edge cases
- Ambiguity about copyright holder or year.
- Selecting a license inconsistent with future distribution or dependencies.
- Packaging script excluding the file if path or name differs from spec.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
- Added MIT LICENSE at repo root and mirrored it at `yoda/LICENSE` for embedded distribution.

Commit suggestion:
```
docs: add MIT license files

Issue: yoda-0021
Path: yoda/project/issues/yoda-0021-license-curta-para-pacote-yoda.md
```