# YODA Framework - Installation and Upgrade

This specification defines how the YODA Framework is installed and upgraded when embedded in external projects.

## Goals
- Provide a simple install path for new projects.
- Enable safe upgrades with verification and rollback.
- Preserve project-specific YODA data (TODOs, logs, issues).
- Support a “forked” embedded YODA (project maintains its own versioned package).

## Artefacts and metadata
- Package artefact: `yoda-framework-<semver+build>.tar.gz`.
- Remote metadata: `latest.json` with fields:
  - `version` (SemVer)
  - `build` (metadata)
  - `package_url`
  - `sha256` (package checksum)
- Package contents follow `23-distribution-and-packaging.md`.

## First install (quick one-liner)
This is the **first option** for convenience. It is less safe because it executes a remote script directly.

```bash
curl -fsSL <url>/yoda-install.sh | sh -s -- --version <semver+build> --root .
```

Security warnings:
- Prefer pinning an explicit `--version`.
- Prefer the manual flow below in production or regulated environments.
- The script must verify the package checksum from `latest.json`.

## First install (manual, recommended)
1) Download `yoda-framework-<semver+build>.tar.gz` and `latest.json`.
2) Verify checksum (`sha256`) from `latest.json` against the tarball.
3) Extract the tarball to a temporary directory.
4) Copy the `yoda/` subtree into the project root:
   - **Overwrite**: `yoda/scripts/`, `yoda/templates/`, `yoda/yoda.md`, `yoda/favicons/`,
     `yoda/CHANGELOG.yaml`, `yoda/PACKAGE_MANIFEST.yaml`, `yoda/README.md` (if present),
     `yoda/LICENSE`.
   - **Preserve**: `yoda/todos/`, `yoda/logs/`, `yoda/project/issues/`.
   - **Ignore**: package root `README.md` and root `LICENSE` (host project owns these).
5) Run init:
```bash
python yoda/scripts/init.py --dev <slug> --root .
```
6) Commit changes in the host project.

## Upgrade flow (recommended)
1) Fetch `latest.json` and compare to current `yoda/PACKAGE_MANIFEST.yaml`.
2) Download the package tarball.
3) Verify checksum from `latest.json`.
4) Backup current YODA subtree to `yoda/_previous/<version>`.
5) Replace only the YODA framework files (same rules as install: overwrite framework files, preserve data).
6) Re-run init to append/update agent entry blocks if needed:
```bash
python yoda/scripts/init.py --dev <slug> --root .
```

## Rollback
- Restore from `yoda/_previous/<version>` by swapping the subtree back.
- Do not delete prior backup automatically.

## Alternative options (not recommended for MVP)
- Git submodule: high friction, repo coupling, and poor fit for embedded/forked YODA.
- Full vendoring with manual copy: lacks verification, error-prone without tooling.
- OS package managers: adds infra cost and complexity beyond MVP.

## Required behavior
- The install/update process MUST preserve `yoda/todos/`, `yoda/logs/`, `yoda/project/issues/`.
- The install/update process MUST NOT overwrite the host `README.md`.
- The YODA license MUST live at `yoda/LICENSE` and may be overwritten by updates.
- Updates MUST use checksum validation from `latest.json`.
- Tools SHOULD allow an explicit `--source` to support private forks/packages.
- Agent entry files MUST be preserved; YODA blocks are appended/updated (no destructive overwrite).

## Follow-ups
- Implement `yoda/scripts/update.py` with `--check`, `--apply`, `--source`.
- Define and ship `yoda-install.sh` with checksum verification.
- Add `yoda/LICENSE` to the package and align it with repository root LICENSE.
