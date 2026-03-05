# YODA Framework - Minimum structure

## Required structure

```text
.
├─ yoda/
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

## Compatibility data

- `yoda/todos/` and legacy log artifacts may persist during migration/compatibility.
- Flow operation in 0.3.0 does not depend on `todo_next.py`.

## Issue file requirements

- Name pattern: `<dev>-<NNNN>-<slug>.md`.
- Front matter and body follow 0.3.0 contracts from specs.
