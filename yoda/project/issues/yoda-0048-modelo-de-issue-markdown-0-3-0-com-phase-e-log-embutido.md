---
schema_version: '2.00'
status: done
depends_on:
- yoda-0047
title: Modelo de issue markdown 0.3.0 com phase e log embutido
description: Especificar front matter e estrutura de log no proprio arquivo .md da
  issue, com formato legivel para humanos e edicao deterministica por script.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:41-03:00'
updated_at: '2026-03-05T11:45:51-03:00'
---

# yoda-0048 - Modelo de issue markdown 0.3.0 com phase e log embutido

## Summary
Definir o contrato canonico da issue markdown no 0.3.0, incluindo front matter final, formato de log embutido e regra de compatibilidade/migracao centralizada no `init.py`. O foco e garantir legibilidade humana, escrita deterministica e migracao coordenada.

## Context
Hoje metadados e historico ficam separados em TODO YAML e log YAML, gerando duplicidade e fragilidade em sincronizacao.

## Objective
Estabelecer contrato final da issue `.md` para 0.3.0 e explicitar como a transicao do formato legado para o novo formato sera aplicada sem edicoes manuais pontuais.

## Scope
- Definir contrato final do arquivo de issue 0.3.0 (`<dev>-<NNNN>-<slug>.md`) com ID derivado do filename.
- Definir front matter canonico e ordenado:
  - `schema_version`
  - `status`
  - `phase` (somente quando `status=doing`)
  - `depends_on` (opcional, omitido se vazio)
  - `title`
  - `description`
  - `priority`
  - `extern_issue_file` (opcional, omitido se vazio)
  - `created_at`
  - `updated_at`
- Definir que `id` nao existe no front matter.
- Definir corpo canonico sem `## Dependencies` e com `## Entry points` em lista simples (`- <entry point>`).
- Definir secao de log embutido `## Flow log` com append-only de uma linha por entrada.
- Definir estrategia de compatibilidade/migracao no `init.py` (`--check` e `--apply`) para normalizacao estrutural.

## Out of scope
- Implementar parser/leitor nesta issue.
- Implementar comandos de fluxo nesta issue.
- Aplicar manualmente migracao estrutural de issues existentes (fica para `init.py --apply`).

## Requirements
- O formato deve manter legibilidade para humano sem perder previsibilidade para script.
- O contrato deve declarar explicitamente que o ID vem apenas do filename (`<dev>-<NNNN>-<slug>.md`).
- O contrato deve declarar erro bloqueante para filename invalido:
  - `INVALID_ISSUE_FILENAME: expected <dev>-<NNNN>-<slug>.md; got <filename>`
- `phase` so pode existir quando `status=doing`.
- `depends_on` e `extern_issue_file` vazios devem ser omitidos.
- `## Dependencies` nao deve existir no corpo.
- `## Entry points` deve ser apenas lista simples.
- `## Flow log` deve usar uma entrada por linha, compacta, append-only.
- Formato canonico do `## Flow log`:
  - `- <ISO8601> | <source> | <mensagem-curta>`
- A migracao estrutural deve ser centralizada no `init.py`:
  - `--check`: auditar diferencas sem mutacao.
  - `--apply`: normalizar para o contrato 0.3.0.
- Durante transicao, scripts devem ler formatos legado e novo; a conversao estrutural nao deve ser implicita em `todo_update.py`/`log_add.py`.

## Acceptance criteria
- [x] Existe definicao completa do front matter 0.3.0 com `phase` condicional.
- [x] Existe definicao formal de ID derivado por filename e erro canonico de filename invalido.
- [x] Existe definicao formal da secao `## Flow log` com append em uma linha por entrada.
- [x] Existe regra de ordenacao e normalizacao para escrita deterministica.
- [x] O modelo 0.3.0 nao inclui secao `## Dependencies` no corpo da issue.
- [x] O modelo 0.3.0 nao inclui `id` no front matter.
- [x] O modelo 0.3.0 define `## Entry points` apenas como lista simples.
- [x] A migracao estrutural esta definida como responsabilidade do `init.py --apply`, com `--check` sem mutacao.


## Entry points
- `project/specs`
- `yoda/templates/issue.md`
- `yoda/project/extern_issues/github-3.json`

## Implementation notes
Nao executar mudancas estruturais manuais em massa nesta issue. A normalizacao de arquivos existentes deve ocorrer de forma coordenada via `init.py --apply`.

## Tests
Definir cenarios documentais para futura validacao:
- front matter valido/invalidado por `phase` fora de `doing`;
- filename valido/invalido com erro canonico;
- corpo sem `## Dependencies` e com `## Entry points` em lista simples;
- `## Flow log` com entradas de uma linha no formato canonico;
- `init.py --check` sem mutacao e `init.py --apply` aplicando normalizacao esperada.

## Risks and edge cases
- Ambiguidade entre leitura de legado e normalizacao 0.3.0 pode gerar comportamento inconsistente.
- Conversao estrutural parcial fora do `init.py` pode reintroduzir divergencias.

## Result log
docs(model): definir contrato canonico da issue markdown 0.3.0

Foram implementadas as definicoes do modelo de issue 0.3.0 no escopo da `yoda-0048`: contrato de front matter com ordem canonica e `phase` condicional, regra de ID derivado por filename com erro canonico, corpo sem `## Dependencies`, `## Entry points` em lista simples, e secao `## Flow log` com entradas append-only de uma linha (`- <ISO8601> | <source> | <short-message>`). Tambem foi formalizada a estrategia de normalizacao estrutural via `init.py --check/--apply`, sem migracao manual em massa nesta issue.

- **GitHub Issue** :   #3

- **Issue**: `yoda-0048`

- **Path**: `yoda/project/issues/yoda-0048-modelo-de-issue-markdown-0-3-0-com-phase-e-log-embutido.md`

## Flow log
- 2026-03-04T20:33:41-03:00 issue_add created | title: Modelo de issue markdown 0.3.0 com phase e log embutido | description: Especificar front matter e estrutura de log no proprio arquivo.md da issue, com formato legivel para humanos e edicao deterministica por script. | slug: modelo-de-issue-markdown-0-3-0-com-phase-e-log-embutido | extern_issue_file: external issue linked
- 2026-03-04T20:34:07-03:00 todo_update | depends_on: -> yoda-0047
- 2026-03-05T07:31:01-03:00 todo_update | status: to-do -> doing
- 2026-03-05T07:51:35-03:00 Document updated with definitions for issue contract, Flow log format, and init.py check/apply migration policy.
- 2026-03-05T07:54:25-03:00 Implemented 0.3.0 issue model docs: template updated for simple Entry points and Flow log format; specs 04/14 aligned.
- 2026-03-05T11:45:51-03:00 Evaluate completed: ACs checked and result log finalized for issue-model 0.3.0 contract.
- 2026-03-05T11:45:51-03:00 todo_update | status: doing -> done
