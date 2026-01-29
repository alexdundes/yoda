---
agent: Human
created_at: '2026-01-29T06:31:28-03:00'
depends_on:
- yoda-0016
description: Criar README conciso para o artefato distribuível, com instruções rápidas
  de uso, comandos package/init, conteúdo do pacote e links essenciais.
entrypoints: []
id: yoda-0022
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: readme-curto-do-pacote-yoda
status: to-do
tags: []
title: README curto do pacote YODA
updated_at: '2026-01-29T06:31:31-03:00'
---

# yoda-0022 - README curto do pacote YODA
<!-- AGENT: Replace yoda-0022 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and README curto do pacote YODA with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Author a concise README (English) to ship inside the YODA package, giving consumers a quick start: what the package is, how to extract/use it, and where to find the full manual/scripts.

## Context
The packaging spec (`23-distribution-and-packaging.md`) mandates a short README in the artefact. Without it, recipients of the tarball lack immediate guidance on contents, commands (`package`/`init`), and links to the embedded manual.

## Objective
Create a lightweight `README` placed at package root that orients users to the bundled files (`yoda/` tree, manifest, changelog, license) and points to the embedded manual `yoda/yoda.md`.

## Scope
- Define structure and content for the short README (English).
- Cover: package purpose, how to unpack, entrypoints (`yoda/yoda.md`, scripts), version/build info from manifest, and how to run `init` once available.
- Place the file at repo root and ensure it is included in the package.
- Reference changelog/manifest and where to find them inside the tarball.

## Out of scope
- Full user manual content (covered by yoda-0017).
- Detailed CLI UX for `package`/`init` implementations.
- Localization.

## Requirements
- README must be English, concise (aim ≤ ~200–300 words).
- Located at repo root so packaging includes it.
- Sections: “What this package is”, “What’s inside”, “How to use”, “Version/build info”, “Where to read more”.
- Link (relative) to `yoda/yoda.md` and mention `yoda/PACKAGE_MANIFEST.yaml` and `yoda/CHANGELOG.yaml`.
- Mention extraction command example for `tar.gz`.

## Acceptance criteria
- [ ] README present at repo root, concise, English, with required sections.
- [ ] References to `yoda/yoda.md`, `yoda/PACKAGE_MANIFEST.yaml`, and `yoda/CHANGELOG.yaml` are correct.
- [ ] Includes quick extract/run instructions for the package format (tar.gz).
- [ ] Aligned with the distribution contract in `23-distribution-and-packaging.md`.

## Dependencies
yoda-0016

## Entry points
- path: project/specs/23-distribution-and-packaging.md
  type: doc
- path: project/specs/summary.md
  type: doc
- path: yoda/yoda.md
  type: doc

## Implementation notes
- Keep to plain Markdown, no badges or heavy formatting.
- Include example extraction command: `tar -xzf yoda-framework-<version>.tar.gz -C <target>`.
- Note that `init` command will set up AGENTS/TODO in the host project once available.

## Tests
- Not applicable (doc); manual check that packaging rules include the file.

## Risks and edge cases
- README becomes too long and duplicates the manual.
- Paths or filenames change in the packaging spec and desync the instructions.
- Future formats (zip) might need an extra extraction example.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
