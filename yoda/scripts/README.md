# yoda/scripts

Scripts for YODA TODO, issue, and log automation. See `project/specs/13-yoda-scripts-v1.md`.

## Quickstart

Use a virtual environment, install the requirements from `yoda/scripts/requirements.txt`, and run the scripts as needed.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r yoda/scripts/requirements.txt

python yoda/scripts/issue_add.py --title "Example issue" --description "Short description"
python yoda/scripts/todo_update.py --issue dev-0001 --status doing
python yoda/scripts/log_add.py --issue dev-0001 --message "[dev-0001] Started work"
```

## Package artefact

Build the distributable YODA package (tar.gz) and let `package.py` create the release entry in `CHANGELOG.yaml`.

```bash
python package.py --dev <slug> --next-version 1.3.0 --summary "Release summary" --archive-format tar.gz --dir dist
python package.py --dev <slug> --next-version 1.3.0 --summary "Release summary" --dry-run
```

Notes:
- Requires `README.md`, `LICENSE`, and `CHANGELOG.yaml` (or `--changelog`).
- `--next-version` generates build metadata as `YYYYMMDD.<short-commit>` and prepends the changelog entry.
- Excludes `yoda/scripts/tests` from the package.
- `--dev` defines `built_by` in the manifest; use `--json` or `--format json` for JSON output.

## Init a host project

Prepare a host project after extracting the YODA package.

```bash
python yoda/scripts/init.py --dev <slug>
python yoda/scripts/init.py --dev <slug> --root /path/to/project --dry-run
python yoda/scripts/init.py --dev <slug> --force
```

Notes:
- Creates/updates `AGENTS.md`, `gemini.md`, `CLAUDE.md`, `agent.md`, plus `yoda/todos/TODO.<dev>.yaml` and required folders.
- Preserves existing agent file content (appends the YODA block); `--force` only overwrites the TODO file.

## Tests

```bash
python3 -m pytest yoda/scripts/tests
```
