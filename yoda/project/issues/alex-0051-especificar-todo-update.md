---
schema_version: "1.0"
id: alex-0051
title: Especificar script de atualizacao de TODO (todo_update.py)
slug: especificar-todo-update
description: Especificar o comportamento do todo_update.py e criar a spec em project/specs/20-todo-update-script.md.
status: done
priority: 3
lightweight: false
agent: Human
depends_on: [alex-0010]
pending_reason: ""
created_at: "2026-01-27T12:42:31-03:00"
updated_at: "2026-01-27T12:58:18-03:00"
entrypoints: []
tags: [scripts, todo, python]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-0051 - Especificar script de atualizacao de TODO (todo_update.py)

## Summary
Especificar o comportamento do `todo_update.py` e produzir a spec em `project/specs/20-todo-update-script.md`.

## Context
O `todo_update.py` deve seguir o contrato de scripts v1 e regras de ordenacao/validacao do TODO. A especificacao precisa existir antes da implementacao.

## Objective
Definir requisitos completos e nao ambiguos para o `todo_update.py`, documentados em `project/specs/20-todo-update-script.md`.

## Scope
- Definir escopo, entradas, saidas e erros do `todo_update.py`.
- Documentar regras de atualizacao de campos e validacoes obrigatorias.
- Criar a spec em `project/specs/20-todo-update-script.md`.

## Out of scope
- Implementar o script.
- Alterar outros scripts v1.

## Requirements
- A spec deve ser escrita em ingles e ficar em `project/specs/20-todo-update-script.md`.
- Especificar flags suportadas, comportamento de `--dry-run`, codigos de saida e mensagens.
- Especificar validacoes obrigatorias antes de gravar arquivos.
- Definir tratamento de conflitos (issue inexistente, campos invalidos).
- Incluir regra de registro de log ao executar atualizacoes.

## Acceptance criteria
- [x] A spec existe em `project/specs/20-todo-update-script.md`.
- [x] A spec cobre CLI, entradas, saidas, erros e `--dry-run`.
- [x] A spec cobre regras de validacao conforme `project/specs/04-todo-dev-yaml-issues.md` e `project/specs/05-scripts-and-automation.md`.
- [x] A spec esta alinhada com `project/specs/13-yoda-scripts-v1.md`.

## Dependencies
- alex-0010

## Entry points
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: project/specs/04-todo-dev-yaml-issues.md
  type: doc
- path: project/specs/17-scripts-python-structure.md
  type: doc
- path: project/specs/20-todo-update-script.md
  type: doc

## Implementation notes
- A spec deve seguir o padrao dos demais arquivos em `project/specs/`.

## Tests
Not applicable.

## Risks and edge cases
- Especificacao incompleta pode gerar updates inconsistentes no TODO.
- Regras de validacao divergentes podem quebrar compatibilidade.

## Decisions
- Campos atualizaveis sao definidos por flags dedicadas (sem update generico por key=value em v1).
- `pending_reason` deve ser limpo ao sair de `pending`, a menos que explicitamente informado.

## Result log
Spec de `todo_update.py` criada em `project/specs/20-todo-update-script.md` e regra de log registrada em `project/specs/17-scripts-python-structure.md`.

docs(yoda): especificar todo_update.py

Issue: alex-0051
Path: `yoda/project/issues/alex-0051-especificar-todo-update.md`
