---
agent: Human
created_at: '2026-02-25T15:36:44-03:00'
depends_on: []
description: 'Eliminar os comentarios de instrucao do agente no template de issue
  que nao sao substituidos e acabam vazando para os arquivos finais. A issue gerada
  deve nascer limpa, sem blocos de comentario operacional do template. Regra transversal:
  atualizar primeiro project/specs/ e depois yoda/.'
entrypoints:
- path: yoda/templates/issue.md
  type: doc
- path: yoda/scripts/issue_add.py
  type: code
- path: project/specs/
  type: doc
id: yoda-0034
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 4
schema_version: '1.0'
slug: remover-comentario-instrucao-do-template-de-issue
status: done
tags: []
title: Remover comentario-instrucao do template de issue
updated_at: '2026-02-25T18:28:21-03:00'
---

# yoda-0034 - Remover comentario-instrucao do template de issue
<!-- AGENT: Replace yoda-0034 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Remover comentario-instrucao do template de issue with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Remover apenas o comentario-instrucao inicial de substituicao de ID/titulo do template de issue, que vaza para os arquivos gerados. Os demais comentarios de apoio por secao permanecem.

## Context
Atualmente, comentarios do template continuam no markdown criado por `issue_add.py`, o que gera ruido e aparenta conteudo incompleto. Isso reduz legibilidade e qualidade do backlog.

## Objective
Garantir que o template final de issue nao inclua o comentario inicial de substituicao de ID/titulo.

## Scope
- Atualizar `project/specs/` com regra explicita sobre remocao do comentario inicial de substituicao de ID/titulo.
- Ajustar `yoda/templates/issue.md` e `yoda/templates/issue-lightweight-process.md` para remover apenas esse comentario inicial.
- Ajustar `issue_add.py` somente se for necessario para manter a saida sem esse comentario.

## Out of scope
- Redesenhar estrutura completa da issue.
- Remover comentarios de orientacao das secoes (Summary, Context, etc.).
- Alterar semantica de campos nao relacionados ao comentario inicial.

## Requirements
- Ordem obrigatoria: `project/specs/` antes de `yoda/`.
- Issue criada por script nao deve conter o comentario inicial `<!-- AGENT: Replace [ID] ... -->`.

## Acceptance criteria
- [ ] Specs atualizadas com regra explicita.
- [ ] Templates padrao e lightweight nao contem o comentario inicial `Replace [ID] ...`.
- [ ] Nova issue criada via `issue_add.py` nao contem o comentario inicial `Replace [ID] ...`.

## Dependencies
None.

## Entry points
- path: project/specs/
  type: doc
- path: yoda/templates/issue.md
  type: doc
- path: yoda/scripts/issue_add.py
  type: code

## Implementation notes
Manter os demais comentarios de orientacao das secoes; remover somente o comentario inicial de substituicao de ID/titulo.

## Tests
Criar issue de teste via script e validar especificamente ausencia do comentario inicial `Replace [ID] ...`.

## Risks and edge cases
- Reintroducao de comentarios em futuros templates se nao houver regra de revisao.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->