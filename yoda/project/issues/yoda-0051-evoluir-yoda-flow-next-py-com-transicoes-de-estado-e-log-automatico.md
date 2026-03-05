---
schema_version: '1.02'
id: yoda-0051
status: to-do
depends_on:
- yoda-0050
title: Evoluir yoda_flow_next.py com transicoes de estado e log automatico
description: Adicionar parametros de transicao e registro automatico de eventos no
  log embutido da issue, retirando log_add.py do fluxo padrao.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:41-03:00'
updated_at: '2026-03-04T20:34:07-03:00'
---

# yoda-0051 - Evoluir yoda_flow_next.py com transicoes de estado e log automatico

## Summary
Evoluir `yoda_flow_next.py` para aplicar transicoes de estado/fase e registrar historico operacional automaticamente. O objetivo e retirar `log_add.py` do caminho padrao do agente.

## Context
Hoje o fluxo depende de chamadas manuais adicionais para atualizar estado e gravar logs, o que aumenta passos e risco de erro.

## Objective
Permitir que o agente avance no fluxo com comandos deterministicos e menos etapas manuais.

## Scope
- Adicionar parametros de acao/transicao no `yoda_flow_next.py`.
- Persistir mudancas de status/fase conforme regras do fluxo.
- Registrar eventos no historico embutido da issue markdown.
- Padronizar mensagens de log automatico por acao.

## Out of scope
- Migracao de dados legados.
- Remocao fisica imediata de `log_add.py`.
- Alteracoes de empacotamento/release.

## Requirements
- Transicoes invalidas devem falhar com erro claro.
- Escrita de log deve ser append-only e deterministica.
- Fluxo padrao nao deve exigir `log_add.py`.

## Acceptance criteria
- [ ] `yoda_flow_next.py` executa transicoes basicas de fase/estado.
- [ ] Eventos operacionais sao registrados no markdown da issue.
- [ ] Cenarios de transicao invalida possuem testes.

## Dependencies
Depende de `yoda-0050`.

## Entry points
- path: yoda/scripts/yoda_flow_next.py
  type: code
- path: yoda/scripts/lib
  type: code
- path: yoda/project/issues
  type: data

## Implementation notes
Definir estrutura minima de eventos para facilitar leitura humana e parse futuro.

## Tests
Cobrir transicoes validas, invalidas e comportamento de append no historico embutido.

## Risks and edge cases
- Concorrencia de escrita pode gerar conflitos de merge.
- Ordem incorreta de eventos pode comprometer auditoria do fluxo.

## Result log
