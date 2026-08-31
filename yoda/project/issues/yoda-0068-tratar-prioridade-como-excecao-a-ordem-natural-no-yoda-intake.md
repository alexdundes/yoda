---
schema_version: '2.01'
status: doing
phase: study
title: Tratar prioridade como excecao a ordem natural no YODA Intake
description: Clarificar na politica de Intake, no runbook do yoda_intake.py e na ajuda
  do issue_add.py que o agente nao deve ranquear um lote de issues nem usar priority
  para codificar a sequencia planejada. Manter priority 5 por padrao, derivar a ordem
  natural da issue em doing, das dependencias reais e da ordem estavel de ID, e alterar
  a prioridade apenas para antecipar ou postergar uma issue contra essa ordem, com
  justificativa relativa. Diferenciar tambem os papeis de todo_list.py, todo_next.py
  e yoda_flow_next.py nos textos operacionais.
priority: 5
extern_issue_file: ../extern_issues/github-010.json
created_at: '2026-08-31T18:03:51-03:00'
updated_at: '2026-08-31T18:20:16-03:00'
---

# yoda-0068 - Tratar prioridade como excecao a ordem natural no YODA Intake

## Summary

Corrigir a semantica de `priority` nos textos operacionais do YODA. A prioridade
deve expressar uma excecao deliberada a ordem natural do backlog, nunca a
posicao de uma issue dentro de um plano de execucao. O agente nao deve ranquear
um lote de issues criadas no mesmo Intake.

## Context

A politica atual em `yoda/yoda.md` diz apenas: "Priority baseline is `5`; change
only with explicit relative justification against open issues". A regra fixa o
valor padrao, mas admite a leitura de que o agente deve avaliar a importancia
relativa de todas as issues e distribuir valores distintos entre elas.

Em uso real, registrado na issue externa GitHub #10, isso levou o agente a
atribuir prioridades decrescentes `10, 9, 8, 7` apenas para representar a
sequencia planejada de um lote. Isso transforma `priority` em numero ordinal do
plano e duplica responsabilidades que ja pertencem a ordem natural das issues e
ao campo `depends_on`.

A auditoria dos textos vigentes mostra onde a ambiguidade vive:

- `yoda/yoda.md` fixa o baseline sem proibir ranqueamento de lote.
- `project/specs/11-yoda-intake.md` pede registrar por que a issue e
  "relatively more/less important" que as abertas. O enquadramento por
  importancia e exatamente o que produz o ranqueamento.
- `issue_add.py --help` repete o baseline sem tratar o caso do lote.
- O runbook emitido por `yoda_intake.py` nao menciona prioridade em nenhum
  ponto. Como e o texto que o agente segue no momento da criacao, essa omissao
  e a lacuna mais provavel de causar o desvio.

Os papeis de `todo_list.py`, `todo_next.py` e `yoda_flow_next.py` ja estao
diferenciados em `project/specs/05-scripts-and-automation.md` e
`project/specs/13-yoda-scripts-v1.md`, mas essa distincao nao aparece nos
runbooks nem nas ajudas operacionais, onde ela e necessaria para impedir que uma
listagem seja lida como plano de execucao.

## Objective

Fazer com que os textos operacionais do YODA definam prioridade como excecao a
ordem natural, de modo que um agente sem contexto previo nao interprete a
criacao de um lote como um exercicio de ranqueamento.

## Scope

- Atualizar a politica de YODA Intake em `yoda/yoda.md`.
- Atualizar o runbook emitido por `yoda_intake.py`, hoje silencioso sobre
  prioridade.
- Atualizar a orientacao exibida por `issue_add.py --help`.
- Alinhar `project/specs/11-yoda-intake.md` e
  `project/specs/18-issue-add-script.md`, removendo o enquadramento por
  importancia relativa.
- Atualizar `yoda/scripts/README.md` caso descreva prioridade ou ordenacao.
- Registrar um exemplo valido e um exemplo invalido de alteracao de prioridade.
- Diferenciar nos textos operacionais os papeis de `todo_list.py`,
  `todo_next.py` e `yoda_flow_next.py`.
- Adicionar testes de contrato que impecam a remocao acidental dessa orientacao
  dos runbooks e das ajudas geradas.

## Out of scope

- Alterar o intervalo permitido de prioridades.
- Remover o campo `priority` do schema.
- Calcular prioridades automaticamente.
- Alterar retroativamente as prioridades de issues existentes ou de projetos
  consumidores.
- Modificar o algoritmo de selecao, salvo se o Study encontrar divergencia entre
  o comportamento implementado e a semantica documentada.

## Requirements

- Os textos operacionais MUST declarar que o agente nao ranqueia um lote de
  issues e nao usa `priority` para codificar sequencia planejada.
- Novas issues MUST ser criadas com `priority: 5` quando nao houver razao
  concreta para romper a ordem natural.
- A documentacao MUST definir a ordem natural como: issue em `doing` retomada
  primeiro, issues bloqueadas por dependencia nao concluida adiadas, e as demais
  na ordem estavel de ID.
- A documentacao MUST distinguir `depends_on`, que expressa precedencia real, de
  `priority`, que expressa excecao deliberada a ordem natural, e MUST proibir
  usar um no lugar do outro.
