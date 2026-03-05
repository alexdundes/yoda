---
schema_version: '1.02'
id: yoda-0052
status: to-do
depends_on:
- yoda-0051
title: Migracao de legado TODO e logs YAML para issue markdown
description: Criar migracao em update.py para converter TODO.<dev>.yaml e yoda/logs/*.yaml
  para o modelo 0.3.0 baseado em issue markdown unica.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:42-03:00'
updated_at: '2026-03-04T20:34:08-03:00'
---

# yoda-0052 - Migracao de legado TODO e logs YAML para issue markdown

## Summary
Implementar a migracao dos artefatos legados para o formato unificado de issue markdown 0.3.0. A migracao deve preservar historico essencial e permitir execucao idempotente.

## Context
Sem migracao, o novo fluxo quebra instalacoes existentes que ainda usam TODO YAML e logs YAML separados.

## Objective
Fornecer caminho seguro de upgrade para 0.3.0 sem perda de rastreabilidade.

## Scope
- Definir e implementar conversao de TODO YAML para metadados em issue markdown.
- Consolidar entradas de log YAML no historico embutido da issue.
- Integrar migracao ao fluxo de `yoda/scripts/update.py`.
- Garantir operacao idempotente com dry-run.

## Out of scope
- Otimizacoes de performance fora do necessario.
- Refatoracoes nao relacionadas ao processo de migracao.
- Mudancas de UX do agente alem do runbook.

## Requirements
- Migracao nao pode sobrescrever dados sem backup/estrategia de seguranca.
- Deve existir sinalizacao clara do que foi migrado.
- Deve ser possivel reexecutar sem duplicar historico.

## Acceptance criteria
- [ ] Conversao de TODO/log legado para issue markdown funciona em fixture realista.
- [ ] Execucao repetida nao duplica registros (idempotencia).
- [ ] `update.py` documenta e executa caminho oficial de migracao 0.3.0.

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
Priorizar migracao incremental com checkpoints claros para rollback manual.

## Tests
Criar testes de migracao com fixtures de multiplos cenarios (com/sem dependencias, com/sem log).

## Risks and edge cases
- Perda de granularidade historica ao consolidar logs.
- Incompatibilidades de timezone/timestamp entre formatos antigos.

## Result log
