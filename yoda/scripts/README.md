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

`--dev` receives a developer slug: a stable namespace used as the issue ID
prefix. Use lowercase ASCII letters, digits, and hyphens, beginning with a
letter (example: `mynick`). In command examples, `<developer-slug>` is a
placeholder to replace; do not type the angle brackets.

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

- Deterministic issue selection and phase transitions: `yoda_flow_next.py`
- Next-selection inspection without mutation: `todo_next.py`
- Ordered backlog view, not an execution plan: `todo_list.py`
- Explicit issue Study/Document preparation: `yoda_prep_flow.py`
- Intake runbooks: `yoda_intake.py`
- Manual semantic/process adjustments: `todo_update.py`
- Exceptional manual logging: `log_add.py`

### Intake priority policy

Keep `priority: 5` by default and do not rank issues in a batch or encode their
planned sequence with priority. Natural order resumes the current `doing` issue,
defers unresolved real dependencies, and then follows stable issue ID order.
Create batch issues in that desired order and use `depends_on` only for real
precedence.

Values above `5` anticipate and values below `5` postpone work against natural
order. Either is an exception: record the relative reason in the issue Markdown.
Omitting `--priority` in `issue_add.py` is the normal path.

### External issue collection

`get_extern_issue.py` prefers the authenticated provider CLI. When the origin
is `github.com`, a public issue is fetched through unauthenticated HTTP if `gh`
is missing or its authentication is unavailable. Private repositories, GitHub
Enterprise, and GitLab still require valid CLI authentication.

The command reports `authenticated-cli` or `public-http`; this operational
detail is not written into the external issue JSON consumed by Intake. Public
GitHub access has a lower rate limit, and an ambiguous access/404 error directs
the operator to `gh auth login` rather than asserting that the issue does not
exist.

## Init in a host project

`init.py` manages YODA-owned structure under `yoda/`; it does not create or edit
host-root agent or intent files.

```bash
python yoda/scripts/init.py --dev <developer-slug>
python yoda/scripts/init.py --dev <developer-slug> --root /path/to/project --dry-run
python yoda/scripts/init.py --dev <developer-slug> --reconcile-layout
```

Normal first use does not need `--reconcile-layout`. That option is an advanced
migration operation that touches Markdown files under the project root and
reconciles legacy TODO/issue metadata.

## Issue front matter (canonical order)

Current schema is `2.01`; readers accept `2.00` during migration.

`schema_version`, `status`, `phase` (when `status=doing`),
`flow_prepared_until` (optional), `pending_reason` (only for `pending`),
`depends_on`, `title`, `description`, `priority`, `extern_issue_file`,
`created_at`, `updated_at`.
