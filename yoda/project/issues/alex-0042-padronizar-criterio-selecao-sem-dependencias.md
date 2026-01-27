---
schema_version: "1.0"
id: alex-0042
title: Padronizar criterio de selecao sem dependencias
slug: padronizar-criterio-selecao-sem-dependencias
description: Substituir "without dependencies" por "with all dependencies resolved" em yoda/yoda.md e specs.
status: done
priority: 5
lightweight: false
agent: Codex
depends_on: []
pending_reason: ""
created_at: "2026-01-26T21:02:48-03:00"
updated_at: "2026-01-26T21:03:39-03:00"
entrypoints:
  - path: yoda/yoda.md
    type: doc
  - path: project/specs/07-agent-entry-and-root-file.md
    type: doc
  - path: project/specs/summary.md
    type: doc
tags: []
origin:
  system: ""
  external_id: ""
  requester: ""
---

# alex-0042 - Padronizar criterio de selecao sem dependencias

## Summary
Substituir a expressao "highest-priority issue without dependencies" por uma formulacao que deixe claro que dependencias resolvidas sao aceitaveis. A frase recomendada e "highest-priority selectable issue (with all dependencies resolved)".

## Context
A expressao "without dependencies" pode ser interpretada como depends_on vazio, o que conflita com as regras de selecao baseadas em dependencias resolvidas.

## Objective
Padronizar a linguagem em yoda/yoda.md e nas specs para evitar ambiguidades.

## Scope
- Atualizar textos em yoda/yoda.md.
- Atualizar textos em project/specs/07-agent-entry-and-root-file.md.
- Atualizar o resumo em project/specs/summary.md.

## Out of scope
- Alterar regras de selecao ou logica de prioridade.

## Requirements
- Usar a frase "highest-priority selectable issue (with all dependencies resolved)" nos pontos relevantes.
- Remover ocorrencias de "without dependencies" ligadas ao criterio de selecao.

## Acceptance criteria
- [ ] yoda/yoda.md usa a nova frase nos trechos de entrada e selecao.
- [ ] 07-agent-entry-and-root-file.md usa a nova frase.
- [ ] summary.md usa a nova frase.

## Dependencies
None.

## Entry points
- path: yoda/yoda.md
  type: doc
- path: project/specs/07-agent-entry-and-root-file.md
  type: doc
- path: project/specs/summary.md
  type: doc

## Implementation notes
- Ajustar frases correlatas que mencionam "next issue without dependencies" para manter consistencia.

## Tests
Not applicable.

## Risks and edge cases
- Nenhum; apenas alteracao textual.

## Result log
Texto padronizado para “highest-priority selectable issue (with all dependencies resolved)” em yoda/yoda.md e specs relacionadas.

docs: padronizar criterio de selecao de issues

Issue: `alex-0042`
Path: `yoda/project/issues/alex-0042-padronizar-criterio-selecao-sem-dependencias.md`
