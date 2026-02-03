# Agent entry and root file

## Problem

Agent tools do not agree on which file to read (`AGENTS.md`, `gemini.md`, etc.).

## YODA proposal

- Root file: `yoda/yoda.md`.
- This file contains the agent instructions for the project.
- In an embedded YODA setup, `yoda/yoda.md` is the **README.md** for the YODA layer inside a host project (human-readable context for agents).
- init creates/updates agent entry files (`AGENTS.md`, `gemini.md`, `CLAUDE.md`, `agent.md`) pointing to `yoda/yoda.md`, appending a delimited YODA block to preserve existing content.

## Interoperability

- `AGENTS.md` (Codex), `gemini.md` (Gemini CLI / anti-gravity), and other supported files only route to `yoda/yoda.md`.

## Simplified entry flow

1) User starts the agent with zero context.
2) User types a natural phrase indicating entering YODA Flow and taking the highest-priority selectable issue (with all dependencies resolved, and no issue currently `doing`).
   - The phrase must explicitly mention "YODA Flow" (or "YODA") and intent to take the highest-priority selectable issue (with all dependencies resolved).
   - Example: "Vamos entrar no YODA Flow e pegar a issue prioritaria sem dependencias."
3) Agent reads `yoda/yoda.md`.
4) Agent resolves the developer slug in this order:
   - --dev `<slug>` flag (preferred when available)
   - YODA_DEV environment variable
   - Ask the user (fallback)
   - Slug format: lowercase ASCII, digits, and hyphens only; must start with a letter; no spaces.
5) Agent loads `yoda/todos/TODO.<dev>.yaml`, selects the highest-priority selectable issue (status `to-do`, dependencies resolved, and no issue `doing`) using the canonical id, and follows the flow.
   - If the expected TODO file is missing, ask the user which TODO to use.
