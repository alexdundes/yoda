---
schema_version: '1.02'
id: yoda-0049
status: to-do
depends_on:
- yoda-0048
title: Camada de leitura deterministica baseada apenas em issues markdown
description: Implementar leitura e indexacao de yoda/project/issues/*.md para montar
  estado em memoria sem dependencia de TODO.<dev>.yaml.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:41-03:00'
updated_at: '2026-03-04T20:34:07-03:00'
---

# yoda-0049 - Camada de leitura deterministica baseada apenas em issues markdown

## Summary
Construir a camada de leitura que indexa issues markdown como fonte unica de estado do fluxo. Essa camada sera a base para selecao, transicao e runbooks deterministas.

## Context
A base atual depende do TODO YAML como indice principal. Para 0.3.0, os scripts devem operar diretamente a partir das issues markdown.

## Objective
Entregar API/utilitarios internos que leem front matter e corpo das issues, aplicam validacoes e expoem estado consolidado em memoria.

## Scope
- Ler `yoda/project/issues/*.md` com parse robusto de front matter.
- Normalizar campos obrigatorios e opcionais segundo spec 0.3.0.
- Implementar ordenacao deterministica para selecao.
- Emitir erros claros para arquivos invalidos.

## Out of scope
- Criacao do comando `yoda_flow_next.py`.
- Migracao automatica dos arquivos legados.
- Reescrita de playbook.

## Requirements
- Resultado da leitura deve ser estavel entre execucoes identicas.
- Regras de elegibilidade devem respeitar status, fase e dependencias.
- Falhas de schema devem retornar erro acionavel.

## Acceptance criteria
- [ ] Leitor lista issues e metadados sem uso de `TODO.<dev>.yaml`.
- [ ] Ordenacao/elegibilidade sao deterministicas e cobertas por testes.
- [ ] Erros de parse/schema sao reportados com contexto util.

## Dependencies
Depende de `yoda-0048`.

## Entry points
- path: yoda/scripts/lib
  type: code
- path: yoda/project/issues
  type: data
- path: yoda/scripts/tests
  type: code

## Implementation notes
Criar unidade reutilizavel para evitar duplicacao de parse em comandos futuros.

## Tests
Adicionar testes de leitura com fixtures para casos validos, invalidos e ambiguos.

## Risks and edge cases
- Arquivos parcialmente preenchidos podem quebrar parse.
- Dependencias ciclicas precisam ser detectadas de forma previsivel.

## Result log
