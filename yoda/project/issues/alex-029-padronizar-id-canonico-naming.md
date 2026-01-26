---
schema_version: "1.0"
id: alex-029
title: Padronizar id canonico e naming de arquivos
slug: padronizar-id-canonico-naming
description: Alinhar id canonico com naming de issues e logs nas specs.
status: doing
priority: 7
lightweight: false
agent: Human
depends_on: []
pending_reason: ""
created_at: "2026-01-26T11:16:29-03:00"
updated_at: "2026-01-26T11:19:17-03:00"
entrypoints: []
tags: [specs, naming]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-029 - Padronizar id canonico e naming de arquivos

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

## Out of scope
- Alterar arquivos fora de `project/specs`.
- Renomear arquivos reais no repositorio.

## Requirements
- Padronizar o id canonico e o formato de naming nas specs.
- Atualizar exemplos de paths e outputs esperados dos scripts.
- Manter terminologia consistente com `project/specs/00-conventions.md`.

## Acceptance criteria
- [ ] `project/specs/04-todo-dev-yaml-issues.md` reflete o id canonico e naming correto.
- [ ] `project/specs/12-yoda-structure.md` reflete o naming correto nas estruturas e exemplos.
- [ ] `project/specs/05-scripts-and-automation.md` usa o formato correto para logs.
- [ ] `project/specs/13-yoda-scripts-v1.md` descreve outputs com id canonico e naming correto.

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

## Result log
