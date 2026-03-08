# Agent entry and root file

## Problem

Agent tools do not agree on which file to read (`AGENTS.md`, `GEMINI.md`, etc.).

## YODA proposal

- Root file: `yoda/yoda.md`.
- This file contains the agent instructions for the project.
- In an embedded YODA setup, `yoda/yoda.md` is the **README.md** for the YODA layer inside a host project (human-readable context for agents).
- init creates/updates agent entry files (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`) pointing to `yoda/yoda.md`, appending a delimited YODA block to preserve existing content.

## Interoperability

- `AGENTS.md` (Codex), `GEMINI.md` (Gemini CLI / anti-gravity), and other supported files only route to `yoda/yoda.md`.

## Simplified entry flow

1) User starts the agent with zero context.
2) User types a natural phrase indicating entering YODA Flow and taking the highest-priority selectable issue (with all dependencies resolved, and no issue currently `doing`).
   - The phrase must explicitly mention "YODA Flow" (or "YODA") and intent to take the highest-priority selectable issue (with all dependencies resolved).
   - Example: "Vamos entrar no YODA Flow e pegar a issue prioritaria sem dependencias."
3) Agent reads `yoda/yoda.md`.
4) Agent resolves the developer slug in this order:
   - --dev `<slug>` flag
   - Ask the user when `--dev` is missing
   - Slug format: lowercase ASCII, digits, and hyphens only; must start with a letter; no spaces.
5) Agent executes `yoda/scripts/yoda_flow_next.py --dev <slug>` to select/resume the deterministic issue from markdown index (`yoda/project/issues/<dev>-<NNNN>-<slug>.md`) and follow the returned runbook.
   - If no selectable issue exists, the script returns blocker guidance and the agent must ask for resolution/next action.
