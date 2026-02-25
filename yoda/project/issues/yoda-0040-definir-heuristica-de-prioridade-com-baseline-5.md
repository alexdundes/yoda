---
agent: Human
created_at: '2026-02-25T15:36:45-03:00'
depends_on: []
description: 'Orientar o agente para tratar prioridade 5 como baseline padrao e ajustar
  para cima/baixo apenas por importancia relativa frente as demais issues abertas.
  Documentar isso em yoda/yoda.md e alinhar com specs. Regra transversal: atualizar
  primeiro project/specs/ e depois yoda/.'
entrypoints:
- path: project/specs/
  type: doc
- path: yoda/yoda.md
  type: doc
id: yoda-0040
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 4
schema_version: '1.0'
slug: definir-heuristica-de-prioridade-com-baseline-5
status: done
tags: []
title: Definir heuristica de prioridade com baseline 5
updated_at: '2026-02-25T18:32:04-03:00'
---

# yoda-0040 - Definir heuristica de prioridade com baseline 5
<!-- AGENT: Replace yoda-0040 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Definir heuristica de prioridade com baseline 5 with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Definir regra de priorizacao para agentes com baseline em prioridade `5`. A prioridade deve subir ou descer somente por importancia relativa entre issues abertas.

## Context
Sem heuristica explicita, a priorizacao tende a ficar inconsistente entre ciclos e agentes. Uma regra simples melhora previsibilidade do backlog.

## Objective
Padronizar a atribuicao de prioridade com baseline `5` e ajuste comparativo.

## Scope
- Atualizar `project/specs/` com a regra de baseline e calibragem relativa.
- Atualizar `yoda/yoda.md` com instrucao objetiva para agentes.
- Ajustar exemplos/documentacao de Intake e abertura de issue.

## Out of scope
- Reescalar historico inteiro de prioridades antigas.
- Introduzir algoritmo automatico complexo de ranking.

## Requirements
- Ordem obrigatoria: `project/specs/` antes de `yoda/`.
- Nova issue deve iniciar em prioridade `5` por padrao, salvo justificativa explicita.
- Ajustes acima/abaixo de `5` devem considerar comparacao com issues abertas e registrar justificativa curta no markdown da issue.
- Regra precisa ficar clara no trecho de Intake em `yoda/yoda.md`.

## Acceptance criteria
- [x] Specs documentam baseline `5` e criterio para ajustar prioridade por comparacao relativa.
- [x] Specs deixam explicito que prioridade diferente de `5` requer justificativa curta no markdown da issue.
- [x] `yoda/yoda.md` instrui explicitamente esse comportamento no trecho de Intake e referencia de script.
- [x] Exemplos de Intake/issue creation refletem a regra.

## Dependencies
None.

## Entry points
- path: project/specs/
  type: doc
- path: yoda/yoda.md
  type: doc

## Implementation notes
Manter a regra simples para favorecer aplicacao consistente em conversas de Intake.
Aplicar nos docs com texto normativo e sem obrigar mudanca de codigo em `issue_add.py` (default `5` ja existe).

## Tests
Nao aplicavel para testes automatizados diretos; validar por revisao documental e exemplos atualizados.

## Risks and edge cases
- Prioridade pode continuar subjetiva sem comparacao explicita com backlog atual.
- Agente pode inflar prioridade sem registrar justificativa.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
Atualizado o baseline de prioridade para `5` como regra padrao em `project/specs/` e no manual `yoda/yoda.md`, com criterio de ajuste relativo ao backlog aberto e exigencia de justificativa curta quando prioridade for diferente de `5`.

docs(yoda): definir baseline 5 para prioridade no Intake
Issue: `yoda-0040`
Path: `yoda/project/issues/yoda-0040-definir-heuristica-de-prioridade-com-baseline-5.md`