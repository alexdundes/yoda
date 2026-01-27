---
agent: Human
created_at: '2026-01-27T13:32:13-03:00'
depends_on: []
description: Clarificar se a validacao e um comando dedicado (validate.py) ou embutida
  em scripts que alteram metadados.
entrypoints: []
id: yoda-0034
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: clarificar-validacao-scripts
status: done
tags: []
title: Clarificar validacao vs comandos v1
updated_at: '2026-01-27T13:32:40-03:00'
---

# yoda-0034 - Clarificar validacao vs comandos v1

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
- Registrar que validacao e obrigatoria e embutida nos scripts que alteram metadados.

## Acceptance criteria
- [x] `project/specs/05-scripts-and-automation.md` e `project/specs/13-yoda-scripts-v1.md` descrevem a abordagem de validacao de forma consistente.

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
Validacao definida como obrigatoria e embutida em scripts que alteram metadados, com regras de exit code e escrita consistente.

docs(yoda): tornar validacao obrigatoria em scripts v1

Issue: `yoda-0034`
Path: `yoda/project/issues/yoda-0034-clarificar-validacao-scripts.md`