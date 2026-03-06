---
schema_version: '2.00'
id: yoda-0036
status: done
depends_on:
- yoda-0038
title: Remover entrypoints do YAML e manter apenas no markdown
description: 'Hoje entrypoints aparecem no front matter YAML e tambem no corpo do
  markdown da issue. Simplificar para manter entrypoints apenas no markdown e remover
  esse campo do YAML de issue/TODO/log quando aplicavel. Regra transversal: atualizar
  primeiro project/specs/ e depois yoda/. Como envolve layout YAML, aplicar politica
  de versao de schema e tratamento de compatibilidade conforme update.py quando aplicavel.'
priority: 3
created_at: '2026-02-25T15:36:44-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0036 - Remover entrypoints do YAML e manter apenas no markdown

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
- Classificacao definida: **subtle**.
- Rollout definido em conjunto com `yoda-0035` e `yoda-0037`: aplicar **um unico incremento menor** de `schema_version` para o pacote `0.1.3`.

## Acceptance criteria
- [x] Specs definem entrypoints apenas no markdown da issue.
- [x] YAML de TODO/issue/log nao inclui mais `entrypoints`.
- [x] Scripts de criacao/atualizacao continuam funcionais sem esse campo no YAML.
- [x] Migracao dos dados existentes e validada.

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
Decisao de planejamento: tratar esta mudanca como `subtle` e coordenar com `yoda-0035`/`yoda-0037` para um unico bump menor de schema na release `0.1.3`.
Garantir que relatorios/listagens nao percam contexto apos mover a fonte para markdown.

## Tests
Adicionar testes de leitura/escrita de issue sem `entrypoints` em YAML, preservando comportamento esperado.

## Risks and edge cases
- Ferramentas internas que assumem `entrypoints` no YAML podem quebrar silenciosamente.
- Dados historicos com campo legado podem falhar sem migracao.

## Result log
`entrypoints` foi removido do YAML (TODO/front matter/log contract) e mantido somente na secao markdown da issue. Scripts foram ajustados para nao ler/escrever `entrypoints` no metadata (`issue_add.py` sem `--entrypoint` e sem persistencia do campo). Specs e manual de scripts foram alinhados; dados existentes em `TODO` e front matter das issues foram migrados para remover o campo legado.

test: `python3 -m pytest yoda/scripts/tests` => 33 passed.

refactor(yoda): remover entrypoints do YAML e manter apenas no markdown
Issue: `yoda-0036`
Path: `yoda/project/issues/yoda-0036-remover-entrypoints-do-yaml-e-manter-apenas-no-markdown.md`

## Flow log
2026-02-25T15:36:44-03:00 | [yoda-0036] issue_add created | title: Remover entrypoints do YAML e manter apenas no markdown | description: Hoje entrypoints aparecem no front matter YAML e tambem no corpo do markdown da issue. Simplificar para manter entrypoints apenas no markdown e remover esse campo do YAML de issue/TODO/log quando aplicavel. Regra transversal: atualizar primeiro project/specs/ e depois yoda/. Como envolve layout YAML, aplicar politica de versao de schema e tratamento de compatibilidade conforme update.py quando aplicavel. | slug: remover-entrypoints-do-yaml-e-manter-apenas-no-markdown | priority: 3 | entrypoints: project/specs/:doc, yoda/templates/issue.md:doc, yoda/scripts/:code
2026-02-25T15:36:56-03:00 | [yoda-0036] todo_update | depends_on: [] -> yoda-0038
2026-02-25T18:58:33-03:00 | [yoda-0036] planning decision: classificada como subtle; rollout coordenado com yoda-0035/yoda-0037 com um unico bump menor de schema na release 0.1.3.
2026-02-25T19:09:30-03:00 | [yoda-0036] todo_update | status: to-do -> doing
2026-02-25T19:11:56-03:00 | [yoda-0036] evaluate: migracao de dados legados concluida (entrypoints removido de TODO/issues) e testes yoda/scripts/tests aprovados (33 passed).
2026-02-25T19:12:32-03:00 | [yoda-0036] implement: removido entrypoints do YAML (TODO/front matter/log contract), issue_add sem --entrypoint e specs alinhadas para manter entrypoints apenas no markdown.
2026-02-25T19:12:32-03:00 | [yoda-0036] todo_update (no changes)
2026-02-25T19:18:57-03:00 | [yoda-0036] todo_update (no changes)
2026-02-25T19:19:45-03:00 | [yoda-0036] closure: markdown da issue ressincronizado com criterios marcados e result log final apos revert local.
