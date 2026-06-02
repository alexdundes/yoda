# YODA Framework - Minimum structure

## Required structure

```text
.
├─ yoda/
│  ├─ AGENTS.md
│  ├─ GEMINI.md
│  ├─ CLAUDE.md
│  ├─ yoda.md
│  ├─ templates/
│  │  └─ issue.md
│  ├─ scripts/
│  ├─ project/
│  │  ├─ issues/
│  │  └─ extern_issues/
│  ├─ logs/                  # compatibility and auxiliary logs
│  └─ todos/                 # compatibility artifacts during migration
```

## Canonical execution data

- Canonical flow execution data lives in `yoda/project/issues/*.md`.
- Issue IDs are filename-derived.

## Agent entry files

- YODA-local agent entry files live in `yoda/AGENTS.md`, `yoda/GEMINI.md`, and `yoda/CLAUDE.md`.
- These files point to `yoda/yoda.md` and are framework files.
- Host-root agent files are outside YODA ownership and are not created or modified by `init.py`.

## Compatibility data

- `yoda/todos/` and legacy log artifacts may persist during migration/compatibility.
- Flow operation in 0.3.0 does not depend on `todo_next.py`.

## Issue file requirements

- Name pattern: `<dev>-<NNNN>-<slug>.md`.
- Front matter and body follow 0.3.0 contracts from specs.
