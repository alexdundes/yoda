---
agent: Human
created_at: '2026-01-27T13:32:14-03:00'
depends_on:
- yoda-0036
description: Especificar o comportamento do `issue_add.py` e produzir a spec em `project/specs/18-issue-add-script.md`.
entrypoints: []
id: yoda-0037
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 3
schema_version: '1.0'
slug: especificar-script-issue-add
status: done
tags: []
title: Especificar script de inclusao de issue (issue_add.py)
updated_at: '2026-01-27T13:32:40-03:00'
---

# yoda-0037 - Especificar script de inclusao de issue (issue_add.py)

## Summary
Especificar o comportamento do `issue_add.py` e produzir a spec em `project/specs/18-issue-add-script.md`.

## Context
O `issue_add.py` e o primeiro script v1 e precisa de uma especificacao formal antes da implementacao. A issue anterior combinava especificacao e implementacao; agora elas foram separadas.

## Objective
Definir requisitos completos e nao ambiguos para o `issue_add.py`, documentados em `project/specs/18-issue-add-script.md`.

## Scope
- Definir escopo, entradas, saidas e erros do `issue_add.py`.
- Documentar regras de id/slug, selecao de template e tratamento de conflitos.
- Criar a spec em `project/specs/18-issue-add-script.md`.

## Out of scope
- Implementar o script.
- Alterar outros scripts v1.

## Requirements
- A spec deve ser escrita em ingles e ficar em `project/specs/18-issue-add-script.md`.
- Especificar flags suportadas, comportamento de `--dry-run`, codigos de saida e mensagens.
- Especificar atualizacao do TODO e geracao do arquivo de issue via template.
- Definir validacoes obrigatorias antes de gravar arquivos.
- Definir tratamento de conflitos (id/arquivo existente).
- Definir comportamento de log de criacao da issue.
- Definir comportamento quando `yoda/todos/TODO.<dev>.yaml` nao existe (criar com defaults).

## Acceptance criteria
- [x] A spec existe em `project/specs/18-issue-add-script.md`.
- [x] A spec cobre CLI, entradas, saidas, erros e `--dry-run`.
- [x] A spec cobre regras de id/slug, template e conflitos de arquivo.
- [x] A spec esta alinhada com `project/specs/13-yoda-scripts-v1.md` e `project/specs/05-scripts-and-automation.md`.

## Dependencies
- yoda-0036

## Entry points
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: project/specs/14-issue-templates-usage.md
  type: doc
- path: project/specs/15-scripts-python-structure.md
  type: doc
- path: yoda/templates/issue.md
  type: doc
- path: project/specs/18-issue-add-script.md
  type: doc

## Implementation notes
- A spec deve seguir o padrao dos demais arquivos em `project/specs/`.
- Decisao: selecao de template via flag `--lightweight` (sem flag de template customizado).
- Decisao: permitir `--slug` opcional; caso ausente, gerar a partir do title usando regras de slug.

## Tests
Not applicable.

## Risks and edge cases
- Especificacao incompleta pode gerar implementacao divergente.
- Regras de slug/ids inconsistentes com specs existentes.

## Decisions
- Template: `--lightweight` seleciona `issue-lightweight-process.md`; sem suporte a template customizado em v1.
- Slug: `--slug` opcional; se ausente, gerar a partir do title seguindo regras de slug.

## Result log
Spec de `issue_add.py` criada em `project/specs/18-issue-add-script.md`, incluindo comportamento de criacao do TODO quando ausente e timezone local.

docs(yoda): especificar issue_add.py

Issue: yoda-0037
Path: `yoda/project/issues/yoda-0037-especificar-script-issue-add.md`