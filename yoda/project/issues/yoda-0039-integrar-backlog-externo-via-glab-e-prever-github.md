---
created_at: '2026-02-25T15:36:45-03:00'
depends_on:
- yoda-0038
description: 'Redefinir o uso de origin para mapear e traduzir backlog externo em
  issues YODA usando glab (GitLab CLI), permitindo que uma issue externa gere uma
  ou varias issues YODA. Prever tambem operacao equivalente com issues do GitHub (gh).
  Regra transversal: atualizar primeiro project/specs/ e depois yoda/.'
id: yoda-0039
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 1
schema_version: '1.01'
slug: integrar-backlog-externo-via-glab-e-prever-github
status: to-do
title: Integrar backlog externo via glab e prever GitHub
updated_at: '2026-02-25T20:02:28-03:00'
---

# yoda-0039 - Integrar backlog externo via glab e prever GitHub
<!-- AGENT: Replace yoda-0039 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Integrar backlog externo via glab e prever GitHub with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Evoluir o tratamento de origem de backlog para integrar issues externas via `glab` (GitLab CLI), permitindo traduzir uma issue externa em uma ou varias issues YODA. Prever o mesmo modelo para GitHub (`gh`).

## Context
O campo `origin` atual esta subutilizado e sem fluxo claro de ingestao de backlog externo. Falta um processo operacional para conectar tracking externo com planejamento YODA.

## Objective
Definir e implementar um fluxo de intake a partir de issues GitLab/GitHub para gerar backlog YODA rastreavel.

## Scope
- Atualizar specs com fluxo de ingestao de backlog externo.
- Definir modelo de mapeamento origem externa -> uma ou N issues YODA.
- Implementar suporte inicial com `glab` e previsao para `gh`.
- Revisar uso do bloco `origin` no schema, conforme necessidade.

## Out of scope
- Sincronizacao bidirecional completa de estado entre plataformas.
- Cobrir todos provedores de issue tracker alem de GitLab/GitHub.

## Requirements
- Ordem obrigatoria: `project/specs/` antes de `yoda/`.
- Fluxo deve permitir selecionar issue externa e gerar issues YODA relacionadas.
- Deve existir rastreabilidade entre issue YODA e origem externa.
- Classificacao planejada: **subtle** (se houver alteracao de layout YAML, manter compatibilidade sem migracao breaking).

## Acceptance criteria
- [ ] Specs descrevem fluxo com `glab` e previsao equivalente para `gh`.
- [ ] Existe implementacao minima operacional para importar/traduzir issue GitLab.
- [ ] Uma issue externa pode gerar multiplas issues YODA com vinculo de origem.
- [ ] Manual (`yoda/yoda.md`) orienta como usar o fluxo no Intake.

## Dependencies
`yoda-0038` caso haja alteracao de layout YAML/origin.

## Entry points
- path: project/specs/
  type: doc
- path: yoda/scripts/
  type: code
- path: yoda/yoda.md
  type: doc

## Implementation notes
Decisao de planejamento: tratar esta issue como `subtle`.
Preferir primeiro um fluxo manual-assistido robusto (comandos claros) antes de automacao ampla.

## Tests
Adicionar testes para parser/mapeamento de origem externa e geracao de multiplas issues YODA.

## Risks and edge cases
- Limitacoes de autenticacao/escopo de token no `glab` e `gh`.
- Diferencas de modelo de dados entre GitLab e GitHub.
- Duplicacao de issues se nao houver controle de idempotencia na importacao.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->