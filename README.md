# YODA Framework Package

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="yoda/favicons/yoda-dark.svg">
  <img src="yoda/favicons/yoda-light.svg" alt="YODA Framework Logo" width="256" height="256">
</picture>

> **YODA Framework Package — YAML-Oriented Documentation & Agents**  
> A document-first framework for agent-assisted development, where YAML/Markdown are the source of truth. This package is meant to be embedded in other projects.

## What this package is
YODA Framework is a document-first system: we clarify intent before implementation, and we treat documentation as executable guidance. YAML captures structured state (TODOs, metadata, dependencies), Markdown captures narrative context (issues, decisions, constraints), and scripts operate on those artifacts deterministically.

The framework is organized around two cycles: **YODA Intake** (discovery/triage) and **YODA Flow** (execution). When the agent enters a cycle, it assumes the corresponding **skin** (Intake skin or Flow skin) to align posture, outputs, and constraints with that cycle.

## Quick install (one-liner)
This is the fastest path, but it executes a remote script directly. Use it only if you trust the source.

<!-- TODO: confirm GitHub Pages /docs hosting is enabled and URLs are correct. -->
```bash
curl -fsSL https://alexdundes.github.io/yoda/install/yoda-install.sh | sh -s -- --version <semver+build> --root .
```

Safety tips:
- Pin an explicit `--version`.
- Review the script if you are in a regulated environment.
- The installer must verify the tarball checksum from `latest.json`.

## Manual install (recommended)
1) Download `yoda-framework-<semver+build>.tar.gz` and `latest.json`.
2) Verify the `sha256` from `latest.json` matches the tarball.
3) Extract the package:
```bash
tar -xzf yoda-framework-<semver+build>.tar.gz -C <target>
```
4) Copy the `yoda/` subtree into the project root (preserve `yoda/todos/`, `yoda/logs/`, `yoda/project/issues/`).
5) Run init:
```bash
python yoda/scripts/init.py --dev <slug> --root .
```

## First run / Init
`init` appends the YODA entry block to agent files, creates the YODA folder structure if needed, and seeds `TODO.<dev>.yaml` when missing. It is idempotent and safe to rerun.

## What's inside
- `yoda/yoda.md` (embedded manual)
- `yoda/scripts/` (CLI tools)
- `yoda/templates/` (issue templates)
- `yoda/PACKAGE_MANIFEST.yaml` (build metadata)
- `yoda/CHANGELOG.yaml` (release history)

## Inspirations
- **DocDD**: documentation as the driver for software outcomes.
- **Docs-as-Code**: docs live in the repo, versioned and reviewed like code.
- **Design-first / Contract-first**: clarify interfaces and constraints before building.
- **Literate Programming**: a parallel to modern vibe-coding with issues and narrative context.

## Issues (Doc First in practice)
YODA Intake focuses on shaping issues before execution: define scope, acceptance criteria, risks, and dependencies. Those artifacts become the contract for YODA Flow, where a human-guided agent executes the work with higher quality and fewer surprises.

## Why the name YODA
YODA stands for **YAML-Oriented Documentation & Agents**. We always pair YODA with a context word (Framework, Intake, Flow) so it is clear whether we are talking about the overall framework or a specific cycle.

## Why YAML + scripts and Markdown
- **YAML + scripts**: YAML holds structured state; scripts read/write it deterministically for repeatable automation.
- **Markdown**: issues and decisions need narrative context that is human-readable and reviewable.

## Version & integrity
Check `yoda/PACKAGE_MANIFEST.yaml` for version/build metadata and `yoda/CHANGELOG.yaml` for release notes. Integrity is validated using the `latest.json` checksum model.

## Upgrade & rollback
Upgrades replace only the framework files under `yoda/` and preserve project data. Keep a backup at `yoda/_previous/<version>` to rollback by restoring the prior subtree.

## Source of truth
The authoritative specification lives in the upstream repo: https://github.com/alexdundes/yoda (see `project/specs/`).

## Where to read more
- `yoda/yoda.md` for the embedded manual
- `yoda/scripts/README.md` for script usage

## License
See `LICENSE` at the repo root.
