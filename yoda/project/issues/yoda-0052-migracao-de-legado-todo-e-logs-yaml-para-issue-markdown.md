---
schema_version: '2.00'
id: yoda-0052
status: done
depends_on:
- yoda-0051
title: Migracao de legado TODO e logs YAML para issue markdown
description: Criar migracao em update.py para converter TODO.<dev>.yaml e yoda/logs/*.yaml
  para o modelo 0.3.0 baseado em issue markdown unica.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:42-03:00'
updated_at: '2026-03-06T18:59:30-03:00'
---

# yoda-0052 - Migracao de legado TODO e logs YAML para issue markdown

## Summary
Implementar a migracao dos artefatos legados para o formato unificado de issue markdown 0.3.0. A migracao deve preservar historico essencial e permitir execucao idempotente.

## Context
Sem migracao, o novo fluxo quebra instalacoes existentes que ainda usam TODO YAML e logs YAML separados.

## Objective
Fornecer caminho seguro de upgrade para 0.3.0 sem perda de rastreabilidade.

## Scope
- Implementar migracao no `yoda/scripts/init.py` (nao no `update.py` legado).
- Converter TODO YAML para metadados em issue markdown com `schema_version: '2.00'`.
- Consolidar entradas de `yoda/logs/*.yaml` em `## Flow log` no markdown com formato de linha unico.
- Adaptar scripts do fluxo para operar no modelo markdown 2.00 sem dependencia de TODO YAML.
- Remover `TODO.<dev>.yaml` e logs YAML somente apos migracao total bem-sucedida.

## Out of scope
- Otimizacoes de performance fora do necessario.
- Refatoracoes nao relacionadas ao processo de migracao.
- Mudancas de UX do agente alem do runbook.

## Requirements
- `update.py` permanece responsavel por backup; a migracao ocorre no `init.py` atualizado.
- Se `TODO.<dev>.yaml` nao existir, considerar workspace ja migrado e nao executar conversao.
- Se `TODO.<dev>.yaml` existir, executar conversao para markdown 2.00 e remover arquivo apenas ao final com sucesso total.
- Migrar logs legados substituindo quebra de linha por ` | ` (espacos antes/depois do pipe).
- Migrar logs apenas quando a secao `## Flow log` ainda nao existir na issue; se existir, nao migrar nada para aquela issue.
- Apos migracao, scripts (exceto `init.py`) devem operar somente com `schema_version: '2.00'`.
- `init.py` deve aceitar leitura de `1.02` e `2.00` para tratar fase de transicao.

## Acceptance criteria
- [x] `init.py` executa migracao de TODO/log legado para issue markdown 2.00 em fixture realista.
- [x] Logs YAML sao consolidados em `## Flow log` no formato `<timestamp> | <mensagem>`.
- [x] `TODO.<dev>.yaml` e `yoda/logs/*.yaml` sao removidos apenas em sucesso total da migracao.
- [x] Scripts operacionais do fluxo funcionam sem dependencia de TODO YAML apos migracao.
- [x] Scripts (exceto `init.py`) rejeitam layout anterior e operam apenas com schema 2.00.

## Dependencies
Depende de `yoda-0051`.

## Entry points
- path: yoda/scripts/update.py
  type: code
- path: yoda/todos
  type: data
- path: yoda/logs
  type: data
- path: yoda/project/issues
  type: data

## Implementation notes
A migracao e de execucao unica por workspace: inexistencia de `TODO.<dev>.yaml` indica ambiente ja convertido. O `init.py` faz a ponte de transicao (1.02->2.00), enquanto os demais scripts passam a tratar 2.00 como unico layout valido.

## Tests
Cobrir:
- migracao completa com TODO+logs legados presentes;
- caso sem `TODO.<dev>.yaml` (skip deterministico);
- remocao de artefatos legados apenas em sucesso total;
- comportamento quando issue ja possui `## Flow log` (nao migrar entradas);
- validacao de scripts consumindo apenas schema 2.00 apos migracao.

## Risks and edge cases
- Perda de granularidade historica ao consolidar logs.
- Incompatibilidades de timezone/timestamp entre formatos antigos.

## Result log
feat(migration): migrar TODO/log YAML para markdown 2.00 no init e scripts do flow

Foi implementada a migracao legado no `init.py`, convertendo front matter das issues para `schema_version: '2.00'`, incorporando entradas de `yoda/logs/*.yaml` no `## Flow log` com formato compacto de linha e removendo `TODO.<dev>.yaml`/logs YAML somente em sucesso total. Tambem foram adaptados `issue_add.py`, `todo_next.py`, `todo_list.py`, `todo_update.py`, `log_add.py` e validacoes do `issue_index` para operacao markdown-only no schema 2.00 (com `init.py` mantendo ponte de transicao). A suite `python3 -m pytest yoda/scripts/tests` foi executada com `51 passed`.

- **GitHub Issue** :   #3

- **Issue**: `yoda-0052`

- **Path**: `yoda/project/issues/yoda-0052-migracao-de-legado-todo-e-logs-yaml-para-issue-markdown.md`

## Flow log
2026-03-04T20:33:42-03:00 | [yoda-0052] issue_add created | title: Migracao de legado TODO e logs YAML para issue markdown | description: Criar migracao em update.py para converter TODO.<dev>.yaml e yoda/logs/*.yaml para o modelo 0.3.0 baseado em issue markdown unica. | slug: migracao-de-legado-todo-e-logs-yaml-para-issue-markdown | extern_issue_file: external issue linked
2026-03-04T20:34:08-03:00 | [yoda-0052] todo_update | depends_on:  -> yoda-0051
2026-03-06T18:23:43-03:00 | yoda-0052: todo_update status: to-do -> doing
2026-03-06T18:23:53-03:00 | yoda-0052: Study iniciado com leitura da issue e dos scripts update/init para mapear estrategia de migracao TODO/log YAML para markdown.
2026-03-06T18:38:52-03:00 | yoda-0052: Document concluido com decisoes finais de migracao no init.py, schema 2.00, adaptacao de todos os scripts e remocao de artefatos legados em sucesso total.
2026-03-06T18:52:45-03:00 yoda-0052: Implement concluido com migracao no init.py, scripts operando markdown 2.00 e suite yoda/scripts/tests com 51 passed.
2026-03-06T18:59:30-03:00 yoda-0052: Evaluate concluido com ACs validados, Result log preenchido e suite completa com 51 passed.
2026-03-06T18:59:30-03:00 yoda-0052: todo_update status: doing -> done
