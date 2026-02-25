---
created_at: '2026-02-25T15:36:45-03:00'
depends_on:
- yoda-0038
description: 'O campo tags esta subutilizado e deve ser eliminado por completo do
  YODA (schema, scripts, filtros e templates). Regra transversal: atualizar primeiro
  project/specs/ e depois yoda/. Como envolve layout YAML, aplicar politica de versao
  de schema e tratamento de compatibilidade conforme update.py quando aplicavel.'
id: yoda-0037
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 3
schema_version: '1.01'
slug: remover-conceito-de-tags-do-yoda
status: done
title: Remover conceito de tags do YODA
updated_at: '2026-02-25T20:02:28-03:00'
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
- Incluir no `init.py` um parametro de manutencao para "touch" em todos os `*.md` e reconciliacao estrutural de `TODO.<dev>.yaml` e `<dev>-NNNN-*.md`, para uso em atualizacoes.

## Out of scope
- Criar sistema alternativo de classificacao no mesmo ciclo.
- Mudar criterio de prioridade (tratado em issue dedicada).

## Requirements
- Ordem obrigatoria: `project/specs/` antes de `yoda/`.
- CLI nao deve expor flags relacionadas a tags ao final.
- Por alterar layout YAML, aplicar politica de versionamento definida em `yoda-0038`.
- Classificacao definida: **subtle**.
- Rollout definido em conjunto com `yoda-0035` e `yoda-0036`: aplicar **um unico incremento menor** de `schema_version` para o pacote `0.1.3`.
- A partir desta issue, considerar `schema_version` alvo `1.01`.
- `issue_add` pode manter mencao de `tags` no texto de log historico, mas sem manter `tags` como campo ativo no modelo.
- Nao remover `tags` dos dados existentes agora; a limpeza/reconciliacao deve ocorrer via nova capacidade de manutencao no `init.py`.
- `todo_list.py` deve remover suporte ao filtro `--tags`.
- `todo_update.py` deve remover suporte a `--tags` e `--clear-tags`.

## Acceptance criteria
- [x] Specs e manual nao tratam mais `tags` como campo ativo.
- [x] Scripts funcionam sem `--tags`/`--clear-tags` (flags removidas).
- [x] Testes cobrem comportamento apos remocao.
- [x] `init.py` possui parametro de manutencao para touch/reconciliacao e ele corrige `TODO.<dev>.yaml` e front matter dos `*.md` conforme schema alvo `1.01`.

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
Decisao de planejamento: tratar esta mudanca como `subtle` e coordenar com `yoda-0035`/`yoda-0036` para um unico bump menor de schema na release `0.1.3`.
Nao remover `tags` imediatamente dos artefatos existentes; usar um fluxo de reconciliacao acionado por parametro no `init.py`.
Manter compatibilidade de log historico em `issue_add` (linha textual), sem promover `tags` como campo ativo no schema.

## Tests
Atualizar testes de CLI para validar remocao de `--tags` e `--clear-tags`.
Adicionar teste para o novo parametro de manutencao do `init.py` cobrindo touch/reconciliacao de `TODO.<dev>.yaml` e front matter de issues.

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
Tags foi removido como conceito ativo do modelo e da CLI: `todo_list.py` sem `--tags`, `todo_update.py` sem `--tags/--clear-tags`, `issue_add.py` sem campo `tags` no metadata novo. A documentacao foi atualizada para schema alvo `1.01`, sem `tags` no schema ativo. Foi adicionado `--reconcile-layout` em `init.py` para touch de `*.md` e reconciliacao de `TODO.<dev>.yaml` + front matter das issues, e esse recurso foi executado para corrigir o workspace atual para `schema_version 1.01`.

test: `python3 -m pytest yoda/scripts/tests` => 35 passed.

refactor(yoda): desativar tags no modelo e adicionar reconciliacao de layout no init
Issue: `yoda-0037`
Path: `yoda/project/issues/yoda-0037-remover-conceito-de-tags-do-yoda.md`