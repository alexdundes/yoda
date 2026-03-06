---
schema_version: '2.00'
id: yoda-0056
status: to-do
depends_on:
- yoda-0048
title: Eliminar redundancia de Dependencies no corpo da issue
description: 'Remover a secao ## Dependencies do corpo das issues e manter apenas
  depends_on no front matter como fonte unica de dependencia.'
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:55:15-03:00'
updated_at: '2026-03-04T20:56:02-03:00'
---

# yoda-0056 - Eliminar redundancia de Dependencies no corpo da issue

## Summary
A estrutura atual duplica dependencias em dois lugares: `depends_on` no front matter e `## Dependencies` no corpo. Esta issue remove a duplicacao e define `depends_on` como unica fonte de verdade.

## Context
A duplicidade aumenta risco de divergencia entre metadado e texto, principalmente em updates manuais e revisoes.

## Objective
Simplificar o modelo de issue 0.3.0 removendo redundancia e reduzindo ambiguidade operacional.

## Scope
- Atualizar specs para declarar `depends_on` como fonte unica.
- Atualizar template de issue removendo secao `## Dependencies`.
- Ajustar scripts/validacoes que assumam a secao no corpo.
- Atualizar issues abertas do pacote 0.3.0 para o novo padrao.

## Out of scope
- Alterar semantica de dependencias alem da fonte de armazenamento.
- Redesenhar outras secoes do template sem relacao com dependencias.

## Requirements
- Scripts devem ler e escrever dependencias apenas via front matter.
- Corpo da issue nao deve conter secao de dependencias.
- Regras de selecao deterministica devem permanecer inalteradas.

## Acceptance criteria
- [ ] Specs 0.3.0 documentam `depends_on` como unica fonte de dependencias.
- [ ] Template de issue nao possui mais `## Dependencies`.
- [ ] Testes/validacoes cobrem ausencia da secao no corpo.

## Dependencies
Depende de `yoda-0048`.

## Entry points
- `project/specs`
- `yoda/templates/issue.md`
- `yoda/scripts`
- `yoda/project/issues`

## Implementation notes
Ao remover a secao no template, garantir que scripts antigos nao reintroduzam o bloco ao renderizar issue.

## Tests
Criar fixtures para validar issue sem `## Dependencies` e validar selecao/dependencias via front matter.

## Risks and edge cases
- Issues antigas podem manter secao residual ate migracao.
- Ferramentas externas que parseiam corpo podem precisar ajuste.

## Result log

## Flow log
2026-03-04T20:55:15-03:00 | [yoda-0056] issue_add created | title: Eliminar redundancia de Dependencies no corpo da issue | description: Remover a secao ## Dependencies do corpo das issues e manter apenas depends_on no front matter como fonte unica de dependencia. | slug: eliminar-redundancia-de-dependencies-no-corpo-da-issue | extern_issue_file: external issue linked
2026-03-04T20:56:02-03:00 | [yoda-0056] todo_update | depends_on:  -> yoda-0048
