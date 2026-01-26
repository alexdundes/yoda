---
schema_version: "1.0"
id: alex-0032
title: Explicitar path default do TODO nas specs
slug: explicitar-path-todo-default
description: Padronizar referencias a yoda/todos/TODO.<dev>.yaml e bootstrap.
status: done
priority: 6
lightweight: false
agent: Human
depends_on: []
pending_reason: ""
created_at: "2026-01-26T11:16:29-03:00"
updated_at: "2026-01-26T11:46:30-03:00"
entrypoints: []
tags: [specs, todo]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-0032 - Explicitar path default do TODO nas specs

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

Issue: `alex-0032`
Path: `yoda/project/issues/alex-0032-explicitar-path-todo-default.md`
