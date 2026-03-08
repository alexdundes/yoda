---
schema_version: '2.00'
status: done
depends_on:
- yoda-0048
title: Verificar contrato de ID derivado do nome do arquivo (forward-only)
description: Verificar, por varredura manual e sem migracao retroativa, que o contrato
  vigente define ID derivado do filename e nao orienta campo id no front matter.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:58:43-03:00'
updated_at: '2026-03-07T08:59:15-03:00'
---

# yoda-0057 - Verificar contrato de ID derivado do nome do arquivo (forward-only)

## Summary
Esta issue deixa de ser uma alteracao estrutural e passa a ser uma verificacao de consistencia do contrato vigente sobre identificacao de issues. O objetivo e confirmar que o ID e derivado do nome do arquivo e que o contrato documental nao orienta `id` no front matter para novos artefatos.

## Context
A direcao tecnica ja foi definida na spec 0.3.0 e na orientacao de template. O trabalho restante desta issue e validar coerencia documental e registrar o resultado.

## Objective
Executar verificacao forward-only do contrato de ID por filename no YODA, sem migracao retroativa de issues antigas.

## Scope
- Verificar em `project/specs` que o ID canonico e derivado do filename.
- Verificar em `project/specs/14-issue-templates-usage.md` que o contrato nao orienta `id` no front matter.
- Registrar nesta issue o resultado da varredura manual.

## Out of scope
- Migrar issues antigas para remover `id`.
- Alterar scripts/validacoes automatizadas.
- Criar novos testes automatizados.

## Requirements
- A verificacao deve ser apenas por varredura manual.
- O criterio de conformidade deve considerar apenas o contrato vigente para frente.
- O corpo desta issue nao deve conter secao `## Dependencies`.

## Acceptance criteria
- [x] `project/specs` confirma ID derivado do nome do arquivo.
- [x] `project/specs/14-issue-templates-usage.md` nao orienta `id` no front matter.
- [x] Resultado da varredura manual esta registrado nesta issue.

## Entry points
- `project/specs/04-todo-dev-yaml-issues.md`
- `project/specs/14-issue-templates-usage.md`
- `yoda/yoda.md`
- `yoda/project/issues/yoda-0057-remover-id-do-front-matter-e-derivar-id-pelo-nome-do-arquivo.md`

## Implementation notes
Issue de verificacao apenas; nao aplicar mudancas de migracao em lote.

## Tests
Nao aplicavel. Validacao por varredura manual.

## Risks and edge cases
- Interpretacao incorreta de conformidade ao incluir issues legadas fora do escopo forward-only.

## Result log
docs(verification): confirmar contrato forward-only de ID por filename

Foi executada varredura manual dos pontos de entrada da issue para confirmar que o contrato vigente permanece consistente: a spec define o identificador canonico derivado do nome do arquivo e a regra de template nao orienta campo `id` no front matter para novas issues. A issue foi mantida como verificacao (forward-only), sem migracao retroativa, sem alteracoes de scripts e sem testes automatizados.

- **GitHub Issue** :   #3

- **Issue**: `yoda-0057`

- **Path**: `yoda/project/issues/yoda-0057-remover-id-do-front-matter-e-derivar-id-pelo-nome-do-arquivo.md`

## Flow log
- 2026-03-04T20:58:43-03:00 issue_add created | title: Remover id do front matter e derivar ID pelo nome do arquivo | description: Eliminar o campo id do front matter no modelo 0.3.0 e definir o nome do arquivo da issue como fonte canonica para derivacao do ID. | slug: remover-id-do-front-matter-e-derivar-id-pelo-nome-do-arquivo | extern_issue_file: external issue linked
- 2026-03-04T20:59:15-03:00 todo_update | depends_on: -> yoda-0048
- 2026-03-07T08:58:02-03:00 transition to-do->doing phase=study
- 2026-03-07T08:58:23-03:00 transition doing/study->doing/document
- 2026-03-07T08:58:27-03:00 Document scope updated: issue reframed to forward-only verification with manual sweep and no automated changes.
- 2026-03-07T08:58:50-03:00 transition doing/document->doing/implement
- 2026-03-07T08:58:54-03:00 transition doing/implement->doing/evaluate
- 2026-03-07T08:59:01-03:00 Evaluate completed: ACs validated by manual sweep and Result log finalized.
- 2026-03-07T08:59:15-03:00 transition doing/evaluate->done
