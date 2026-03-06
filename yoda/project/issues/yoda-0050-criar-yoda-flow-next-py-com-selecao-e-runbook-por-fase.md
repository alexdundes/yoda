---
schema_version: '1.02'
id: yoda-0050
status: done
depends_on:
- yoda-0049
title: Criar yoda_flow_next.py com selecao e runbook por fase
description: Introduzir comando que seleciona issue elegivel de forma deterministica
  e retorna runbook compacto para Study, Document, Implement ou Evaluate.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:41-03:00'
updated_at: '2026-03-06T17:30:24-03:00'
---

# yoda-0050 - Criar yoda_flow_next.py com selecao e runbook por fase

## Summary
Criar o comando `yoda_flow_next.py` como orquestrador de entrada do YODA Flow. O script deve selecionar/retomar issue de forma deterministica e emitir runbook curto, legivel e orientado apenas para a fase atual.

## Context
No fluxo atual, o agente combina instrucoes longas de playbook com comandos separados, aumentando chance de desvio operacional.

## Objective
Centralizar selecao e instrucao operacional de fase em um unico comando deterministico.

## Scope
- Criar CLI `yoda_flow_next.py` com flags globais padrao.
- Retomar issue `doing` quando existir.
- Selecionar issue elegivel usando `selectable` da camada de leitura markdown (`issue_index`).
- Nunca selecionar issue `pending`, mas sempre informar pendencias no output.
- Emitir runbook compacto por fase (`study`, `document`, `implement`, `evaluate`), sem mutacao de estado nesta issue.
- Definir formato de saida `md/json` com `next_step` fixo e `blocked_reason` fixo.

## Out of scope
- Transicoes/mutacoes de status/phase (ficam para `yoda-0051`).
- Escrita automatica de log operacional (fica para `yoda-0051`).
- Migracao de dados legados.

## Requirements
- Se existir issue `doing`, o comando deve retomar essa issue como alvo.
- Na ausencia de `doing`, a selecao deve usar `selectable` da camada `issue_index`.
- Issues `pending` nunca devem ser selecionadas, mas devem ser sempre reportadas.
- `next_step` deve usar valores fixos: `study | document | implement | evaluate | blocked`.
- `blocked_reason` deve usar valores fixos:
  - `no_selectable_issue`
  - `only_pending_issues`
  - `dependency_blocked`
- No output markdown, a explicacao de bloqueio deve ser legivel para o agent (texto claro), sem perder o codigo fixo em `blocked_reason`.
- O runbook deve orientar somente a fase atual e ser curto.
- Nesta issue, o script nao deve mutar metadados (status/phase/log).

## Acceptance criteria
- [x] Comando retoma issue `doing` quando existir.
- [x] Comando seleciona issue elegivel de forma deterministica usando `selectable`.
- [x] Issues `pending` nao sao selecionadas e sao sempre reportadas.
- [x] `next_step` usa apenas valores fixos.
- [x] `blocked_reason` usa apenas valores fixos.
- [x] Output markdown inclui secao `Runbook` legivel para o agent.
- [x] Em bloqueio, output markdown traz explicacao legivel + codigo fixo de bloqueio.
- [x] Nenhuma mutacao de status/phase/log ocorre na `yoda-0050`.

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
Runbooks devem ser pequenos para reduzir tokens e variacao de interpretacao. O markdown deve priorizar legibilidade operacional para o agent (instrucao direta da fase e resumo objetivo de bloqueio quando aplicavel).

## Tests
Cobrir:
- retomada de issue `doing`;
- selecao via `selectable` quando nao ha `doing`;
- exclusao de `pending` da selecao com pending hint obrigatoria;
- valores fixos de `next_step` e `blocked_reason`;
- saida `md` com secao `Runbook` legivel;
- ausencia de mutacao de estado na execucao da `yoda-0050`.

## Risks and edge cases
- Erro na selecao pode escolher issue incorreta.
- Runbook extenso demais pode contrariar objetivo de compactacao.
- Mensagem de bloqueio pouco clara pode gerar operacao incorreta pelo agent.

## Result log
feat(flow): criar yoda_flow_next deterministico com runbook legivel

Foi implementado `yoda/scripts/yoda_flow_next.py` com modelo implicito de proximo passo, retomada de issue `doing`, selecao deterministica por `selectable` quando nao ha `doing`, e pending hint obrigatoria sem selecionar issues `pending`. O output em `md/json` inclui `next_step` fixo, `blocked_reason` fixo e secao `Runbook` legivel para o agent. Tambem foi ajustada a camada `issue_index` para permitir leitura sem mutacao (`ensure_flow_log=False`) e adicionada suite de testes dedicada (`test_yoda_flow_next.py`) cobrindo retomada, selecao, bloqueios, runbook e ausencia de mutacao. Validacao executada com `5 passed`.

- **GitHub Issue** :   #3

- **Issue**: `yoda-0050`

- **Path**: `yoda/project/issues/yoda-0050-criar-yoda-flow-next-py-com-selecao-e-runbook-por-fase.md`