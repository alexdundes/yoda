---
agent: Human
created_at: '2026-01-27T13:32:13-03:00'
depends_on: []
description: Padronizar referencias ao path default do TODO (`yoda/todos/TODO.<dev>.yaml`)
  e ao path bootstrap (`yoda/todos/TODO.<dev>.md`).
entrypoints: []
id: yoda-0032
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 6
schema_version: '1.0'
slug: explicitar-path-todo-default
status: done
tags: []
title: Explicitar path default do TODO nas specs
updated_at: '2026-01-27T13:32:39-03:00'
---

# yoda-0032 - Explicitar path default do TODO nas specs

## Summary
Padronizar referencias ao path default do TODO (`yoda/todos/TODO.<dev>.yaml`) e ao path bootstrap (`yoda/todos/TODO.<dev>.md`).

## Context
Alguns arquivos citam `TODO.<dev>.yaml` sem explicitar o path, o que pode gerar suposicoes erradas por agents.

## Objective
Garantir que as specs sempre indiquem o path default completo para o TODO e a excecao de bootstrap.

## Scope
- Atualizar referencias em arquivos de entrada e scripts v1.
- Indicar o path default e o path bootstrap.
- Atualizar todas as ocorrencias encontradas nas specs para padronizar o path.

## Out of scope
- Alterar a estrutura real do repositorio.
- Atualizar README fora das specs.

## Requirements
- Referenciar `yoda/todos/TODO.<dev>.yaml` como default.
- Referenciar `yoda/todos/TODO.<dev>.md` como excecao de bootstrap.
- Usar convencao clara e consistente para indicar paths canonicos.

## Acceptance criteria
- [x] `project/specs/13-yoda-scripts-v1.md` explicita o path default do TODO.
- [x] `project/specs/07-agent-entry-and-root-file.md` explicita o path default do TODO.
- [x] `project/specs/04-todo-dev-yaml-issues.md` explicita o path default do TODO.
- [x] Todas as ocorrencias nas specs foram padronizadas para o path canonico.

## Dependencies
None

## Entry points
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/07-agent-entry-and-root-file.md
  type: doc
- path: project/specs/04-todo-dev-yaml-issues.md
  type: doc

## Implementation notes
- Evitar linguagem ambigua sobre caminhos e defaults.

## Tests
Not applicable.

## Risks and edge cases
- Inconsistencias de path podem causar comportamento divergente em scripts futuros.

## Result log
Specs atualizadas para usar `yoda/todos/TODO.<dev>.yaml` como path default e `yoda/todos/TODO.<dev>.md` no bootstrap, com padronizacao das ocorrencias.

docs(yoda): explicitar path default do TODO nas specs

Issue: `yoda-0032`
Path: `yoda/project/issues/yoda-0032-explicitar-path-todo-default.md`