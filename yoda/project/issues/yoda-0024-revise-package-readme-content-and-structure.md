---
created_at: '2026-02-04T09:38:21-03:00'
depends_on: []
description: Define the full content and structure for the package README.md (English,
  friendly). Include logo block, short tagline, cycles + agent skin concept, inspirations
  (DocDD, Docs-as-Code, Design-first/Contract-first, Literate Programming parallel),
  quick one-liner install with warnings, manual install, init, contents, version/integrity,
  upgrade/rollback, source-of-truth link to upstream specs (TODO placeholder), and
  license note. Add TODO comments for unresolved URLs/hosting. Require updates to
  specs/playbook/yoda/yoda.md to include the agent-skin-in-cycle concept. This issue
  must be higher priority than yoda-0023; yoda-0023 should depend on this.
id: yoda-0024
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 7
schema_version: '1.01'
slug: revise-package-readme-content-and-structure
status: done
title: Revise package README content and structure
updated_at: '2026-02-25T20:02:28-03:00'
---

# yoda-0024 - Revise package README content and structure
<!-- AGENT: Replace yoda-0024 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Revise package README content and structure with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Define the complete content and structure for the package `README.md` in English, with a friendly tone and full conceptual overview. The current README is too thin relative to the intended YODA narrative and install/upgrade guidance. This issue standardizes the required blocks, placeholders, and the cycle/skin concept, and aligns core specs/playbook with that concept.

## Context
The package README is the first human-facing document for embedded YODA, but it no longer carries the conceptual depth of the original PT-BR README. We also introduced the install/upgrade flow (including a one-liner option) and need the README to reflect that structure and warnings. In addition, we want to formalize the idea that the agent assumes a "skin" when entering a cycle (YODA Intake or YODA Flow), which requires spec/playbook updates for consistency.

## Objective
Deliver a clear, friendly, English package README with all required blocks and TODO placeholders, and update the relevant specs and playbook to include the agent-skin-in-cycle concept.

## Scope
<!-- AGENT: List what is in scope for this issue. -->
- Rewrite `README.md` (English, friendly) with the full block structure defined below.
- Add the logo block directly after the title.
- Add a short tagline that conveys package nature, YODA acronym, and purpose.
- Emphasize one-liner install first (with warnings), followed by manual install and init.
- Add conceptual sections: What this is, Inspirations, Issues (Doc First + Intake/Flow roles), Why the name YODA, Why YAML/scripts and Markdown.
- Include Version & integrity, Upgrade & rollback, Where to read more, Source of truth, and License blocks.
- Insert HTML TODO comments for unresolved URLs/hosting placeholders.
- Update specs/playbook and `yoda/yoda.md` to include the "agent assumes a skin when entering a cycle" concept.
- Ensure yoda-0023 depends on this issue.

## Out of scope
<!-- AGENT: List what is explicitly NOT part of this issue. -->
- Implementing the installer/update scripts or hosting.
- Localizing the README into other languages.
- Changing package format or publish pipeline.

## Requirements
<!-- AGENT: List functional requirements as bullet points. -->
- README is English and friendly (human-oriented, not spec-like).
- No word-count limit; prioritize completeness and clarity.
- Title followed by the exact logo markup block:
  ```
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="yoda/favicons/yoda-dark.svg">
    <img src="yoda/favicons/yoda-light.svg" alt="YODA Framework Logo" width="256" height="256">
  </picture>
  ```
- Tagline directly under the logo, conveying:
  - Package nature (embedded YODA)
  - YODA acronym (YAML-Oriented Documentation & Agents)
  - Brief purpose (doc-first, YAML/Markdown as source of truth)
- "What this is" section explains YODA Framework concepts, including:
  - Doc First / Document first
  - Document as source of truth
  - Docs-as-code
  - YODA cycles (Intake, Flow) and their roles (explicitly name YODA Intake and YODA Flow)
  - Agent assumes a skin when entering a cycle
- "Quick install (one-liner)" appears before manual install, with warnings.
- "Manual install (recommended)" includes tar.gz extraction command and init step.
- "First run / Init" section explicitly states what init does.
- "Inspirations" section cites by name:
  - DocDD
  - Docs-as-Code
  - Design-first / Contract-first
  - Literate Programming (parallel to modern vibe-coding with issues)
