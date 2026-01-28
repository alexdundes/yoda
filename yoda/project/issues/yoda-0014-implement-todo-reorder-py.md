---
agent: Human
created_at: '2026-01-28T14:51:24-03:00'
depends_on: []
description: 'Implement todo_reorder.py per spec: reorder modes, validation, output,
  and tests.'
entrypoints: []
id: yoda-0014
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: implement-todo-reorder-py
status: doing
tags: []
title: Implement todo_reorder.py
updated_at: '2026-01-28T15:14:42-03:00'
---

# yoda-0014 - Implement todo_reorder.py
<!-- AGENT: Replace yoda-0014 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Implement todo_reorder.py with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Implementar `todo_reorder.py` conforme a spec: reordenação de issues no `TODO.<dev>.yaml`, validação de inputs, saída `md`/`json` e testes.

## Context
Ainda não há comando para reordenar o TODO, o que dificulta ajustar a ordem de execução determinística sem editar YAML manualmente.

## Objective
Entregar o script `todo_reorder.py` com comportamento determinístico e testes, alinhado à spec `yoda-0013`.

## Scope
- Implementar CLI e modos de reordenação definidos.
- Aplicar validações e atualizar timestamps.
- Saída `md` e `json` conforme contrato global.
- Adicionar testes unitários.

## Out of scope
- Alterações de schema não previstas na spec.
- Implementar comandos além de `todo_reorder.py`.

## Requirements
- Deve reordenar issues no TODO com base no modo escolhido.
- Deve validar ID e posição e falhar com exit code 2 em erro.
- Deve atualizar `updated_at` do TODO root e do item movido.
- Deve produzir saída `md` e `json` conforme contrato global.

## Acceptance criteria
- [ ] `todo_reorder.py` implementado conforme a spec `yoda-0013`.
- [ ] Reordenação funciona para mover acima/abaixo e posição absoluta.
- [ ] Inputs inválidos retornam exit code 2 e mensagem clara.
- [ ] Timestamps atualizados corretamente.
- [ ] Testes cobrindo casos principais passam.

## Dependencies
Depends on: yoda-0013.

## Entry points
- path: yoda/scripts
  type: code
- path: yoda/scripts/lib
  type: code
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/15-scripts-python-structure.md
  type: doc
- path: yoda/project/issues/yoda-0013-specify-todo-reorder-py.md
  type: doc

## Implementation notes
Reusar helpers em `yoda/scripts/lib` quando possível. A reordenação deve ser estável para itens não movidos.

## Tests
Adicionar testes em `yoda/scripts/tests` cobrindo os modos de reordenação e validações.

## Risks and edge cases
- ID inexistente no TODO.
- Posição fora do intervalo.
- Conflito de flags de modo.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->