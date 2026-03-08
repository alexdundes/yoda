---
schema_version: '2.00'
status: done
title: Specify todo_reorder.py
description: Define CLI, ordering behaviors, and output formats for todo_reorder.py.
priority: 5
created_at: '2026-01-28T14:51:19-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0013 - Specify todo_reorder.py

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


## Entry points
- `project/specs/13-yoda-scripts-v1.md`
- `project/specs/05-scripts-and-automation.md`
- `project/specs/15-scripts-python-structure.md`

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
Defined `todo_reorder.py` specification including default ordering (pending/active/done), prioritization behavior, CLI, validation, and outputs.
Updated prioritization rules: only `to-do`, and reject when A depends on B.

docs(specs): add todo_reorder command specification

Issue: `yoda-0013`
Path: `yoda/project/issues/yoda-0013-specify-todo-reorder-py.md`

## Flow log
2026-01-28T14:51:19-03:00 | [yoda-0013] issue_add created | title: Specify todo_reorder.py | description: Define CLI, ordering behaviors, and output formats for todo_reorder.py. | slug: specify-todo-reorder-py
2026-01-28T14:54:54-03:00 | [yoda-0013] todo_update | status: to-do -> doing
2026-01-28T15:10:29-03:00 | [yoda-0013] implement: added todo_reorder spec and updated indices
2026-01-28T15:10:34-03:00 | [yoda-0013] todo_update | status: doing -> done
2026-01-28T15:13:46-03:00 | [yoda-0013] todo_update | status: done -> doing
2026-01-28T15:14:05-03:00 | [yoda-0013] document: added prioritization validation (to-do only, reject dependency)
2026-01-28T15:14:10-03:00 | [yoda-0013] todo_update | status: doing -> done
2026-01-28T15:26:03-03:00 | [yoda-0013] document: aligned reorder spec with implementation (updated_at only on change; no forced A before B)