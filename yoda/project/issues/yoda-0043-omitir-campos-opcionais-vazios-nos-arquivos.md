---
schema_version: '2.00'
status: done
title: Omitir campos opcionais vazios nos arquivos
description: Quando um campo opcional estiver vazio, ele nao deve ser definido/persistido
  nos arquivos gerados ou atualizados.
priority: 5
extern_issue_file: ../extern_issues/github-2.json
created_at: '2026-02-26T18:57:50-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0043 - Omitir campos opcionais vazios nos arquivos

## Summary
Reduzir tamanho e ruido dos artefatos YAML/Markdown omitindo campos opcionais quando estiverem vazios. Em vez de persistir chaves com string vazia, lista vazia ou valor padrao sem informacao util, os scripts devem simplesmente nao escrever essas chaves nos arquivos de saida. A regra deve ser consistente entre criacao, update e reconciliacao.

## Context
Atualmente varios arquivos persistem campos opcionais vazios, o que aumenta volume, dificulta leitura e amplia diferencas em PRs sem ganho funcional. Essa verbosidade tambem eleva o custo de manutencao do schema e dos templates. A padronizacao de omissao para opcionais vazios simplifica artefatos e torna mudancas mais claras.

## Objective
Definir e implementar politica unica de serializacao para que campos opcionais vazios sejam omitidos dos arquivos internos do YODA, preservando compatibilidade operacional e validacao.

## Scope
- Mapear e formalizar os campos opcionais relevantes em TODO, issue front matter e logs aplicaveis.
- Ajustar escrita de arquivos em scripts que criam/atualizam dados para omitir opcionais vazios.
- Ajustar templates para nao forcar emissao de campos opcionais vazios.
- Atualizar validacao para aceitar ausencia desses campos.
- Atualizar/reconciliar artefatos existentes quando aplicavel.

## Out of scope
- Remover campos obrigatorios do schema.
- Alterar significado semantico de campos opcionais quando presentes.
- Mudancas funcionais nao relacionadas a serializacao/compactacao de artefatos.

## Requirements
- Campo opcional vazio nao deve ser persistido em novos arquivos.
- Campo opcional que ficar vazio apos update deve ser removido do arquivo.
- Validadores devem considerar a ausencia de opcional como valida.
- Renderizacao/serializacao deve permanecer deterministica para evitar diffs instaveis.
- Documentacao de scripts deve refletir a regra de omissao de opcionais vazios.
- Manter `schema_version: "1.02"` (sem bump), pois esta versao ainda nao entrou em producao.

## Acceptance criteria
- [x] `issue_add.py` nao grava campos opcionais vazios no front matter e no item do TODO.
- [x] `todo_update.py` remove campo opcional quando atualizado para vazio.
- [x] `init.py --reconcile-layout` (ou fluxo equivalente) consegue limpar campos opcionais vazios em arquivos legados.
- [x] Validacao aceita arquivos sem campos opcionais omitidos.
- [x] Testes automatizados cobrem criacao, update e reconciliacao com omissao de opcionais.
- [x] Decisao de versao registrada: manter `schema_version: "1.02"` nesta entrega.


## Entry points
- `yoda/scripts/issue_add.py`
- `yoda/scripts/todo_update.py`
- `yoda/scripts/init.py`
- `yoda/scripts/lib/validate.py`
- `yoda/scripts/lib/front_matter.py`
- `yoda/templates/issue.md`
- `yoda/todos/TODO.yoda.yaml`

## Implementation notes
A regra de "opcional vazio = omitido" deve ser centralizada em utilitario compartilhado de serializacao para evitar divergencia entre scripts. Necessario definir com precisao o que e "vazio" por tipo (string vazia, lista vazia, objeto vazio, null) e aplicar de forma uniforme.

Decisoes de Document (derivadas do Study):
- Manter `schema_version: "1.02"` sem incremento nesta issue.
- Definicao de "vazio" para omissao: `""`, lista vazia `[]`, objeto vazio `{}`, `null`/`None`.
- Campos alvo para omissao quando vazios em TODO/front matter:
  - `extern_issue_file`: omitir quando nao houver vinculo externo.
  - `pending_reason`: omitir quando `status != pending`.
  - `depends_on`: omitir quando lista vazia.
- Campos obrigatorios que permanecem sempre presentes: `id`, `title`, `slug`, `description`, `status`, `priority`, `created_at`, `updated_at`, `schema_version`.
- Reconciliacao (`init.py --reconcile-layout`) deve remover chaves opcionais vazias existentes em legado, sem alterar semantica dos demais campos.

## Tests
- Adicionar testes unitarios para serializacao com omissao de opcionais vazios.
- Atualizar fixtures de TODO/issue para novo comportamento.
- Cobrir caminho de migracao/reconciliacao de arquivos existentes.
- Rodar `python3 -m pytest yoda/scripts/tests`.
- Executado: `python3 -m pytest yoda/scripts/tests -q` -> `54 passed`.

## Risks and edge cases
- Remocao indevida de campo que parecia opcional, mas e exigido por algum fluxo especifico.
- Mudanca gerar incompatibilidade com ferramentas externas que esperam chave presente vazia.
- Reconciliacao em massa produzir diffs grandes; precisa de criterio claro de rollout.

## Result log
refactor(yoda): omit empty optional metadata in TODO and issue front matter

Issue: `yoda-0043`
Path: `yoda/project/issues/yoda-0043-omitir-campos-opcionais-vazios-nos-arquivos.md`

Implementado utilitario compartilhado para remover opcionais vazios (`depends_on`, `pending_reason`, `extern_issue_file`) e integracao em `issue_add.py`, `todo_update.py` e reconciliacao de `init.py`. A validacao foi ajustada para aceitar ausencia de opcionais e manter a regra de `pending_reason` obrigatorio quando `status=pending`. Template e documentacao dos scripts foram alinhados, com manutencao de `schema_version: "1.02"` sem bump.

## Flow log
2026-02-26T18:57:50-03:00 | [yoda-0043] issue_add created | title: Omitir campos opcionais vazios nos arquivos | description: Quando um campo opcional estiver vazio, ele nao deve ser definido/persistido nos arquivos gerados ou atualizados. | slug: omitir-campos-opcionais-vazios-nos-arquivos | priority: 5 | origin: external issue linked
2026-03-03T11:51:27-03:00 | [yoda-0043] todo_update (no changes)
2026-03-03T12:11:14-03:00 | [yoda-0043] todo_update | status: to-do -> doing
2026-03-03T12:15:26-03:00 | [yoda-0043] Document phase updated issue text\n- Registered decision to keep schema_version 1.02 (no bump)\n- Defined empty-value omission policy\n- Scoped optional fields for omission: extern_issue_file, pending_reason, depends_on\n- Kept mandatory metadata fields explicit
2026-03-03T12:21:42-03:00 | [yoda-0043] Implement phase completed\n- Added shared optional-metadata pruning helper and wired it into issue_add, todo_update, and init reconcile\n- Validation now accepts missing optional fields while preserving pending rules\n- Updated issue template and scripts README for optional omission policy\n- Updated tests for creation/update/reconcile behavior; full yoda/scripts test suite green (54 passed)
2026-03-03T12:25:01-03:00 | [yoda-0043] Evaluate phase completed\n- Acceptance criteria marked as done in issue markdown\n- Result log filled with conventional commit suggestion\n- Validation recorded: python3 -m pytest yoda/scripts/tests -q (54 passed)\n- Schema decision preserved: 1.02 without bump
2026-03-03T12:25:56-03:00 | [yoda-0043] todo_update | status: doing -> done | depends_on: [] -> | pending_reason:  ->