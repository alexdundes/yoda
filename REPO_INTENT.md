# Repository Intent

This repository is a meta-implementation of the YODA Framework.

## Purpose

- project/specs/ is the source of truth for the future YODA Framework.
- yoda/ is the implementation workspace under construction.
- Until scripts v1 exist, yoda/ uses Markdown for TODOs and logs by design.

## Guardrails

- Do not "fix" yoda/ to match project/specs without an explicit issue.
- If there is a conflict, assume yoda/ is in bootstrap and do not migrate formats.

## Entry order for agents

1) REPO_INTENT.md
2) yoda/yoda.md
3) project/specs/
4) current issue file