- "Issues" section explains:
  - Intake creates/clarifies issues before execution
  - Flow executes issues with human-guided agent work
  - This is the practical expression of Doc First
- "Why the name YODA" section:
  - Explains acronym
  - Explains why we say YODA Framework / YODA Intake / YODA Flow
- "Why YAML + scripts and Markdown" section:
  - Two bullets: (1) YAML + scripts together; (2) Markdown for issue narrative
- "Version & integrity" mentions `yoda/PACKAGE_MANIFEST.yaml`, `yoda/CHANGELOG.yaml`, and `latest.json` checksum model.
- "Upgrade & rollback" includes high-level flow and backup location `yoda/_previous/<version>`.
- "Source of truth" points explicitly to `https://github.com/alexdundes/yoda` and its `project/specs` path.
- "Where to read more" links to `yoda/yoda.md` and `yoda/scripts/README.md`.
- "License" references root `LICENSE` (do not mention embedded `yoda/LICENSE` here).
- Add HTML TODO comments for unresolved URLs (installer script, metadata).
- Update specs/playbook/yoda manual to define the agent-skin-in-cycle concept:
  - `project/specs/00-conventions.md`
  - `project/specs/02-yoda-flow-process.md`
  - `project/specs/11-yoda-intake.md`
  - `project/specs/06-agent-playbook.md`
  - `yoda/yoda.md`

## Acceptance criteria
<!-- AGENT: List testable acceptance criteria. Use checkboxes. -->
- [ ] `README.md` includes all required sections/blocks in English, friendly tone.
- [ ] Logo markup is inserted immediately after the title.
- [ ] One-liner install appears before manual install and includes warnings.
- [ ] README contains HTML TODO comments for unresolved URLs/hosting.
- [ ] Cycles and agent skin concept are described in README.
- [ ] Inspirations cite the required sources by name.
- [ ] Specs/playbook/yoda manual are updated to include the agent-skin-in-cycle concept.
- [ ] yoda-0023 depends on this issue.

## Dependencies
<!-- AGENT: List dependencies and related issues (IDs). If none, write "None". -->
None. (This issue blocks yoda-0023.)

## Entry points
<!-- AGENT: List relevant files or artifacts used as references for implementation. -->
- path: README.md
  type: doc
- path: project/specs/00-conventions.md
  type: doc
- path: project/specs/02-yoda-flow-process.md
  type: doc
- path: project/specs/11-yoda-intake.md
  type: doc
- path: project/specs/06-agent-playbook.md
  type: doc
- path: yoda/yoda.md
  type: doc
- path: project/specs/24-installation-and-upgrade.md
  type: doc

## Implementation notes
<!-- AGENT: Add technical notes, constraints, or decisions needed to implement. -->
- Use "cycle" as the canonical term; "skin" is an agent stance when entering a cycle.
- Keep README Markdown simple (no badges).
- Use HTML comments for TODO placeholders:
  - Installer script base URL
  - `latest.json` metadata URL
- Suggested block order (conventional):
  1) Title + logo + tagline
  2) What this package is (concept + cycles)
  3) Quick install (one-liner, warnings)
  4) Manual install (recommended)
  5) First run / Init
  6) Inspirations
  7) Issues (Intake → Flow)
  8) Why the name YODA
  9) Why YAML/scripts and Markdown
  10) Version & integrity
  11) Upgrade & rollback
  12) Source of truth (explicit repo link)
  13) Where to read more
  14) License

## Tests
<!-- AGENT: Describe tests to be added or updated. If not applicable, write \"Not applicable\". -->
Not applicable (documentation-only).

## Risks and edge cases
<!-- AGENT: List risks, edge cases, or failure scenarios to consider. -->
- README becomes too long or drifts from specs.
- Ambiguous "skin" concept without spec alignment.
- Placeholder URLs remain unresolved and are not tracked.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
- Rewrote root `README.md` with the full friendly package narrative, logo/tagline, cycle/skin concept, install flows, inspirations, and placeholders.
- Updated specs and manual to codify the agent-skin-in-cycle concept across YODA Flow/Intake guidance.

Commit suggestion:
```
docs: expand package readme and codify cycle skins

Issue: yoda-0024
Path: yoda/project/issues/yoda-0024-revise-package-readme-content-and-structure.md
```