# Python structure for YODA scripts

This document defines the base Python project structure for YODA scripts in `yoda/scripts/`. It is a shared foundation for all v1 commands.

## Goals

- Keep scripts simple, consistent, and reusable.
- Minimize duplication via a small shared library.
- Prefer standard Python tools available on most machines.

## Layout

```
yoda/
  scripts/
    issue_add.py
    issue_render.py
    todo_list.py
    todo_update.py
    todo_next.py
    todo_reorder.py
    log_add.py
    requirements.txt
    lib/
      __init__.py
      cli.py
      paths.py
      io.py
      yaml_io.py
      front_matter.py
      templates.py
      validate.py
      errors.py
```

Notes:
- Command files live directly in `yoda/scripts/`.
- Reusable helpers live in `yoda/scripts/lib/`.

## Dependencies

- Standard library is preferred by default.
- External dependencies are allowed when they simplify correctness or maintenance.
- Package installation uses `pip` with `yoda/scripts/requirements.txt`.

Recommended dependencies for v1:
- PyYAML (YAML parsing/serialization).
- python-frontmatter (Markdown front matter parsing/serialization).

## Imports and reuse

- Command scripts MUST import shared logic from `yoda/scripts/lib/`.
- Do not duplicate parsing, IO, or validation logic in each script.
- Common concerns (paths, IO, YAML, front matter, validation, CLI flags) live in `lib/`.

## CLI conventions

- Each script MUST expose a `main()` entrypoint.
- Use `argparse` for CLI parsing.
- Global flags are defined once in `yoda/scripts/lib/cli.py` and reused:
  - `--dev <slug>`
  - `--format md|json`
  - `--json`
  - `--dry-run`
  - `--verbose`

## Logging and errors

- Use Python stdlib `logging`.
- Default level: INFO.
- `--verbose` MUST enable DEBUG logging.
- Errors MUST be written to stderr with short, actionable messages.
- Exit codes must follow the CLI contract in `project/specs/13-yoda-scripts-v1.md`.
- Every script execution that mutates metadata MUST append a log entry via `log_add.py` (or equivalent shared helper) before exiting successfully.
- Log messages should be detailed and traceable (one change per line with `field: old -> new`), or initial values on creation.

## Validation

- Validation is mandatory and embedded in any script that mutates metadata.
- Validation lives in `yoda/scripts/lib/validate.py` and is invoked before any write.

## IO and concurrency

- No special concurrency handling is required for v1.
- IO utilities live in `yoda/scripts/lib/io.py` and should be the only place for file writes.

## Paths and repo layout

- All paths are relative to repo root.
- TODO path: `yoda/todos/TODO.<dev>.yaml`.
- Issue path: `yoda/project/issues/<id>-<slug>.md`.
- Log path: `yoda/logs/<id>-<slug>.yaml`.

## Tests

- Use pytest as the standard testing framework.
- Unit tests are required for script development.
- Tests live in `yoda/scripts/tests/`.

## Versioning

- Scripts follow the CLI contract and schema versioning rules in `project/specs/13-yoda-scripts-v1.md`.
