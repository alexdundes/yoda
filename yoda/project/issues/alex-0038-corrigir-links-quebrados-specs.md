---
schema_version: "1.0"
id: alex-0038
title: Corrigir links quebrados em project/specs
slug: corrigir-links-quebrados-specs
description: Padronizar links para repo-root em project/specs para evitar caminhos invalidos.
status: done
priority: 7
lightweight: false
agent: Codex
depends_on: []
pending_reason: ""
created_at: "2026-01-26T20:44:12-03:00"
updated_at: "2026-01-26T20:45:10-03:00"
entrypoints:
  - path: project/specs/README.md
    type: doc
  - path: project/specs/summary.md
    type: doc
  - path: project/specs/07-agent-entry-and-root-file.md
    type: doc
  - path: project/specs/04-todo-dev-yaml-issues.md
    type: doc
  - path: project/specs/13-yoda-scripts-v1.md
    type: doc
  - path: project/specs/influences/
    type: doc
  - path: AGENTS.md
    type: doc
  - path: gemini.md
    type: doc
tags: []
origin:
  system: ""
  external_id: ""
  requester: ""
---

# alex-0038 - Corrigir links quebrados em project/specs

## Summary
Padronizar os links de arquivos dentro de project/specs para apontarem para o repo-root usando paths absolutos (ex.: /yoda/..., /AGENTS.md). Isso evita links quebrados quando os docs estao em subpastas.

## Context
Hoje, varios arquivos em project/specs usam links relativos com "../" que funcionariam apenas se estivessem um nivel abaixo do repo-root. Como os docs estao em project/specs/ e subpastas, esses links apontam para project/yoda/... e quebram em navegacao no GitHub.

## Objective
Garantir que os links internos em project/specs apontem corretamente para o repo-root, funcionando de qualquer profundidade de pasta.

## Scope
- Atualizar links em project/specs que usam ../ para chegar ao repo-root.
- Padronizar links para /yoda/..., /AGENTS.md, /gemini.md e outras referencias no repo-root.

## Out of scope
- Alterar conteudo tecnico das specs.
- Mudar paths fora de project/specs.

## Requirements
- Substituir links relativos quebrados por links para repo-root usando "/".
- Manter consistencia de formatacao dos links existentes.

## Acceptance criteria
- [ ] Nao existem links do tipo "../yoda/" em project/specs.
- [ ] Nao existem links do tipo "../AGENTS.md" ou "../gemini.md" em project/specs.
- [ ] Navegacao dos links atualizados funciona a partir de subpastas (ex.: project/specs/influences/).

## Dependencies
None.

## Entry points
- path: project/specs/README.md
  type: doc
- path: project/specs/summary.md
  type: doc
- path: project/specs/07-agent-entry-and-root-file.md
  type: doc
- path: project/specs/04-todo-dev-yaml-issues.md
  type: doc
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/influences/
  type: doc

## Implementation notes
- Usar `rg` para localizar links com ../ em project/specs.
- Preferir links absolutos no repo-root (ex.: /yoda/todos/).

## Tests
Not applicable.

## Risks and edge cases
- Links relativos que apontam para caminhos dentro de project/specs devem permanecer relativos se nao forem para o repo-root.

## Result log
Atualizados os links em project/specs para apontarem para o repo-root, substituindo paths relativos ../yoda, ../AGENTS.md e ../gemini.md. Nenhuma alteracao de conteudo tecnico.

Commit sugerido:
chore(specs): corrigir links de repo-root

Issue: alex-0038
Path: yoda/project/issues/alex-0038-corrigir-links-quebrados-specs.md
