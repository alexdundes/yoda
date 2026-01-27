---
agent: Human
created_at: '2026-01-27T13:32:13-03:00'
depends_on: []
description: Revisar a regra de timezone em `project/specs/00-conventions.md` para
  exigir timezone explicita, recomendar UTC como default e permitir timezone configurada
  no TODO, com padrao compatível com Python.
entrypoints: []
id: yoda-0033
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: revisar-timezone-conventions
status: done
tags: []
title: Revisar regra de timezone em conventions
updated_at: '2026-01-27T13:32:40-03:00'
---

# yoda-0033 - Revisar regra de timezone em conventions

## Summary
Revisar a regra de timezone em `project/specs/00-conventions.md` para exigir timezone explicita, recomendar UTC como default e permitir timezone configurada no TODO, com padrao compatível com Python.

## Context
A regra atual exige America/Sao_Paulo, o que pode limitar o framework futuro e forcar conversoes desnecessarias.

## Objective
Atualizar a regra para MUST de timezone explicita e SHOULD de UTC, com timezone configurada no TODO como opcional.

## Scope
- Ajustar a regra em `project/specs/00-conventions.md`.
- Atualizar as specs de metadata para incluir campo(s) obrigatorio(s) de timezone no TODO.

## Out of scope
- Alterar timestamps existentes no repositorio.
- Criar arquivo de configuracao separado para timezone.

## Requirements
- Manter MUST para timezone explicita.
- Definir UTC como default recomendado.
- Permitir timezone configurada no TODO (campo(s) obrigatorio(s) no metadata).
- Definir padrao de timezone compatível com Python.

## Acceptance criteria
- [x] `project/specs/00-conventions.md` reflete a nova regra de timezone.
- [x] Specs de metadata incluem campo(s) obrigatorio(s) de timezone no TODO.

## Dependencies
None

## Entry points
- path: project/specs/00-conventions.md
  type: doc

## Implementation notes
- Preservar o uso de linguagem normativa (MUST/SHOULD).

## Tests
Not applicable.

## Risks and edge cases
- Ambiguidade se a especificacao nao indicar onde a timezone do projeto e definida.

## Result log
Regra de timezone revisada com UTC como default e campo obrigatorio `timezone` no TODO. Schema e validacao atualizados para exigir valor compatível com Python `zoneinfo`.

docs(yoda): revisar regra de timezone e metadata do TODO

Issue: `yoda-0033`
Path: `yoda/project/issues/yoda-0033-revisar-timezone-conventions.md`