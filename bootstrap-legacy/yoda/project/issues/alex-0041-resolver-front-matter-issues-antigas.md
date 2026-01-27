---
schema_version: "1.0"
id: alex-0041
title: Resolver inconsistencias de front matter nas issues antigas
slug: resolver-front-matter-issues-antigas
description: Documentar excecao de bootstrap para issues antigas sem front matter em 15-bootstrap.md.
status: done
priority: 6
lightweight: false
agent: Codex
depends_on: []
pending_reason: ""
created_at: "2026-01-26T21:00:06-03:00"
updated_at: "2026-01-26T21:00:39-03:00"
entrypoints:
  - path: project/specs/15-bootstrap.md
    type: doc
  - path: yoda/project/issues/
    type: doc
tags: []
origin:
  system: ""
  external_id: ""
  requester: ""
---

# alex-0041 - Resolver inconsistencias de front matter nas issues antigas

## Summary
Documentar no bootstrap que issues antigas podem nao ter YAML front matter, enquanto novas issues devem seguir o padrao atual. Isso elimina ambiguidade sem backfill.

## Context
As specs exigem front matter obrigatorio, mas as issues alex-0001..alex-0026 nao possuem YAML front matter. A partir de alex-0027, o padrao foi adotado. Sem uma excecao documentada, agentes podem assumir que front matter sempre existe.

## Objective
Registrar a excecao do bootstrap no 15-bootstrap.md para refletir a realidade historica e orientar agentes.

## Scope
- Atualizar project/specs/15-bootstrap.md com a excecao de bootstrap para issues antigas.

## Out of scope
- Backfill de front matter em issues antigas.
- Alterar regras de front matter fora do contexto de bootstrap.

## Requirements
- Declarar que, no bootstrap, issues antigas podem nao ter front matter.
- Reafirmar que novas issues devem incluir front matter.

## Acceptance criteria
- [ ] 15-bootstrap.md documenta a excecao de issues antigas sem front matter.
- [ ] 15-bootstrap.md explicita que novas issues devem seguir o padrao com front matter.

## Dependencies
None.

## Entry points
- path: project/specs/15-bootstrap.md
  type: doc

## Implementation notes
- Adicionar um bullet ou paragrafo curto na secao de bootstrap.

## Tests
Not applicable.

## Risks and edge cases
- Nenhum; alteracao documental.

## Result log
Documentada a excecao de bootstrap para issues antigas sem front matter e reafirmado que novas issues devem incluir front matter.

docs: documentar excecao de front matter no bootstrap

Issue: `alex-0041`
Path: `yoda/project/issues/alex-0041-resolver-front-matter-issues-antigas.md`
