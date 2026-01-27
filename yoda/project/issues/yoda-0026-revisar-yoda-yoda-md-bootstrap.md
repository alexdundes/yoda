---
agent: Human
created_at: '2026-01-27T13:32:13-03:00'
depends_on: []
description: Revisar as instrucoes em yoda/yoda.md para garantir alinhamento com toda
  a especificacao em project/specs/. O objetivo e remover ambiguidades sobre bootstrap
  (TODOs, logs, ausencia de scripts e hierarquia de fontes de verdade) e, se necessario,
  ajustar project/specs/15-bootstrap.md para refletir regras adicionais.
entrypoints: []
id: yoda-0026
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 6
schema_version: '1.0'
slug: revisar-yoda-yoda-md-bootstrap
status: done
tags: []
title: Revisar yoda/yoda.md com foco no bootstrap
updated_at: '2026-01-27T13:32:38-03:00'
---

# yoda-0026 - Revisar yoda/yoda.md com foco no bootstrap

## Summary
Revisar as instrucoes em yoda/yoda.md para garantir alinhamento com toda a especificacao em project/specs/. O objetivo e remover ambiguidades sobre bootstrap (TODOs, logs, ausencia de scripts e hierarquia de fontes de verdade) e, se necessario, ajustar project/specs/15-bootstrap.md para refletir regras adicionais.

## Context
yoda/yoda.md e o ponto de entrada do agente, mas o repositorio opera em modo bootstrap. As regras de bootstrap estao descritas nas specs e no REPO_INTENT.md, e precisam estar coerentes com as instrucoes operacionais do agente. Caso existam lacunas ou ambiguidades, o ajuste deve ser feito nas specs, especialmente em project/specs/15-bootstrap.md.

## Objective
Alinhar yoda/yoda.md com project/specs/ e, quando necessario, evoluir project/specs/15-bootstrap.md para eliminar ambiguidades no modo bootstrap.

## Scope
- Revisar todo project/specs/ para identificar regras aplicaveis ao bootstrap.
- Ajustar yoda/yoda.md para refletir as regras de bootstrap e a hierarquia de fontes de verdade.
- Se necessario, atualizar project/specs/15-bootstrap.md com regras adicionais para remover ambiguidades.
- Tornar explicitas as excecoes temporarias (TODO em Markdown, logs em Markdown, ausencia de scripts).

## Out of scope
- Alterar specs que nao estejam relacionadas ao bootstrap.
- Criar ou modificar scripts.
- Migrar TODOs ou logs para YAML.

## Requirements
- yoda/yoda.md reflete todas as regras relevantes de project/specs/ para bootstrap.
- A regra de conflito entre project/specs/ e yoda/ fica clara para o agente.
- A regra de uso do TODO em Markdown permanece consistente com as specs.
- Se houver ambiguidade nas specs, project/specs/15-bootstrap.md deve ser atualizado.
- Em bootstrap, nao existe coexistencia entre `TODO.<dev>.md` e `TODO.<dev>.yaml`; um substitui o outro.
- A documentacao de bootstrap e provisoria e deve ser removida quando scripts existirem.

## Acceptance criteria
- [x] yoda/yoda.md explicita o modo bootstrap e suas excecoes, alinhado com project/specs/.
- [x] As instrucoes de entrada do agente permanecem operacionais e sem ambiguidade.
- [x] Nao ha conflito com project/specs/ e REPO_INTENT.md.
- [x] Se ajustes em project/specs/15-bootstrap.md forem necessarios, eles foram aplicados.
- [x] Nao ha regra que permita coexistencia de `TODO.<dev>.md` e `TODO.<dev>.yaml` em bootstrap.
- [x] A condicao provisoria do bootstrap e sua remocao futura estao explicitas nas specs.

## Dependencies
None

## Entry points
- path: yoda/yoda.md
  type: issue
- path: project/specs/README.md
  type: issue
- path: project/specs/15-bootstrap.md
  type: issue
- path: project/specs/07-agent-entry-and-root-file.md
  type: issue
- path: project/specs/00-conventions.md
  type: issue
- path: REPO_INTENT.md
  type: issue

## Implementation notes
- Manter o texto direto e orientado a acao.
- Preservar a regra de nao editar TODOs sem solicitacao explicita.
- Se houver mudancas em project/specs/15-bootstrap.md, garantir consistencia com project/specs/summary.md.
- Evitar adicionar regras sobre front matter de issues durante o bootstrap.

## Tests
Not applicable.

## Risks and edge cases
- Ajustes no texto podem introduzir inconsistencias com outras specs se nao forem revisadas.

## Result log
Alinhei yoda/yoda.md com as regras de bootstrap, explicando a nao coexistencia entre TODO em Markdown e YAML e o fim do bootstrap quando scripts existirem. Atualizei project/specs/15-bootstrap.md para explicitar a regra de nao coexistencia e a remocao futura da documentacao de bootstrap.

Commit:
docs(yoda): clarify bootstrap rules and yoda entry

Issue: yoda-0026
Path: yoda/project/issues/yoda-0026-revisar-yoda-yoda-md-bootstrap.md