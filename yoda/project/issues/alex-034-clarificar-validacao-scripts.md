---
schema_version: "1.0"
id: alex-034
title: Clarificar validacao vs comandos v1
slug: clarificar-validacao-scripts
description: Explicitar se validacao e embutida ou via validate.py.
status: to-do
priority: 5
lightweight: false
agent: Human
depends_on: []
pending_reason: ""
created_at: "2026-01-26T11:16:29-03:00"
updated_at: "2026-01-26T11:16:29-03:00"
entrypoints: []
tags: [specs, scripts]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-034 - Clarificar validacao vs comandos v1

## Summary
Clarificar se a validacao e um comando dedicado (validate.py) ou embutida em scripts que alteram metadados.

## Context
`project/specs/05-scripts-and-automation.md` descreve validacao e checks, mas `project/specs/13-yoda-scripts-v1.md` nao define se existe um comando especifico.

## Objective
Definir e documentar a abordagem oficial de validacao na v1.

## Scope
- Ajustar `project/specs/05-scripts-and-automation.md`.
- Ajustar `project/specs/13-yoda-scripts-v1.md`.

## Out of scope
- Implementar scripts.
- Alterar outros documentos fora de `project/specs`.

## Requirements
- Declarar explicitamente se ha `validate.py` na v1.
- Se nao houver, registrar que validacao e embutida nos scripts que alteram metadados.

## Acceptance criteria
- [ ] `project/specs/05-scripts-and-automation.md` e `project/specs/13-yoda-scripts-v1.md` descrevem a abordagem de validacao de forma consistente.

## Dependencies
None

## Entry points
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: project/specs/13-yoda-scripts-v1.md
  type: doc

## Implementation notes
- Manter consistencia com o contrato de CLI e exit codes.

## Tests
Not applicable.

## Risks and edge cases
- Se ficar ambiguo, agents podem implementar validacao duplicada ou ausente.

## Result log
