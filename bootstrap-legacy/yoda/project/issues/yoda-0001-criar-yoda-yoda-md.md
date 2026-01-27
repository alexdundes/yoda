---
agent: Human
created_at: '2026-01-27T13:32:11-03:00'
depends_on: []
description: Criar o arquivo raiz de instrucoes do agente em yoda/yoda.md para este
  repositorio. O objetivo e definir como o agente entra no YODA Flow e qual fonte
  de verdade deve ler antes de agir.
entrypoints: []
id: yoda-0001
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 10
schema_version: '1.0'
slug: criar-yoda-yoda-md
status: done
tags: []
title: Criar yoda/yoda.md (entrada do agente)
updated_at: '2026-01-27T13:32:33-03:00'
---

# yoda-0001 - Criar yoda/yoda.md

## Summary
Criar o arquivo raiz de instrucoes do agente em yoda/yoda.md para este repositorio. O objetivo e definir como o agente entra no YODA Flow e qual fonte de verdade deve ler antes de agir.

## Context
Este projeto esta usando o YODA Framework para implementar o proprio YODA Framework. Ainda nao existem scripts completos, e o agente precisa de um ponto de entrada claro que substitua yoda.yaml. As specs definem yoda/yoda.md como o arquivo raiz e que AGENTS.md/gemini.md devem apontar para ele.

## Objective
Definir o arquivo yoda/yoda.md com instrucoes claras para um agente com contexto zero, incluindo como identificar o TODO correto, como selecionar a issue prioritaria sem dependencias e como seguir o YODA Flow.

## Scope
- Criar o arquivo yoda/yoda.md.
- Incluir instrucoes basicas de entrada no YODA Flow.
- Descrever a regra de leitura do TODO.alex.md (excecao temporaria) e a migracao futura para `TODO.<dev>.yaml`.

## Out of scope
- Implementar scripts do YODA.
- Criar AGENTS.md/gemini.md (apenas descrever o comportamento esperado).
- Criar outras issues.

## Requirements
- Deve existir uma secao de "Entrada" indicando a frase natural para iniciar o YODA Flow.
- Deve existir uma secao de "Fonte de verdade" apontando para project/specs.
- Deve existir uma secao de "TODO" indicando o uso temporario de yoda/todos/TODO.alex.md.
- Deve deixar claro que a issue prioritaria sem dependencias deve ser selecionada.

## Acceptance criteria
- [ ] O arquivo yoda/yoda.md existe e segue as regras acima.
- [ ] O texto e direto e operacional para um agente com contexto zero.

## Dependencies
None

## Entry points
- path: project/specs/07-agent-entry-and-root-file.md
  type: issue
- path: project/specs/04-todo-dev-yaml-issues.md
  type: issue
- path: yoda/todos/TODO.alex.md
  type: issue

## Implementation notes
- Usar linguagem direta e comandos claros.
- Referenciar o YODA Flow e o processo leve.
- Indicar que os logs deste projeto sao em Markdown.

## Tests
Nao aplicavel.

## Risks and edge cases
- Se o agente nao encontrar TODO.alex.md, deve perguntar ao usuario qual TODO usar.
- Se houver dependencias na issue prioritaria, deve pular para a proxima sem dependencias.

## Result log
Criado o arquivo yoda/yoda.md com instrucoes de entrada, fontes de verdade, uso temporario do TODO.alex.md, regras do fluxo e tratamento de pendencias.

Sugestao de commit:
docs(yoda): add root agent instructions