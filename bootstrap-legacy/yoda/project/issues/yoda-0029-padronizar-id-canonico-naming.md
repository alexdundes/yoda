---
agent: Human
created_at: '2026-01-27T13:32:13-03:00'
depends_on: []
description: Padronizar o uso do id canonico (dev-####) e alinhar o naming de issues
  e logs em todas as specs relevantes.
entrypoints: []
id: yoda-0029
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 7
schema_version: '1.0'
slug: padronizar-id-canonico-naming
status: done
tags: []
title: Padronizar id canonico e naming de arquivos
updated_at: '2026-01-27T13:32:39-03:00'
---

# yoda-0029 - Padronizar id canonico e naming de arquivos

## Summary
Padronizar o uso do id canonico (dev-####) e alinhar o naming de issues e logs em todas as specs relevantes.

## Context
As specs ainda alternam entre o padrao dev-id-slug.md e o id canonico (dev-####), gerando ambiguidade e duplicacao do dev no nome do arquivo.

## Objective
Definir claramente o id canonico e o formato de arquivos de issue e log, e atualizar referencias nas specs.

## Scope
- Definir id canonico como `<dev>-<NNNN>`.
- Definir filenames como `<id>-<slug>.md` e `<id>-<slug>.yaml` para logs.
- Atualizar exemplos e textos nas specs afetadas.
- Renomear arquivos existentes no repositorio para alinhar com o naming padronizado.
- Atualizar referencias ao naming em documentacao afetada fora das specs principais.

## Out of scope
- Alterar arquivos fora de `project/specs`, exceto renames e atualizacoes de referencia ao naming.

## Requirements
- Padronizar o id canonico e o formato de naming nas specs.
- Atualizar exemplos de paths e outputs esperados dos scripts.
- Manter terminologia consistente com `project/specs/00-conventions.md`.
- Renomear arquivos atuais (issues e logs) para o formato `<id>-<slug>.*`.

## Acceptance criteria
- [x] `project/specs/04-todo-dev-yaml-issues.md` reflete o id canonico e naming correto.
- [x] `project/specs/12-yoda-structure.md` reflete o naming correto nas estruturas e exemplos.
- [x] `project/specs/05-scripts-and-automation.md` usa o formato correto para logs.
- [x] `project/specs/13-yoda-scripts-v1.md` descreve outputs com id canonico e naming correto.
- [x] `project/specs/06-agent-playbook.md` e `project/specs/15-bootstrap.md` usam o naming correto para logs.
- [x] `README.md` usa o naming correto para issues e logs.
- [x] Issues e logs existentes foram renomeados para o formato `<id>-<slug>.*`.

## Dependencies
None

## Entry points
- path: project/specs/04-todo-dev-yaml-issues.md
  type: doc
- path: project/specs/12-yoda-structure.md
  type: doc
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: project/specs/13-yoda-scripts-v1.md
  type: doc

## Implementation notes
- Use o id canonico como base do filename, evitando repeticao do dev no nome.

## Tests
Not applicable.

## Risks and edge cases
- Mudancas de naming podem conflitar com exemplos antigos se nao forem atualizados de forma consistente.
- Renames exigem atualizar referencias em docs e logs para evitar caminhos quebrados.

## Result log
Specs, README e templates alinhados ao naming `<id>-<slug>`, com ids canonicos de 4 digitos. Arquivos de issues e logs renomeados para refletir o id canonico.

docs(yoda): padronizar id canonico e naming de issues/logs

Issue: `yoda-0029`
Path: `yoda/project/issues/yoda-0029-padronizar-id-canonico-naming.md`