---
schema_version: "1.0"
id: alex-0033
title: Revisar regra de timezone em conventions
slug: revisar-timezone-conventions
description: Ajustar MUST/SHOULD para timezone explicita e UTC/configuravel.
status: to-do
priority: 5
lightweight: false
agent: Human
depends_on: []
pending_reason: ""
created_at: "2026-01-26T11:16:29-03:00"
updated_at: "2026-01-26T11:16:29-03:00"
entrypoints: []
tags: [specs, conventions]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-0033 - Revisar regra de timezone em conventions

## Summary
Revisar a regra de timezone em `project/specs/00-conventions.md` para exigir timezone explicita e recomendar UTC ou configuracao do projeto.

## Context
A regra atual exige America/Sao_Paulo, o que pode limitar o framework futuro e forcar conversoes desnecessarias.

## Objective
Atualizar a regra para MUST de timezone explicita e SHOULD de UTC ou timezone configurada do projeto.

## Scope
- Ajustar a regra em `project/specs/00-conventions.md`.

## Out of scope
- Alterar timestamps existentes no repositorio.
- Criar arquivo de configuracao de timezone.

## Requirements
- Manter MUST para timezone explicita.
- Trocar o MUST de America/Sao_Paulo por SHOULD de UTC ou timezone do projeto.

## Acceptance criteria
- [ ] `project/specs/00-conventions.md` reflete a nova regra de timezone.

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
