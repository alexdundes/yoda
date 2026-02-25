---
created_at: '2026-02-04T18:39:22-03:00'
depends_on: []
description: Update package generation to include yoda/LICENSE in the artefact and
  validate its presence. Adjust include list and tests as needed to ensure embedded
  license ships with the package.
id: yoda-0025
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 7
schema_version: '1.01'
slug: update-package-build-to-include-yoda-license
status: done
title: Update package build to include yoda/LICENSE
updated_at: '2026-02-25T20:02:28-03:00'
---

# yoda-0025 - Update package build to include yoda/LICENSE
<!-- AGENT: Replace yoda-0025 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Update package build to include yoda/LICENSE with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Add `yoda/LICENSE` to the packaged artefact so embedded installs carry their own license file. The packaging script currently includes the root `LICENSE` but does not guarantee the embedded copy. This issue updates the package build and tests to ensure `yoda/LICENSE` is always shipped.

## Context
The distribution spec now requires an embedded license at `yoda/LICENSE` for host projects, and we already added that file to the repo. However, the package builder and tests still only cover the root `LICENSE`. Without updating the package build, the artefact can miss the embedded license required by the spec.

## Objective
Ensure `yoda/LICENSE` is required, included in the package, and verified by tests.

## Scope
<!-- AGENT: List what is in scope for this issue. -->
- Update `yoda/scripts/package.py` to require `yoda/LICENSE` and include it in the archive.
- Update include lists/manifest logic to reflect `yoda/LICENSE`.
- Extend package tests to assert `yoda/LICENSE` is present in the tarball.

## Out of scope
<!-- AGENT: List what is explicitly NOT part of this issue. -->
- Changing the license text or licensing model.
- Publishing packages or releases.

## Requirements
<!-- AGENT: List functional requirements as bullet points. -->
- Package build fails if `yoda/LICENSE` is missing.
- Package artefact contains `yoda/LICENSE`.
- Tests cover the embedded license inclusion.

## Acceptance criteria
<!-- AGENT: List testable acceptance criteria. Use checkboxes. -->
- [ ] `yoda/LICENSE` is required by the package builder.
- [ ] Tarball includes `yoda/LICENSE` alongside root `LICENSE`.
- [ ] Tests assert presence of `yoda/LICENSE`.

## Dependencies
<!-- AGENT: List dependencies and related issues (IDs). If none, write "None". -->
None.

## Entry points
<!-- AGENT: List relevant files or artifacts used as references for implementation. -->
- path: yoda/scripts/package.py
  type: code
- path: yoda/scripts/tests/test_package.py
  type: code
- path: project/specs/23-distribution-and-packaging.md
  type: doc

## Implementation notes
<!-- AGENT: Add technical notes, constraints, or decisions needed to implement. -->
- Add `yoda/LICENSE` to the include list and required file checks.
- Ensure manifest hashing includes the embedded license content.
- Spec follow-up: clarify that `LICENSE` and `yoda/LICENSE` are not required to be identical.

## Tests
<!-- AGENT: Describe tests to be added or updated. If not applicable, write \"Not applicable\". -->
- Update `yoda/scripts/tests/test_package.py` to assert `yoda/LICENSE` is present in the tarball.

## Risks and edge cases
<!-- AGENT: List risks, edge cases, or failure scenarios to consider. -->
- Embedded license exists but differs from root; equality is not required, but specs should state this explicitly.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
- Added `yoda/LICENSE` to package inclusion/required checks and updated tests to assert it in the tarball.
- Updated packaging spec to clarify both licenses are required but may differ.

Commit suggestion:
```
docs: include embedded license in package build

Issue: yoda-0025
Path: yoda/project/issues/yoda-0025-update-package-build-to-include-yoda-license.md
```