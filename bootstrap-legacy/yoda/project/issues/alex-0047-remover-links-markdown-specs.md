---
schema_version: "1.0"
id: alex-0047
title: Remover links Markdown em project/specs
slug: remover-links-markdown-specs
description: Substituir links Markdown por inline code em project/specs para reduzir ruido para agentes.
status: done
priority: 4
lightweight: false
agent: Codex
depends_on: []
pending_reason: ""
created_at: "2026-01-26T21:37:11-03:00"
updated_at: "2026-01-26T21:37:50-03:00"
entrypoints:
  - path: project/specs/
    type: doc
tags: []
origin:
  system: ""
  external_id: ""
  requester: ""
---

# alex-0047 - Remover links Markdown em project/specs

## Summary
Substituir links Markdown por inline code no project/specs para reduzir distrações e melhorar a interpretacao por agentes.

## Context
Links em Markdown podem levar agentes a interpretar caminhos como referencias navegaveis e perder o foco. Preferimos texto em inline code.

## Objective
Remover a sintaxe de links Markdown e manter apenas o texto como inline code.

## Scope
- Atualizar arquivos em project/specs/ para remover links Markdown inline.

## Out of scope
- Alterar o conteudo semantico das specs.

## Requirements
- Substituir `[texto](url)` por `texto` em inline code.

## Acceptance criteria
- [ ] project/specs nao contem links Markdown inline.

## Dependencies
None.

## Entry points
- path: project/specs/
  type: doc

## Implementation notes
- Preservar texto do link, removendo apenas a sintaxe de link.

## Tests
Not applicable.

## Risks and edge cases
- Referencias estilo `[nome][id]` nao sao links inline e podem permanecer se nao forem alvo.

## Result log
Links Markdown inline removidos em project/specs e substituidos por inline code.

docs: remover links markdown em project/specs

Issue: `alex-0047`
Path: `yoda/project/issues/alex-0047-remover-links-markdown-specs.md`
