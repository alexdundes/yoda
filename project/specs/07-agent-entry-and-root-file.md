# Agent entry and root file

## Problem

Agent tools do not agree on which file to read (AGENTS.md, gemini.md, etc.).

## YODA proposal

- Root file: yoda/yoda.md.
- This file contains the agent instructions for the project.
- init creates AGENTS.md or gemini.md pointing to yoda/yoda.md.

## Interoperability

- AGENTS.md (Codex) and gemini.md (Gemini CLI / anti-gravity) only route to yoda/yoda.md.

## Simplified entry flow

1) User starts the agent with zero context.
2) User types a natural phrase indicating entering YODA Flow and taking the highest-priority issue without dependencies.
   - The phrase must explicitly mention "YODA Flow" (or "YODA") and intent to take the highest-priority issue without dependencies.
   - Example: "Vamos entrar no YODA Flow e pegar a issue prioritaria sem dependencias."
3) Agent reads yoda/yoda.md.
4) Agent resolves the developer slug in this order:
   - --dev `<slug>` flag (preferred when available)
   - YODA_DEV environment variable
   - Ask the user (fallback)
   - Slug format: lowercase ASCII, digits, and hyphens only; must start with a letter; no spaces.
5) Agent loads `TODO.<dev>.yaml`, selects the highest-priority issue without dependencies using the canonical id, and follows the flow.
