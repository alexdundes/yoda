---
schema_version: '1.02'
id: yoda-0049
status: done
depends_on:
- yoda-0048
title: Camada de leitura deterministica baseada apenas em issues markdown
description: Implementar leitura e indexacao de yoda/project/issues/*.md para montar
  estado em memoria sem dependencia de TODO.<dev>.yaml.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:41-03:00'
updated_at: '2026-03-06T16:54:25-03:00'
---

# yoda-0049 - Camada de leitura deterministica baseada apenas em issues markdown

## Summary
Construir a camada de leitura/indexacao que opera apenas sobre issues markdown como fonte de estado do fluxo. A entrega desta issue define leitura deterministica por `--dev`, validacao basica, normalizacao em memoria e contrato de saida reutilizavel para os proximos scripts.

## Context
A base atual depende do TODO YAML como indice principal. Para 0.3.0, os scripts devem operar diretamente a partir das issues markdown.

## Objective
Entregar API/utilitarios internos que leem front matter e corpo das issues, aplicam validacoes deterministicas e expoem estado consolidado em memoria em formato unico.

## Scope
- Ler `yoda/project/issues/*.md` com parse robusto de front matter.
- Filtrar sempre por `--dev` (prefixo do filename `<dev>-<NNNN>-<slug>.md`).
- Normalizar campos obrigatorios e opcionais segundo spec 0.3.0.
- Implementar ordenacao deterministica igual a logica atual dos scripts Python existentes.
- Emitir erros claros para arquivos invalidos.
- Definir contrato de saida em memoria para reuso por scripts seguintes.

## Out of scope
- Criacao do comando `yoda_flow_next.py`.
- Migracao automatica dos arquivos legados.
- Reescrita de playbook.

## Requirements
- Resultado da leitura deve ser estavel entre execucoes identicas.
- Regras de elegibilidade devem respeitar status, fase e dependencias.
- Comportamento de erro deve ser `fail-fast`.
- ID deve ser sempre derivado do filename; campo `id` legado no front matter deve ser ignorado.
- Se `## Flow log` nao existir no arquivo, incluir a secao no fim do markdown.
- Se `phase` existir com status diferente de `doing`, ignorar o valor sem erro.
- Dependencia inexistente deve ser tratada como `done`; dependencia existente deve ter status validado.
- Erros devem incluir contexto: `path`, `id` derivado, campo/regra violada.
- Contrato de saida em memoria por issue:
  - `id` (derivado do filename)
  - `dev`
  - `slug`
  - `path`
  - `status`
  - `phase` (ou `None`)
  - `depends_on` (lista normalizada)
  - `title`
  - `description`
  - `priority`
  - `extern_issue_file`
  - `created_at`
  - `updated_at`
  - `flow_log_exists` (bool)
- Contrato de saida global:
  - `issues` (lista ordenada)
  - `by_id` (mapa `id -> issue`)
  - `errors` (no `fail-fast`, retorna apenas o primeiro erro)

## Acceptance criteria
- [x] Leitor lista issues e metadados sem uso de `TODO.<dev>.yaml`.
- [x] Filtro por `--dev` e aplicado sempre na selecao de arquivos.
- [x] Ordenacao/elegibilidade seguem exatamente a logica atual dos scripts.
- [x] Regime `fail-fast` esta definido e coberto.
- [x] ID e sempre derivado do filename e `id` legado e ignorado.
- [x] Quando ausente, secao `## Flow log` e adicionada ao fim do arquivo.
- [x] `phase` fora de `doing` e ignorado sem erro.
- [x] Dependencia inexistente e tratada como `done`; existente valida status.
- [x] Contrato de saida em memoria (por issue e global) esta definido.
- [x] Erros de parse/schema sao reportados com contexto util (`path`, `id`, campo/regra).

## Dependencies
Depende de `yoda-0048`.

## Entry points
- path: yoda/scripts/lib
  type: code
- path: yoda/project/issues
  type: data
- path: yoda/scripts/tests
  type: code

## Implementation notes
Criar unidade reutilizavel para evitar duplicacao de parse em comandos futuros. Esta issue deve permanecer limitada a leitura/indexacao/validacao, sem implementar transicoes de fluxo.

## Tests
Adicionar testes com fixtures para:
- filtro por `--dev`;
- parse valido e invalido em `fail-fast`;
- ID derivado por filename com `id` legado ignorado;
- ausencia/presenca de `## Flow log`;
- `phase` fora de `doing` sendo ignorado;
- dependencias inexistentes tratadas como `done`;
- ordenacao igual a logica atual.

## Risks and edge cases
- Arquivos parcialmente preenchidos podem quebrar parse.
- Dependencias ciclicas precisam ser detectadas de forma previsivel.
- Divergencia da ordenacao em relacao aos scripts atuais pode quebrar determinismo esperado.
- Inclusao automatica de `## Flow log` deve evitar alteracoes indevidas fora da secao alvo.

## Result log
feat(lib): adicionar camada de leitura deterministica de issues markdown

Foi implementada a camada `issue_index` em `yoda/scripts/lib/issue_index.py` para carregar e indexar issues `.md` por `--dev`, com `fail-fast`, ID derivado exclusivamente do filename, ignorando `id` legado, normalizacao de metadados em memoria, e contrato de saida reutilizavel (`issues`, `by_id`, `errors`). O comportamento inclui insercao de `## Flow log` quando ausente, ignorar `phase` fora de `doing`, tratar dependencia inexistente como `done`, validar dependencia existente por status, e calcular `selectable/blocked_by` com ordenacao deterministica (prioridade + ordem de origem). Tambem foram adicionados testes dedicados em `yoda/scripts/tests/test_issue_index.py`, com validacao de todos os cenarios acordados, passando com `6 passed`.

- **GitHub Issue** :   #3

- **Issue**: `yoda-0049`

- **Path**: `yoda/project/issues/yoda-0049-camada-de-leitura-deterministica-baseada-apenas-em-issues-markdown.md`