# Agent playbook

## Objective

Define deterministic agent behavior for YODA Flow and YODA Intake.

## YODA Flow entry

When human intent is to start YODA Flow:

1) Resolve developer slug.
2) Run `python3 yoda/scripts/yoda_flow_next.py --dev <slug>`.
3) Present returned issue context and `runbook_line`.
4) Ask human confirmation before moving to next phase action.

## YODA Flow rules

- Issue Markdown is the execution source of truth.
- `yoda_flow_next.py` resolves only the next deterministic step.
- Phase progression is unitary (`study -> document -> implement -> evaluate`).
- On blockers, `yoda_flow_next.py` does not mutate state and provides deterministic instruction for `todo_update.py`.
- `todo_update.py` is the permanent tool for semantic corrections and metadata adjustments.
- `log_add.py` is the permanent tool for issue-related logging outside flow steps.

## Phase discipline

- Move between phases only with explicit human authorization.
- Document phase updates issue text for clarity and approval.
- Implement phase applies only approved scope.
- Evaluate validates acceptance and prepares final result log.

## Logging discipline

- Log entries must be compact and one-line.
- Use `log_add.py` for out-of-flow issue context.

## YODA Intake

- Intake remains separate from Flow.
- Use `yoda_intake.py` runbooks and `issue_add.py` for backlog creation.

## General rules

- Before operating any YODA command, check `<command> --help` for command-specific runbook/guidance.
- Do not rely on removed flow contracts (`todo_next.py`).
- Do not duplicate dependency metadata in issue body.
- Keep `Entry points` as simple list items.
