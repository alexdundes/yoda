# Agent entry and root file

## Problem

Agent tools do not agree on which file to read ([AGENTS.md](../AGENTS.md), [gemini.md](../gemini.md), etc.).

## YODA proposal

- Root file: [`yoda/yoda.md`](../yoda/yoda.md).
- This file contains the agent instructions for the project.
- In an embedded YODA setup, `yoda/yoda.md` is the **README.md** for the YODA layer inside a host project (human-readable context for agents).
- init creates [AGENTS.md](../AGENTS.md) or [gemini.md](../gemini.md) pointing to [`yoda/yoda.md`](../yoda/yoda.md).

## Interoperability

- [AGENTS.md](../AGENTS.md) (Codex) and [gemini.md](../gemini.md) (Gemini CLI / anti-gravity) only route to [`yoda/yoda.md`](../yoda/yoda.md).

## Simplified entry flow

1) User starts the agent with zero context.
2) User types a natural phrase indicating entering YODA Flow and taking the highest-priority issue without dependencies.
   - The phrase must explicitly mention "YODA Flow" (or "YODA") and intent to take the highest-priority issue without dependencies.
   - Example: "Vamos entrar no YODA Flow e pegar a issue prioritaria sem dependencias."
3) Agent reads [`yoda/yoda.md`](../yoda/yoda.md).
4) Agent resolves the developer slug in this order:
   - --dev `<slug>` flag (preferred when available)
   - YODA_DEV environment variable
   - Ask the user (fallback)
   - Slug format: lowercase ASCII, digits, and hyphens only; must start with a letter; no spaces.
5) Agent loads [`yoda/todos/TODO.<dev>.yaml`](../yoda/todos/), selects the highest-priority issue without dependencies using the canonical id, and follows the flow.
   - Bootstrap exception: if YAML is not available, load [`yoda/todos/TODO.<dev>.md`](../yoda/todos/) (see [project/specs/15-bootstrap.md](15-bootstrap.md)).
   - If the expected TODO file is missing, ask the user which TODO to use.
