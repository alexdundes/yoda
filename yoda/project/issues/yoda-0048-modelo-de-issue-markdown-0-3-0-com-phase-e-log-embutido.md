---
schema_version: '1.02'
id: yoda-0048
status: to-do
depends_on:
- yoda-0047
title: Modelo de issue markdown 0.3.0 com phase e log embutido
description: Especificar front matter e estrutura de log no proprio arquivo .md da
  issue, com formato legivel para humanos e edicao deterministica por script.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:41-03:00'
updated_at: '2026-03-04T20:34:07-03:00'
---

# yoda-0048 - Modelo de issue markdown 0.3.0 com phase e log embutido

## Summary
Definir o formato canonico da issue markdown para 0.3.0, incluindo estado de fase e historico operacional no mesmo arquivo. O foco e garantir leitura humana simples e escrita deterministica por script.

## Context
Hoje metadados e historico ficam separados em TODO YAML e log YAML, gerando duplicidade e fragilidade em sincronizacao.

## Objective
Estabelecer esquema e formato unificado de issue para eliminar dependencia de multiplos artefatos de estado.

## Scope
- Definir campo de fase (`Study|Document|Implement|Evaluate`) no front matter.
- Definir secao de historico/log no corpo da issue.
- Definir ordenacao de campos e regras de serializacao deterministica.
- Definir regras de compatibilidade para leitura de arquivos antigos.
- Definir que dependencias ficam apenas em `depends_on` no front matter, removendo a secao `## Dependencies` do corpo.
- Definir que o identificador e derivado do nome do arquivo, removendo `id` do front matter.

## Out of scope
- Implementar parser/leitor.
- Implementar migrador.
- Alterar comportamento de selecao de issue.

## Requirements
- Formato deve manter legibilidade para humano sem perder previsibilidade para script.
- Campos obrigatorios e opcionais devem estar explicitamente definidos.
- Secao de historico deve ter regra de append deterministico.
- Dependencias devem ter fonte unica no front matter (`depends_on`), sem redundancia textual no corpo.
- O campo `id` nao deve existir no front matter 0.3.0.

## Acceptance criteria
- [ ] Existe definicao completa do front matter 0.3.0 com `phase`.
- [ ] Existe definicao formal da secao de historico/log embutido.
- [ ] Existe regra de ordenacao e normalizacao para escrita deterministica.
- [ ] O modelo 0.3.0 nao inclui secao `## Dependencies` no corpo da issue.
- [ ] O modelo 0.3.0 nao inclui `id` no front matter e define derivacao de ID por nome de arquivo.

## Dependencies
Depende de `yoda-0047`.

## Entry points
- path: project/specs
  type: doc
- path: yoda/templates/issue.md
  type: template
- path: yoda/project/extern_issues/github-3.json
  type: data

## Implementation notes
Priorizar formato com diffs pequenos para facilitar review e merges.

## Tests
Definir fixtures markdown validas/invalidas para validar contrato de schema e secao de historico.

## Risks and edge cases
- Secao de historico pouco estruturada pode dificultar parse.
- Campos novos sem defaults claros podem quebrar scripts existentes.

## Result log
