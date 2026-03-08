---
schema_version: '2.00'
status: done
depends_on:
- yoda-0038
title: Corrigir concorrencia no issue_add para criacoes simultaneas
description: 'Ao executar dois issue_add em paralelo, ambos podem receber o mesmo
  proximo ID (ex.: yoda-0031), gerando colisao de arquivos e corrupcao estrutural
  no TODO YAML. Corrigir a alocacao de ID e a escrita de artefatos para suportar concorrencia
  segura (locking/atomicidade/retry). Regra transversal deste backlog: primeiro atualizar
  a documentacao em project/specs/ e somente depois aplicar mudancas em yoda/.'
priority: 2
created_at: '2026-02-25T15:23:19-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0033 - Corrigir concorrencia no issue_add para criacoes simultaneas

## Summary
Corrigir a condicao de corrida no comando `issue_add.py` quando duas criacoes acontecem simultaneamente. O problema atual pode gerar mesmo ID para duas issues, sobrescrita de artefatos e inconsistencias no `TODO` YAML. A solucao deve garantir alocacao unica de ID e escrita segura dos arquivos relacionados.

## Context
Durante o Intake, ao disparar dois `issue_add` em paralelo, foi observado que ambos receberam o mesmo ID (`yoda-0031`), causando colisao entre arquivos e trecho invalido no `yoda/todos/TODO.yoda.yaml`. Isso compromete a confiabilidade do fluxo de backlog.

## Objective
Tornar `issue_add.py` seguro para concorrencia, impedindo IDs duplicados e garantindo integridade dos artefatos (TODO, issue markdown e log).

## Scope
- Atualizar specs em `project/specs/` para definir comportamento esperado sob execucao concorrente.
- Ajustar `yoda/scripts/issue_add.py` para alocacao de ID com sincronizacao/atomicidade.
- Garantir escrita segura de `TODO.<dev>.yaml`, issue markdown e log.
- Adicionar testes cobrindo cenario de duas criacoes simultaneas.

## Out of scope
- Refatoracao ampla de todos os scripts de TODO para concorrencia geral.
- Mudancas de arquitetura fora do fluxo de criacao de issue.
- Alteracoes nao relacionadas a integridade de ID e escrita atomica no `issue_add`.

## Requirements
- Ordem de execucao: atualizar `project/specs/` antes de `yoda/`.
- `issue_add.py` deve impedir emissao de ID duplicado sob concorrencia.
- Lock externo por arquivo (por `--dev`) deve serializar a alocacao/escrita para criacao de issue.
- Escrita de arquivos deve usar estrategia atomica (arquivo temporario + replace) para evitar estado parcial/corrompido.
- Em caso de disputa de lock, o comando deve aplicar retry com 3 tentativas e espera crescente entre tentativas.
- Em caso de falha apos retries, retornar erro explicito (sem rollback).

## Acceptance criteria
- [x] Existe especificacao em `project/specs/` cobrindo criacao concorrente de issues.
- [x] Execucao concorrente de duas chamadas `issue_add.py` resulta em IDs distintos.
- [x] `TODO.<dev>.yaml` permanece valido apos execucoes simultaneas.
- [x] Cada issue criada possui seu markdown e log corretos, sem sobrescrita cruzada.
- [x] Em disputa, `issue_add.py` aplica retry de lock em 3 tentativas com espera crescente.
- [x] Ao esgotar retries ou falhar durante escrita, o comando retorna erro explicito (sem rollback automatico).
- [x] Ha teste automatizado reproduzindo o cenario e validando a correcao.


## Entry points
- `project/specs/`
- `yoda/scripts/issue_add.py`
- `yoda/todos/TODO.yoda.yaml`

## Implementation notes
- Lock externo por `--dev` (arquivo `.lock` dedicado), sem necessidade de estrategia intra-dev adicional.
- A secao critica deve incluir leitura do estado mais recente, alocacao do proximo ID e escrita dos artefatos.
- Retry policy definida: 3 tentativas com espera crescente.
- Falhas devem ser explicitas e abortar sem rollback automatico.

## Tests
Adicionar teste de concorrencia para `issue_add.py` com duas execucoes paralelas, verificando IDs unicos e integridade dos arquivos gerados.

## Risks and edge cases
- Deadlock ou lock nao liberado em falha abrupta.
- Diferencas de comportamento de lock entre sistemas de arquivos.
- Regressao em fluxos sequenciais se o lock/retry for mal calibrado.

## Result log
Implementado controle de concorrencia em `issue_add.py` com lock externo por `--dev`, retry (3 tentativas com espera crescente), e escrita atomica por arquivo (tmp + replace). Atualizadas specs (docs-first) para formalizar o contrato e adicionados testes de concorrencia/contencao de lock.

fix(yoda): make issue_add concurrency-safe with per-dev lock and atomic writes
Issue: `yoda-0033`
Path: `yoda/project/issues/yoda-0033-corrigir-concorrencia-no-issue-add-para-criacoes-simultaneas.md`

## Flow log
- 2026-02-25T15:23:19-03:00 issue_add created | title: Corrigir concorrencia no issue_add para criacoes simultaneas | description: Ao executar dois issue_add em paralelo, ambos podem receber o mesmo proximo ID (ex.: yoda-0031), gerando colisao de arquivos e corrupcao estrutural no TODO YAML. Corrigir a alocacao de ID e a escrita de artefatos para suportar concorrencia segura (locking/atomicidade/retry). Regra transversal deste backlog: primeiro atualizar a documentacao em project/specs/ e somente depois aplicar mudancas em yoda/. | slug: corrigir-concorrencia-no-issue-add-para-criacoes-simultaneas | priority: 2 | tags: release-0.1.2, bug, concurrency, issue-add, docs-first | entrypoints: yoda/scripts/issue_add.py:code, yoda/todos/TODO.yoda.yaml:data, project/specs/:doc
- 2026-02-25T18:46:21-03:00 dependency update: depends_on ajustado para yoda-0038 por decisao de priorizacao do fluxo.
- 2026-02-25T18:46:21-03:00 todo_update | depends_on: [] -> yoda-0038
- 2026-02-26T14:24:41-03:00 todo_update | status: to-do -> doing
- 2026-02-26T14:29:57-03:00 Study decisions finalized\n- Retry policy: 3 attempts with increasing wait\n- Failure mode: explicit error, no rollback\n- Lock strategy: external lock file per --dev (atomicity scope by dev)
- 2026-02-26T14:34:36-03:00 evaluate completed\n- Docs-first specs updated for issue_add concurrency\n- Implemented per-dev lock + retry(3) + atomic writes\n- No rollback policy kept explicit\n- Tests: 39 passed
- 2026-02-26T14:34:40-03:00 todo_update | status: doing -> done
