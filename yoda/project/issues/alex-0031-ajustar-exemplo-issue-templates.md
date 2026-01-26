---
schema_version: "1.0"
id: alex-0031
title: Ajustar exemplos de issue templates para id canonico
slug: ajustar-exemplo-issue-templates
description: Atualizar exemplos de commit e paths no guia de templates.
status: done
priority: 5
lightweight: false
agent: Human
depends_on: []
pending_reason: ""
created_at: "2026-01-26T11:16:29-03:00"
updated_at: "2026-01-26T11:51:08-03:00"
entrypoints: []
tags: [specs, templates]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-0031 - Ajustar exemplos de issue templates para id canonico

## Summary
Atualizar o exemplo de commit e paths em `project/specs/14-issue-templates-usage.md` para refletir o id canonico (dev-####).

## Context
O guia de templates ainda usa um exemplo com alias (A-005) e path com id curto, o que conflita com o padrao canonico.

## Objective
Garantir que os exemplos usem o id canonico e o naming definido nas specs.

## Scope
- Atualizar o exemplo de commit para usar id canonico.
- Atualizar o exemplo de path para refletir o naming padronizado.

## Out of scope
- Alterar a estrutura do template em si.
- Oficializar alias sem especificacao formal.

## Requirements
- Usar id canonico no exemplo de commit.
- Manter linguagem alinhada com as conventions.

## Acceptance criteria
- [x] O exemplo em `project/specs/14-issue-templates-usage.md` usa id canonico e path consistente.

## Dependencies
None

## Entry points
- path: project/specs/14-issue-templates-usage.md
  type: doc

## Implementation notes
- Se alias nao for oficializado, evitar exemplos com alias.

## Tests
Not applicable.

## Risks and edge cases
- Exemplo incoerente pode reforcar o uso do padrao antigo.

## Result log
Exemplo de commit verificado e alinhado ao id canonico e path padronizado.

docs(yoda): ajustar exemplo de templates para id canonico

Issue: `alex-0031`
Path: `yoda/project/issues/alex-0031-ajustar-exemplo-issue-templates.md`
