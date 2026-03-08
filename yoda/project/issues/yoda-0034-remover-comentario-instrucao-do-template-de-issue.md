---
schema_version: '2.00'
status: done
title: Remover comentario-instrucao do template de issue
description: 'Eliminar os comentarios de instrucao do agente no template de issue
  que nao sao substituidos e acabam vazando para os arquivos finais. A issue gerada
  deve nascer limpa, sem blocos de comentario operacional do template. Regra transversal:
  atualizar primeiro project/specs/ e depois yoda/.'
priority: 4
created_at: '2026-02-25T15:36:44-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0034 - Remover comentario-instrucao do template de issue

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
- Issue criada por script nao deve conter o comentario inicial `
`.

## Acceptance criteria
- [ ] Specs atualizadas com regra explicita.
- [ ] Templates padrao e lightweight nao contem o comentario inicial `Replace [ID] ...`.
- [ ] Nova issue criada via `issue_add.py` nao contem o comentario inicial `Replace [ID] ...`.


## Entry points
- `project/specs/`
- `yoda/templates/issue.md`
- `yoda/scripts/issue_add.py`

## Implementation notes
Manter os demais comentarios de orientacao das secoes; remover somente o comentario inicial de substituicao de ID/titulo.

## Tests
Criar issue de teste via script e validar especificamente ausencia do comentario inicial `Replace [ID] ...`.

## Risks and edge cases
- Reintroducao de comentarios em futuros templates se nao houver regra de revisao.

## Result log

## Flow log
2026-02-25T15:36:44-03:00 | [yoda-0034] issue_add created | title: Remover comentario-instrucao do template de issue | description: Eliminar os comentarios de instrucao do agente no template de issue que nao sao substituidos e acabam vazando para os arquivos finais. A issue gerada deve nascer limpa, sem blocos de comentario operacional do template. Regra transversal: atualizar primeiro project/specs/ e depois yoda/. | slug: remover-comentario-instrucao-do-template-de-issue | priority: 4 | entrypoints: yoda/templates/issue.md:doc, yoda/scripts/issue_add.py:code, project/specs/:doc
2026-02-25T15:40:58-03:00 | [yoda-0034] todo_update | status: to-do -> doing
2026-02-25T18:28:17-03:00 | [yoda-0034] evaluate: comentario inicial AGENT removido dos templates issue.md e issue-lightweight-process.md (commit 5070dbb).
2026-02-25T18:28:21-03:00 | [yoda-0034] todo_update | status: doing -> done