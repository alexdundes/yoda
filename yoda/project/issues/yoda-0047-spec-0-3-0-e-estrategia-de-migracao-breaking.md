---
schema_version: '2.00'
status: done
title: Spec 0.3.0 e estrategia de migracao breaking
description: Definir em project/specs o redesenho 0.3.0 do YODA Flow, incluindo escopo
  breaking, compatibilidade temporaria e plano de migracao deterministico.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:41-03:00'
updated_at: '2026-03-04T22:26:56-03:00'
---

# yoda-0047 - Spec 0.3.0 e estrategia de migracao breaking

## Summary
Definir a base documental da versao 0.3.0 como mudanca breaking do YODA Flow. A issue estabelece o contrato de dados/processo alvo, estrategia de compatibilidade temporaria e plano de migracao que orienta as issues seguintes.

## Context
O fluxo atual depende de TODO YAML, issue markdown e log YAML separados. Esse desenho aumenta passos manuais, custo de contexto e chance de inconsistencias entre artefatos.

## Objective
Consolidar o desenho oficial de 0.3.0 com regras normativas para guiar implementacao deterministica e migracao segura.

## Scope
- Atualizar specs de fluxo, estado de fase e runbooks compactos.
- Definir que a fonte canonica de trabalho migra para issue markdown unica.
- Definir plano de migracao e janela de compatibilidade temporaria.
- Registrar classificacao como breaking para release 0.3.0.
- Prever na documentacao 0.3.0 a padronizacao de `Entry points` em markdown legivel (desdobrada em `yoda-0055`).
- Prever na documentacao 0.3.0 a remocao da secao `## Dependencies` do corpo da issue, mantendo apenas `depends_on` no front matter (desdobrada em `yoda-0056`).
- Prever na documentacao 0.3.0 a remocao de `id` do front matter, com derivacao de ID pelo nome do arquivo (desdobrada em `yoda-0057`).
- Definir contrato de `phase` condicional: existe apenas quando `status=doing`.
- Definir contrato do `yoda_flow_next.py` como comando implicito de proximo passo, com runbook obrigatorio em `md` e `json`.
- Formalizar `todo_update.py` e `log_add.py` como scripts permanentes (nao temporarios de migracao).
- Remover `todo_reorder.py` do contrato 0.3.0 por perda de sentido no modelo baseado em issue markdown.
- Formalizar logs compactos de 1 linha para fluxo e scripts auxiliares.
- Formalizar que `--check` e `--apply` ficam no `init.py` atualizado apos update.

## Out of scope
- Implementacao de scripts.
- Execucao da migracao em dados reais.
- Ajustes de testes alem do necessario para validar a especificacao.

## Requirements
- Especificacao deve declarar novo fluxo de fases com estado persistente.
- Deve existir secao explicita de migracao do modelo legado.
- Deve existir secao de deprecacoes e compatibilidade.
- Deve preservar rastreabilidade com issue externa #3.
- A baseline documental deve citar a melhoria de renderizacao de `Entry points` como parte do pacote 0.3.0.
- A baseline documental deve definir `depends_on` no front matter como unica fonte de dependencias, sem duplicacao no corpo da issue.
- A baseline documental deve definir derivacao de ID por nome de arquivo como fonte unica, sem `id` no front matter.
- A baseline documental deve definir `phase` apenas para status `doing`; outros status nao serializam `phase`.
- `yoda_flow_next.py` deve operar sem subcomandos, sempre resolvendo apenas o proximo passo deterministico.
- A saida `md` e `json` de `yoda_flow_next.py` deve conter runbook do proximo passo em uma linha curta.
- Em bloqueios, `yoda_flow_next.py` nao deve mutar estado e deve instruir uso de `todo_update.py`.
- `todo_update.py` deve aceitar ajuste de `phase` e registrar log direto em uma linha.
- `log_add.py` deve permanecer como mecanismo oficial para logs fora do YODA Flow, com mensagem de uma linha.
- `todo_next.py` deve ser removido no 0.3.0.
- `todo_reorder.py` deve ser removido no 0.3.0.
- `todo_update.py` e `log_add.py` devem permanecer scripts oficiais do framework.

## Acceptance criteria
- [x] `project/specs` documenta o alvo 0.3.0 com linguagem normativa.
- [x] A mudanca e marcada como breaking com orientacao de migracao.
- [x] Nao ha conflitos entre resumo, specs detalhadas e playbook.
- [x] A documentacao base 0.3.0 antecipa explicitamente a mudanca de `Entry points` (issue `yoda-0055`).
- [x] A documentacao base 0.3.0 antecipa explicitamente a remocao da secao `## Dependencies` do corpo (issue `yoda-0056`).
- [x] A documentacao base 0.3.0 antecipa explicitamente a remocao de `id` no front matter (issue `yoda-0057`).
- [x] A documentacao base 0.3.0 define `phase` condicional (somente em `doing`).
- [x] A documentacao base 0.3.0 define `yoda_flow_next.py` implicito com runbook obrigatorio em `md` e `json`.
- [x] A documentacao base 0.3.0 define bloqueios sem mutacao automatica e instrucao objetiva para `todo_update.py`.
- [x] A documentacao base 0.3.0 remove `todo_next.py` e mantem `todo_update.py` + `log_add.py` como scripts permanentes.
- [x] A documentacao base 0.3.0 remove `todo_reorder.py` do contrato de scripts.
- [x] A documentacao base 0.3.0 define logs compactos de uma linha para fluxo e scripts auxiliares.
- [x] A documentacao base 0.3.0 explicita que `--check` e `--apply` ficam no `init.py` atualizado apos update.


