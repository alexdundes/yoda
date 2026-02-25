---
agent: Human
created_at: '2026-01-28T17:35:28-03:00'
depends_on: []
description: Create a spec and update docs to define the YODA Intake concept.
entrypoints: []
id: yoda-0015
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: specify-yoda-intake
status: done
tags: []
title: Specify YODA Intake
updated_at: '2026-01-28T17:45:41-03:00'
---

# yoda-0015 - Specify YODA Intake
<!-- AGENT: Replace yoda-0015 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Specify YODA Intake with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Definir o conceito e o ciclo do **YODA Intake** como etapa anterior ao YODA Flow, focada em descoberta/triagem e criação de issues prontas para execução. A issue deve produzir uma spec formal e ajustes de documentação para padronizar entrada, passos, artefatos e handoff para o YODA Flow.

## Context
Hoje existe apenas o YODA Flow (execução de uma issue já definida). Falta um ciclo explícito para **coletar desejos**, **triagem**, **deduplicação**, **decomposição** e **criação de issues** com Definition of Ready (DoR). Sem isso, há risco de backlog inconsistente e issues mal formadas.

## Objective
Especificar o YODA Intake e atualizar a documentação para que o agente saiba quando e como entrar nesse ciclo, quais passos seguir e como produzir issues prontas para o YODA Flow.

## Scope
- Definir o conceito de YODA Intake e sua relação com o YODA Flow.
- Revisar o YODA Flow para explicitar termos e distinções entre Intake e Flow (objetivo de cada ciclo).
- Descrever gatilhos de entrada, passos do ciclo e regras do agente.
- Definir critérios mínimos de “issue pronta” (DoR).
- Definir artefatos/outputs esperados (issues criadas, TODO atualizado, ordem revisada).
- Atualizar as docs necessárias (specs e playbook do agent).

## Out of scope
- Implementação de novos scripts.
- Alterações de schema além do necessário para documentação.
- Execução do YODA Flow em issues específicas.

## Requirements
- Nome oficial do ciclo: **YODA Intake** (pareado com YODA Flow).
- Definir gatilho de entrada (frases naturais do humano).
- Definir passos: coleta inicial → triagem/deduplicação → decomposição → DoR → criação de issues → reordenar backlog → handoff.
- Incluir orientação de usar `todo_list.py` para triagem e visão do backlog.
- Incluir orientação de usar `issue_add.py` para criação das issues e edição do Markdown.
- Definir handoff explícito para o YODA Flow ao final do Intake.
- Revisar as specs base para deixar claro o objetivo de YODA Intake vs YODA Flow.
- Revisar o playbook para orientar o agent no novo ciclo.

## Acceptance criteria
- [x] Spec do YODA Intake criada em `project/specs/`.
- [x] Playbook do agent atualizado para incluir entrada/saída do YODA Intake.
- [x] DoR mínimo documentado para issues criadas pelo Intake.
- [x] Handoff para YODA Flow documentado.

## Dependencies
None.

## Entry points
- path: project/specs/02-yoda-flow-process.md
  type: doc
- path: project/specs/06-agent-playbook.md
  type: doc
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: yoda/yoda.md
  type: doc

## Implementation notes
Tratar YODA Intake como ciclo “backlog-centric” distinto do YODA Flow (issue-centric). Definir regras operacionais do agente (consultar `todo_list.py`, não criar issue sem DoR, encerrar ciclo explicitamente).

## Tests
Not applicable (docs/spec only).

## Risks and edge cases
- Risco de misturar Intake com Flow e gerar issues sem DoR.
- Backlog duplicado se triagem/deduplicação não for seguida.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
Defined the YODA Intake cycle and updated Flow and playbook docs to clarify roles and handoff.

docs(specs): add YODA Intake cycle

Issue: `yoda-0015`
Path: `yoda/project/issues/yoda-0015-specify-yoda-intake.md`