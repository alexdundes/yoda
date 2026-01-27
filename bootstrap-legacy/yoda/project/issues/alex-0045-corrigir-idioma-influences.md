---
schema_version: "1.0"
id: alex-0045
title: Corrigir trechos em portugues nos influences
slug: corrigir-idioma-influences
description: Substituir trechos em portugues por ingles nos influences, alinhando com a politica de idioma.
status: done
priority: 4
lightweight: false
agent: Codex
depends_on: []
pending_reason: ""
created_at: "2026-01-26T21:25:16-03:00"
updated_at: "2026-01-26T21:25:57-03:00"
entrypoints:
  - path: project/specs/influences/01-documentation-driven-development-docdd.md
    type: doc
  - path: project/specs/influences/03-docs-as-code.md
    type: doc
  - path: project/specs/influences/04-design-first-contract-first-apis.md
    type: doc
tags: []
origin:
  system: ""
  external_id: ""
  requester: ""
---

# alex-0045 - Corrigir trechos em portugues nos influences

## Summary
Substituir frases em portugues nos arquivos de influences por equivalentes em ingles para manter a politica de idioma das specs.

## Context
project/specs define que o conteudo deve estar em ingles, mas alguns trechos em influences ainda estao em portugues.

## Objective
Alinhar as frases com a politica de idioma usando equivalentes em ingles.

## Scope
- Atualizar frases em portugues nos arquivos de influences listados.

## Out of scope
- Alterar o sentido das referencias ou requisitos.

## Requirements
- Trocar "quando houver fluxo PR/CI" por "when a PR/CI workflow exists".
- Trocar "v2+ / quando CI existir" por "v2+ / when CI exists".

## Acceptance criteria
- [ ] Nenhum dos trechos citados permanece em portugues.
- [ ] As frases mantem o sentido original em ingles.

## Dependencies
None.

## Entry points
- path: project/specs/influences/01-documentation-driven-development-docdd.md
  type: doc
- path: project/specs/influences/03-docs-as-code.md
  type: doc
- path: project/specs/influences/04-design-first-contract-first-apis.md
  type: doc

## Implementation notes
- Substituicoes textuais diretas.

## Tests
Not applicable.

## Risks and edge cases
- Nenhum; apenas linguagem.

## Result log
Trechos em portugues nos influences substituidos por equivalentes em ingles, alinhando com a politica de idioma das specs.

docs: corrigir idioma em influences

Issue: `alex-0045`
Path: `yoda/project/issues/alex-0045-corrigir-idioma-influences.md`
