---
schema_version: "1.0"
id: alex-0054
title: Sincronizar front matter ao atualizar TODO (todo_update.py)
slug: sincronizar-front-matter-todo-update
description: Garantir que todo_update.py copie metadados do TODO para o front matter da issue.
status: done
priority: 3
lightweight: false
agent: Human
depends_on: [alex-0052]
pending_reason: ""
created_at: "2026-01-27T13:30:03-03:00"
updated_at: "2026-01-27T13:33:13-03:00"
entrypoints: []
tags: [scripts, todo, metadata]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-0054 - Sincronizar front matter ao atualizar TODO (todo_update.py)

## Summary
Atualizar specs e `todo_update.py` para copiar metadados do TODO para o front matter da issue a cada update.

## Context
Hoje o `todo_update.py` atualiza apenas o TODO e o log. O front matter da issue fica desatualizado, contrariando a regra de sincronizacao.

## Objective
Garantir que `todo_update.py` sincronize o front matter da issue com o item do TODO ao final de cada update.

## Scope
- Atualizar a spec de `todo_update.py` para explicitar a sincronizacao.
- Atualizar o script para reescrever o front matter da issue.

## Out of scope
- Implementar outros scripts.
- Alterar o corpo da issue.

## Requirements
- O `todo_update.py` deve atualizar o front matter da issue correspondente.
- Deve falhar se o arquivo de issue nao existir.
- Manter o corpo da issue inalterado.

## Acceptance criteria
- [x] Spec de `todo_update.py` menciona sincronizacao de front matter.
- [x] `todo_update.py` atualiza front matter da issue conforme o TODO.
- [x] Falha com erro claro quando a issue nao existe.

## Dependencies
- alex-0052

## Entry points
- path: project/specs/20-todo-update-script.md
  type: doc
- path: project/specs/04-todo-dev-yaml-issues.md
  type: doc
- path: yoda/scripts/todo_update.py
  type: code

## Implementation notes
- Usar `python-frontmatter` para atualizar apenas o metadata.

## Tests
Not applicable.

## Risks and edge cases
- Metadados divergentes podem causar inconsistencias se a issue estiver ausente.

## Result log
Atualizada a spec e `todo_update.py` para sincronizar o front matter da issue a cada update, mantendo o corpo intacto.

feat(yoda): sincronizar front matter no todo_update

Issue: alex-0054
Path: `yoda/project/issues/alex-0054-sincronizar-front-matter-todo-update.md`
