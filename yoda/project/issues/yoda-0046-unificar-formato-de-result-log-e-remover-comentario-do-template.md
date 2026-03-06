---
schema_version: '2.00'
id: yoda-0046
status: done
title: Unificar formato de Result log e remover comentario do template
description: Remover comentario instrucional do Result log no template e alinhar o
  formato do Evaluate no yoda/yoda.md, com linha de issue externa condicional quando
  houver vinculo.
priority: 5
extern_issue_file: ../extern_issues/github-2.json
created_at: '2026-02-26T19:27:28-03:00'
updated_at: '2026-03-03T15:05:09-03:00'
---

# yoda-0046 - Unificar formato de Result log e remover comentario do template

## Summary
Remover o comentario instrucional do bloco `Result log` no template de issue para evitar que ele seja mantido acidentalmente por agentes durante Evaluate. Unificar o formato de `Result log` entre template e playbook (`yoda/yoda.md`) para eliminar conflito de instrucoes. Definir regra condicional para a linha de issue externa: so deve aparecer quando a issue interna estiver associada a uma issue externa.

## Context
Foi observado comportamento recorrente em que o comentario HTML do template nao e removido no fechamento da issue. Alem disso, o formato de `Result log` no template e no playbook Evaluate nao esta alinhado, gerando saidas inconsistentes. Essa divergencia aumenta retrabalho e dificulta padronizacao de logs de conclusao.

## Objective
Padronizar `Result log` com um unico formato oficial, remover comentario residual do template e tornar explicita a regra de emissao condicional da linha `GitLab|GitHub Issue`.

## Scope
- Remover comentario instrucional do `Result log` em `yoda/templates/issue.md`.
- Atualizar `yoda/yoda.md` (fase Evaluate) com o formato oficial de `Result log`.
- Garantir que o template e o playbook usem o mesmo formato.
- Definir regra condicional: linha `- **<GitLab|GitHub> Issue** :   #NNN` apenas quando houver associacao externa.
- Ajustar orientacoes de fluxo para manter `#NNN` quando houver issue externa, permitindo vinculacao no provedor.

## Out of scope
- Alterar a estrutura de outras secoes da issue fora de `Result log`.
- Mudar comportamento de scripts de fechamento alem do necessario para respeitar o formato padrao.
- Mudancas de schema nao relacionadas ao tema de log de resultado.

## Requirements
- O template de issue deve manter a secao `Result log` vazia (apenas o heading), sem comentario HTML e sem formato preenchido.
- O playbook Evaluate deve declarar este formato unico:
  - `<First line: conventional commit message.>`
  - linha em branco
  - `<descricao do que foi feito>`
  - linha em branco
  - `- **<GitLab|GitHub> Issue** :   #NNN` (somente quando houver issue externa associada)
  - linha em branco
  - `- **Issue**: \`<ID>\``
  - linha em branco
  - `- **Path**: \`<issue path>\``
- A linha `GitLab|GitHub Issue` so deve ser emitida quando existir `extern_issue_file` no front matter da issue.
- Quando houver issue externa associada, a linha deve incluir `#NNN` obrigatoriamente, derivando `NNN` do nome do arquivo externo (ex.: `../extern_issues/github-2.json` -> `#2`).
- Quando nao houver issue externa associada, a linha `GitLab|GitHub Issue` deve ser omitida.
- O playbook (`yoda/yoda.md`) deve ser a unica fonte de verdade do formato de `Result log`.

## Acceptance criteria
- [x] `yoda/templates/issue.md` deixa `Result log` vazio (sem comentario e sem placeholders de formato).
- [x] `yoda/yoda.md` (Evaluate) descreve exatamente o formato oficial definido.
- [x] O formato existe apenas no playbook, sem regra duplicada no template.
- [x] Caso com issue externa inclui linha `GitLab|GitHub Issue` com `#NNN`.
- [x] Caso sem issue externa nao inclui a linha `GitLab|GitHub Issue`.

## Dependencies
Origem externa `github #2`.

## Entry points
- path: yoda/templates/issue.md
  type: template
- path: yoda/yoda.md
  type: doc
- path: yoda/project/issues/
  type: data

## Implementation notes
Classificacao sugerida: `subtle` (ajuste de padronizacao e instrucao operacional, sem quebra de compatibilidade funcional esperada). A regra condicional da issue externa deve ser objetiva e testavel para evitar ambiguidade de output.

