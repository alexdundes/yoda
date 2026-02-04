# YODA Framework - Distribution and Packaging

Defines the distributable artefact of the YODA Framework and the contract expected by the `package` and `init` commands.

## Goals
- Provide a deterministic, minimal package that agents can embed in other projects.
- Keep meta-specs (`project/specs/`) out of the artefact.
- Ensure every package is traceable (version + build metadata, source commit, manifest, changelog).

## Artefact format
- Default format: `tar.gz`.
- Filename pattern: `yoda-framework-<semver+build>.tar.gz` (build metadata is required).
  - Build metadata format: `YYYYMMDD.<short-commit>` (example: `1.3.0+20260129.a1b2c3`).
- Only `tar.gz` is supported in v1; `zip` is deferred.

## Versioning and compatibility
- Use SemVer; build metadata is mandatory for every artefact.
- Breaking changes increment MAJOR; additive changes increment MINOR; fixes increment PATCH.
- `init` and consumers MUST compare version + build; packages with different builds of the same SemVer are distinct.

## Included content
- `yoda/yoda.md` (or successors) — embedded manual for agents.
- `yoda/templates/` — issue templates.
- `yoda/scripts/` — official scripts (`todo_*`, `issue_add`, `log_add`, etc.), excluding `yoda/scripts/tests/`.
- `yoda/favicons/` (if present) — lightweight assets referenced by the manual/UI.
- `LICENSE` — short license file for the package.
- `yoda/LICENSE` — embedded YODA license for host projects.
- `README.md` — concise package README.
- `yoda/PACKAGE_MANIFEST.yaml` — package manifest (see below).
- `yoda/CHANGELOG.yaml` — structured changelog (see below).

## Excluded content
- `project/specs/` and any meta-implementation material.
- `bootstrap-legacy/`, any top-level `project/` content outside `yoda/`.
- Runtime data: `yoda/logs/`, `yoda/todos/`, `yoda/project/issues/`.
- `yoda/scripts/tests/`.
- Caches, VCS data, virtualenvs, test artefacts, temporary files.

## Internal layout
```
<root>/yoda/...
<root>/LICENSE
<root>/README.md
<root>/yoda/LICENSE
<root>/yoda/PACKAGE_MANIFEST.yaml
<root>/yoda/CHANGELOG.yaml
```
- The package preserves relative paths; `init` relies on this structure after extraction.

## Package manifest (`yoda/PACKAGE_MANIFEST.yaml`)
Required fields:
- `schema_version`
- `package_filename`
- `format` (e.g., tar.gz)
- `version` (SemVer) and `build` (metadata)
- `built_at` (ISO 8601 with offset)
- `built_by` (agent/human/CI tag)
- `source_commit` (SHA), `source_dirty` (bool)
- `package_sha256`
- `includes` / `excludes` (concise glob lists applied)
- `changelog_version` (SemVer+build) and `changelog_entry_digest` (sha256 of that entry)
- `notes` (optional, short)

Rules:
- Manifest MUST reflect the exact packaged content; divergence is a build error.
- Manifest holds only summary data; detailed change text stays in the changelog.
- `package_sha256` is computed with the manifest's `package_sha256` field treated as empty to avoid self-reference.

## Structured changelog (`yoda/CHANGELOG.yaml`)
- Single file versioned in the repo and included in the package.
- Entry schema per release:
  - `version` (SemVer), `build` (metadata), `date` (ISO 8601, offset)
  - `summary` (1–3 bullet strings)
  - `breaking` (list)
  - `additions` (list)
  - `fixes` (list)
  - `notes` (optional)
  - `commit` (SHA or tag)
  - `package_sha256` (optional; filled by `package`)
- `package` MUST:
  - Fail if no changelog entry matches the requested version+build.
  - Compute a digest of the entry and record it in `PACKAGE_MANIFEST.yaml`.
  - Copy `CHANGELOG.yaml` into the package.

## `package` command requirements (will be implemented separately)
- Minimum flags: `--version`, `--output` (or directory), `--archive-format` (default tar.gz), `--dry-run`.
- `--archive-format` only accepts `tar.gz` in v1.
- Uses the include/exclude rules above; fails if a required item is missing.
- Generates `PACKAGE_MANIFEST.yaml` and a checksum of the package.
- Orders files deterministically for reproducible builds.
- Supports `--changelog` to point to a custom changelog path (default `yoda/CHANGELOG.yaml`).

## `init` command requirements (consumer; implemented separately)
- Assumes the layout defined here.
- Creates the host project skeleton (AGENTS.md, `yoda/todos/TODO.<dev>.yaml`, etc.) without relying on `project/specs/`.
- MUST validate package version/build and warn on incompatibilities (MAJOR or older build).

## Compatibility and upgrade
- Consumers SHOULD keep the previous package to allow rollback; keeping the manifest is recommended.
- MAJOR updates MAY require manual steps; record them under `breaking` in the changelog.

## Non-goals
- UX details of the CLIs (handled in implementation issues).
- Publication pipeline.

## Cross-references
- Update `project/specs/summary.md` to reference this document.
- Related issues: yoda-0016 (this spec), yoda-0018 (package command), yoda-0019 (init command), yoda-0020 (install/upgrade/rollback).
