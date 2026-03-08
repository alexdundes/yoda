---
schema_version: '2.00'
status: done
title: Implement todo_list.py
description: 'Implement todo_list.py per spec: filters, ordering, md/json output,
  and optional text/regex search in selected issue markdown files.'
priority: 5
created_at: '2026-01-28T12:25:58-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
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


## Entry points
- `yoda/scripts`
- `yoda/scripts/lib`
- `project/specs/13-yoda-scripts-v1.md`
- `project/specs/20-todo-update-script.md`
- `project/specs/21-todo-next-script.md`
- `yoda/project/issues/yoda-0011-specify-todo-list-py.md`

## Implementation notes
Reusar helpers em `yoda/scripts/lib` quando possível (CLI, validação, output). Implementar ordenação com dependências de forma estável e determinística. Para busca textual, ler arquivos apenas da seleção filtrada.

## Tests
Adicionados testes em `yoda/scripts/tests/test_todo_list.py` para: filtros padrão, ordenação por prioridade/YAML, ordenação alternativa, busca textual simples e regex.

## Risks and edge cases
- Regex inválida deve retornar erro de validação.
- Issue Markdown ausente durante busca textual.
- Dependências múltiplas e ciclos devem ser tratadas com fallback determinístico.

## Result log
Implemented `todo_list.py` with filters, ordering, md/json output, and grep search, plus supporting helpers and tests.

feat(scripts): add todo_list command

Issue: `yoda-0012`
Path: `yoda/project/issues/yoda-0012-implement-todo-list-py.md`

## Flow log
- 2026-01-28T12:25:58-03:00 issue_add created | title: Implement todo_list.py | description: Implement todo_list.py per spec: filters, ordering, md/json output, and optional text/regex search in selected issue markdown files. | slug: implement-todo-list-py
- 2026-01-28T14:33:16-03:00 todo_update | status: to-do -> doing
- 2026-01-28T14:37:35-03:00 document: clarified tags filter uses AND and pending block only for selected issues
- 2026-01-28T14:42:01-03:00 implement: added todo_list command and tests
- 2026-01-28T14:42:06-03:00 evaluate: tests pass and result log updated
- 2026-01-28T14:42:11-03:00 todo_update | status: doing -> done
- 2026-01-28T14:47:11-03:00 refactor: reused lib helpers in todo_list
