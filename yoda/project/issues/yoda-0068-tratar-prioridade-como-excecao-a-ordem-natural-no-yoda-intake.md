---
schema_version: '2.01'
status: done
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
updated_at: '2026-08-31T18:38:39-03:00'
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
- Alinhar `project/specs/07-agent-entry-files.md`, subordinando a selecao da
  issue prioritaria a ordem natural e ao uso de prioridade como excecao.
- Alinhar `project/specs/16-todo-list-script.md`, tratando sua ordenacao padrao
  como visao do backlog e nao como plano de execucao.
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
- Modificar o algoritmo de selecao; o Study confirmou que o comportamento
  implementado ja corresponde a semantica aprovada.

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
- A justificativa MUST ser registrada no corpo Markdown da issue, sem criar novo
  campo de front matter ou alterar o schema.
- Antecipar e postergar MUST ser tratados como desvios equivalentes, ambos
  exigindo justificativa.
- Valores acima de `5` antecipam e valores abaixo de `5` postergam uma issue
  contra a ordem natural; nenhum dos dois sentidos representa posicao ordinal.
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

- [x] O Intake afirma explicitamente que o agente nao deve ranquear um lote de
      issues.
- [x] O Intake orienta manter `priority: 5` quando nao houver necessidade de
      romper a ordem natural.
- [x] A documentacao distingue ordem natural, dependencia e prioridade.
- [x] A documentacao orienta criar issues de um lote na ordem natural desejada.
- [x] A documentacao exige justificativa comparativa para qualquer prioridade
      diferente de `5`, recusando afirmacao generica de importancia.
- [x] Ha ao menos um exemplo valido e um exemplo invalido de alteracao de
      prioridade.
- [x] A ajuda de `issue_add.py` nao induz o agente a escolher uma prioridade
      quando o padrao e suficiente.
- [x] O runbook emitido por `yoda_intake.py` contem a orientacao de prioridade.
- [x] Os papeis de `todo_list.py`, `todo_next.py` e `yoda_flow_next.py` estao
      diferenciados nos textos operacionais.
- [x] A spec 07 contextualiza `highest-priority selectable issue` pela ordem
      natural e pelo carater excepcional da prioridade.
- [x] A spec 16 descreve a ordenacao padrao como visao do backlog, nao como
      plano de execucao.
- [x] `project/specs/11-yoda-intake.md` nao enquadra mais a prioridade por
      importancia relativa.
- [x] Ha testes de contrato que falham se a orientacao sair dos runbooks ou das
      ajudas geradas.
- [x] `yoda/scripts/tests` e `project/tests` permanecem passando.

## Entry points

- `yoda/yoda.md`
- `yoda/scripts/yoda_intake.py`
- `yoda/scripts/issue_add.py`
- `yoda/scripts/README.md`
- `project/specs/11-yoda-intake.md`
- `project/specs/18-issue-add-script.md`
- `project/specs/07-agent-entry-files.md`
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

O Study confirmou que o algoritmo de selecao ja implementa a ordem natural
descrita. O indice ordena por prioridade decrescente com desempate pela ordem
estavel de ID, issues bloqueadas nao sao selecionaveis e `_pick_target` retoma
uma issue em `doing` antes de iniciar outra. Com o baseline comum `5`, a ordem
resultante e a ordem de ID; valores diferentes funcionam como excecao. A entrega
nao altera esse algoritmo.

Criar uma constante textual compartilhada no codigo para o runbook do Intake e
a ajuda de `issue_add.py`, em vez de duas copias que possam divergir. Specs e
manual continuam autocontidos nos respectivos contextos.

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

## Study findings

- `load_issue_index()` ordena issues por prioridade decrescente e ordem estavel
  de origem/ID. Quando todas usam o baseline `5`, a prioridade nao cria ranking
  adicional.
- `todo_next.py` e `yoda_flow_next.py` retomam uma issue em `doing` antes de
  escolher uma nova e excluem da selecao as issues bloqueadas por dependencias
  nao concluidas.
- A implementacao, portanto, ja representa prioridade como o mecanismo que pode
  romper a ordem por ID entre issues selecionaveis; nao ha divergencia de
  algoritmo a corrigir.
- `todo_list.py` produz uma visao por prioridade/ID com ajuste topologico de
  dependencias, mas nao aplica a regra operacional de retomar `doing` primeiro.
  A tabela nao e equivalente a um plano de execucao.
- A spec 16 chama a ordenacao da lista de `Default (execution order)`, moldura
  que incentiva a leitura equivocada da tabela como plano.
- A spec 07 usa `highest-priority selectable issue` sem explicar que o baseline
  conserva a ordem natural e que prioridade diferente e excecao justificada.
- A spec 11 ainda fala em trabalho `more/less important` e em ajustar prioridade
  por urgencia, sem exigir que a justificativa explique por que a ordem natural
  deixou de servir.
- O runbook de `yoda_intake.py` e silencioso sobre prioridade; a ajuda de
  `issue_add.py` menciona apenas justificativa relativa. Nenhum dos dois impede
  o ranqueamento ordinal de um lote.
- Os testes atuais provam a selecao de `doing`, dependencias e baseline, mas nao
  protegem a orientacao textual nos runbooks e ajudas.

## Document contract

O Implement deve seguir este contrato document-first e nao introduzir mudanca
no algoritmo ou no schema de issues.

