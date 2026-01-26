---
schema_version: "1.0"
id: alex-0037
title: Criar script de inclusao de issue (issue_add.py)
slug: criar-script-issue-add
description: Especificar e implementar o script de inclusao de issues usando a estrutura definida.
status: to-do
priority: 6
lightweight: false
agent: Human
depends_on: [alex-0036]
pending_reason: ""
created_at: "2026-01-26T13:50:33-03:00"
updated_at: "2026-01-26T13:50:33-03:00"
entrypoints: []
tags: [scripts, issue, python]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-0037 - Criar script de inclusao de issue (issue_add.py)

## Summary
Especificar e implementar o script `issue_add.py` para criar entradas no TODO e gerar o Markdown da issue a partir do template.

## Context
O `issue_add.py` e o primeiro script v1 e precisa seguir a estrutura definida em `alex-0036`. Ele deve criar o id canonico, atualizar o TODO e gerar o arquivo de issue corretamente.

## Objective
Entregar o script `yoda/scripts/issue_add.py` conforme specs v1, com validacao embutida e saidas padronizadas.

## Scope
- Especificar detalhes de comportamento do `issue_add.py`.
- Implementar o script em Python.
- Garantir compatibilidade com `yoda/todos/TODO.<dev>.yaml` e templates.

## Out of scope
- Implementar outros scripts v1.
- Criar um CLI global.

## Requirements
- Gerar o proximo id canonico `<dev>-<NNNN>`.
- Atualizar `yoda/todos/TODO.<dev>.yaml` com o novo item.
- Gerar `yoda/project/issues/<id>-<slug>.md` a partir do template.
- Preencher campos basicos no template (id, title, summary, metadata).
- Validacao obrigatoria antes de gravar.
- Respeitar `timezone` no TODO.

## Acceptance criteria
- [ ] `issue_add.py` cria entrada no TODO e arquivo de issue com naming correto.
- [ ] O script respeita `--dev`, `--dry-run`, `--format` e exit codes.
- [ ] Validacao embutida bloqueia escrita em caso de erro.
- [ ] O template e preenchido com metadata basica conforme specs.

## Dependencies
- alex-0036

## Entry points
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: yoda/templates/issue.md
  type: doc

## Implementation notes
- Registrar decisoes em aberto dentro da issue antes de implementar.

## Tests
Not applicable (definir na issue se necessario).

## Risks and edge cases
- Erros em id/slug podem quebrar naming de arquivos e logs.
- Falhas em templates podem gerar front matter invalida.

## Open decisions
- Como resolver slug a partir do title (normalizacao e stopwords?).
- Como tratar conflito de id/arquivo existente.
- Como selecionar template (padrao vs lightweight).
- Campos obrigatorios minimos e defaults no TODO (agent, tags, priority, lightweight, timezone).
- Estrategia para atualizar `updated_at` e ordenar items.

## Result log
