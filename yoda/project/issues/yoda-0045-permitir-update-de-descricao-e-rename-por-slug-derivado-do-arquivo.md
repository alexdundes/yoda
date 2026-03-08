---
schema_version: '2.00'
status: done
title: Permitir update de descricao e rename por slug derivado do arquivo
description: "Permitir alterar descricao e rename do arquivo da issue; remover campo\
  \ slug do modelo e derivar slug sempre do nome do arquivo (sem ID), com regras claras\
  \ de rec\xE1lculo no update."
priority: 5
extern_issue_file: ../extern_issues/github-2.json
created_at: '2026-02-26T19:12:53-03:00'
updated_at: '2026-03-03T14:38:25-03:00'
---

# yoda-0045 - Permitir update de descricao e rename por slug derivado do arquivo

## Summary
Evoluir o fluxo de update para permitir alteracao de `title` e `description` com rename do arquivo da issue, usando regras consistentes de slug. O slug deixa de ser um campo persistido e passa a ser sempre derivado do nome do arquivo (sem o prefixo de ID), com base no `title` quando nao informado explicitamente no update. Com isso, evita-se divergencia entre metadados e filename.

## Context
Foi identificado que o fluxo atual nao permite atualizar descricao de forma completa e segura, e tambem pode manter `slug` inconsistente quando o nome do arquivo muda. Hoje existe acoplamento entre campo `slug` persistido e nome de arquivo, o que abre espaco para drift. A proposta elimina a fonte de inconsistencia ao tratar o slug como dado derivado do filename.

## Objective
Permitir update de `title`/`description` e rename de issue com regras explicitas: `slug` derivado exclusivamente do nome do arquivo, sem campo `slug` no `TODO.<dev>.yaml` nem no front matter.

## Scope
- Adicionar suporte de update para alterar `title` da issue.
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
- Se o `title` for alterado e nenhum slug for informado, recalcular slug a partir do `title` e renomear o arquivo.
- Se `title` e slug forem informados, usar o slug informado para renomear o arquivo.
- Para manter slug atual ao alterar `title`, o usuario deve informar explicitamente o slug atual.
- O rename deve ser operacionalizado como: gravar novo arquivo com o novo nome e apagar o arquivo anterior.
- Update deve manter rastreabilidade e integridade de referencias internas (id, paths e logs).
- Em colisao de arquivo (arquivo de destino ja existente) ou em duplicidade de arquivos por `id` (`<id>-*.md` mais de um), retornar erro e nao aplicar rename parcial.
- Em rename, o arquivo de log tambem deve ser renomeado para refletir o novo slug.
- Localizacao operacional da issue por `id` deve usar busca por `yoda/project/issues/<id>-*.md`.

## Acceptance criteria
- [x] `todo_update.py` (ou comando de update aplicavel) permite alterar `title` e descricao.
- [x] Update com novo `title` e sem slug informado recalcula slug (a partir de `title`) e renomeia arquivo.
- [x] Update com novo `title` + slug informado usa slug informado e renomeia arquivo.
- [x] Update com novo `title` + slug atual preserva nome/slug existente.
- [x] Em rename, o arquivo antigo deixa de existir e o novo arquivo passa a ser a unica fonte da issue.
- [x] Em rename, o arquivo de log antigo deixa de existir e o novo arquivo de log passa a ser o unico.
- [x] `TODO.<dev>.yaml` e front matter de novas issues nao possuem campo `slug`.
- [x] Validacao e listagem funcionam com slug derivado do filename.
- [x] Em caso de colisao/duplicidade por `id`, update falha com erro explicito.
- [x] Migracao/reconciliacao via `init.py --reconcile-layout` remove `slug` legado e mantem compatibilidade.
- [x] Testes automatizados cobrem cenarios de rename e derivacao.


## Entry points
- `yoda/scripts/todo_update.py`
- `yoda/scripts/issue_add.py`
- `yoda/scripts/todo_list.py`
- `yoda/scripts/lib/validate.py`
- `yoda/scripts/lib/front_matter.py`
- `yoda/scripts/update.py`
- `yoda/scripts/init.py`
- `yoda/project/issues/`
- `yoda/todos/TODO.yoda.yaml`

## Implementation notes
Mudanca classificada como `subtle`: apesar de remover o campo persistido `slug`, ele nao e utilizado operacionalmente no fluxo atual, portanto a retirada nao deve gerar quebra de compatibilidade. Ainda assim, manter reconciliacao/migracao por `yoda/scripts/update.py` e `yoda/scripts/init.py` para padronizar artefatos legados.

Decisoes de Document:
- Colisao e tratada como erro: se existir arquivo de destino ou mais de um `<id>-*.md`, abortar.
- Em rename de issue, renomear tambem o arquivo de log para o novo slug.
- Derivacao automatica de slug usa sempre `title` (mesma regra de `issue_add.py`).
- `todo_update.py` passa a suportar update de `title`.
- `init.py --reconcile-layout` e o caminho oficial de ajuste de legado para remocao de `slug`.
- Ordem canonica de metadata permanece a mesma da `yoda-0044`, apenas sem o campo `slug`.

