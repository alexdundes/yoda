# Repository Intent

This repository is a meta-implementation of the YODA Framework.

## Purpose

- project/specs/ is the source of truth for the future YODA Framework.
- yoda/ is the implementation workspace under construction.
- yoda/ is aligned with the framework specs and uses YAML-based TODOs and logs.
- bootstrap-legacy/ preserves artifacts generated during the bootstrap of this meta-implementation.

## bootstrap-legacy/ (historical)

- Created during bootstrap when scripts were not available and YAML artifacts in the spec did not exist.
- During bootstrap, agents used Markdown alternatives in place of the YAML files.
- By the end of bootstrap, some scripts existed; Markdown records were used to generate YAML files to validate concepts.
- This folder is legacy-only, not used by the current workflow, and kept for historical verification.

## Guardrails

- Do not "fix" yoda/ to match project/specs without an explicit issue.
- If there is a conflict, prioritize project/specs/ and resolve via an explicit issue.

## Entry order for agents

1) REPO_INTENT.md
2) yoda/yoda.md
3) project/specs/
4) current issue file

<!-- YODA:BEGIN -->
## YODA Framework

Read in order:

1) REPO_INTENT.md
2) yoda/yoda.md
<!-- YODA:END -->
