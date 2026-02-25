---
created_at: '2026-01-28T12:25:53-03:00'
depends_on: []
description: Define CLI, filters, ordering, output formats, and text search behavior
  for todo_list.py.
id: yoda-0011
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.01'
slug: specify-todo-list-py
status: done
title: Specify todo_list.py
updated_at: '2026-02-25T20:02:28-03:00'
---

# yoda-0011 - Specify todo_list.py

## Summary
Definir a especificação do comando `todo_list.py`, incluindo CLI, filtros, ordenação padrão e opções de ordenação alternativa, formatos de saída (md/json) e busca textual/regex nas issues Markdown. A spec deve orientar implementação consistente e testável.

## Context
O comando `todo_list.py` ainda não existe e precisa de uma definição clara para evitar implementações divergentes. A listagem deve atender tanto humanos quanto agentes, com saída legível e filtros/ordenações determinísticos.

## Objective
Especificar completamente o comportamento de `todo_list.py` para permitir implementação direta, incluindo regras de ordenação, filtros, saída e busca textual.

## Scope
- Definir CLI e parâmetros (filtros, ordenação, formato).
- Definir comportamento padrão de seleção e ordenação.
- Definir comportamento da busca textual/regex em issues Markdown.
- Definir formatos de saída (md e json) e estrutura mínima.

## Out of scope
- Implementação do script.
- Alterações de schema fora do necessário para a especificação.

## Requirements
- Deve listar issues do `TODO.<dev>.yaml` com filtros por status e outros critérios definidos na spec.
- Padrão: listar apenas issues não concluídas (status != done), em ordem de execução.
- Ordem padrão: prioridade desc, ordem YAML como desempate, e dependências não concluídas devem aparecer antes das dependentes.
- Deve aceitar opção para trocar a ordenação padrão (definir critérios alternativos na spec).
- Saída em `md` ou `json`, seguindo o contrato global.
- Se parâmetro de busca textual for fornecido, aplicar filtros primeiro, depois fazer busca estilo grep nas issues Markdown selecionadas.
- Busca textual deve aceitar regex.
- Quando houver busca textual, saída muda para texto fluído em Markdown, incluindo linhas inteiras onde o texto foi encontrado.
- Quando não houver busca textual, saída em Markdown deve ser tabela com largura amigável para humanos e agents (campos essenciais; respeitar largura de tela).
- Filtros suportados: status, tags, agent, faixa de prioridade, depends_on, lightweight, faixa de data de criação e faixa de data de atualização.
- Ordenação alternativa por data de criação e data de atualização (crescente e decrescente).
- JSON deve retornar, no mínimo, `id`, `slug`, `status`, `priority`, `title` para cada issue selecionada.
- Busca textual é case-insensitive por padrão, com flag para modo case-sensitive.
- Regex inválida deve retornar erro de validação.
- Se o arquivo Markdown de uma issue selecionada não existir durante busca textual, o script deve ignorar silenciosamente.

## Acceptance criteria
- [x] Spec define CLI, filtros e valores padrão.
- [x] Spec define regras de ordenação padrão e alternativas.
- [x] Spec define saída `md` (tabela) e `json` (estrutura mínima).
- [x] Spec define comportamento de busca textual/regex e formato de saída em busca.
- [x] Spec define ordenação com dependências (dependência não concluída aparece antes).
- [x] Spec define filtros por status, tags, agent, faixa de prioridade, depends_on, lightweight, e faixas de datas.
- [x] Spec define ordenação alternativa por data de criação/atualização (asc/desc).
- [x] Spec define JSON mínimo (`id`, `slug`, `status`, `priority`, `title`).
- [x] Spec define busca textual case-insensitive por padrão e flag case-sensitive.
- [x] Spec define erro em regex inválida e silêncio para arquivo Markdown ausente na busca.
- [x] Spec define tratamento visual de pending na saída Markdown (bloco antes da tabela; pending fora da tabela).
- [x] Spec define JSON com todos os campos do item de issue.

## Dependencies
None.

## Entry points
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: project/specs/15-scripts-python-structure.md
  type: doc
- path: project/specs/04-todo-dev-yaml-issues.md
  type: doc

## Implementation notes
Definir a regra de ordenação com dependências de forma determinística (ex.: ordenação estável que move itens bloqueados para depois da dependência não concluída). Definir colunas da tabela MD com largura ajustada para leitura humana e por agent. Definir formato do texto fluído na busca textual (issue + linha encontrada).

## Tests
Not applicable (spec-only).

## Risks and edge cases
- Dependências múltiplas podem complicar a ordenação estável.
- Regex inválida deve gerar erro de validação.
- Issues sem Markdown (arquivo faltando) quando buscar texto.
- Datas com timezone inválido devem falhar em validação.

## Result log
Defined the `todo_list.py` specification covering CLI, filters, ordering, output formats, and text/regex search behavior.
Updated spec to add pending alert block behavior in Markdown output and full issue payloads in JSON output.

docs(specs): add todo_list command specification

Issue: `yoda-0011`
Path: `yoda/project/issues/yoda-0011-specify-todo-list-py.md`