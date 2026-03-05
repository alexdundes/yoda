---
schema_version: '1.02'
id: yoda-0047
status: to-do
title: Spec 0.3.0 e estrategia de migracao breaking
description: Definir em project/specs o redesenho 0.3.0 do YODA Flow, incluindo escopo
  breaking, compatibilidade temporaria e plano de migracao deterministico.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:41-03:00'
updated_at: '2026-03-04T20:33:41-03:00'
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

## Acceptance criteria
- [ ] `project/specs` documenta o alvo 0.3.0 com linguagem normativa.
- [ ] A mudanca e marcada como breaking com orientacao de migracao.
- [ ] Nao ha conflitos entre resumo, specs detalhadas e playbook.
- [ ] A documentacao base 0.3.0 antecipa explicitamente a mudanca de `Entry points` (issue `yoda-0055`).
- [ ] A documentacao base 0.3.0 antecipa explicitamente a remocao da secao `## Dependencies` do corpo (issue `yoda-0056`).
- [ ] A documentacao base 0.3.0 antecipa explicitamente a remocao de `id` no front matter (issue `yoda-0057`).

## Dependencies
None.
Relacionada: `yoda-0055` (desdobramento de UX documental previsto no pacote 0.3.0).
Relacionada: `yoda-0056` (fonte unica de dependencias via `depends_on` no front matter).
Relacionada: `yoda-0057` (fonte unica de ID via nome do arquivo).

## Entry points
- path: project/specs
  type: doc
- path: yoda/yoda.md
  type: doc
- path: yoda/project/extern_issues/github-3.json
  type: data

## Implementation notes
Document First obrigatorio: especificacao vem antes de qualquer alteracao em scripts.

## Tests
Validacao documental por consistencia entre arquivos de spec e ausencia de contradicoes com o playbook.

## Risks and edge cases
- Ambiguidade de contrato pode causar implementacoes divergentes.
- Escopo largo sem fatiamento pode travar execucao do fluxo.

## Result log
