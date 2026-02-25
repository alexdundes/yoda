---
created_at: '2026-02-25T15:36:44-03:00'
depends_on:
- yoda-0038
description: 'O conceito de lightweight esta subutilizado e deve ser removido por
  completo do YODA (schema, scripts, templates e playbooks). Regra transversal: atualizar
  primeiro project/specs/ e depois yoda/. Como envolve layout YAML, aplicar politica
  de versao de schema e tratamento de compatibilidade conforme update.py quando aplicavel.'
id: yoda-0035
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 3
schema_version: '1.01'
slug: remover-conceito-de-lightweight-do-yoda
status: done
title: Remover conceito de lightweight do YODA
updated_at: '2026-02-25T20:02:28-03:00'
---

# yoda-0035 - Remover conceito de lightweight do YODA
<!-- AGENT: Replace yoda-0035 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Remover conceito de lightweight do YODA with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Eliminar o conceito de `lightweight` do YODA por estar subutilizado. A remocao deve cobrir schema, scripts, templates e documentacao, sem deixar caminhos alternativos ativos.

## Context
O campo/fluxo `lightweight` adiciona complexidade e variacoes pouco usadas no processo. A simplificacao reduz ambiguidade no Intake e no Flow.

## Objective
Remover completamente `lightweight` do modelo operacional e dos artefatos do YODA.

## Scope
- Atualizar `project/specs/` removendo o conceito.
- Atualizar `yoda/yoda.md` e playbooks relacionados.
- Remover campo `lightweight` dos YAMLs e dos scripts que o leem/escrevem.
- Ajustar templates e testes.

## Out of scope
- Introduzir novo modo alternativo de fluxo no lugar de lightweight.
- Mudancas de priorizacao nao relacionadas ao lightweight.

## Requirements
- Ordem obrigatoria: `project/specs/` antes de `yoda/`.
- Nenhum comando deve depender de `lightweight` ao final.
- Por alterar layout YAML, aplicar politica de versionamento definida em `yoda-0038`.
- Classificacao definida: **subtle**.
- Rollout definido em conjunto com `yoda-0036` e `yoda-0037`: aplicar **um unico incremento menor** de `schema_version` para o pacote `0.1.3`.

## Acceptance criteria
- [x] Specs e manual nao mencionam `lightweight` como conceito ativo.
- [x] YAML/TODO/log/issue nao usam campo `lightweight`.
- [x] Scripts funcionam sem flags/filtros `lightweight`.
- [x] Testes cobrindo fluxo principal passam apos remocao.

## Dependencies
`yoda-0038` (politica de versionamento de layout YAML).

## Entry points
- path: project/specs/
  type: doc
- path: yoda/yoda.md
  type: doc
- path: yoda/scripts/
  type: code

## Implementation notes
Decisao de planejamento: tratar esta mudanca como `subtle` e coordenar com `yoda-0036`/`yoda-0037` para um unico bump menor de schema na release `0.1.3`.

## Tests
Adicionar/atualizar testes para garantir ausencia de `lightweight` no parse, filtros e output dos scripts.

## Risks and edge cases
- Regressao em repositorios com dados antigos que ainda contenham campo legado.
- Divergencia entre schema documentado e parser dos scripts.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
Remocao de `lightweight` aplicada no YODA: specs e manual atualizados para fluxo unico (sem lightweight), `issue_add.py` e `todo_list.py` sem flag/filtro `lightweight`, validacoes ajustadas, template lightweight removido e template padrao simplificado. Artefatos existentes (TODO e front matter de issues) foram limpos para nao carregar mais o campo `lightweight`.

test: `python3 -m pytest yoda/scripts/tests` => 33 passed.

refactor(yoda): remover conceito de lightweight do fluxo e schema
Issue: `yoda-0035`
Path: `yoda/project/issues/yoda-0035-remover-conceito-de-lightweight-do-yoda.md`