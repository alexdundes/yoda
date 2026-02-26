---
created_at: '2026-02-26T19:12:53-03:00'
depends_on: []
description: Permitir alterar descricao e rename do arquivo da issue; remover campo
  slug do modelo e derivar slug sempre do nome do arquivo (sem ID), com regras claras
  de recálculo no update.
id: yoda-0045
origin:
  external_id: '2'
  requester: ''
  system: github
pending_reason: ''
priority: 5
schema_version: '1.01'
slug: permitir-update-de-descricao-e-rename-por-slug-derivado-do-arquivo
status: to-do
title: Permitir update de descricao e rename por slug derivado do arquivo
updated_at: '2026-02-26T19:12:53-03:00'
---

# yoda-0045 - Permitir update de descricao e rename por slug derivado do arquivo

## Summary
Evoluir o fluxo de update para permitir alteracao de descricao e rename do arquivo da issue com regras consistentes de slug. O slug deixa de ser um campo persistido e passa a ser sempre derivado do nome do arquivo (sem o prefixo de ID). Com isso, evita-se divergencia entre metadados e filename.

## Context
Foi identificado que o fluxo atual nao permite atualizar descricao de forma completa e segura, e tambem pode manter `slug` inconsistente quando o nome do arquivo muda. Hoje existe acoplamento entre campo `slug` persistido e nome de arquivo, o que abre espaco para drift. A proposta elimina a fonte de inconsistencia ao tratar o slug como dado derivado do filename.

## Objective
Permitir update de descricao e rename de issue com regras explicitas: `slug` derivado exclusivamente do nome do arquivo, sem campo `slug` no `TODO.<dev>.yaml` nem no front matter.

## Scope
- Adicionar suporte de update para alterar descricao da issue.
- Adicionar suporte de update para alterar slug (rename de arquivo da issue).
- Remover persistencia do campo `slug` do `TODO.<dev>.yaml`.
- Remover persistencia do campo `slug` do front matter da issue markdown.
- Definir regra de derivacao de slug a partir do nome do arquivo (`<id>-<slug>.md`).
- Ajustar validacao, listagem e fluxo de selecao para usar slug derivado.
- Implementar migracao/reconciliacao de arquivos legados com campo `slug`.

## Out of scope
- Alterar formato base do ID da issue.
- Alterar secoes textuais do corpo da issue alem do necessario para update de descricao.
- Mudancas nao relacionadas a derivacao de slug e rename de arquivo.

## Requirements
- `slug` deve ser sempre derivado do nome do arquivo sem o ID (ex.: `yoda-0045-meu-slug.md` -> `meu-slug`).
- Campo `slug` nao deve mais existir em `TODO.<dev>.yaml`.
- Campo `slug` nao deve mais existir no front matter da issue.
- Se a descricao for alterada e nenhum slug for informado, recalcular slug e renomear o arquivo.
- Se descricao e slug forem informados, usar o slug informado para renomear o arquivo.
- Para manter slug atual ao alterar descricao, o usuario deve informar explicitamente o slug atual.
- O rename deve ser operacionalizado como: gravar novo arquivo com o novo nome e apagar o arquivo anterior.
- Update deve manter rastreabilidade e integridade de referencias internas (id, paths e logs).

## Acceptance criteria
- [ ] `todo_update.py` (ou comando de update aplicavel) permite alterar descricao.
- [ ] Update com nova descricao e sem slug informado recalcula slug e renomeia arquivo.
- [ ] Update com nova descricao + slug informado usa slug informado e renomeia arquivo.
- [ ] Update com nova descricao + slug atual preserva nome/slug existente.
- [ ] Em rename, o arquivo antigo deixa de existir e o novo arquivo passa a ser a unica fonte da issue.
- [ ] `TODO.<dev>.yaml` e front matter de novas issues nao possuem campo `slug`.
- [ ] Validacao e listagem funcionam com slug derivado do filename.
- [ ] Migracao/reconciliacao remove `slug` legado e mantem compatibilidade.
- [ ] Testes automatizados cobrem cenarios de rename e derivacao.

## Dependencies
Relacionada a `yoda-0042` (extern_issue_file), `yoda-0043` (omissao de opcionais vazios), `yoda-0044` (front matter ordenado/sem defaults) e origem externa `github #2`.

## Entry points
- path: yoda/scripts/todo_update.py
  type: code
- path: yoda/scripts/issue_add.py
  type: code
- path: yoda/scripts/todo_list.py
  type: code
- path: yoda/scripts/lib/validate.py
  type: code
- path: yoda/scripts/lib/front_matter.py
  type: code
- path: yoda/scripts/update.py
  type: code
- path: yoda/scripts/init.py
  type: code
- path: yoda/project/issues/
  type: data
- path: yoda/todos/TODO.yoda.yaml
  type: data

## Implementation notes
Mudanca classificada como `subtle`: apesar de remover o campo persistido `slug`, ele nao e utilizado operacionalmente no fluxo atual, portanto a retirada nao deve gerar quebra de compatibilidade. Ainda assim, manter reconciliacao/migracao por `yoda/scripts/update.py` e `yoda/scripts/init.py` para padronizar artefatos legados.

## Tests
- Adicionar testes de update para alteracao de descricao com/sem slug informado.
- Adicionar testes de rename de arquivo e derivacao de slug pelo filename.
- Atualizar fixtures removendo campo `slug` de TODO/front matter.
- Adicionar teste de migracao/reconciliacao de layout legado.
- Rodar `python3 -m pytest yoda/scripts/tests`.

## Risks and edge cases
- Rename quebrar referencias em logs/links se path nao for atualizado adequadamente.
- Colisao de nome de arquivo ao recalcular slug para valor ja existente.
- Caracteres invalidos no slug informado exigirem normalizacao/erro claro.
- Fluxo parcial (descricao alterada sem rename concluido) gerar estado inconsistente.
- Falha entre criacao do novo arquivo e remocao do antigo pode deixar duplicidade temporaria.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