- Lotes criados no mesmo Intake MUST ser gerados na ordem natural desejada, sem
  dependencias artificiais para organizar o backlog.
- Qualquer valor diferente de `5` MUST vir acompanhado de justificativa relativa
  a outra issue ou ao backlog disponivel, explicando por que a ordem natural nao
  serve. Uma afirmacao generica de importancia MUST NOT ser aceita.
- Antecipar e postergar MUST ser tratados como desvios equivalentes, ambos
  exigindo justificativa.
- Um pedido explicito do humano para antecipar ou adiar trabalho MUST ser
  considerado justificativa valida.
- Os textos operacionais MUST esclarecer que `todo_list.py` apresenta uma visao
  ordenada do backlog e nao um plano de execucao, e que `todo_next.py` e
  `yoda_flow_next.py` consideram estado e dependencias.
- O runbook de `yoda_intake.py` MUST passar a conter a orientacao de prioridade.
- Specs, manual embarcado e ajudas MUST permanecer consistentes entre si e em
  ingles onde o documento existente estiver em ingles.
- Nenhum texto em `project/specs/` pode citar a issue externa por link, numero
  ou ID; o rationale entra autocontido.

## Acceptance criteria

- [ ] O Intake afirma explicitamente que o agente nao deve ranquear um lote de
      issues.
- [ ] O Intake orienta manter `priority: 5` quando nao houver necessidade de
      romper a ordem natural.
- [ ] A documentacao distingue ordem natural, dependencia e prioridade.
- [ ] A documentacao orienta criar issues de um lote na ordem natural desejada.
- [ ] A documentacao exige justificativa comparativa para qualquer prioridade
      diferente de `5`, recusando afirmacao generica de importancia.
- [ ] Ha ao menos um exemplo valido e um exemplo invalido de alteracao de
      prioridade.
- [ ] A ajuda de `issue_add.py` nao induz o agente a escolher uma prioridade
      quando o padrao e suficiente.
- [ ] O runbook emitido por `yoda_intake.py` contem a orientacao de prioridade.
- [ ] Os papeis de `todo_list.py`, `todo_next.py` e `yoda_flow_next.py` estao
      diferenciados nos textos operacionais.
- [ ] `project/specs/11-yoda-intake.md` nao enquadra mais a prioridade por
      importancia relativa.
- [ ] Ha testes de contrato que falham se a orientacao sair dos runbooks ou das
      ajudas geradas.
- [ ] `yoda/scripts/tests` e `project/tests` permanecem passando.

## Entry points

- `yoda/yoda.md`
- `yoda/scripts/yoda_intake.py`
- `yoda/scripts/issue_add.py`
- `yoda/scripts/README.md`
- `project/specs/11-yoda-intake.md`
- `project/specs/18-issue-add-script.md`
- `project/specs/16-todo-list-script.md`
- `yoda/scripts/tests/test_yoda_intake.py`
- `yoda/scripts/tests/test_cli_contracts.py`
- `yoda/project/extern_issues/github-010.json`

## Implementation notes

Formulacao curta sugerida pela fonte externa, reutilizavel nos runbooks:

> Keep priority `5` by default. Do not rank issues in a batch or use priority to
> encode their planned sequence. Natural order comes from the current `doing`
> issue, real dependencies, and stable issue order. Change priority only when an
> issue must intentionally run before or after that natural order, and record
> the relative reason.

O Study deve confirmar se o algoritmo de selecao ja implementa a ordem natural
descrita. A ordenacao por prioridade decrescente com desempate por ID e a
retomada de issues em `doing` sugerem que sim, caso em que a entrega e
exclusivamente documental. Se houver divergencia, ela deve ser decidida
explicitamente antes de alinhar texto e codigo.

Preferir uma formulacao central reutilizada por manual, runbook e ajuda, em vez
de tres textos independentes que possam divergir com o tempo, seguindo o mesmo
padrao ja adotado para a regra de saida dos comandos.

## Tests

- Adicionar teste de contrato sobre o runbook emitido por `yoda_intake.py`.
- Adicionar teste de contrato sobre `issue_add.py --help`.
- Executar `python3 -m pytest yoda/scripts/tests`.
- Executar `python3 -m pytest project/tests`. As duas suites nao podem ser
  executadas na mesma invocacao.

## Risks and edge cases

- Escrever a regra apenas no manual e deixar o runbook do Intake silencioso,
  mantendo a lacuna que originou o desvio.
- Tornar o texto tao restritivo que um pedido legitimo do humano para antecipar
  trabalho pareca proibido.
- Duplicar a formulacao em varios arquivos e permitir que as copias divirjam.
- Confundir a correcao documental com mudanca no algoritmo de selecao.
- Introduzir nas specs uma referencia a issue concreta, reprovada pelo lint de
  independencia.

## Result log

## Flow log

- 2026-08-31T18:03:51-03:00 issue_add created title=Tratar prioridade como excecao a ordem natural no YODA Intake; priority=5
- 2026-08-31T18:04:59-03:00 Intake concluido a partir da GitHub #10: prioridade definida como excecao a ordem natural, sem ranqueamento de lote
- 2026-08-31T18:20:16-03:00 transition to-do->doing/study | Evaluate aprovado: fallback publico validado com contexto de falha dupla e suites passando
