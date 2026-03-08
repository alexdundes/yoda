---
schema_version: '2.00'
status: done
title: Corrigir yoda_flow_next --dry-run sem mutacao de arquivos
description: 'Garantir que yoda_flow_next.py respeite --dry-run de forma estrita:
  sem alterar front matter e sem escrever em Flow log, inclusive em caminhos bloqueados
  (no selectable/dependency/pending).'
priority: 5
created_at: '2026-03-07T20:36:29-03:00'
updated_at: '2026-03-07T20:50:25-03:00'
---

# yoda-0059 - Corrigir yoda_flow_next --dry-run sem mutacao de arquivos

## Summary
`yoda_flow_next.py` expõe `--dry-run`, mas no estado atual ainda grava front matter e `Flow log`.
Isso viola o contrato esperado de simulacao e pode alterar estado de issues por engano.
Esta issue corrige o comportamento para dry-run estrito (zero escrita) e adiciona testes de regressao.

## Context
Foi validado por inspeccao de codigo que o fluxo atual chama `_apply_transition` e `_append_log` mesmo quando `--dry-run` esta ativo.
O problema tambem aparece no caminho de bloqueio (`pending`/`dependency`) porque o comando grava log de bloqueio.
Sem esta correcao, o operador nao pode confiar no `--dry-run` para validacao segura antes da execucao real.

## Objective
Garantir que `yoda_flow_next.py --dry-run` simule o proximo passo de forma deterministica sem alterar arquivos de issue em nenhum caminho de execucao.

## Scope
- Ajustar `yoda_flow_next.py` para respeitar `args.dry_run` em transicoes e em caminhos bloqueados.
- Evitar qualquer escrita em front matter quando `--dry-run` estiver ativo.
- Evitar qualquer append em `## Flow log` quando `--dry-run` estiver ativo.
- Incluir no payload de saida sinalizacao explicita de simulacao quando aplicavel.
- Adicionar testes automatizados cobrindo os cenarios de dry-run.

## Out of scope
- Redesenho de runbook, mensagens de fase ou heuristica de selecao de issue.
- Mudancas de contrato para execucao real sem `--dry-run`.
- Migracao de historico antigo de logs.

## Requirements
- `--dry-run` nao pode modificar `status`, `phase` ou `updated_at` em arquivos de issue.
- `--dry-run` nao pode criar ou alterar entradas em `## Flow log`, inclusive no payload bloqueado.
- A saida deve continuar retornando proximo passo/runbook esperado para tomada de decisao humana.
- Devem existir testes de regressao para os caminhos: selecionavel, dependency blocked e only pending.
- Em `--dry-run`, `log_timestamp` deve ser apenas simulado (sem escrita em arquivo) para manter compatibilidade de payload.
- Em bloqueio com `--dry-run`, o comando deve manter `exit code` de bloqueio (`3`) sem qualquer mutacao de arquivo.

## Acceptance criteria
- [x] Executar `yoda_flow_next.py --dev <slug> --dry-run` nao altera o conteudo do arquivo da issue alvo.
- [x] Em cenario bloqueado, `--dry-run` nao adiciona linha em `## Flow log` da issue usada no payload.
- [x] Execucao sem `--dry-run` continua mutando estado/log normalmente.
- [x] Suite de testes de `yoda/scripts/tests` cobre os novos comportamentos de dry-run.
- [x] Em `--dry-run`, payload continua informando `status/phase/next_step` simulados sem escrita em disco.
- [x] Em bloqueio com `--dry-run`, retorno permanece bloqueado (`exit code 3`) e sem escrita em `Flow log`.

## Entry points
- `yoda/scripts/yoda_flow_next.py`
- `yoda/scripts/lib/flow_log.py`
- `yoda/scripts/lib/front_matter.py`
- `yoda/scripts/tests`
- `yoda/project/issues/yoda-0059-corrigir-yoda-flow-next-dry-run-sem-mutacao-de-arquivos.md`

## Implementation notes
Preferir ramo explicito para simulacao (sem funcoes de escrita) em vez de condicoes espalhadas para reduzir risco de regressao.
Manter saida compativel com consumidores atuais (CLI/JSON), adicionando campos novos apenas se forem opcionais.
Decisoes aprovadas no Study:
- `log_timestamp` em dry-run deve ser simulado sem escrita.
- payload de dry-run deve manter `status/phase/next_step` simulados.
- caminhos bloqueados em dry-run mantem `exit code 3`, sem escrita.

## Tests
Adicionar testes unitarios/integracao no pacote `yoda/scripts/tests` que comparem hash/conteudo do arquivo antes/depois de `--dry-run`.
Cobrir tambem o cenario controle sem `--dry-run` para confirmar que a mutacao real continua funcionando.

## Risks and edge cases
- Implementacao parcial que bloqueia transicao, mas ainda grava logs em caminhos alternativos.
- Divergencia entre output em `md` e `json` no modo simulacao.
- Falso positivo de teste se fixture de issue nao contiver secao `## Flow log` valida.

## Result log
fix(flow): respeitar --dry-run no yoda_flow_next sem mutacao de arquivos

Foi implementada separacao explicita entre transicao real e simulacao no `yoda_flow_next.py`. Com `--dry-run`, o comando agora calcula o proximo estado de forma deterministica e retorna payload simulado (`status/phase/next_step` e `log_timestamp`) sem escrever front matter nem adicionar linhas em `## Flow log`. Tambem foi removida escrita de logs nos caminhos bloqueados quando `--dry-run` esta ativo, mantendo retorno bloqueado com `exit code 3`.

Foram adicionados testes de regressao em `yoda/scripts/tests/test_yoda_flow_next.py` para cobrir: (1) cenario selecionavel sem mutacao de arquivo em dry-run, (2) cenario bloqueado sem escrita em log e com retorno bloqueado em dry-run, e (3) preservacao do comportamento normal sem dry-run. Validacao executada com sucesso em `test_yoda_flow_next.py` (8 passed) e na suite completa `yoda/scripts/tests` (57 passed).

- **Issue**: `yoda-0059`

- **Path**: `yoda/project/issues/yoda-0059-corrigir-yoda-flow-next-dry-run-sem-mutacao-de-arquivos.md`

## Flow log
- 2026-03-07T20:36:29-03:00 issue_add created title=Corrigir yoda_flow_next --dry-run sem mutacao de arquivos; priority=5
- 2026-03-07T20:41:56-03:00 transition to-do->doing/study
- 2026-03-07T20:44:17-03:00 transition doing/study->doing/document | Study approved: dry-run simulado sem escrita; payload simulado mantido; bloqueio preserva exit 3 sem escrita
- 2026-03-07T20:44:45-03:00 transition doing/document->doing/implement | Document approved: implementar dry-run estrito sem escrita com payload simulado e bloqueio exit 3
- 2026-03-07T20:49:33-03:00 transition doing/implement->doing/evaluate | Implement concluido: dry-run sem escrita, simulacao de transicao, e testes de regressao adicionados
- 2026-03-07T20:50:25-03:00 transition doing/evaluate->done | Evaluate aprovado: ACs validados e Result log concluido
