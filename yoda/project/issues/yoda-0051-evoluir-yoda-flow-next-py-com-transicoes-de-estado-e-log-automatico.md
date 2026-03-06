---
schema_version: '2.00'
id: yoda-0051
status: done
depends_on:
- yoda-0050
title: Evoluir yoda_flow_next.py com transicoes de estado e log automatico
description: Adicionar parametros de transicao e registro automatico de eventos no
  log embutido da issue, retirando log_add.py do fluxo padrao.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:41-03:00'
updated_at: '2026-03-06T18:09:11-03:00'
---

# yoda-0051 - Evoluir yoda_flow_next.py com transicoes de estado e log automatico

## Summary
Evoluir `yoda_flow_next.py` para aplicar transicoes de estado/fase e registrar historico operacional automaticamente. O objetivo e retirar `log_add.py` do caminho padrao do agente.

## Context
Hoje o fluxo depende de chamadas manuais adicionais para atualizar estado e gravar logs, o que aumenta passos e risco de erro.

## Objective
Permitir que o agente avance no fluxo com comandos deterministicos e menos etapas manuais.

## Scope
- Manter interface deterministica com unico parametro operacional `--dev`.
- Quando chamado sem `--dev`, retornar instrucao curta de como obter/informar o developer slug.
- Persistir mudancas de status/fase conforme regras do fluxo.
- Registrar eventos no historico embutido da issue markdown.
- Tratar `TODO.<dev>.yaml` como legado neste script.

## Out of scope
- Migracao de dados legados.
- Remocao fisica imediata de `log_add.py` e `todo_update.py`.
- Alteracoes de empacotamento/release.

## Requirements
- `yoda_flow_next.py` nao recebe flags de acao/status/phase; apenas `--dev`.
- Com `--dev`, o comando deve resolver a issue selecionavel, aplicar a proxima transicao valida e retornar runbook da fase resultante.
- Sem `--dev`, o comando deve retornar orientacao objetiva para obter/informar o slug.
- Matriz de transicao aprovada:
  - `to-do` -> `doing` com `phase=study`
  - `doing+study` -> `doing+document`
  - `doing+document` -> `doing+implement`
  - `doing+implement` -> `doing+evaluate`
  - `doing+evaluate` -> `done` removendo `phase`
- Issue `pending` nunca pode ser selecionada automaticamente.
- Dependencia inexistente deve ser tratada como `done`; dependencia existente deve validar status.
- Escrita de log deve ser append-only e deterministica.
- Cada entrada de log deve ter uma unica linha: `<timestamp> <mensagem-curta>`.
- `todo_update.py` permanece caminho oficial para ajustes manuais de status/phase fora da automacao do flow.

## Acceptance criteria
- [x] `yoda_flow_next.py` opera de forma implicita com `--dev` e sem flags de acao.
- [x] Sem `--dev`, o comando responde com instrucao curta para resolver o slug.
- [x] Com `--dev`, o comando aplica exatamente uma transicao valida por execucao.
- [x] Issues `pending` sao sempre ignoradas na selecao automatica.
- [x] Dependencias inexistentes sao consideradas `done`; dependencias existentes sao validadas.
- [x] Eventos operacionais sao registrados no markdown da issue em linha unica compacta.
- [x] Cenarios de transicao invalida e de bloqueio possuem testes.

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
Runbook permanece compacto e orienta somente a fase atual. A automacao deve registrar decisao em todas as execucoes (inclusive bloqueio) para rastreabilidade, mantendo formato de log em uma linha curta.

## Tests
Cobrir:
- chamada sem `--dev` com instrucao deterministica;
- transicoes validas unitarias em sequencia;
- bloqueios por dependencia;
- exclusao de `pending` da selecao;
- log automatico em linha unica por execucao;
- comportamento com YAML tratado como legado.

## Risks and edge cases
- Concorrencia de escrita pode gerar conflitos de merge.
- Ordem incorreta de eventos pode comprometer auditoria do fluxo.

## Result log
feat(flow): evoluir yoda_flow_next com transicao automatica e continuidade assistida

Foi implementada a evolucao do `yoda_flow_next.py` para executar transicoes deterministicas por chamada usando apenas `--dev`, com mutacao de status/fase, registro automatico no `## Flow log` em linha unica e tratamento de bloqueios com motivo fixo. O runbook de `evaluate` passou a explicitar o formato oficial de `Result log`, e ao concluir em `done` o script retorna a proxima issue candidata e prompt de confirmacao para continuidade do fluxo. Tambem foi adicionado suporte de `phase` no `todo_update.py` com regra de persistencia apenas em `doing`, e a cobertura de testes foi atualizada para os novos contratos.

- **GitHub Issue** :   #3

- **Issue**: `yoda-0051`

- **Path**: `yoda/project/issues/yoda-0051-evoluir-yoda-flow-next-py-com-transicoes-de-estado-e-log-automatico.md`

## Flow log
2026-03-04T20:33:41-03:00 | [yoda-0051] issue_add created | title: Evoluir yoda_flow_next.py com transicoes de estado e log automatico | description: Adicionar parametros de transicao e registro automatico de eventos no log embutido da issue, retirando log_add.py do fluxo padrao. | slug: evoluir-yoda-flow-next-py-com-transicoes-de-estado-e-log-automatico | extern_issue_file: external issue linked
2026-03-04T20:34:08-03:00 | [yoda-0051] todo_update | depends_on:  -> yoda-0050
2026-03-06T17:42:34-03:00 | [yoda-0051] todo_update | status: to-do -> doing
2026-03-06T17:42:46-03:00 | yoda-0051: fase Study iniciada; issue movida para doing e contexto tecnico de transicoes+log automatico levantado.
2026-03-06T17:55:31-03:00 | yoda-0051: Document concluido com contrato aprovado de interface implicita, transicoes fixas, log 1 linha e YAML como legado.
2026-03-06T18:01:47-03:00 | yoda-0051: Implement concluido com transicao automatica no yoda_flow_next, log embutido 1 linha, suporte --phase no todo_update e testes passando.
2026-03-06T18:06:39-03:00 | yoda-0051: ajuste por review aplicado no yoda_flow_next com runbook Evaluate detalhando Result log e saida done com proxima issue + confirmacao.
2026-03-06T18:09:11-03:00 | yoda-0051: Evaluate concluido com ACs validados, Result log preenchido e testes 24 passed.
2026-03-06T18:09:11-03:00 | yoda-0051: todo_update status: doing -> done
