---
schema_version: "1.0"
id: alex-0049
title: Especificar script de log (log_add.py)
slug: especificar-log-add
description: Especificar o comportamento do log_add.py e criar a spec em project/specs/19-log-add-script.md.
status: done
priority: 3
lightweight: false
agent: Human
depends_on: [alex-0014]
pending_reason: ""
created_at: "2026-01-27T08:50:15-03:00"
updated_at: "2026-01-27T08:54:08-03:00"
entrypoints: []
tags: [scripts, log, python]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-0049 - Especificar script de log (log_add.py)

## Summary
Especificar o comportamento do `log_add.py` e produzir a spec em `project/specs/19-log-add-script.md`.

## Context
O `log_add.py` precisa seguir o contrato de logs definido em `project/specs/05-scripts-and-automation.md` e deve ser especificado antes da implementacao.

## Objective
Definir requisitos completos e nao ambiguos para o `log_add.py`, documentados em `project/specs/19-log-add-script.md`.

## Scope
- Definir escopo, entradas, saidas e erros do `log_add.py`.
- Documentar regras de selecao de issue/log e append de entradas.
- Criar a spec em `project/specs/19-log-add-script.md`.

## Out of scope
- Implementar o script.
- Alterar outros scripts v1.

## Requirements
- A spec deve ser escrita em ingles e ficar em `project/specs/19-log-add-script.md`.
- Especificar flags suportadas, comportamento de `--dry-run`, codigos de saida e mensagens.
- Especificar validacoes obrigatorias antes de gravar arquivos.
- Definir tratamento de conflitos (issue inexistente, log ausente).
- Definir comportamento para criacao do log quando ausente.

## Acceptance criteria
- [x] A spec existe em `project/specs/19-log-add-script.md`.
- [x] A spec cobre CLI, entradas, saidas, erros e `--dry-run`.
- [x] A spec cobre regras de log e validacao conforme `project/specs/05-scripts-and-automation.md`.
- [x] A spec esta alinhada com `project/specs/13-yoda-scripts-v1.md`.

## Dependencies
- alex-0014

## Entry points
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: project/specs/17-scripts-python-structure.md
  type: doc
- path: project/specs/19-log-add-script.md
  type: doc

## Implementation notes
- A spec deve seguir o padrao dos demais arquivos em `project/specs/`.

## Tests
Not applicable.

## Risks and edge cases
- Especificacao incompleta pode gerar logs inconsistentes.
- Falhas em timestamp ou schema podem quebrar validacao.

## Decisions
- Resolver slug a partir do TODO pelo issue id.
- Se o log nao existir, criar com schema valido antes de append.

## Result log
Spec de `log_add.py` criada em `project/specs/19-log-add-script.md`.

docs(yoda): especificar log_add.py

Issue: alex-0049
Path: `yoda/project/issues/alex-0049-especificar-log-add.md`
