---
created_at: '2026-02-26T18:50:40-03:00'
depends_on: []
description: 'Substituir origin.system, origin.external_id e origin.requester por
  um único campo extern_issue_file com caminho relativo para o JSON da issue externa
  (ex.: ../github-2.json).'
id: yoda-0042
origin:
  external_id: '2'
  requester: ''
  system: github
pending_reason: ''
priority: 5
schema_version: '1.01'
slug: simplificar-origem-externa-para-extern-issue-file
status: to-do
title: Simplificar origem externa para extern_issue_file
updated_at: '2026-02-26T18:50:40-03:00'
---

# yoda-0042 - Simplificar origem externa para extern_issue_file

## Summary
Simplificar o modelo de rastreabilidade de origem externa em issues internas do YODA. Em vez do bloco `origin` com `system`, `external_id` e `requester`, adotar um único campo `extern_issue_file` apontando para o JSON externo salvo em `yoda/project/extern-issues/`. O valor deve ser um caminho relativo ao arquivo de issue interna (exemplo: `../extern-issues/github-2.json`).

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
- Definir e implementar migracao/reconciliacao para arquivos existentes.

## Out of scope
- Alterar formato do JSON externo em `yoda/project/extern-issues/*.json`.
- Reescrever historico de logs antigos alem do necessario para compatibilidade.
- Mudancas nao relacionadas ao modelo de origem externa.

## Requirements
- O front matter de issue interna deve suportar `extern_issue_file` (string).
- `extern_issue_file` deve apontar para caminho relativo a partir de `yoda/project/issues/`.
- Exemplo valido esperado: `../extern-issues/github-2.json`.
- Campos `origin.system`, `origin.external_id` e `origin.requester` devem ser removidos do schema operacional.
- Fluxos sem origem externa devem manter `extern_issue_file` vazio.
- O fluxo de update/migracao deve tratar arquivos legados com `origin.*`.

## Acceptance criteria
- [ ] `issue_add.py --help` e docs relevantes deixam claro o novo contrato com `extern_issue_file`.
- [ ] Nova issue criada com `--extern-issue 2` grava `extern_issue_file` relativo para o JSON externo correspondente.
- [ ] Front matter de novas issues nao inclui mais `origin.system`, `origin.external_id` e `origin.requester`.
- [ ] Validacoes aceitam formato novo e rejeitam combinacoes invalidas.
- [ ] Fluxo de migracao/reconciliacao converte arquivos legados `origin.*` para `extern_issue_file`.
- [ ] Suite de testes cobre criacao, validacao e migracao.

## Dependencies
`github #2` (origem externa)

## Entry points
- path: yoda/project/extern-issues/github-2.json
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
Esta mudanca e de schema/layout e deve ser tratada como `breaking` por remover campos existentes e introduzir novo contrato. Deve incluir bump de major schema e handling de migracao em `yoda/scripts/update.py`, seguido de reconciliacao por `yoda/scripts/init.py` conforme politica yoda-0038.

## Tests
- Adicionar/ajustar testes de `issue_add.py` para persistencia de `extern_issue_file`.
- Adicionar/ajustar testes de validacao de TODO/issue para novo campo.
- Adicionar teste de migracao (`update.py`) cobrindo conversao de `origin.*` para `extern_issue_file`.
- Rodar `python3 -m pytest yoda/scripts/tests`.

## Risks and edge cases
- Caminho relativo incorreto quebrar rastreabilidade entre issue interna e JSON externo.
- Casos legados sem JSON externo existente exigirem fallback/erro explicito.
- Regressao em scripts que ainda leem `origin.*` implicitamente.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
