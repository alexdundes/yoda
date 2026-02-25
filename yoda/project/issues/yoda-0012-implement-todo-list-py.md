---
agent: Human
created_at: '2026-01-28T12:25:58-03:00'
depends_on: []
description: 'Implement todo_list.py per spec: filters, ordering, md/json output,
  and optional text/regex search in selected issue markdown files.'
entrypoints: []
id: yoda-0012
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: implement-todo-list-py
status: done
tags: []
title: Implement todo_list.py
updated_at: '2026-01-28T14:42:11-03:00'
---

# yoda-0012 - Implement todo_list.py

## Summary
Implementar `todo_list.py` conforme a especificação: filtros, ordenação padrão e alternativa, saída md/json e busca textual/regex nas issues Markdown selecionadas. Incluir testes cobrindo filtros, ordenação e busca.

## Context
O comando `todo_list.py` não existe e é necessário para listar e filtrar issues de forma legível e automatizável. A implementação precisa seguir a spec para evitar divergências.

## Objective
Entregar o script `todo_list.py` com comportamento determinístico e testes, alinhado à spec `yoda-0011`.

## Scope
- Implementar CLI, filtros e ordenações definidas na spec.
- Implementar saída `md` (tabela) e `json`.
- Implementar busca textual/regex nas issues Markdown selecionadas.
- Adicionar testes unitários para os principais fluxos.

## Out of scope
- Alterar schemas do TODO/issue/log fora do necessário.
- Criar comandos adicionais além de `todo_list.py`.

## Requirements
- Deve ler `TODO.<dev>.yaml` e aplicar filtros conforme CLI.
- Padrão: listar apenas issues não concluídas e ordenadas pela regra de execução definida na spec.
- Permitir trocar o critério de ordenação via parâmetro.
- Saída em `md` ou `json` conforme `--format/--json`.
- Se busca textual for informada, aplicar filtros antes e fazer busca nas issues Markdown selecionadas.
- Suportar regex na busca textual.
- Saída de busca textual deve ser texto fluído em Markdown com as linhas encontradas.
- Saída padrão em Markdown deve ser tabela com colunas essenciais e largura legível.
- `--tags` deve exigir que a issue tenha **todas** as tags fornecidas (AND).

## Acceptance criteria
- [x] `todo_list.py` implementado conforme a spec `yoda-0011`.
- [x] Saída `md` padrão é tabela legível com colunas essenciais.
- [x] Saída `json` contém os campos mínimos definidos.
- [x] Busca textual/regex funciona e retorna linhas completas encontradas.
- [x] Ordenação padrão respeita prioridade, ordem YAML e dependências não concluídas.
- [x] Filtro de tags usa AND (todas as tags).
- [ ] Testes cobrindo filtros, ordenação e busca passam.

## Dependencies
Depends on: yoda-0011.

## Entry points
- path: yoda/scripts
  type: code
- path: yoda/scripts/lib
  type: code
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/20-todo-update-script.md
  type: doc
- path: project/specs/21-todo-next-script.md
  type: doc
- path: yoda/project/issues/yoda-0011-specify-todo-list-py.md
  type: doc

## Implementation notes
Reusar helpers em `yoda/scripts/lib` quando possível (CLI, validação, output). Implementar ordenação com dependências de forma estável e determinística. Para busca textual, ler arquivos apenas da seleção filtrada.

## Tests
Adicionados testes em `yoda/scripts/tests/test_todo_list.py` para: filtros padrão, ordenação por prioridade/YAML, ordenação alternativa, busca textual simples e regex.

## Risks and edge cases
- Regex inválida deve retornar erro de validação.
- Issue Markdown ausente durante busca textual.
- Dependências múltiplas e ciclos devem ser tratadas com fallback determinístico.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
Implemented `todo_list.py` with filters, ordering, md/json output, and grep search, plus supporting helpers and tests.

feat(scripts): add todo_list command

Issue: `yoda-0012`
Path: `yoda/project/issues/yoda-0012-implement-todo-list-py.md`