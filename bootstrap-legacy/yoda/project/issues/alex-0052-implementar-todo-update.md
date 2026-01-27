---
schema_version: "1.0"
id: alex-0052
title: Implementar script de atualizacao de TODO (todo_update.py)
slug: implementar-todo-update
description: Implementar o todo_update.py conforme a spec project/specs/20-todo-update-script.md.
status: done
priority: 3
lightweight: false
agent: Human
depends_on: [alex-0051]
pending_reason: ""
created_at: "2026-01-27T12:42:31-03:00"
updated_at: "2026-01-27T13:01:23-03:00"
entrypoints: []
tags: [scripts, todo, python]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-0052 - Implementar script de atualizacao de TODO (todo_update.py)

## Summary
Implementar o `todo_update.py` seguindo a spec definida em `project/specs/20-todo-update-script.md`.

## Context
A especificacao do `todo_update.py` sera criada em `project/specs/20-todo-update-script.md`. Esta issue cobre apenas a implementacao baseada naquela spec.

## Objective
Entregar o script `yoda/scripts/todo_update.py` conforme a spec, com validacao e saidas padronizadas.

## Scope
- Implementar o script `yoda/scripts/todo_update.py` conforme a spec.
- Garantir atualizacao de campos do TODO e `updated_at` conforme regras.
- Manter compatibilidade com a estrutura definida em `project/specs/15-scripts-python-structure.md`.

## Out of scope
- Alterar a spec do `todo_update.py`.
- Implementar outros scripts v1.

## Requirements
- Implementacao deve seguir `project/specs/20-todo-update-script.md` sem divergencias.
- Validacao deve bloquear escrita em caso de erro.
- Suporte a `--dev`, `--dry-run`, `--format` e codigos de saida conforme spec.

## Acceptance criteria
- [x] `yoda/scripts/todo_update.py` existe e segue a spec `project/specs/20-todo-update-script.md`.
- [x] O script atualiza o TODO correto e respeita `--dry-run`.
- [x] Validacao embutida impede escrita em caso de erro.

## Dependencies
- alex-0051

## Entry points
- path: project/specs/20-todo-update-script.md
  type: doc
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: project/specs/04-todo-dev-yaml-issues.md
  type: doc
- path: project/specs/15-scripts-python-structure.md
  type: doc
- path: yoda/scripts/README.md
  type: doc

## Implementation notes
- Seguir o layout de pacotes e padroes de saida descritos em `project/specs/15-scripts-python-structure.md`.

## Tests
Not applicable.

## Risks and edge cases
- Divergencias com a spec podem quebrar a compatibilidade dos scripts v1.
- Erros de validacao podem bloquear updates legitimos.

## Result log
Implementado `yoda/scripts/todo_update.py` com suporte a atualizacao de campos e append de log via `log_add.py`.

feat(yoda): implementar todo_update.py

Issue: alex-0052
Path: `yoda/project/issues/alex-0052-implementar-todo-update.md`
