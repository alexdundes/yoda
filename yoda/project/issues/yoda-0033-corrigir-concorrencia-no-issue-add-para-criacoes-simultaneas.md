---
created_at: '2026-02-25T15:23:19-03:00'
depends_on:
- yoda-0038
description: 'Ao executar dois issue_add em paralelo, ambos podem receber o mesmo
  proximo ID (ex.: yoda-0031), gerando colisao de arquivos e corrupcao estrutural
  no TODO YAML. Corrigir a alocacao de ID e a escrita de artefatos para suportar concorrencia
  segura (locking/atomicidade/retry). Regra transversal deste backlog: primeiro atualizar
  a documentacao em project/specs/ e somente depois aplicar mudancas em yoda/.'
id: yoda-0033
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 2
schema_version: '1.01'
slug: corrigir-concorrencia-no-issue-add-para-criacoes-simultaneas
status: done
title: Corrigir concorrencia no issue_add para criacoes simultaneas
updated_at: '2026-02-26T14:34:39-03:00'
---

# yoda-0033 - Corrigir concorrencia no issue_add para criacoes simultaneas
<!-- AGENT: Replace yoda-0033 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Corrigir concorrencia no issue_add para criacoes simultaneas with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

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

## Dependencies
None.

## Entry points
- path: project/specs/
  type: doc
- path: yoda/scripts/issue_add.py
  type: code
- path: yoda/todos/TODO.yoda.yaml
  type: data

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