## Entry points
- `project/specs`
- `yoda/yoda.md`
- `yoda/project/extern_issues/github-3.json`
- `yoda/scripts/init.py`

## Implementation notes
Document First obrigatorio: especificacao vem antes de qualquer alteracao em scripts.

## Tests
Definir na documentacao os cenarios minimos de validacao para 0.3.0:
- transicao feliz por fases com avancos unitarios;
- bloqueio por dependencia com instrucao de `todo_update.py`;
- `phase` presente apenas em `doing`;
- ausencia de `id` no front matter com derivacao por filename;
- ausencia de `## Dependencies` no corpo;
- `Entry points` renderizando como lista simples;
- `todo_update.py` atualizando `phase` com log de uma linha;
- `log_add.py` registrando contexto fora do flow com log de uma linha;
- update preservando backup e executando `init.py` atualizado para `--check/--apply`.

## Risks and edge cases
- Ambiguidade de contrato pode causar implementacoes divergentes.
- Escopo largo sem fatiamento pode travar execucao do fluxo.

## Result log
docs(specs): consolidar contrato 0.3.0 do YODA Flow

A fase Implement/Evaluate da `yoda-0047` consolidou as especificacoes e o playbook para o modelo 0.3.0: fluxo deterministico por fase com `yoda_flow_next.py` implicito, issue markdown como fonte canonica de execucao, remocao de `id` no front matter, remocao da secao `## Dependencies` do corpo, `Entry points` como lista simples, permanencia de `todo_update.py` e `log_add.py`, logs compactos em uma linha e formalizacao de `--check/--apply` no `init.py` atualizado apos update. Tambem foi removido do contrato o `todo_reorder.py` por perda de sentido no novo modelo.

- **GitHub Issue** :   #3

- **Issue**: `yoda-0047`

- **Path**: `yoda/project/issues/yoda-0047-spec-0-3-0-e-estrategia-de-migracao-breaking.md`

## Flow log
- 2026-03-04T20:33:41-03:00 issue_add created | title: Spec 0.3.0 e estrategia de migracao breaking | description: Definir em project/specs o redesenho 0.3.0 do YODA Flow, incluindo escopo breaking, compatibilidade temporaria e plano de migracao deterministico. | slug: spec-0-3-0-e-estrategia-de-migracao-breaking | extern_issue_file: external issue linked
- 2026-03-04T21:10:11-03:00 todo_update | status: to-do -> doing
- 2026-03-04T21:56:20-03:00 Document phase updated with final 0.3.0 decisions: phase conditional, implicit yoda_flow_next, permanent todo_update/log_add, one-line logs, check/apply in init.
- 2026-03-04T22:16:13-03:00 Removed todo_reorder.py from 0.3.0 documentation contract and specs index.
- 2026-03-04T22:26:56-03:00 Evaluate completed: ACs checked, result log finalized, issue ready to close.
- 2026-03-04T22:26:56-03:00 todo_update | status: doing -> done
- 2026-03-04T22:32:20-03:00 Removed project/specs/summary.md and cleaned references; kept yoda/yoda.md unchanged by request.
- 2026-03-05T07:51:35-03:00 Updated yoda-0048 Document text with finalized definitions for points 1, 2, and 3.
- 2026-03-05T07:54:25-03:00 Applied yoda-0048 Implement updates to issue-model docs/template (Flow log, Entry points, init check/apply normalization).
- 2026-03-05T11:45:51-03:00 Evaluate of yoda-0048 completed with issue-model contract definitions and AC closure.
- 2026-03-06T16:33:20-03:00 Started Study for yoda-0049 to map undefined points before Document.
- 2026-03-06T16:33:31-03:00 yoda-0049 Study completed with summary and undefined points list for definition before Document.
- 2026-03-06T16:33:40-03:00 Corrected yoda-0049 status back to doing to keep Study active.
- 2026-03-06T16:39:24-03:00 Logged yoda-0049 Study decisions (1-7,9,10 accepted; point 8 pending clarification).
- 2026-03-06T16:41:24-03:00 Updated yoda-0049 Document with finalized Study decisions and output-contract definition.
- 2026-03-06T16:52:29-03:00 Implemented yoda-0049 code layer (issue_index + tests) and validated with pytest.
- 2026-03-06T16:54:25-03:00 yoda-0049 evaluated and closed with deterministic issue-index implementation.
- 2026-03-06T16:56:10-03:00 Started Study for yoda-0050 to define implicit yoda_flow_next selection and runbook behavior.
- 2026-03-06T17:16:32-03:00 Updated yoda-0050 Document with closed Study decisions for deterministic selection and runbook output.
- 2026-03-06T17:25:48-03:00 Implemented yoda-0050 code and tests (yoda_flow_next) with deterministic selection and readable runbook output.
- 2026-03-06T17:30:24-03:00 yoda-0050 evaluated and closed with deterministic yoda_flow_next implementation.
- 2026-03-06T17:31:43-03:00 checkpoint de Evaluate sem alvo ativo; yoda-0050 permanece done; proxima selecionavel yoda-0051.
