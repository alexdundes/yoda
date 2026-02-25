---
created_at: '2026-01-28T14:51:19-03:00'
depends_on: []
description: Define CLI, ordering behaviors, and output formats for todo_reorder.py.
id: yoda-0013
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.01'
slug: specify-todo-reorder-py
status: done
title: Specify todo_reorder.py
updated_at: '2026-02-25T20:02:28-03:00'
---

# yoda-0013 - Specify todo_reorder.py
<!-- AGENT: Replace yoda-0013 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Specify todo_reorder.py with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Definir a especificação do comando `todo_reorder.py` para reordenar issues no `TODO.<dev>.yaml`. A spec deve cobrir CLI, modos de ordenação, validações e formatos de saída para permitir implementação consistente e testável.

## Context
O YODA usa a ordem no YAML como desempate determinístico. Falta um comando dedicado para reordenar a lista sem alterar outros metadados. Uma spec clara evita divergências.

## Objective
Especificar completamente o comportamento de `todo_reorder.py` (inputs, regras, validação, outputs e erros).

## Scope
- Definir CLI e parâmetros de reordenação.
- Definir modos (mover para cima/baixo, posição explícita).
- Definir validações e tratamento de erro.
- Definir saída `md`/`json` conforme contrato global.

## Out of scope
- Implementação do script.
- Alterações de schema fora do necessário para a spec.

## Requirements
- Deve reordenar issues em `yoda/todos/TODO.<dev>.yaml` sem alterar outros campos.
- Deve aceitar mover uma issue para cima/baixo e definir posição absoluta.
- Deve atualizar `updated_at` do TODO root e do item movido.
- Deve validar inputs e falhar com exit code 2 em erros de validação.
- Saída em `md` ou `json` conforme contrato global.
- Rodando sem parâmetros, deve reordenar o YAML conforme a mesma lógica de `todo_list`, incluindo `done` no fim.
- `pending` deve aparecer antes de todos, ordenado por `updated_at` asc.
- `done` deve aparecer no fim, ordenado por `updated_at` desc.
- Deve suportar comando de priorização: `--prefer <id-a> --over <id-b>`.
- Ao priorizar: se a prioridade de A for menor que a de B, A deve assumir a prioridade de B e então ficar antes de B.
- O comando de priorização deve executar e depois fazer a reordenação geral (não é exclusivo).
- Ao priorizar, A e B devem estar com status `to-do`.
- Ao priorizar, se A depender de B, deve retornar erro de validação.

## Acceptance criteria
- [x] Spec define CLI, parâmetros e exemplos de reordenação.
- [x] Spec define validações (ids, posições, limites).
- [x] Spec define atualização de timestamps.
- [x] Spec define outputs `md`/`json` e exit codes.
- [x] Spec define ordenação default com `pending` no topo, `done` no fim e ativo no meio.
- [x] Spec define comando `--prefer/--over` e regra de ajuste de prioridade.
- [x] Spec define validações extras para priorização (status `to-do` e dependência).

## Dependencies
None.

## Entry points
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: project/specs/15-scripts-python-structure.md
  type: doc

## Implementation notes
A reordenação deve ser determinística e preservar a ordem relativa dos demais itens. Reaproveitar lógica de ordenação de `todo_list` quando possível. Definir como lidar com conflito de flags e IDs inexistentes.

## Tests
Not applicable (spec-only).

## Risks and edge cases
- Ordem inválida se o ID não existir.
- Índices fora da faixa.
- Conflito quando múltiplos modos de reordenação são fornecidos.
- `--prefer` ou `--over` ausentes/inválidos.
- `--prefer` igual a `--over`.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
Defined `todo_reorder.py` specification including default ordering (pending/active/done), prioritization behavior, CLI, validation, and outputs.
Updated prioritization rules: only `to-do`, and reject when A depends on B.

docs(specs): add todo_reorder command specification

Issue: `yoda-0013`
Path: `yoda/project/issues/yoda-0013-specify-todo-reorder-py.md`