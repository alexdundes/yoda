---
agent: Human
created_at: '2026-01-27T19:14:48-03:00'
depends_on: []
description: Revise 06-agent-playbook.md and yoda/yoda.md to reflect YODA Flow with
  available scripts
entrypoints: []
id: yoda-0010
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: update-agent-playbook-to-use-scripts
status: done
tags: []
title: Update agent playbook to use scripts
updated_at: '2026-01-27T20:40:15-03:00'
---

# yoda-0010 - Update agent playbook to use scripts

## Summary
Revise the agent playbook and `yoda/yoda.md` to describe a script-backed YODA Flow entry and cycle, aligned with the human↔agent handshake and the single-issue rule.

## Context
We now have `todo_next.py`, `todo_update.py`, and `log_add.py`. The playbook should reflect how the agent uses them within the YODA Flow. Issue creation (`issue_add.py`) is out of scope for the YODA Flow and will be defined in a separate cycle later.

## Objective
Document a script-backed YODA Flow in `project/specs/06-agent-playbook.md` and align `yoda/yoda.md` entry instructions with the entry trigger phrases, selection rules, and per-phase script usage.

## Scope
- Update `project/specs/06-agent-playbook.md` to include script usage per phase and the human confirmation loop.
- Update `yoda/yoda.md` to reflect the entry phrase, `todo_next.py` selection, and script-driven state/log updates.

## Out of scope
- Implementing new scripts.
- Defining the issue-creation cycle (outside YODA Flow).
- Changing YODA Flow semantics beyond clarifying the script-backed flow.

## Requirements
- YODA Flow entry is triggered by a natural phrase (e.g., “Vamos fazer o YODA Flow”, “YODA Flow, lá vamos nós”, “YODA Flow, próxima issue”).
- Agent resolves developer slug if missing, then calls `todo_next.py`.
- Playbook must define how to handle `todo_next.py` errors and pending hints.
- Agent confirms with the human before starting the selected issue (e.g., “Inicio o YODA Flow da issue dev-0001?”).
- On confirmation, agent sets status to `doing` via `todo_update.py`, then enters Study.
- Study repeats as needed; agent asks permission to move to Document.
- If the human requests pending during the cycle, agent sets status to `pending` with `todo_update.py` and includes the provided reason.
- If Study discovers blocking dependencies, agent updates `depends_on` (and priority if needed) via `todo_update.py`, then continues Study.
- Document updates the issue text, logs decisions via `log_add.py`, and asks for approval; rejection returns to Study.
- Implement executes the issue plan; if new decisions arise, log them via `log_add.py`.
- Evaluate checks criteria, updates the “Result log” with commit suggestion, and asks for approval.
- If approved, agent marks `done` via `todo_update.py`; if rejected, return to Study.
- After finishing, agent runs `todo_next.py` and offers the next cycle or a non-YODA activity.
- Issue creation is explicitly out of scope for YODA Flow.
- Playbook must include example script invocations for each phase.

## Acceptance criteria
- [x] `project/specs/06-agent-playbook.md` describes the full script-backed YODA Flow cycle and human confirmation loop.
- [x] `yoda/yoda.md` entry instructions reflect the YODA Flow entry phrases and `todo_next.py` usage.
- [x] Out-of-scope note clearly excludes issue creation from the YODA Flow.

## Dependencies
None.

## Entry points
- path: project/specs/06-agent-playbook.md
  type: doc
- path: yoda/yoda.md
  type: doc

## Implementation notes
Keep the flow rules consistent with existing specs (single issue doing, pending handling, to-do-only selection).

## Tests
Not applicable.

## Risks and edge cases
- Docs can drift if script behavior changes; keep references specific.

## Result log
Updated the agent playbook with a script-backed YODA Flow entry and per-phase examples, including pending/depends_on handling, and aligned `yoda/yoda.md` with entry phrases and `todo_next.py` usage. Explicitly excluded issue creation from the flow.

Commit suggestion:
docs: script-backed yoda flow

Issue: `yoda-0010`
Path: `yoda/project/issues/yoda-0010-update-agent-playbook-to-use-scripts.md`