---
agent: Human
created_at: '2026-01-27T13:32:14-03:00'
depends_on: []
description: Decidir como tratar bootstrap dentro de `project/specs` para manter as
  specs normativas e evitar ruido de meta-implementacao.
entrypoints: []
id: yoda-0035
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: revisar-bootstrap-specs
status: done
tags: []
title: Revisar bootstrap e meta-implementation nas specs
updated_at: '2026-01-27T13:32:40-03:00'
---

# yoda-0035 - Revisar bootstrap e meta-implementation nas specs

## Summary
Decidir como tratar bootstrap dentro de `project/specs` para manter as specs normativas e evitar ruido de meta-implementacao.

## Context
Alguns trechos nas specs mencionam bootstrap e a meta-implementacao, o que pode conflitar com a ideia de specs normativas do framework futuro.

## Objective
Definir a abordagem (appendix informativa ou mover bootstrap para fora das specs) e ajustar os arquivos relevantes.

## Scope
- Revisar `project/specs/12-yoda-structure.md`.
- Revisar `project/specs/15-bootstrap.md`.
- Documentar a decisao escolhida nas specs.

## Out of scope
- Alterar README fora das specs.
- Implementar scripts ou migracoes.

## Requirements
- Escolher entre: (A) appendix informativa ou (B) mover bootstrap para fora de `project/specs`.
- Decisao: manter bootstrap como appendix informativa (nao-normativa) dentro de `project/specs`.
- Atualizar os textos para refletir a decisao escolhida e marcar bootstrap como informativo.

## Acceptance criteria
- [x] `project/specs/12-yoda-structure.md` e `project/specs/15-bootstrap.md` refletem a decisao escolhida.
- [x] A distincao entre specs normativas e conteudo de bootstrap fica explicita.

## Dependencies
None

## Entry points
- path: project/specs/12-yoda-structure.md
  type: doc
- path: project/specs/15-bootstrap.md
  type: doc

## Implementation notes
- Evitar linguagem que indique remocao futura sem uma decisao formal.

## Tests
Not applicable.

## Risks and edge cases
- Decisao pode impactar documentacao existente se nao for aplicada de forma consistente.

## Result log
Bootstrap marcado como appendix informativa (nao-normativa) nas specs, com referencia cruzada na estrutura minima.

docs(yoda): marcar bootstrap como appendix informativa

Issue: `yoda-0035`
Path: `yoda/project/issues/yoda-0035-revisar-bootstrap-specs.md`