---
schema_version: '1.02'
id: yoda-0050
status: to-do
depends_on:
- yoda-0049
title: Criar yoda_flow_next.py com selecao e runbook por fase
description: Introduzir comando que seleciona issue elegivel de forma deterministica
  e retorna runbook compacto para Study, Document, Implement ou Evaluate.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:41-03:00'
updated_at: '2026-03-04T20:34:07-03:00'
---

# yoda-0050 - Criar yoda_flow_next.py com selecao e runbook por fase

## Summary
Criar o comando `yoda_flow_next.py` como orquestrador de entrada do YODA Flow. O script deve selecionar issue elegivel e emitir runbook curto e assertivo da fase atual.

## Context
No fluxo atual, o agente combina instrucoes longas de playbook com comandos separados, aumentando chance de desvio operacional.

## Objective
Centralizar selecao e instrucao operacional de fase em um unico comando deterministico.

## Scope
- Criar CLI `yoda_flow_next.py` com flags globais padrao.
- Selecionar issue elegivel usando a camada de leitura de markdown.
- Emitir runbook compacto por fase (`Study`, `Document`, `Implement`, `Evaluate`).
- Definir formato de saida md/json.

## Out of scope
- Transicoes avancadas de estado.
- Escrita automatica de log operacional.
- Migracao de dados legados.

## Requirements
- Deve bloquear quando existir issue `doing` nao concluida.
- Deve justificar bloqueios por dependencia/estado de forma objetiva.
- Deve produzir runbook curto, sem instrucoes ambiguas.

## Acceptance criteria
- [ ] Comando seleciona issue elegivel de forma deterministica.
- [ ] Runbook por fase e emitido em formato compacto.
- [ ] Saidas de erro cobrem casos de bloqueio comuns.

## Dependencies
Depende de `yoda-0049`.

## Entry points
- path: yoda/scripts/yoda_flow_next.py
  type: code
- path: yoda/scripts/lib
  type: code
- path: yoda/scripts/tests
  type: code

## Implementation notes
Runbooks devem ser pequenos para reduzir tokens e variacao de interpretacao.

## Tests
Cobrir selecao, bloqueios, saida md/json e mensagens de runbook por fase.

## Risks and edge cases
- Erro na selecao pode escolher issue incorreta.
- Runbook extenso demais pode contrariar objetivo de compactacao.

## Result log
