# yoda/scripts

Operational scripts for the YODA Framework (issue-markdown-driven flow).

This directory is self-contained for embedded YODA usage. For operational details,
read each command's `--help` output and follow the Agent guidance/runbook printed
by the command.

## Quick rules

- Always check `<command> --help` before running a command.
- `--dev` is required for YODA commands.
- Exception: `update.py` may run without `--dev`.
- `yoda_flow_next.py` is the primary YODA Flow command.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r yoda/scripts/requirements.txt

python yoda/scripts/yoda_flow_next.py --dev dev
python yoda/scripts/yoda_flow_next.py --dev dev --log-message "Study completed"
python yoda/scripts/yoda_prep_flow.py --dev dev --issue dev-0001
python yoda/scripts/yoda_intake.py --dev dev
python yoda/scripts/get_extern_issue.py --dev dev --extern-issue 123
python yoda/scripts/todo_update.py --dev dev --issue dev-0001 --status doing --phase study
python yoda/scripts/log_add.py --dev dev --issue dev-0001 --message "Additional context"
```

## Flow and Intake

- Deterministic YODA Flow: `yoda_flow_next.py`
- Explicit issue Study/Document preparation: `yoda_prep_flow.py`
- Intake runbooks: `yoda_intake.py`
- Manual semantic/process adjustments: `todo_update.py`
- Exceptional manual logging: `log_add.py`

## Init in a host project

`init.py` manages YODA-owned structure under `yoda/`; it does not create or edit
host-root agent or intent files.

```bash
python yoda/scripts/init.py --dev <slug>
python yoda/scripts/init.py --dev <slug> --root /path/to/project --dry-run
python yoda/scripts/init.py --dev <slug> --force
python yoda/scripts/init.py --dev <slug> --reconcile-layout
```

## Issue front matter (canonical order)

`schema_version`, `status`, `phase` (when `status=doing`), `depends_on`, `title`, `description`, `priority`, `extern_issue_file`, `created_at`, `updated_at`.
