---
schema_version: '2.00'
id: yoda-0037
status: done
depends_on:
- yoda-0038
title: Remover conceito de tags do YODA
description: 'O campo tags esta subutilizado e deve ser eliminado por completo do
  YODA (schema, scripts, filtros e templates). Regra transversal: atualizar primeiro
  project/specs/ e depois yoda/. Como envolve layout YAML, aplicar politica de versao
  de schema e tratamento de compatibilidade conforme update.py quando aplicavel.'
priority: 3
created_at: '2026-02-25T15:36:45-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0037 - Remover conceito de tags do YODA

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
Tags foi removido como conceito ativo do modelo e da CLI: `todo_list.py` sem `--tags`, `todo_update.py` sem `--tags/--clear-tags`, `issue_add.py` sem campo `tags` no metadata novo. A documentacao foi atualizada para schema alvo `1.01`, sem `tags` no schema ativo. Foi adicionado `--reconcile-layout` em `init.py` para touch de `*.md` e reconciliacao de `TODO.<dev>.yaml` + front matter das issues, e esse recurso foi executado para corrigir o workspace atual para `schema_version 1.01`.

test: `python3 -m pytest yoda/scripts/tests` => 35 passed.

refactor(yoda): desativar tags no modelo e adicionar reconciliacao de layout no init
Issue: `yoda-0037`
Path: `yoda/project/issues/yoda-0037-remover-conceito-de-tags-do-yoda.md`

## Flow log
2026-02-25T15:36:45-03:00 | [yoda-0037] issue_add created | title: Remover conceito de tags do YODA | description: O campo tags esta subutilizado e deve ser eliminado por completo do YODA (schema, scripts, filtros e templates). Regra transversal: atualizar primeiro project/specs/ e depois yoda/. Como envolve layout YAML, aplicar politica de versao de schema e tratamento de compatibilidade conforme update.py quando aplicavel. | slug: remover-conceito-de-tags-do-yoda | priority: 3 | entrypoints: project/specs/:doc, yoda/scripts/:code, yoda/templates/issue.md:doc
2026-02-25T15:36:56-03:00 | [yoda-0037] todo_update | depends_on: [] -> yoda-0038
2026-02-25T18:58:33-03:00 | [yoda-0037] planning decision: classificada como subtle; rollout coordenado com yoda-0035/yoda-0036 com um unico bump menor de schema na release 0.1.3.
2026-02-25T19:21:38-03:00 | [yoda-0037] todo_update | status: to-do -> doing
2026-02-25T19:27:29-03:00 | [yoda-0037] document: decisoes registradas - remover flags de tags, manter tags legado ate reconciliacao via novo parametro no init.py, schema alvo 1.01 a partir desta issue.
2026-02-25T19:35:18-03:00 | [yoda-0037] todo_update (no changes)
2026-02-25T19:35:38-03:00 | [yoda-0037] implement: removido suporte ativo a tags em scripts e specs; schema alvo atualizado para 1.01; init.py recebeu --reconcile-layout para touch/reconciliacao de TODO e front matter.
2026-02-25T19:35:38-03:00 | [yoda-0037] evaluate: validado comportamento sem --tags/--clear-tags e suite de scripts aprovada (35 passed).
2026-02-25T19:35:38-03:00 | [yoda-0037] todo_update | status: doing -> done
2026-02-25T19:36:45-03:00 | [yoda-0037] note: log schema version confirmado em 1.0 conforme decisao.
