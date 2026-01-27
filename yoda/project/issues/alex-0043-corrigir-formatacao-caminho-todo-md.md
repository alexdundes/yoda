---
schema_version: "1.0"
id: alex-0043
title: Corrigir formatacao de caminho TODO.<slug>.md
slug: corrigir-formatacao-caminho-todo-md
description: Ajustar yoda/yoda.md para manter`yoda/todos/TODO.<slug>.md`sem backticks no meio.
status: done
priority: 4
lightweight: false
agent: Codex
depends_on: []
pending_reason: ""
created_at: "2026-01-26T21:06:43-03:00"
updated_at: "2026-01-26T21:07:11-03:00"
entrypoints:
  - path: yoda/yoda.md
    type: doc
tags: []
origin:
  system: ""
  external_id: ""
  requester: ""
---

# alex-0043 - Corrigir formatacao de caminho TODO.<slug>.md

## Summary
Remover a formatacao quebrada de backticks no meio do caminho TODO.<slug>.md em yoda/yoda.md, garantindo leitura e copia coerentes.

## Context
Atualmente ha trechos com `TODO.`<slug>`.md`, o que pode confundir leitura e copy/paste.

## Objective
Padronizar o caminho completo como `yoda/todos/TODO.<slug>.md` nas ocorrencias relevantes.

## Scope
- Ajustar as ocorrencias de TODO.<slug> em yoda/yoda.md.

## Out of scope
- Alterar outras regras do bootstrap.

## Requirements
- Substituir `TODO.`<slug>`.md` por `yoda/todos/TODO.<slug>.md`.
- Manter o restante do texto inalterado.

## Acceptance criteria
- [ ] Todas as ocorrencias usam o caminho completo e continuo `yoda/todos/TODO.<slug>.md`.

## Dependencies
None.

## Entry points
- path: yoda/yoda.md
  type: doc

## Implementation notes
- Ajustar apenas a formatacao do path no texto.

## Tests
Not applicable.

## Risks and edge cases
- Nenhum; mudanca textual.

## Result log
Formatacao do caminho atualizada para`yoda/todos/TODO.<slug>.md`em yoda/yoda.md, removendo backticks no meio.

docs: corrigir caminho TODO.<slug>.md no bootstrap

Issue: `alex-0043`
Path: `yoda/project/issues/alex-0043-corrigir-formatacao-caminho-todo-md.md`
