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
    yoda_intake.py
    get_extern_issue.py
    todo_list.py
    todo_update.py
    todo_next.py
    log_add.py
    yoda_flow_next.py
    yoda_prep_flow.py
    init.py
    update.py
    requirements.txt
    lib/
      __init__.py
      cli.py
      dev.py
      error_messages.py
      errors.py
      external_issue_utils.py
      flow_log.py
      front_matter.py
      io.py
      issue_index.py
      issue_metadata.py
      issue_utils.py
      logging_utils.py
      order_utils.py
      output.py
      parse_utils.py
      paths.py
      provider_github.py
      provider_gitlab.py
      slug_utils.py
      templates.py
      time_utils.py
      todo_utils.py
      validate.py
      yaml_io.py
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
  - `--dev <developer-slug>`
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
- Every script execution that mutates metadata MUST append a compact entry via
  the shared Flow-log helper (or the command's own transition logger) before
  exiting successfully.
- Log messages should be detailed and traceable (one change per line with `field: old -> new`), or initial values on creation.

## Validation

- Validation is mandatory and embedded in any script that mutates metadata.
- Validation lives in `yoda/scripts/lib/validate.py` and is invoked before any write.

## IO and concurrency

- `issue_add.py` MUST implement concurrency control per developer slug (`--dev`) using an external lock file.
- Lock acquisition in `issue_add.py` MUST use retry with 3 attempts and increasing wait between attempts.
- If lock acquisition fails after retries, `issue_add.py` MUST fail with an explicit conflict error.
- No automatic rollback is required when a write step fails after lock acquisition; failure must be explicit.
- Writes that mutate artifacts during `issue_add.py` MUST use atomic replace semantics (temporary file + replace) to avoid partial/corrupted files.
- IO utilities live in `yoda/scripts/lib/io.py` and should be the only place for file writes.

## Paths and repo layout

- All paths are relative to repo root.
- Issue path: `yoda/project/issues/<id>-<slug>.md`.
- Flow log: `## Flow log` inside the issue Markdown file.
- Legacy compatibility paths: `yoda/todos/TODO.<dev>.yaml` and
  `yoda/logs/<id>-<slug>.yaml`; neither is a current Flow source of truth.

## Tests

- Use pytest as the standard testing framework.
- Unit tests are required for script development.
- Tests live in `yoda/scripts/tests/`.

## Versioning

- Scripts follow the CLI contract and schema versioning rules in `project/specs/13-yoda-scripts-v1.md`.
