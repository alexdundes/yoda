---
schema_version: '1.02'
id: yoda-0054
status: to-do
depends_on:
- yoda-0052
- yoda-0053
- yoda-0055
- yoda-0056
- yoda-0057
title: Validacao end to end e preparacao de release 0.3.0
description: Cobrir testes de selecao deterministica, retomada por fase e migracao
  de dados, garantindo criterios de aceite para empacotamento da versao 0.3.0.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:42-03:00'
updated_at: '2026-03-04T20:59:15-03:00'
---

# yoda-0054 - Validacao end to end e preparacao de release 0.3.0

## Summary
Consolidar validacao tecnica e operacional do novo fluxo 0.3.0 antes da release. O foco e garantir determinismo, migracao confiavel e aderencia aos criterios da issue externa.

## Context
Sem uma etapa final de integracao, mudancas grandes em schema e fluxo podem entrar em release com quebras ocultas.

## Objective
Assegurar prontidao de release 0.3.0 com testes de ponta a ponta e checklist objetivo.

## Scope
- Executar testes de selecao deterministica e transicoes por fase.
- Validar migracao legado -> 0.3.0 em cenarios representativos.
- Validar documentacao final e runbooks compactos.
- Preparar checklist de release e versao.

## Out of scope
- Novas features fora do escopo 0.3.0.
- Refatoracoes oportunisticas apos freeze.
- Alteracoes grandes em UX de comandos.

## Requirements
- Cobertura de testes deve incluir casos felizes e falhas criticas.
- Checklist final deve mapear criterios de aceite da issue externa #3.
- Preparacao de release deve respeitar fluxo oficial de empacotamento.

## Acceptance criteria
- [ ] Suite de testes relevante executa sem falhas para fluxo 0.3.0.
- [ ] Cenarios de migracao validam ausencia de perda de dados chave.
- [ ] Checklist de release 0.3.0 esta completo e aprovado.

## Dependencies
Depende de `yoda-0052` e `yoda-0053`.

## Entry points
- path: yoda/scripts/tests
  type: code
- path: project/specs
  type: doc
- path: yoda/yoda.md
  type: doc
- path: CHANGELOG.yaml
  type: data

## Implementation notes
Executar apos conclusao das issues anteriores para reduzir retrabalho de validacao.

## Tests
Executar testes unitarios/integracao dos scripts afetados e validar dry-run de migracao.

## Risks and edge cases
- Falso positivo de prontidao por cobertura incompleta de migracao.
- Divergencia entre comportamento real e runbook publicado.

## Result log