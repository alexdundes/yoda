# Agent entry and root file

## Problem

There is no consensus among agent tools about which file to read (AGENTS.md, gemini.md, etc.).

## YODA proposal

- Root file: yoda/yoda.md.
- This file contains the agent instructions for the project.
- init creates AGENTS.md or gemini.md pointing to yoda/yoda.md.

## Interoperability

- AGENTS.md (Codex) and gemini.md (Gemini CLI / anti-gravity) only route to yoda/yoda.md.

## Simplified entry flow

1) User starts the agent with zero context.
2) User types a natural phrase indicating entering YODA Flow and taking the highest-priority issue without dependencies.
3) Agent reads yoda/yoda.md.
4) Agent loads the corresponding TODO.dev.yaml, selects the highest-priority issue without dependencies using the canonical id, and follows the flow.
