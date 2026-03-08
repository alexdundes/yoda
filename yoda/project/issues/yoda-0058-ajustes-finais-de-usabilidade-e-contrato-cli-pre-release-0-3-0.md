---
schema_version: '2.00'
status: done
title: Ajustes finais de usabilidade e contrato CLI pre-release 0.3.0
description: 'Consolidar ajustes document-first antes da validacao final: padrao de
  log sem prefixo redundante de issue, suporte de mensagem de log no yoda_flow_next.py,
  orientacao/runbook via --help nos comandos quando aplicavel, padronizacao de --dev
  como entrada obrigatoria (exceto update.py) e reposicionamento de favicons para
  fora de yoda/.'
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-07T11:31:39-03:00'
updated_at: '2026-03-07T11:57:32-03:00'
---

# yoda-0058 - Ajustes finais de usabilidade e contrato CLI pre-release 0.3.0

## Summary
Consolidar em uma unica micro-issue os ajustes finais de ergonomia e contrato operacional antes da validacao de release 0.3.0. O foco e reduzir redundancia no log, melhorar suporte de logging no fluxo por fase, padronizar entrada de `--dev`, reforcar orientacoes via `--help` e ajustar fronteira de empacotamento movendo `favicons` para fora de `yoda/`.

## Context
A base 0.3.0 ja esta funcional, mas ainda existem pontos de consistencia operacional que podem gerar friccao no uso por agentes e ambiguidade de contrato CLI. Como a release final depende de `yoda-0054`, estes ajustes devem entrar antes da etapa de validacao end-to-end.

## Objective
Aplicar e documentar ajustes finais document-first para o fluxo 0.3.0, mantendo escopo compacto e rastreavel em uma unica issue.

## Scope
- Atualizar `project/specs` para explicitar que entradas de `## Flow log` nao devem repetir prefixo redundante de issue por linha (aplicacao somente daqui para frente).
- Especificar e implementar parametro `--log-message` em `yoda_flow_next.py` para registrar mensagem resumida de acao no `Flow log`, junto da transicao de fase/estado.
- Revisar os 11 comandos em `yoda/scripts/*.py` para incluir orientacoes/runbook no `--help` quando couber e atualizar `yoda/yoda.md` para orientar uso desses `--help`.
- Padronizar `--dev` como unica entrada de developer slug nos comandos YODA (exceto `update.py`), com orientacao explicita para o agente solicitar ao humano quando ausente.
- Mover `favicons` de `yoda/favicons` para `favicons/` na raiz do repositorio, deixando claro que nao faz parte do empacotamento.
- Manter abordagem document-first: atualizar specs/playbook antes de implementacao.

## Out of scope
- Reescrever historico antigo de `Flow log` ja registrado.
- Alteracoes estruturais fora dos pontos acima.
- Mudancas em `package.py`.

## Requirements
- As regras novas de log valem apenas para registros futuros.
- O novo parametro `--log-message` em `yoda_flow_next.py` deve ser opcional e deterministico.
- Todos os comandos YODA afetados devem manter comportamento consistente quando `--dev` estiver ausente, com orientacao de solicitacao ao humano.
- `update.py` permanece excecao explicita para a regra de `--dev` obrigatorio.
- A reorganizacao para `favicons/` na raiz deve preservar funcionamento esperado e deixar fronteira de empacotamento explicita.

## Acceptance criteria
- [x] Specs/playbook atualizados primeiro (document-first) cobrindo os cinco ajustes desta issue.
- [x] `yoda_flow_next.py` aceita `--log-message` opcional e registra no `Flow log` junto da transicao.
- [x] Os 11 comandos em `yoda/scripts/*.py` foram revisados com orientacoes em `--help` quando aplicavel e regra de `--dev` unificada (com excecao de `update.py`).
- [x] `favicons` foi movido de `yoda/favicons` para `favicons/` com impacto de empacotamento/documentacao ajustado.
- [x] `yoda-0054` depende desta issue para validacao final da release.

## Entry points
- `project/specs`
- `yoda/yoda.md`
- `yoda/scripts/yoda_flow_next.py`
- `yoda/scripts/*.py`
- `yoda/scripts/README.md`
- `yoda/favicons`
- `favicons`
- `yoda/project/issues/yoda-0054-validacao-end-to-end-e-preparacao-de-release-0-3-0.md`

## Implementation notes
Aplicar em duas etapas: (1) documentacao/specs/playbook; (2) implementacao tecnica. Ao atualizar CLI help, priorizar mensagens curtas e acionaveis para agentes.

## Tests
Adicionar/ajustar testes apenas onde houver mudanca comportamental (ex.: logging parametrizado no `yoda_flow_next.py` e regra de `--dev`). Para itens puramente documentais, validacao por varredura manual.

## Risks and edge cases
- Mudancas de contrato de log podem divergir de parsers legados se nao forem alinhadas nas specs.
- Endurecimento de `--dev` pode quebrar fluxos antigos que dependam de fallback implicito.
- Movimentacao de `favicons` pode impactar scripts/caminhos se houver referencias hardcoded.

## Flow log
- 2026-03-07T11:31:39-03:00 issue_add created title=Ajustes finais de usabilidade e contrato CLI pre-release 0.3.0; priority=5
- 2026-03-07T11:31:56-03:00 Intake created aggregated pre-release issue covering log format, yoda_flow_next logging parameter, --help guidance, --dev contract, and favicons location.

- 2026-03-07T11:42:09-03:00 transition to-do->doing phase=study
- 2026-03-07T11:44:58-03:00 transition doing/study->doing/document
- 2026-03-07T11:45:05-03:00 Document decisions locked: --log-message in yoda_flow_next, favicons moved to /favicons, full review of 11 script helps, --dev contract unified except update.py.
- 2026-03-07T11:56:30-03:00 transition doing/document->doing/implement | Implement completed: document-first specs, script contracts, help guidance, dev resolution, and favicons relocation applied with tests.
- 2026-03-07T11:56:39-03:00 transition doing/implement->doing/evaluate | Evaluate started after implementation and full script test suite execution.
- 2026-03-07T11:56:48-03:00 Evaluate completed: ACs validated, result log filled, and regression tests passed.
- 2026-03-07T11:57:32-03:00 transition doing/evaluate->done | Issue closed after AC validation, result log completion, and 59 passing tests.

## Result log
feat(flow): consolidar ajustes finais de contrato CLI e empacotamento pre-0.3.0

A entrega da `yoda-0058` foi concluida em abordagem document-first. Foram atualizados specs/playbook para o novo contrato de Flow log sem prefixo redundante de issue, incluindo suporte ao parametro opcional `--log-message` no `yoda_flow_next.py`. Os 11 comandos de `yoda/scripts/*.py` receberam orientacao de agente no `--help`; o contrato de `--dev` foi unificado para exigir entrada explicita em comandos YODA (com excecao de `update.py`); e o utilitario de resolucao de slug deixou de usar fallback por `YODA_DEV`/prompt interativo. Tambem foi feita a movimentacao de `yoda/favicons` para `favicons/` na raiz, com ajuste de empacotamento e validacao de testes garantindo que assets de favicon nao entram no artefato.

- **GitHub Issue** :   #3

- **Issue**: `yoda-0058`

- **Path**: `yoda/project/issues/yoda-0058-ajustes-finais-de-usabilidade-e-contrato-cli-pre-release-0-3-0.md`