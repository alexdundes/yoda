---
agent: Human
created_at: '2026-02-25T15:23:19-03:00'
depends_on:
- yoda-0038
description: 'Ao executar dois issue_add em paralelo, ambos podem receber o mesmo
  proximo ID (ex.: yoda-0031), gerando colisao de arquivos e corrupcao estrutural
  no TODO YAML. Corrigir a alocacao de ID e a escrita de artefatos para suportar concorrencia
  segura (locking/atomicidade/retry). Regra transversal deste backlog: primeiro atualizar
  a documentacao em project/specs/ e somente depois aplicar mudancas em yoda/.'
entrypoints:
- path: yoda/scripts/issue_add.py
  type: code
- path: yoda/todos/TODO.yoda.yaml
  type: data
- path: project/specs/
  type: doc
id: yoda-0033
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 2
schema_version: '1.0'
slug: corrigir-concorrencia-no-issue-add-para-criacoes-simultaneas
status: to-do
tags:
- release-0.1.2
- bug
- concurrency
- issue-add
- docs-first
title: Corrigir concorrencia no issue_add para criacoes simultaneas
updated_at: '2026-02-25T18:46:21-03:00'
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
- Escrita de arquivos deve evitar estado parcial/corrompido em falhas intermediarias.
- Em caso de disputa, o comando deve tentar novamente de forma controlada ou falhar com erro claro.

## Acceptance criteria
- [ ] Existe especificacao em `project/specs/` cobrindo criacao concorrente de issues.
- [ ] Execucao concorrente de duas chamadas `issue_add.py` resulta em IDs distintos.
- [ ] `TODO.<dev>.yaml` permanece valido apos execucoes simultaneas.
- [ ] Cada issue criada possui seu markdown e log corretos, sem sobrescrita cruzada.
- [ ] Ha teste automatizado reproduzindo o cenario e validando a correcao.

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
Preferir estrategia simples e robustas: lock por arquivo de TODO, escrita atomica com arquivo temporario + rename, e leitura de estado apos lock antes de definir proximo ID.

## Tests
Adicionar teste de concorrencia para `issue_add.py` com duas execucoes paralelas, verificando IDs unicos e integridade dos arquivos gerados.

## Risks and edge cases
- Deadlock ou lock nao liberado em falha abrupta.
- Diferencas de comportamento de lock entre sistemas de arquivos.
- Regressao em fluxos sequenciais se o lock/retry for mal calibrado.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->