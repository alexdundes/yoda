# Agent Entry

Read in order:

1) REPO_INTENT.md
2) yoda/yoda.md

## Packaging instruction

When the user asks to generate a distribution/package, run `python3 package.py --help` and follow the "Agent runbook" returned by the command.
Use `package.py` as the source of truth for packaging steps and changelog release-entry creation.

## YAML Schema Versioning (yoda-0038)

Internal YODA development policy for YAML layout/schema changes:

- `subtle`: backward-compatible layout/schema change; bump only minor schema version (same major).
- `breaking`: incompatible layout/schema change; bump major schema version and require migration handling in `yoda/scripts/update.py`.
- Rollout: after update flow, run/re-run `yoda/scripts/init.py` to re-sync embedded entry files/defaults when needed.
- Planning note for current backlog: `yoda-0035`, `yoda-0036`, and `yoda-0037` are classified as `subtle` and share a single minor schema bump in package `0.1.3`.

<!-- YODA:BEGIN -->
## YODA Framework

Read in order:

1) yoda/yoda.md
<!-- YODA:END -->
