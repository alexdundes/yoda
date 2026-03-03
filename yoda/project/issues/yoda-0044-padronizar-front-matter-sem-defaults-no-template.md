---
schema_version: '1.02'
id: yoda-0044
status: done
title: Padronizar front matter sem defaults no template
description: Remover valores padrao do front matter no template markdown; issue_add.py
  e todo_update.py passam a preencher/atualizar campos. Definir ordem fixa de campos
  no front matter para leitura consistente.
priority: 5
extern_issue_file: ../extern_issues/github-2.json
created_at: '2026-02-26T19:04:01-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0044 - Padronizar front matter sem defaults no template

## Summary
Remover do template markdown os valores padrao preenchidos no front matter, deixando a estrutura neutra para ser populada pelos scripts operacionais. O preenchimento inicial deve ficar a cargo de `issue_add.py` e as alteracoes posteriores por `todo_update.py` (ou script equivalente no fluxo). Alem disso, os campos do front matter devem seguir uma ordem fixa predefinida para melhorar leitura e reduzir diffs ruidosos.

## Context
Hoje parte dos valores aparece predefinida no template, o que mistura responsabilidade de apresentacao com responsabilidade de persistencia de dados. Isso gera ambiguidade sobre a origem dos valores e dificulta manutencao do fluxo. A falta de ordem canonica de campos tambem prejudica legibilidade e aumenta variacao de diff entre execucoes.

## Objective
Separar claramente template e preenchimento de dados: template sem defaults, scripts como unica fonte de escrita/atualizacao, e ordem canonica de campos no front matter para todos os arquivos de issue.

## Scope
- Atualizar `yoda/templates/issue.md` para remover valores padrao do front matter.
- Definir ordem canonica dos campos de front matter de issue.
- Ajustar `issue_add.py` para preencher todos os campos necessarios na ordem definida.
- Ajustar `todo_update.py` (ou caminho equivalente de update) para manter a mesma ordem ao atualizar front matter.
- Reconciliar issues existentes para aplicar ordenacao padrao quando pertinente.

## Out of scope
- Alterar conteudo semantico de campos obrigatorios ja estabelecidos.
- Mudancas funcionais fora do front matter de issue markdown.
- Reformular estrutura do corpo da issue (secoes Summary/Context/etc.).

## Requirements
- O template nao deve carregar valores de dados operacionais predefinidos.
- `issue_add.py` deve preencher front matter completo no momento da criacao.
- `todo_update.py` (ou script equivalente) deve atualizar mantendo ordem canonica.
- Ordem de campos deve ser unica e documentada.
- Serializacao deve ser deterministica para evitar reorder acidental.
- Ordem canonica obrigatoria de front matter:
  - `schema_version`, `id`, `slug`, `status`, `pending_reason` (quando presente), `depends_on` (quando presente), `title`, `description`, `priority`, `extern_issue_file` (quando presente), `created_at`, `updated_at`.
- Politica de opcionais vazios confirmada: omitir `pending_reason`, `depends_on` e `extern_issue_file` quando vazios.
- No template, manter apenas delimitadores de front matter (`---`), sem placeholders de dados.
- `init.py --reconcile-layout` deve aplicar a mesma ordem canonica ao legado ao reconciliar front matter de issues.

## Acceptance criteria
- [x] `yoda/templates/issue.md` nao contem defaults operacionais no front matter.
- [x] Nova issue criada por `issue_add.py` sai com campos preenchidos e ordenados conforme padrao.
- [x] Update de issue preserva a mesma ordem de campos no front matter.
- [x] Fixtures/testes de front matter cobrem ordem fixa e ausencia de defaults no template.
- [x] Reconciliacao (quando aplicada) nao quebra validacao dos arquivos existentes.
- [x] A ordem relativa `status -> pending_reason -> depends_on` e respeitada quando os campos existem.
- [x] `title` aparece antes de `description` no front matter final.

## Dependencies
Relacionada a `yoda-0043` (omissao de opcionais vazios) e `yoda-0042` (simplificacao de origem externa); origem externa `github #2`.

## Entry points
- path: yoda/templates/issue.md
  type: template
- path: yoda/scripts/issue_add.py
  type: code
- path: yoda/scripts/todo_update.py
  type: code
- path: yoda/scripts/lib/front_matter.py
  type: code
- path: yoda/scripts/lib/validate.py
  type: code
- path: yoda/project/issues/
  type: data

## Implementation notes
Se `todo_update.py` ainda nao cobrir update de front matter no fluxo atual, definir explicitamente o caminho responsavel por essa atualizacao e manter nomenclatura/documentacao consistente. A ordem canonica pode ser centralizada em utilitario unico para evitar divergencia entre criacao e update.

Decisoes de Document:
- Campo temporal canonico: `created_at` (nao `create_at`).
- `title` deve aparecer antes de `description`.
- Template de issue sem placeholders de metadata; scripts passam a ser a unica fonte de preenchimento de front matter.

## Tests
- Adicionar testes de renderizacao do template sem defaults.
- Adicionar testes de `issue_add.py` validando ordem fixa do front matter.
- Adicionar/ajustar testes de update para garantir preservacao da ordem.
- Rodar `python3 -m pytest yoda/scripts/tests`.
- Executado: `python3 -m pytest yoda/scripts/tests -q` -> `56 passed`.

## Risks and edge cases
- Divergencia entre scripts se a ordenacao nao for centralizada.
- Quebra de compatibilidade com parsers externos que dependem de ordem anterior.
- Casos legados com front matter incompleto exigirem normalizacao cuidadosa.

## Result log
refactor(yoda): canonicalize issue front matter order and remove template metadata defaults

Issue: `yoda-0044`
Path: `yoda/project/issues/yoda-0044-padronizar-front-matter-sem-defaults-no-template.md`

Foi centralizada uma ordem canonica unica para metadata de issue e a serializacao de front matter passou a preservar essa ordem de forma deterministica. O template `yoda/templates/issue.md` foi reduzido para shell de front matter vazio (`---`/`---`), deixando o preenchimento totalmente a cargo dos scripts. `issue_add.py`, `todo_update.py` e `init.py --reconcile-layout` foram ajustados para emitir metadata ordenada com politica de omissao de opcionais vazios, e os testes foram atualizados para cobrir ordem fixa, ausencia de defaults e posicionamento relativo de `status`, `pending_reason` e `depends_on`.