## Tests
- Validar manualmente/por teste de fixture que o template deixa `Result log` vazio.
- Validar que o playbook Evaluate contem o formato oficial e a regra condicional da issue externa.
- Validar cenario com issue externa (ex.: `yoda-0046` com `extern_issue_file: ../extern_issues/github-2.json`) incluindo linha `GitHub Issue` com `#2`.
- Validar cenario sem issue externa (baseline `yoda-0001` a `yoda-0041`) omitindo a linha `GitLab|GitHub Issue`.

## Risks and edge cases
- Agentes antigos podem continuar reproduzindo formato legado se instrucoes cacheadas forem usadas.
- Omissao indevida da linha externa em issue vinculada pode perder automacao de vinculacao por `#NNN`.
- Inclusao indevida da linha externa em issue sem vinculo pode gerar referencia incorreta.

## Result log
docs(yoda): unificar Result log no playbook e manter template vazio

A secao `## Result log` do template foi esvaziada (apenas heading), e o formato oficial ficou centralizado no `Evaluate` de `yoda/yoda.md`. Tambem foi adicionada instrucao operacional explicita para o agente preencher o `Result log` no markdown da issue antes de rodar `log_add.py` e somente depois concluir com `todo_update.py --status done`.

- **GitHub Issue** :   #2

- **Issue**: `yoda-0046`

- **Path**: `yoda/project/issues/yoda-0046-unificar-formato-de-result-log-e-remover-comentario-do-template.md`

## Flow log
2026-02-26T19:27:28-03:00 | [yoda-0046] issue_add created | title: Unificar formato de Result log e remover comentario do template | description: Remover comentario instrucional do Result log no template e alinhar o formato do Evaluate no yoda/yoda.md, com linha de issue externa condicional quando houver vinculo. | slug: unificar-formato-de-result-log-e-remover-comentario-do-template | priority: 5 | origin: external issue linked
2026-03-03T11:51:27-03:00 | [yoda-0046] todo_update (no changes)
2026-03-03T14:44:56-03:00 | [yoda-0046] todo_update | status: to-do -> doing
2026-03-03T14:53:29-03:00 | [yoda-0046] Document phase updated issue text | - Formalized official Result log sequence including required blank lines between blocks | - Confirmed conditional external line rule: emit only when extern_issue_file exists | - Confirmed external issue number source: derive #NNN from extern_issue_file filename (e.g., github-2.json -> #2) | - Added explicit test scenarios for with-external (yoda-0046) and no-external baseline (yoda-0001..yoda-0041)
2026-03-03T14:55:22-03:00 | [yoda-0046] Implement phase completed | - Replaced Result log AGENT HTML comment in issue template with official final output format | - Added explicit Evaluate Result log contract in yoda/yoda.md, including conditional external issue line behavior based on extern_issue_file | - Documented provider/number derivation rule from extern_issue_file (example: github-2.json -> GitHub #2) | - Added tests for template/manual format contract and conditional external rule messaging | - Validation run: python3 -m pytest yoda/scripts/tests/test_issue_add.py -q (9 passed)
2026-03-03T14:58:44-03:00 | [yoda-0046] Implement refinement applied per review | - Updated template contract: Result log section is now empty (heading only) to avoid duplication/conflict with playbook | - Updated yoda/yoda.md to make Evaluate section the single source of truth for Result log formatting and added explicit template-empty rule | - Updated issue requirements/acceptance/tests text to match new contract (format only in playbook) | - Updated tests to assert template Result log is empty and manual retains official formatting/external-rule guidance | - Validation run: python3 -m pytest yoda/scripts/tests/test_issue_add.py -q (9 passed)
2026-03-03T15:05:09-03:00 | [yoda-0046] Evaluate phase completed | - Acceptance criteria marked as done in issue markdown | - Result log filled in issue markdown using playbook official format | - Confirmed external line included for linked case (GitHub #2 via extern_issue_file) | - Confirmed no format duplication in template (Result log heading kept empty) | - Validation recorded: python3 -m pytest yoda/scripts/tests/test_issue_add.py -q (9 passed)
2026-03-03T15:05:09-03:00 | [yoda-0046] todo_update | status: doing -> done
