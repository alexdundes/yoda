# Agent entry files

## Problem

Agent tools do not agree on which file to read (`AGENTS.md`, `GEMINI.md`, etc.).

## YODA proposal

- YODA is non-intrusive in host projects.
- YODA-owned agent entry files live under `yoda/`:
  - `yoda/AGENTS.md`
  - `yoda/GEMINI.md`
  - `yoda/CLAUDE.md`
- These files route agents to `yoda/yoda.md`.
- `yoda/yoda.md` contains the operational instructions for the embedded YODA layer.
- `init.py` MUST NOT create, update, append to, merge, or delete host-root agent or intent files such as `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `REPO_INTENT.md`, or `repo.intent.yaml`.

## Interoperability

- Host projects MAY keep their own root-level agent files.
- If a host project wants agent tools to discover YODA automatically, the host may manually point its own files to `yoda/yoda.md` or the YODA-local entry files.
- YODA package/update owns only files under `yoda/`.

## Simplified entry flow

1) User starts the agent with zero context.
2) User types a natural phrase indicating entering YODA Flow and taking the highest-priority selectable issue (with all dependencies resolved, and no issue currently `doing`).
   - The phrase must explicitly mention "YODA Flow" (or "YODA") and intent to take the highest-priority selectable issue (with all dependencies resolved).
   - Example: "Vamos entrar no YODA Flow e pegar a issue prioritaria sem dependencias."
3) Agent reads the relevant YODA-local entry file (`yoda/AGENTS.md`, `yoda/GEMINI.md`, or `yoda/CLAUDE.md`) when available, then reads `yoda/yoda.md`.
4) Agent resolves the developer slug in this order:
   - --dev `<slug>` flag
   - Ask the user when `--dev` is missing
   - Slug format: lowercase ASCII, digits, and hyphens only; must start with a letter; no spaces.
5) Agent executes `yoda/scripts/yoda_flow_next.py --dev <slug>` to select/resume the deterministic issue from markdown index (`yoda/project/issues/<dev>-<NNNN>-<slug>.md`) and follow the returned runbook.
   - If no selectable issue exists, the script returns blocker guidance and the agent must ask for resolution/next action.