Decisoes aprovadas no encerramento do Study:

1. A entrega e documental e de testes de contrato; a selecao implementada nao
   muda.
2. A spec 07 entra no escopo para contextualizar sua formulacao centrada em
   `highest-priority selectable issue`.
3. A spec 16 passa a chamar sua ordenacao padrao de visao do backlog e declara
   que ela nao e plano de execucao.
4. A justificativa de qualquer prioridade diferente de `5` fica no corpo
   Markdown da issue, sem novo campo YAML.
5. Runbook do Intake e ajuda de `issue_add.py` reutilizam uma constante textual
   central para evitar divergencia.
6. Valores acima de `5` antecipam e abaixo de `5` postergam, sempre como excecao
   justificada e nunca como numero ordinal do plano.

### 1. Politica normativa

- `project/specs/11-yoda-intake.md`: definir ordem natural, proibir ranking de
  lote, separar `depends_on` de `priority`, exigir criacao do lote na ordem
  natural desejada e substituir importancia generica por desvio relativo
  justificavel. Alinhar tambem as regras que usam sinais do log externo.
- `project/specs/18-issue-add-script.md`: manter default e intervalo, declarar
  que `--priority` e opcional porque `5` e suficiente por padrao, exigir
  justificativa no corpo e incluir exemplos valido e invalido.
- `project/specs/16-todo-list-script.md`: renomear `Default (execution order)`
  para `Default backlog view`, preservar o algoritmo de ordenacao e explicar que
  apenas os comandos de selecao consideram retomada operacional.
- `project/specs/07-agent-entry-files.md`: manter a entrada simplificada, mas
  explicar que a issue prioritaria selecionavel resulta da ordem natural e de
  excecoes justificadas, nao de ranking criado durante Intake.

Nenhuma spec pode citar a fonte externa ou uma issue concreta por link, numero
ou ID. Exemplos normativos usam placeholders genericos.

### 2. Manual e textos operacionais

- `yoda/yoda.md`: expandir `Intake policy` com a regra completa e diferenciar
  os tres comandos: `todo_list.py` mostra uma visao; `todo_next.py` inspeciona a
  proxima selecao; `yoda_flow_next.py` e a autoridade que seleciona e transita.
- Criar uma constante curta compartilhada em `yoda/scripts/lib/cli.py` para
  proibir ranking de lote, manter `5`, resumir a ordem natural e exigir motivo
  relativo quando houver excecao.
- `yoda_intake.py`: inserir essa orientacao nos runbooks completos com e sem
  fonte externa, antes da criacao das issues.
- `issue_add.py --help`: reutilizar a mesma constante e esclarecer que omitir
  `--priority` e o caminho normal.
- `yoda/scripts/README.md`: registrar os papeis distintos dos comandos de lista,
  inspecao e Flow e a regra de prioridade do Intake.

### 3. Exemplos obrigatorios

- Valido: elevar prioridade porque a issue deve preceder o backlog disponivel
  enquanto cada nova execucao continua perdendo dados necessarios.
- Invalido: elevar prioridade apenas porque a issue e `muito importante`.
- Lote: criar as issues na ordem natural desejada, todas com `priority: 5`, e
  registrar `depends_on` somente quando uma nao puder ser executada corretamente
  antes da outra.

### 4. Verificacao

- Adicionar teste do runbook de Intake com e sem fonte externa, exigindo baseline,
  proibicao de ranking e ordem natural.
- Adicionar teste de `issue_add.py --help` exigindo a mesma constante e o caminho
  normal sem `--priority`.
- Manter testes existentes de selecao como evidencia de que `doing`, dependencias
  e prioridade continuam com o comportamento atual.
- Rodar `yoda/scripts/tests` e `project/tests` em invocacoes separadas e conferir
  as ajudas afetadas contra as specs.

## Result log

docs(yoda): treat priority as a natural-order exception

Clarifies Intake priority as a justified exception instead of a batch ranking,
aligns specs and distributed guidance, and protects the shared runbook/help
policy with contract tests without changing selection or issue schema.

- **GitHub Issue** :   #10

- **Issue**: `yoda-0068`

- **Path**: `yoda/project/issues/yoda-0068-tratar-prioridade-como-excecao-a-ordem-natural-no-yoda-intake.md`

## Flow log

- 2026-08-31T18:03:51-03:00 issue_add created title=Tratar prioridade como excecao a ordem natural no YODA Intake; priority=5
- 2026-08-31T18:04:59-03:00 Intake concluido a partir da GitHub #10: prioridade definida como excecao a ordem natural, sem ranqueamento de lote
- 2026-08-31T18:20:16-03:00 transition to-do->doing/study | Evaluate aprovado: fallback publico validado com contexto de falha dupla e suites passando
- 2026-08-31T18:24:17-03:00 transition doing/study->doing/document | Study aprovado: documentar prioridade como excecao sem alterar algoritmo de selecao
- 2026-08-31T18:27:09-03:00 transition doing/document->doing/implement | Document aprovado: implementar politica de prioridade como excecao sem alterar selecao
- 2026-08-31T18:35:39-03:00 transition doing/implement->doing/evaluate | Implement aprovado: politica de prioridade alinhada em specs, manual, runbooks e testes
- 2026-08-31T18:38:39-03:00 transition doing/evaluate->done | Evaluate aprovado: criterios atendidos, Result log preenchido e suites passando
