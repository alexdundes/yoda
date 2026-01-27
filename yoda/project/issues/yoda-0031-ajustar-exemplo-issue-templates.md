---
agent: Human
created_at: '2026-01-27T13:32:13-03:00'
depends_on: []
description: Atualizar o exemplo de commit e paths em `project/specs/14-issue-templates-usage.md`
  para refletir o id canonico (dev-####).
entrypoints: []
id: yoda-0031
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 5
schema_version: '1.0'
slug: ajustar-exemplo-issue-templates
status: done
tags: []
title: Ajustar exemplos de issue templates para id canonico
updated_at: '2026-01-27T13:32:39-03:00'
---

# yoda-0031 - Ajustar exemplos de issue templates para id canonico

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

Issue: `yoda-0031`
Path: `yoda/project/issues/yoda-0031-ajustar-exemplo-issue-templates.md`