# Scripts and automation

## Objective

Standardize repetitive tasks and reduce the need for manual edits.

## Location and language

- Folder: yoda/scripts
- Language: Python
- Rule: the .py file name is the command name

## Minimum scripts (v1)

- init.py: creates the minimum YODA Framework structure
- issue_add.py: adds an issue to `TODO.<dev>.yaml` and generates the issue Markdown from the template using basic fields provided by the agent
- `TODO.<dev>.yaml` maintenance scripts (list, update, reorder, etc.)
- scripts to present `TODO.<dev>.yaml` in a human-readable format for humans and agents
- log scripts to record flow events
- pending resolution script (sets status from pending and clears pending_reason)

## Logs

- One log per issue at yoda/logs/dev-id-slug.yaml

## Principles

- Scripts are the official way to change metadata.
- The human or orchestrator executes the commands.
- When scripts are available, they are mandatory for metadata changes; bootstrap is the only exception.

## Benefits

- Consistent structure.
- Fewer errors when handling metadata.
- Easier auditing and reproducibility.
