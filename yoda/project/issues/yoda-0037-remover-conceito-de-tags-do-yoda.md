---
agent: Human
created_at: '2026-02-25T15:36:45-03:00'
depends_on:
- yoda-0038
description: 'O campo tags esta subutilizado e deve ser eliminado por completo do
  YODA (schema, scripts, filtros e templates). Regra transversal: atualizar primeiro
  project/specs/ e depois yoda/. Como envolve layout YAML, aplicar politica de versao
  de schema e tratamento de compatibilidade conforme update.py quando aplicavel.'
entrypoints:
- path: project/specs/
  type: doc
- path: yoda/scripts/
  type: code
- path: yoda/templates/issue.md
  type: doc
id: yoda-0037
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 3
schema_version: '1.0'
slug: remover-conceito-de-tags-do-yoda
status: to-do
tags: []
title: Remover conceito de tags do YODA
updated_at: '2026-02-25T15:36:56-03:00'
---

# yoda-0037 - Remover conceito de tags do YODA
<!-- AGENT: Replace yoda-0037 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Remover conceito de tags do YODA with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Remover completamente o conceito de `tags` do YODA por baixa utilizacao. Isso inclui schema, filtros CLI, templates e documentacao operacional.

## Context
As tags nao estao gerando valor proporcional a complexidade adicionada no schema e nos scripts. A simplificacao reduz superficie de manutencao.

## Objective
Eliminar `tags` de todo o fluxo YODA mantendo os comandos coerentes e previsiveis.

## Scope
- Atualizar `project/specs/` removendo tags do modelo.
- Atualizar scripts que recebem/filtram tags.
- Remover tags de templates e exemplos.
- Ajustar `yoda/yoda.md` quando houver mencoes.

## Out of scope
- Criar sistema alternativo de classificacao no mesmo ciclo.
- Mudar criterio de prioridade (tratado em issue dedicada).

## Requirements
- Ordem obrigatoria: `project/specs/` antes de `yoda/`.
- CLI nao deve expor flags relacionadas a tags ao final.
- Por alterar layout YAML, aplicar politica de versionamento definida em `yoda-0038`.
- Se houver breaking no upgrade, implementar tratamento em `update.py`.

## Acceptance criteria
- [ ] Specs e manual nao tratam mais `tags` como campo ativo.
- [ ] YAML de TODO/issue/log nao inclui `tags`.
- [ ] Scripts funcionam sem `--tags`/`--clear-tags` ou equivalentes.
- [ ] Testes cobrem comportamento apos remocao.

## Dependencies
`yoda-0038` (politica de versionamento de layout YAML).

## Entry points
- path: project/specs/
  type: doc
- path: yoda/scripts/
  type: code
- path: yoda/templates/issue.md
  type: doc

## Implementation notes
Planejar migracao para limpar tags existentes nos dados historicos.

## Tests
Atualizar testes de CLI e schema para validar ausencia de tags.

## Risks and edge cases
- Automacoes externas que usam filtros por tags podem falhar apos mudanca.
- Remocao parcial em scripts pode causar comportamento inconsistente.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
