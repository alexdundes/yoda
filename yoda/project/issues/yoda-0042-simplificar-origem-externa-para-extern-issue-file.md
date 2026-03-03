---
schema_version: '1.02'
id: yoda-0042
status: done
title: Simplificar origem externa para extern_issue_file
description: "Substituir origin.system, origin.external_id e origin.requester por\
  \ um \xFAnico campo extern_issue_file com caminho relativo para o JSON da issue\
  \ externa (ex.: ../github-2.json)."
priority: 5
extern_issue_file: ../extern_issues/github-2.json
created_at: '2026-02-26T18:50:40-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0042 - Simplificar origem externa para extern_issue_file

## Summary
Simplificar o modelo de rastreabilidade de origem externa em issues internas do YODA. Em vez do bloco `origin` com `system`, `external_id` e `requester`, adotar um único campo `extern_issue_file` apontando para o JSON externo salvo em `yoda/project/extern_issues/`. O valor deve ser um caminho relativo ao arquivo de issue interna (exemplo: `../extern_issues/github-2.json`).

## Context
Hoje a origem externa é distribuida em tres campos, o que aumenta complexidade de leitura, escrita e migracao de schema. Como o JSON externo ja concentra os dados de origem e contexto, manter campos redundantes na issue interna gera duplicacao e risco de inconsistencias. A simplificacao para um ponteiro de arquivo reduz acoplamento e preserva rastreabilidade completa.

## Objective
Definir e implementar o novo contrato de issue interna com `extern_issue_file` como referencia unica de origem externa, removendo os campos `origin.system`, `origin.external_id` e `origin.requester` do schema operacional.

## Scope
- Atualizar specs e contratos para substituir `origin.*` por `extern_issue_file`.
- Atualizar `issue_add.py` para gravar `extern_issue_file` quando houver `--extern-issue`.
- Atualizar validacoes de schema (TODO/issue) para novo campo.
- Ajustar template de issue para refletir o novo front matter.
- Ajustar intake para preencher `extern_issue_file` com caminho relativo correto.
- Nao implementar migracao/reconciliacao automatica para arquivos existentes (abordagem destrutiva para campos legados).

## Out of scope
- Alterar formato do JSON externo em `yoda/project/extern_issues/*.json`.
- Reescrever historico de logs antigos alem do necessario para compatibilidade.
- Mudancas nao relacionadas ao modelo de origem externa.

## Requirements
- O front matter de issue interna deve suportar `extern_issue_file` (string).
- `extern_issue_file` deve apontar para caminho relativo a partir de `yoda/project/issues/`.
- Exemplo valido esperado: `../extern_issues/github-2.json`.
- Campos `origin.system`, `origin.external_id` e `origin.requester` devem ser removidos do schema operacional.
- Fluxos sem origem externa devem manter `extern_issue_file` vazio.
- Nao deve haver migracao automatica via `update.py`/`init.py`; o fluxo passa a usar apenas `extern_issue_file` para novos dados.

## Acceptance criteria
- [ ] `issue_add.py --help` e docs relevantes deixam claro o novo contrato com `extern_issue_file`.
- [ ] Nova issue criada com `--extern-issue 2` grava `extern_issue_file` relativo para o JSON externo correspondente.
- [ ] Front matter de novas issues nao inclui mais `origin.system`, `origin.external_id` e `origin.requester`.
- [ ] Validacoes aceitam formato novo e rejeitam combinacoes invalidas.
- [ ] Nao ha migracao/reconciliacao automatica em `update.py`/`init.py`; abordagem adotada e destrutiva para campos legados.
- [ ] Suite de testes cobre criacao e validacao do novo contrato.

## Dependencies
`github #2` (origem externa)

## Entry points
- path: yoda/project/extern_issues/github-2.json
  type: data
- path: yoda/scripts/issue_add.py
  type: code
- path: yoda/scripts/yoda_intake.py
  type: code
- path: yoda/scripts/lib/validate.py
  type: code
- path: yoda/templates/issue.md
  type: template
- path: yoda/todos/TODO.yoda.yaml
  type: data
- path: yoda/scripts/update.py
  type: code

## Implementation notes
Esta mudanca e de schema/layout e foi classificada como `subtle` para rollout interno, com bump para `schema_version` `1.02` e sem implementar migracao/reconciliacao em `yoda/scripts/update.py`/`yoda/scripts/init.py`.

## Tests
- Adicionar/ajustar testes de `issue_add.py` para persistencia de `extern_issue_file`.
- Adicionar/ajustar testes de validacao de TODO/issue para novo campo.
- Nao adicionar teste de migracao em `update.py` para esta entrega (sem migracao automatica).
- Rodar `python3 -m pytest yoda/scripts/tests`.

## Risks and edge cases
- Caminho relativo incorreto quebrar rastreabilidade entre issue interna e JSON externo.
- Casos legados sem JSON externo existente exigirem fallback/erro explicito.
- Regressao em scripts que ainda leem `origin.*` implicitamente.

## Result log
refactor(yoda): replace origin metadata with extern_issue_file and bump schema to 1.02

Body:
Issue: `yoda-0042`
Path: `yoda/project/issues/yoda-0042-simplificar-origem-externa-para-extern-issue-file.md`

- Atualizadas specs e manual para `extern_issue_file`, pasta `yoda/project/extern_issues/` e schema `1.02`.
- `issue_add.py` passou a gerar `extern_issue_file` relativo (`../extern_issues/<provider>-<NNN>.json`) e removeu flags `--origin-system`/`--origin-requester`.
- Template de issue, validacao e paths de intake/coleta externa foram alinhados ao novo contrato.
- Pasta de dados externos foi renomeada para `yoda/project/extern_issues/`.
- Suite validada com `python3 -m pytest yoda/scripts/tests` (49 passed).