# Agent playbook

## Objective

Define deterministic agent behavior for YODA Flow and YODA Intake.

## YODA Flow entry

When human intent is to start YODA Flow:

1) Resolve developer slug.
2) Run `python3 yoda/scripts/yoda_flow_next.py --dev <slug>` to enter the phase
   before doing any of its work.
3) Present returned issue context and `runbook_line`.
4) Execute only that phase, present its deliverable, and stop.
5) Ask human authorization before the next transition.

Command output is the input of the next step. The agent MUST NOT discard,
silence, or redirect the output of a YODA command.

## YODA Flow rules

- Issue Markdown is the execution source of truth.
- `yoda_flow_next.py` resolves only the next deterministic step.
- Phase progression is unitary (`study -> document -> implement -> evaluate`).
- On blockers, `yoda_flow_next.py` does not mutate state and provides deterministic instruction for `todo_update.py`.
- `todo_update.py` is the permanent tool for semantic corrections and metadata adjustments.
- `log_add.py` is the permanent tool for issue-related logging outside flow steps.

## YODA Prep Flow entry

When human intent explicitly names YODA Prep Flow:

1) Read `python3 yoda/scripts/yoda_prep_flow.py --help`.
2) Run it with `--dev <slug> --issue <id>`.
3) Execute only the returned Study or Document instruction.
4) Wait for explicit human authorization before the next prep step.
5) Do not implement while operating YODA Prep Flow.

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

- For embedded YODA, use the YODA-local entry files under `yoda/` and `yoda/yoda.md`; do not assume YODA controls host-root agent files.
- Before operating any YODA command, check `<command> --help` for command-specific runbook/guidance.
- Use `todo_next.py` and `todo_list.py` only for inspection; do not use them to
  replace deterministic phase transitions in `yoda_flow_next.py`.
- Do not duplicate dependency metadata in issue body.
- Keep `Entry points` as simple list items.
