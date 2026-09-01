# YODA Framework Package

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="favicons/yoda-dark.svg">
  <img src="favicons/yoda-light.svg" alt="YODA Framework Logo" width="256" height="256">
</picture>

> **YODA Framework Package — YAML-Oriented Documentation & Agents**  
> A document-first framework for agent-assisted development, where issue Markdown is the operational source of truth. This package is meant to be embedded in other projects.

## What this package is
YODA Framework is a document-first system: we clarify intent before implementation, and we treat documentation as executable guidance. Issue Markdown captures both structured metadata and narrative context (issues, decisions, constraints), and scripts operate on those artifacts deterministically.

The framework is organized around two primary cycles: **YODA Intake**
(discovery/triage) and **YODA Flow** (execution). **YODA Prep Flow** can prepare
an explicit issue through Study and Document before it enters implementation.
When the agent enters a cycle, it assumes the corresponding posture, outputs,
and constraints.

Visit the [YODA Framework site](https://alexdundes.github.io/yoda/) for the
published guide and project story. The site is maintained from this
repository's `docs/` directory.

### Who this README is for

This file serves two audiences at once. Most of it — installing, initializing,
and running YODA — applies to any project with YODA embedded. Sections marked
**(development repository)** apply only to the repository where YODA itself is
built, and describe files that are not part of the distributed package.

## Command placeholders

Text inside angle brackets, such as `<semver+build>` or `<target>`, is a
placeholder that must be replaced. Do not type the `<` and `>` characters.

## Choose your developer slug

The **developer slug** is a short, stable namespace used as the prefix of your
YODA issue IDs. For example, the developer slug `mynick` produces issue IDs
such as `mynick-0001`. Reuse the same value in later YODA commands.

Use lowercase ASCII letters, digits, and hyphens, and start with a letter.

- Valid: `mynick`, `fernando`, `time-backend`
- Invalid: `MeuNick` (uppercase), `123fernando` (starts with a digit),
  `fernando_silva` (underscore)

## Quick install (one-liner)
This is the fastest path, but it executes a remote script directly. Use it only if you trust the source.

Latest (no version, simplest):
```bash
curl -fsSL https://alexdundes.github.io/yoda/install/yoda-install.sh | sh -s -- --root .
```

Pinned expected version (fails if current `latest.json` differs):
```bash
curl -fsSL https://alexdundes.github.io/yoda/install/yoda-install.sh | sh -s -- --version <semver+build> --root .
```

Safety tips:
- Prefer the pinned command for production or regulated environments.
- Review the script before running it in sensitive contexts.
- The installer verifies the tarball checksum from `latest.json`.

## Manual install (recommended)
1) Download `yoda-framework-<semver+build>.tar.gz` and `latest.json`.
2) Verify the `sha256` from `latest.json` matches the tarball.
3) Extract the package:
```bash
tar -xzf yoda-framework-<semver+build>.tar.gz -C <target>
```
4) Copy the `yoda/` subtree into the project root (preserve `yoda/project/issues/` and `yoda/project/extern_issues/` if already present).
5) Run init:
```bash
python3 yoda/scripts/init.py --dev mynick --root .
```

`mynick` is a concrete example: replace it with your chosen developer slug.
`--root .` initializes the current directory.

## First run / Init

The minimal first-run flow is:

1. Install or extract YODA into the project.
2. Choose and remember your developer slug.
3. Run `python3 yoda/scripts/init.py --dev mynick --root .`, replacing
   `mynick` with your value.
4. Review the reported directories and files created, migrated, reconciled, or
   skipped.
5. Start YODA Intake to create the first issue:

```bash
python3 yoda/scripts/yoda_intake.py --dev mynick
```

`init` creates or reconciles YODA-managed structure and compatible metadata
under `yoda/`. It does not create or edit host-project agent files such as
`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `REPO_INTENT.md`, or
`repo.intent.yaml`. Host projects may point their own agent files to
`yoda/yoda.md` manually.

## What's inside
- `yoda/yoda.md` (embedded manual)
- `yoda/AGENTS.md`, `yoda/GEMINI.md`, `yoda/CLAUDE.md` (YODA-local agent entries)
- `yoda/scripts/` (CLI tools)
- `yoda/templates/` (issue templates)
- `yoda/PACKAGE_MANIFEST.yaml` (build metadata)
- `CHANGELOG.yaml` (release history)

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
- **Markdown + scripts (canonical)**: issue Markdown is the operational contract for backlog and flow.
- **YAML (compatibility)**: YAML artifacts may appear in migration/legacy paths, but are not the primary execution source in 0.4.x.

## Version & integrity
Check `yoda/PACKAGE_MANIFEST.yaml` for version/build metadata and `CHANGELOG.yaml` for release notes. Integrity is validated using the `latest.json` checksum model.

## Upgrade & rollback
Upgrades replace only the framework files under `yoda/` and preserve project data. Keep a backup at `yoda/_previous/<version>` to rollback by restoring the prior subtree.

## Source of truth
For embedded projects, the operational source of truth is inside the package:
issue Markdown under `yoda/project/issues/`, the embedded manual at
`yoda/yoda.md`, and the runbooks printed by `yoda/scripts/*.py --help`.

## Test suites (development repository)
Two suites, each with its own scope. **Run one at a time.** They cannot be
passed to the same `pytest` invocation: each has its own `conftest.py`, and
pytest imports them under the same module name, so a combined run fails during
collection.

```bash
python3 -m pytest yoda/scripts/tests
```

Validates the product: scripts, flow transitions, issue index, packaging, and
CLI contracts. This suite ships with the source tree but is excluded from the
distribution package.

```bash
python3 -m pytest project/tests
```

Validates the boundary between this repository and the distributed product:
that the specification set stays portable and free of references to the
development history, and that the package neither ships nor needs it. This
suite exists only in the development repository.

## Where to read more
- `yoda/yoda.md` for the embedded manual
- `yoda/scripts/README.md` for script usage

## License
See `LICENSE` at the repo root.
