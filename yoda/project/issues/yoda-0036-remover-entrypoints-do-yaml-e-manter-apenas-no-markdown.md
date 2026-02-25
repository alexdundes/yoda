---
agent: Human
created_at: '2026-02-25T15:36:44-03:00'
depends_on:
- yoda-0038
description: 'Hoje entrypoints aparecem no front matter YAML e tambem no corpo do
  markdown da issue. Simplificar para manter entrypoints apenas no markdown e remover
  esse campo do YAML de issue/TODO/log quando aplicavel. Regra transversal: atualizar
  primeiro project/specs/ e depois yoda/. Como envolve layout YAML, aplicar politica
  de versao de schema e tratamento de compatibilidade conforme update.py quando aplicavel.'
entrypoints:
- path: project/specs/
  type: doc
- path: yoda/templates/issue.md
  type: doc
- path: yoda/scripts/
  type: code
id: yoda-0036
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 3
schema_version: '1.0'
slug: remover-entrypoints-do-yaml-e-manter-apenas-no-markdown
status: to-do
tags: []
title: Remover entrypoints do YAML e manter apenas no markdown
updated_at: '2026-02-25T15:36:56-03:00'
---

# yoda-0036 - Remover entrypoints do YAML e manter apenas no markdown
<!-- AGENT: Replace yoda-0036 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Remover entrypoints do YAML e manter apenas no markdown with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Eliminar a duplicidade de `entrypoints` entre YAML e markdown de issue. O conceito deve permanecer apenas no corpo markdown da issue para reduzir redundancia e divergencia.

## Context
Hoje os entrypoints aparecem no front matter e tambem em secao dedicada no markdown. Essa duplicidade aumenta manutencao e risco de inconsistencias.

## Objective
Manter `entrypoints` somente na secao markdown da issue e remover do YAML.

## Scope
- Atualizar specs para definir fonte unica de verdade para entrypoints.
- Remover `entrypoints` do schema YAML e dos scripts.
- Ajustar templates para manter somente secao markdown.
- Tratar migracao de dados existentes.

## Out of scope
- Redesenhar toda estrutura de issue alem do campo `entrypoints`.
- Adicionar novos metadados de navegacao.

## Requirements
- Ordem obrigatoria: `project/specs/` antes de `yoda/`.
- Nenhum script deve requerer `entrypoints` em YAML ao final.
- Por alterar layout YAML, aplicar politica de versionamento definida em `yoda-0038`.
- Se houver breaking no upgrade, implementar tratamento em `update.py`.

## Acceptance criteria
- [ ] Specs definem entrypoints apenas no markdown da issue.
- [ ] YAML de TODO/issue/log nao inclui mais `entrypoints`.
- [ ] Scripts de criacao/atualizacao continuam funcionais sem esse campo no YAML.
- [ ] Migracao dos dados existentes e validada.

## Dependencies
`yoda-0038` (politica de versionamento de layout YAML).

## Entry points
- path: project/specs/
  type: doc
- path: yoda/templates/issue.md
  type: doc
- path: yoda/scripts/
  type: code

## Implementation notes
Garantir que relatorios/listagens nao percam contexto apos mover a fonte para markdown.

## Tests
Adicionar testes de leitura/escrita de issue sem `entrypoints` em YAML, preservando comportamento esperado.

## Risks and edge cases
- Ferramentas internas que assumem `entrypoints` no YAML podem quebrar silenciosamente.
- Dados historicos com campo legado podem falhar sem migracao.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
