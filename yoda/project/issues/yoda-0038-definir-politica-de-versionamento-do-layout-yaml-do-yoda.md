---
agent: Human
created_at: '2026-02-25T15:36:45-03:00'
depends_on: []
description: 'Definir e documentar regra obrigatoria de versionamento de schema/layout
  YAML do YODA: mudancas sutis incrementam versao menor (1.x), mudancas breaking que
  exigem tratamento em update.py incrementam versao maior. Incluir como regra operacional
  em specs e yoda.md, com criterio claro para classificacao e rollout.'
entrypoints:
- path: project/specs/
  type: doc
- path: yoda/yoda.md
  type: doc
- path: yoda/scripts/update.py
  type: code
id: yoda-0038
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 2
schema_version: '1.0'
slug: definir-politica-de-versionamento-do-layout-yaml-do-yoda
status: done
tags: []
title: Definir politica de versionamento do layout YAML do YODA
updated_at: '2026-02-25T18:51:16-03:00'
---

# yoda-0038 - Definir politica de versionamento do layout YAML do YODA
<!-- AGENT: Replace yoda-0038 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Definir politica de versionamento do layout YAML do YODA with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Definir uma politica obrigatoria para versionar mudancas no layout/schema YAML do YODA. A regra deve distinguir mudancas sutis (incremento menor em `1.x`) de mudancas breaking (incremento maior com tratamento via `update.py`).

## Context
As proximas simplificacoes vao alterar campos do YAML e hoje nao ha regra operacional unica para versionamento e migracao. Isso aumenta risco de incompatibilidade entre projetos e atualizacoes.

## Objective
Padronizar classificacao de mudancas de layout YAML e o procedimento de release/migracao correspondente.

## Scope
- Definir regra formal em `project/specs/` para versionamento do schema YAML.
- Definir quando a mudanca exige tratamento em `yoda/scripts/update.py`.
- Incluir exemplos de classificacao (sutil vs breaking).
- Definir como `init.py` deve ser usado no rollout de mudancas de layout.

## Out of scope
- Executar todas migracoes pendentes de campos (serao tratadas em issues especificas).
- Reformular versionamento de pacote fora do tema schema YAML.

## Requirements
- Ordem obrigatoria: `project/specs/` antes de `yoda/`.
- Regra minima:
- Mudanca sutil de layout/schema: incrementar versao menor em `1.x`.
- Mudanca breaking que exige migracao: incrementar versao maior e implementar tratamento no `update.py`.
- A regra deve ser referenciada pelas demais issues de alteracao de YAML.
- Politica fica no contexto interno de desenvolvimento do YODA (specs/scripts), nao no `yoda/yoda.md` embarcado.

## Acceptance criteria
- [x] Specs contem regra explicita e exemplos objetivos.
- [x] Ha criterio claro para obrigatoriedade de migracao em `update.py` e uso de `init.py` no rollout.
- [x] Demais issues de alteracao de YAML podem referenciar esta politica sem ambiguidade.

## Dependencies
None.

## Entry points
- path: project/specs/
  type: doc
- path: yoda/scripts/update.py
  type: code
- path: yoda/scripts/init.py
  type: code

## Implementation notes
Documentar a regra em linguagem operacional curta para evitar interpretacoes subjetivas.

## Tests
Nao aplicavel para testes automatizados diretos; validar por revisao documental e consistencia com o fluxo de `update.py`.

## Risks and edge cases
- Classificacao ambigua entre sutil e breaking pode gerar release incorreto.
- Regra sem exemplos pode ser ignorada em futuras issues.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
Politica de versionamento de layout/schema YAML formalizada no contexto interno de desenvolvimento do YODA (somente specs/scripts): classificacao sutil vs breaking, criterios operacionais, exemplos objetivos e regra de rollout com migracao obrigatoria em `update.py` para major bump e re-sync via `init.py`. O manual embarcado `yoda/yoda.md` nao foi usado para essa politica, conforme decisao.

docs(specs): definir politica de versionamento de layout YAML com rollout update/init
Issue: `yoda-0038`
Path: `yoda/project/issues/yoda-0038-definir-politica-de-versionamento-do-layout-yaml-do-yoda.md`