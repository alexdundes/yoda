---
schema_version: "1.0"
id: alex-0040
title: Clarificar texto sobre corpo livre vs front matter
slug: clarificar-texto-corpo-livre-front-matter
description: Atualizar 04-todo-dev-yaml-issues.md para explicitar que o corpo e livre e o metadata fica no YAML front matter.
status: done
priority: 6
lightweight: false
agent: Codex
depends_on: []
pending_reason: ""
created_at: "2026-01-26T20:57:16-03:00"
updated_at: "2026-01-26T20:57:40-03:00"
entrypoints:
  - path: project/specs/04-todo-dev-yaml-issues.md
    type: doc
tags: []
origin:
  system: ""
  external_id: ""
  requester: ""
---

# alex-0040 - Clarificar texto sobre corpo livre vs front matter

## Summary
Ajustar o texto inicial do 04-todo-dev-yaml-issues.md para remover a ambiguidade entre “corpo livre” e a obrigatoriedade de YAML front matter. A frase deve indicar que o corpo e livre, enquanto o metadata fica no front matter.

## Context
No trecho “Preferred direction” o texto afirma que a issue contem apenas texto livre, mas mais abaixo exige YAML front matter obrigatorio. Isso gera conflito de entendimento.

## Objective
Clarificar a frase para explicitar que apenas o corpo e livre; o metadata continua no YAML front matter.

## Scope
- Atualizar a frase no bloco “Preferred direction” conforme a dica do requester.

## Out of scope
- Alterar outras regras de metadata ou schema.
- Mudar a estrutura do documento.

## Requirements
- Manter a intencao original de corpo livre.
- Indicar explicitamente o YAML front matter como local do metadata.

## Acceptance criteria
- [ ] A frase atualiza para: “Issue files contain only free text in the body (metadata goes in YAML front matter).”
- [ ] Nao ha ambiguidade entre corpo livre e front matter obrigatorio.

## Dependencies
None.

## Entry points
- path: project/specs/04-todo-dev-yaml-issues.md
  type: doc

## Implementation notes
- Atualizar apenas a linha correspondente em “Preferred direction”.

## Tests
Not applicable.

## Risks and edge cases
- Nenhum; mudanca textual simples.

## Result log
Frase de “Preferred direction” ajustada para explicitar corpo livre e metadata no YAML front matter, eliminando a ambiguidade.

docs: clarificar corpo livre vs YAML front matter

Issue: `alex-0040`
Path: `yoda/project/issues/alex-0040-clarificar-texto-corpo-livre-front-matter.md`