## Tests
- Adicionar testes de update para alteracao de descricao com/sem slug informado.
- Adicionar testes de rename de arquivo e derivacao de slug pelo filename.
- Atualizar fixtures removendo campo `slug` de TODO/front matter.
- Adicionar teste de migracao/reconciliacao de layout legado.
- Rodar `python3 -m pytest yoda/scripts/tests`.
- Executado: `python3 -m pytest yoda/scripts/tests -q` -> `58 passed`.
- Executado: `python3 yoda/scripts/init.py --dev yoda --reconcile-layout` -> reconciliacao concluida sem erro.

## Risks and edge cases
- Rename quebrar referencias em logs/links se path nao for atualizado adequadamente.
- Colisao de nome de arquivo ao recalcular slug para valor ja existente.
- Caracteres invalidos no slug informado exigirem normalizacao/erro claro.
- Fluxo parcial (descricao alterada sem rename concluido) gerar estado inconsistente.
- Falha entre criacao do novo arquivo e remocao do antigo pode deixar duplicidade temporaria.

## Result log
refactor(yoda): derive slug from issue filename and support rename in todo_update

Issue: `yoda-0045`
Path: `yoda/project/issues/yoda-0045-permitir-update-de-descricao-e-rename-por-slug-derivado-do-arquivo.md`

Implementado update de `title` e `description` com suporte a rename de arquivo de issue e de log, removendo `slug` persistido de TODO/front matter e adotando resolucao operacional por `id` (`<id>-*.md`/`<id>-*.yaml`). `todo_update.py` agora recalcula slug a partir de `title` quando necessario, aceita override por `--slug`, e falha explicitamente em casos de colisao/duplicidade. `init.py --reconcile-layout` foi alinhado para limpar `slug` legado e reconciliar metadata no novo contrato.

## Flow log
- 2026-02-26T19:12:53-03:00 issue_add created | title: Permitir update de descricao e rename por slug derivado do arquivo | description: Permitir alterar descricao e rename do arquivo da issue; remover campo slug do modelo e derivar slug sempre do nome do arquivo (sem ID), com regras claras de recálculo no update. | slug: permitir-update-de-descricao-e-rename-por-slug-derivado-do-arquivo | priority: 5 | origin: external issue linked
- 2026-03-03T11:51:27-03:00 todo_update (no changes)
- 2026-03-03T14:04:22-03:00 todo_update | status: to-do -> doing
- 2026-03-03T14:05:05-03:00 Study completed\n- todo_update currently cannot update description or trigger rename; it only updates status/priority/depends/pending/extern_issue_file\n- slug is currently required in TODO validation and used as source of truth for issue/log paths across todo_update, todo_next, todo_list, log_add, and init reconcile\n- paths API and helpers are slug-dependent (issue_path/log_path require slug argument)\n- log files are currently named with id+slug and log_add resolves file path using slug from TODO\n- implementing this issue will require a repository-wide shift to derived slug from filename plus rename-safe path resolution\n- key design decisions needed for implementation: collision policy on rename, log filename policy after rename, and backward compatibility for legacy slug fields
- 2026-03-03T14:21:37-03:00 Document phase updated issue text\n- Scope/requirements updated to include title update as first-class input\n- Confirmed slug derivation source as title and explicit override via --slug\n- Added collision policy: duplicate <id>-*.md or destination file conflict must fail\n- Added log rename requirement during issue rename\n- Confirmed lookup by id pattern and legacy migration via init --reconcile-layout\n- Canonical metadata order kept from yoda-0044, without slug field
- 2026-03-03T14:32:25-03:00 Implement phase completed\n- Removed persisted slug from issue metadata in TODO/front matter and canonical order now excludes slug\n- Added id-based issue/log file resolution (<id>-*.md / <id>-*.yaml) with conflict detection for duplicates\n- issue_add now keeps slug only as filename artifact; metadata no longer stores slug\n- todo_update now supports --title, --description, and --slug with rename behavior; title changes derive slug and rename issue plus log files\n- init reconcile drops legacy slug metadata and updates front matter by resolving issue files by id\n- todo_next, todo_list, and log_add migrated to id-based path resolution\n- Added/updated tests for slugless metadata and rename flows\n- Validation run: python3 -m pytest yoda/scripts/tests -q (58 passed)
- 2026-03-03T14:38:25-03:00 Evaluate phase completed\n- Acceptance criteria marked as done in issue markdown\n- Result log filled with conventional commit suggestion\n- Validation recorded: python3 -m pytest yoda/scripts/tests -q (58 passed)\n- Reconcile validation recorded: python3 yoda/scripts/init.py --dev yoda --reconcile-layout (success)
- 2026-03-03T14:38:25-03:00 todo_update | status: doing -> done
