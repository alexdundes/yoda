---
agent: Human
created_at: '2026-01-27T13:32:14-03:00'
depends_on: []
description: Definir uma spec base para a estrutura e organizacao dos scripts Python
  em `yoda/scripts`, incluindo dependencias, layout e reutilizacao de codigo.
entrypoints: []
id: yoda-0036
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 6
schema_version: '1.0'
slug: definir-estrutura-python-scripts
status: done
tags: []
title: Definir estrutura Python dos scripts YODA
updated_at: '2026-01-27T13:32:40-03:00'
---

# yoda-0036 - Definir estrutura Python dos scripts YODA

## Summary
Definir uma spec base para a estrutura e organizacao dos scripts Python em `yoda/scripts`, incluindo dependencias, layout e reutilizacao de codigo.

## Context
O primeiro script (issue_add.py) precisa de uma base clara para organizacao de arquivos, dependencias e reutilizacao entre comandos. Sem uma spec de estrutura, cada script pode divergir e gerar duplicacao.

## Objective
Criar uma spec em `project/specs` que defina a estrutura Python do projeto de scripts e sirva de base para todos os comandos v1.

## Scope
- Definir layout de arquivos em `yoda/scripts`.
- Definir regras de dependencia (stdlib vs terceiros).
- Definir como compartilhar utilitarios (ex.: parsing, IO, templates, validacao).
- Definir convencoes de CLI e entrada (ex.: `main()`, argparse).

## Out of scope
- Implementar scripts.
- Criar pacotes ou publicar distribuicao.

## Requirements
- Adicionar uma nova spec em `project/specs` com a estrutura do projeto Python.
- Documentar dependencias permitidas e proibidas.
- Documentar padrao de imports e reutilizacao entre scripts.
- Documentar como os scripts acessam templates, TODOs e logs.
- Definir gerenciador de pacotes para dependencias externas.
- Definir padrao de testes (pytest).

## Acceptance criteria
- [x] Nova spec criada em `project/specs` com estrutura Python dos scripts.
- [x] A spec cobre layout, dependencias, reuse e convencoes de CLI.
- [x] A spec lista decisoes em aberto e pontos a validar antes de codificar.

## Dependencies
None

## Entry points
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/05-scripts-and-automation.md
  type: doc

## Implementation notes
- Registrar decisoes em aberto dentro da issue antes de fechar.

## Tests
Not applicable.

## Risks and edge cases
- Sem base comum, scripts podem divergir e dificultar manutencao.

## Open decisions
- Layout exato (ex.: scripts soltos vs pacote interno `yoda/scripts/lib`). (decisao: usar `yoda/scripts/lib`)
- Dependencias externas permitidas (ex.: PyYAML) vs stdlib apenas. (decisao: permitir dependencias externas quando necessario)
- Estrategia de parsing YAML e front matter. (decisao: usar biblioteca dedicada)
- Estrategia de IO atomico e lock. (decisao: nao necessario por ausencia de concorrencia)
- Estrategia de logging e mensagens de erro. (decisao: stdlib `logging`, erros em stderr, verbose ativa DEBUG)
- Estrategia de testes (unittest, pytest, nenhum). (decisao: pytest)
- Gerenciador de pacotes para instalacao em outras maquinas. (decisao: pip + `yoda/scripts/requirements.txt`)

## Result log
Spec criada em `project/specs/17-scripts-python-structure.md` com layout, dependencias, CLI, logging e testes. README atualizado para incluir a nova spec. Tests definidos em `yoda/scripts/tests/` e testes unitarios como obrigatorios.

docs(yoda): definir estrutura python dos scripts

Issue: `yoda-0036`
Path: `yoda/project/issues/yoda-0036-definir-estrutura-python-scripts.md`