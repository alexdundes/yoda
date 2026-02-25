---
created_at: '2026-02-25T19:53:46-03:00'
depends_on: []
description: 'Eliminar o campo agent do modelo YAML e do fluxo operacional, seguindo
  a mesma abordagem usada para lightweight, entrypoints e tags: docs-first, classificacao
  subtle, ajuste de scripts e reconciliacao via init.py --reconcile-layout quando
  aplicavel.'
id: yoda-0041
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 3
schema_version: '1.01'
slug: remover-conceito-de-agent-do-yoda
status: done
title: Remover conceito de agent do YODA
updated_at: '2026-02-25T20:07:45-03:00'
---

# yoda-0041 - Remover conceito de agent do YODA

## Summary
Remover o campo `agent` como parte do schema operacional do YODA (TODO YAML e front matter de issue), alinhando com a simplificacao recente de layout. A mudanca segue abordagem docs-first, classificada como subtle, com migracao/reconciliacao por `init.py --reconcile-layout`.

## Context
Atualmente o campo `agent` ainda aparece como metadado ativo em TODO/issue e em opcoes de CLI (`--agent`). Isso adiciona ruido ao modelo, aumenta superficie de manutencao e conflita com a direcao adotada nas issues anteriores de remocao de campos operacionais nao essenciais.

## Objective
Eliminar o conceito de `agent` como atributo operacional no schema e no fluxo de scripts, preservando historico de logs e garantindo reconciliacao automatizada dos arquivos existentes.

## Scope
- Atualizar specs para remover `agent` do schema/contratos de scripts aplicaveis.
- Remover suporte ao campo `agent` em `issue_add.py`, `todo_update.py`, `todo_list.py` e validacoes correlatas.
- Ajustar template de issue para nao escrever `agent` no front matter.
- Garantir reconciliacao via `init.py --reconcile-layout` para remover `agent` de `TODO.<dev>.yaml` e front matter de `<dev>-NNNN-*.md`.
- Manter classificacao da issue como subtle.

## Out of scope
- Reescrever ou limpar historico antigo de logs onde `agent` aparece em mensagens ja registradas.
- Alterar semantica dos arquivos de entrada (`AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `agent.md`) que sao ponteiros de onboarding.
- Mudancas de versao de schema de log (logs permanecem no schema 1.0).

## Requirements
- Scripts nao devem aceitar `--agent` como entrada operacional.
- `validate.py` nao deve exigir `agent` em item de issue.
- `issue_add.py` nao deve persistir `agent` no TODO nem no front matter da issue.
- `todo_update.py` nao deve alterar `agent` e nao deve registrar diffs desse campo.
- `todo_list.py` nao deve oferecer filtro por `agent`.
- `init.py --reconcile-layout` deve remover `agent` dos artefatos alvo e manter formato valido.

## Acceptance criteria
- [x] `issue_add.py --help`, `todo_update.py --help` e `todo_list.py --help` nao exibem `--agent`.
- [x] `issue_add.py` cria issue sem `agent` no item do TODO e no front matter do Markdown.
- [x] `todo_update.py --agent ...` falha por argumento desconhecido.
- [x] `todo_list.py --agent ...` falha por argumento desconhecido.
- [x] Validacao de TODO aceita item sem `agent`.
- [x] `init.py --reconcile-layout` remove `agent` de `TODO.<dev>.yaml` e dos front matters de issue.
- [x] Suite de testes relevante passa sem regressao.
- [x] Logs existentes nao sao reescritos para remover mencoes historicas de `agent`.

## Dependencies
None.

## Entry points
- path: project/specs/04-todo-dev-yaml-issues.md
  type: schema
- path: project/specs/16-todo-list-script.md
  type: doc
- path: project/specs/18-issue-add-script.md
  type: doc
- path: project/specs/20-todo-update-script.md
  type: doc
- path: yoda/scripts/lib/validate.py
  type: code
- path: yoda/scripts/issue_add.py
  type: code
- path: yoda/scripts/todo_update.py
  type: code
- path: yoda/scripts/todo_list.py
  type: code
- path: yoda/scripts/init.py
  type: code
- path: yoda/templates/issue.md
  type: template
- path: yoda/todos/TODO.yoda.yaml
  type: data

## Implementation notes
- Classificacao: subtle (sem breaking change intencional no fluxo de uso esperado).
- Seguir estrategia de reconciliacao ja adotada: corrigir artefatos existentes via `--reconcile-layout` em vez de remocoes manuais ad hoc.
- Manter compatibilidade com schema atual de TODO/issue em `1.01`.
- Nao alterar schema de logs (`1.0`).

## Tests
- Atualizar testes de parser/CLI para ausencia de `--agent`.
- Atualizar fixtures de TODO/issue para formato sem `agent`.
- Adicionar/ajustar teste de `init.py --reconcile-layout` cobrindo remocao de `agent`.
- Rodar `python3 -m pytest yoda/scripts/tests`.

## Risks and edge cases
- Regressao em validacao se algum caminho ainda exigir `agent` implicitamente.
- Reconciliacao parcial em repositorios com arquivos de issue fora do padrao `<id>-<slug>.md`.
- Divergencia entre specs e implementacao se algum documento contratual nao for atualizado.

## Result log
Remocao completa do campo `agent` do schema operacional (TODO/front matter), flags CLI e validacoes correlatas. Specs contratuais e template foram alinhados. Reconciliacao executada com `init.py --reconcile-layout`, preservando historico de logs e mantendo schema de logs em `1.0`.

refactor(yoda): remove operational agent field from TODO and issue metadata
Issue: `yoda-0041`
Path: `yoda/project/issues/yoda-0041-remover-conceito-de-agent-do-yoda.md`