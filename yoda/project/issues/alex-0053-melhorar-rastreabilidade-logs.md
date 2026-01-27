---
schema_version: "1.0"
id: alex-0053
title: Melhorar rastreabilidade dos logs dos scripts
slug: melhorar-rastreabilidade-logs
description: Ajustar specs e scripts para logs com detalhamento de mudancas e dados iniciais.
status: done
priority: 3
lightweight: false
agent: Human
depends_on: [alex-0052]
pending_reason: ""
created_at: "2026-01-27T13:20:00-03:00"
updated_at: "2026-01-27T13:23:23-03:00"
entrypoints: []
tags: [scripts, logs]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-0053 - Melhorar rastreabilidade dos logs dos scripts

## Summary
Atualizar specs e scripts para logs detalhados, com campos alterados e dados iniciais informados.

## Context
Os logs atuais sao genericos e dificultam rastreabilidade. Precisamos registrar alteracoes com detalhe e linha por mudanca.

## Objective
Garantir que logs de scripts v1 descrevam claramente o que mudou e quais dados foram usados na criacao.

## Scope
- Atualizar specs relevantes com requisitos de rastreabilidade em logs.
- Ajustar scripts `issue_add.py` e `todo_update.py` para registrar logs detalhados.
- Retestar com o fluxo de bootstrap usando `TODO.alex.md` como base.

## Out of scope
- Refatorar outros scripts v1.
- Alterar schemas alem do necessario para logs.

## Requirements
- Logs devem registrar mudancas com `campo: valor_antigo -> valor_novo`, uma mudanca por linha.
- Logs de criacao devem incluir dados iniciais informados (omitir nao informados).
- Mensagens devem mencionar o issue id.

## Acceptance criteria
- [x] Specs atualizadas com regra de rastreabilidade e formato de log.
- [x] `issue_add.py` registra log inicial detalhado.
- [x] `todo_update.py` registra log com diffs por campo.
- [x] Testes refeitos no fluxo `yoda` com logs detalhados.

## Dependencies
- alex-0052

## Entry points
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: project/specs/17-scripts-python-structure.md
  type: doc
- path: project/specs/18-issue-add-script.md
  type: doc
- path: project/specs/19-log-add-script.md
  type: doc
- path: project/specs/20-todo-update-script.md
  type: doc
- path: yoda/scripts/issue_add.py
  type: code
- path: yoda/scripts/todo_update.py
  type: code

## Implementation notes
- Padronizar mensagens com uma mudanca por linha.

## Tests
Not applicable.

## Risks and edge cases
- Logs verbosos podem aumentar tamanho, mas sao necessarios para auditabilidade.

## Result log
Atualizadas specs de logs para rastreabilidade, ajustados `issue_add.py` e `todo_update.py` com mensagens detalhadas e testes refeitos no fluxo yoda.

feat(yoda): detalhar logs de scripts

Issue: alex-0053
Path: `yoda/project/issues/alex-0053-melhorar-rastreabilidade-logs.md`
