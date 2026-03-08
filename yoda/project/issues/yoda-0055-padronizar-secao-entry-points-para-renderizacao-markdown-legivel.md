---
schema_version: '2.00'
status: done
depends_on:
- yoda-0048
title: Padronizar secao Entry points para renderizacao markdown legivel
description: Substituir o formato pseudo-YAML da secao Entry points por formato markdown
  legivel no preview humano, mantendo estrutura deterministica para scripts.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:42:02-03:00'
updated_at: '2026-03-07T08:49:09-03:00'
---

# yoda-0055 - Padronizar secao Entry points para renderizacao markdown legivel

## Summary
A secao `Entry points` das issues deve seguir o contrato da spec 0.3.0 como lista markdown simples. Esta issue corrige o texto de orientacao e o template para aplicacao daqui para frente, sem migracao retroativa.

## Context
No estado atual, o bloco em estilo YAML dentro do corpo da issue dificulta leitura em interfaces de preview markdown e gera friccao no uso diario.

## Objective
Padronizar `Entry points` no formato canonico definido em `project/specs` (lista simples em markdown), com orientacao clara para preenchimento por agentes.

## Scope
- Alinhar esta issue ao formato canonico ja definido em `project/specs`.
- Atualizar o comentario de orientacao em `yoda/templates/issue.md` para preenchimento de `Entry points`.
- Validar por varredura manual que as alteracoes desta issue ficaram consistentes.

## Out of scope
- Redesenhar outras secoes da issue sem relacao com `Entry points`.
- Mudancas em fluxo de estado/fase nao relacionadas.
- Migrar issues antigas para o novo formato.
- Criar/alterar validacoes automatizadas ou testes para `Entry points`.

## Requirements
- O formato deve renderizar corretamente em preview markdown.
- O formato deve seguir exatamente o contrato vigente em `project/specs` para `## Entry points`.
- O comentario do template deve orientar preenchimento textual simples, sem pseudo-YAML.

## Acceptance criteria
- [x] `Entry points` possui formato markdown legivel e padronizado.
- [x] Template de issue orienta preenchimento de `Entry points` conforme a spec.
- [x] Varredura manual confirma que as alteracoes desta issue estao corretas.


## Entry points
- `project/specs`
- `yoda/templates/issue.md`
- `yoda/project/issues/yoda-0055-padronizar-secao-entry-points-para-renderizacao-markdown-legivel.md`

## Implementation notes
Nao introduzir tabela para `Entry points`; seguir apenas lista simples conforme spec.

## Tests
Nao aplicavel. Validacao sera por varredura manual dos arquivos alterados.

## Risks and edge cases
- Divergencia futura se instrucoes do template e spec voltarem a se desalinhar.

## Result log
docs(template): padronizar orientacao de Entry points para lista simples

Foi consolidado o escopo aprovado na `yoda-0055` com aplicacao forward-only: a issue foi corrigida para seguir estritamente a spec vigente (`Entry points` como lista markdown simples), removendo ambiguidade sobre tabela, migracao retroativa e validacoes automatizadas. O template `yoda/templates/issue.md` recebeu orientacao explicita para preenchimento textual em lista (`- <path>`) e proibicao de pseudo-YAML (`path:`/`type:`). A validacao foi realizada por varredura manual dos arquivos alterados.

- **GitHub Issue** :   #3

- **Issue**: `yoda-0055`

- **Path**: `yoda/project/issues/yoda-0055-padronizar-secao-entry-points-para-renderizacao-markdown-legivel.md`

## Flow log
2026-03-04T20:42:02-03:00 | [yoda-0055] issue_add created | title: Padronizar secao Entry points para renderizacao markdown legivel | description: Substituir o formato pseudo-YAML da secao Entry points por formato markdown legivel no preview humano, mantendo estrutura deterministica para scripts. | slug: padronizar-secao-entry-points-para-renderizacao-markdown-legivel | extern_issue_file: external issue linked
2026-03-04T20:42:19-03:00 | [yoda-0055] todo_update | depends_on:  -> yoda-0048
2026-03-07T08:34:31-03:00 yoda-0055 transition to-do->doing phase=study
2026-03-07T08:43:45-03:00 yoda-0055 transition doing/study->doing/document
2026-03-07T08:44:05-03:00 | [yoda-0055] Document scope updated: follow spec-only list format, forward-only template guidance, manual sweep validation only.
2026-03-07T08:47:18-03:00 yoda-0055 transition doing/document->doing/implement
2026-03-07T08:47:28-03:00 | [yoda-0055] Implement completed: template Entry points guidance updated to plain list (`- <path>`) and manual sweep confirmed scope alignment.
2026-03-07T08:47:57-03:00 yoda-0055 transition doing/implement->doing/evaluate
2026-03-07T08:48:18-03:00 | [yoda-0055] Evaluate completed: ACs checked and Result log filled after manual sweep validation.
2026-03-07T08:49:09-03:00 yoda-0055 transition doing/evaluate->done