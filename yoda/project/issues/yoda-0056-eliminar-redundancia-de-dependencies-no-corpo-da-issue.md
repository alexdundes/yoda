---
schema_version: '2.00'
id: yoda-0056
status: done
depends_on:
- yoda-0048
title: Verificar ausencia de Dependencies no corpo das issues (forward-only)
description: Verificar, por varredura manual e sem migracao retroativa, que o contrato
  vigente usa apenas depends_on no front matter e nao orienta secao Dependencies no
  corpo.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:55:15-03:00'
updated_at: '2026-03-07T08:56:59-03:00'
---

# yoda-0056 - Verificar ausencia de Dependencies no corpo das issues (forward-only)

## Summary
Esta issue deixa de ser uma alteracao estrutural e passa a ser uma verificacao de consistencia do contrato vigente. O objetivo e confirmar que `depends_on` e a unica fonte de dependencias e que `## Dependencies` nao e mais orientado no corpo para novos artefatos.

## Context
A direcao tecnica ja foi definida previamente na spec 0.3.0, no playbook e no template. O trabalho restante desta issue e validar coerencia documental e registrar a verificacao.

## Objective
Executar verificacao forward-only do contrato de dependencias no YODA, sem migracao retroativa de issues antigas.

## Scope
- Verificar em `project/specs` que `depends_on` e a unica fonte de dependencia.
- Verificar em `yoda/yoda.md` e no template que `## Dependencies` nao e orientado para novas issues.
- Registrar o resultado da verificacao nesta issue.

## Out of scope
- Migrar issues antigas.
- Alterar scripts/validacoes automatizadas.
- Criar novos testes automatizados.

## Requirements
- A verificacao deve ser apenas por varredura manual.
- O criterio de conformidade deve considerar apenas o contrato vigente para frente.
- O corpo desta issue nao deve conter secao `## Dependencies`.

## Acceptance criteria
- [x] `project/specs` confirma `depends_on` como fonte unica de dependencias.
- [x] `yoda/yoda.md` e template nao orientam uso de `## Dependencies` no corpo.
- [x] Resultado da varredura manual esta registrado nesta issue.

## Entry points
- `project/specs/04-todo-dev-yaml-issues.md`
- `project/specs/14-issue-templates-usage.md`
- `yoda/yoda.md`
- `yoda/templates/issue.md`
- `yoda/project/issues/yoda-0056-eliminar-redundancia-de-dependencies-no-corpo-da-issue.md`

## Implementation notes
Issue de verificacao apenas; nao aplicar mudancas de migracao em lote.

## Tests
Nao aplicavel. Validacao por varredura manual.

## Risks and edge cases
- Interpretacao incorreta de conformidade ao incluir issues legadas fora do escopo forward-only.

## Result log
docs(verification): confirmar contrato forward-only de dependencias

Foi executada varredura manual dos pontos de entrada da issue para confirmar que o contrato vigente permanece consistente: `depends_on` esta documentado como fonte unica de dependencia e `## Dependencies` nao e orientado no corpo para novas issues. A issue foi mantida como verificacao (forward-only), sem migracao retroativa, sem alteracoes de scripts e sem testes automatizados.

- **GitHub Issue** :   #3

- **Issue**: `yoda-0056`

- **Path**: `yoda/project/issues/yoda-0056-eliminar-redundancia-de-dependencies-no-corpo-da-issue.md`

## Flow log
2026-03-04T20:55:15-03:00 | [yoda-0056] issue_add created | title: Eliminar redundancia de Dependencies no corpo da issue | description: Remover a secao ## Dependencies do corpo das issues e manter apenas depends_on no front matter como fonte unica de dependencia. | slug: eliminar-redundancia-de-dependencies-no-corpo-da-issue | extern_issue_file: external issue linked
2026-03-04T20:56:02-03:00 | [yoda-0056] todo_update | depends_on:  -> yoda-0048
2026-03-07T08:51:29-03:00 yoda-0056 transition to-do->doing phase=study
2026-03-07T08:54:05-03:00 yoda-0056 transition doing/study->doing/document
2026-03-07T08:54:08-03:00 | [yoda-0056] Document scope updated: issue reframed to forward-only verification with manual sweep and no automated changes.
2026-03-07T08:56:34-03:00 yoda-0056 transition doing/document->doing/implement
2026-03-07T08:56:39-03:00 yoda-0056 transition doing/implement->doing/evaluate
2026-03-07T08:56:43-03:00 | [yoda-0056] Evaluate completed: ACs validated by manual sweep and Result log finalized.
2026-03-07T08:56:59-03:00 yoda-0056 transition doing/evaluate->done
