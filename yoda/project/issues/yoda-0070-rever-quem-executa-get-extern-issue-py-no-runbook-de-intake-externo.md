---
schema_version: '2.01'
status: done
title: Rever quem executa get_extern_issue.py no runbook de Intake externo
description: O runbook de Intake externo e o manual embarcado mandam pedir ao humano
  que execute get_extern_issue.py localmente, texto herdado de quando o comando exigia
  CLI autenticado. Desde a introducao do fallback publico, uma issue publica de github.com
  pode ser coletada sem credenciais, e o proprio manual ja descreve esse fallback
  no passo seguinte, criando contradicao interna. Definir quando o agente pode executar
  o comando e quando deve delegar ao humano, e alinhar runbook, manual e specs 11
  e 25.
priority: 5
created_at: '2026-09-01T08:37:32-03:00'
updated_at: '2026-09-01T08:54:37-03:00'
---

# yoda-0070 - Rever quem executa get_extern_issue.py no runbook de Intake externo

## Summary

O runbook de Intake externo instrui o agente a pedir que o humano execute
`get_extern_issue.py` localmente. O Study mostrou que essa delegacao foi uma
decisao arquitetural deliberada de separacao de responsabilidades, e nao um
residuo da exigencia de CLI autenticado. Depois da introducao do fallback
publico, a instrucao passou a contradizer o proprio manual.

## Context

O texto vive em quatro lugares:

- `yoda/scripts/yoda_intake.py`, na funcao `_extern_fetch_runbook`, passo 1:
  "Ask the human to run this command locally".
- `yoda/yoda.md`, secao `External source path`, passo 1: "ask the human to run".
- `project/specs/11-yoda-intake.md`: "Ask the human to run `get_extern_issue.py`".
- `project/specs/25-yoda-intake-script.md`: "return runbook instructing the agent
  to ask the human to run `get_extern_issue.py`".

Ha contradicao interna no manual embarcado. O passo 1 delega a execucao ao
humano de forma incondicional, enquanto o passo 2, acrescentado junto do
fallback publico, explica que uma issue publica de `github.com` e coletada sem
autenticacao quando o CLI esta ausente ou sem sessao. O leitor recebe as duas
regras sem saber qual prevalece.

Ha uma sutileza que a decisao precisa cobrir. O motivo original de delegar ao
humano nao era apenas a falta do fallback: era que a coleta consome a sessao
autenticada do humano. Quando o agente executa o comando num ambiente onde o
`gh` ja esta autenticado, a coleta continua usando essa sessao, e o transporte
reportado e `authenticated-cli`, nao `public-http`. Ou seja, "o agente pode
executar" e "a execucao dispensa credenciais do humano" nao sao a mesma
afirmacao, e o agente nao sabe de antemao se o repositorio e publico: ele
descobre tentando.

## Objective

Definir de forma inequivoca quem executa `get_extern_issue.py` no Intake
externo, eliminando a contradicao entre delegar a execucao e descrever uma
coleta que dispensa credenciais.

## Scope

- Decidir a regra de execucao: quando o agente pode rodar o comando e quando
  deve delegar ao humano.
- Atualizar o runbook emitido por `yoda_intake.py`.
- Alinhar a secao `External source path` de `yoda/yoda.md`.
- Alinhar `project/specs/11-yoda-intake.md` e
  `project/specs/25-yoda-intake-script.md`.
- Adicionar teste de contrato sobre o texto do runbook externo.

## Out of scope

- Alterar `get_extern_issue.py`, seus transportes ou sua politica de fallback.
- Alterar a restricao do fallback publico a `github.com`.
- Alterar o formato ou o local do JSON de issue externa.
- Alterar as demais etapas do YODA Intake.
- Introduzir deteccao previa de visibilidade do repositorio como pre-requisito
  da coleta.

## Requirements

- A regra de execucao MUST ser unica e coerente entre runbook, manual embarcado
  e specs; nenhuma fonte pode delegar incondicionalmente enquanto outra descreve
  coleta sem credenciais.
- A documentacao MUST distinguir "o agente pode executar o comando" de "a coleta
  dispensa credenciais do humano", que nao sao equivalentes.
- A regra MUST considerar que o agente nao conhece a visibilidade do repositorio
  antes de tentar a coleta.
- Quando o agente executar o comando, ele MUST reportar ao humano o transporte
  retornado, `authenticated-cli` ou `public-http`.
- A politica MUST preservar a possibilidade de o humano executar o comando por
  conta propria quando preferir.
- Os textos MUST permanecer em ingles onde o documento existente estiver em
  ingles.
- Nenhum texto em `project/specs/` pode citar issue concreta por link, numero ou
  ID; o rationale entra autocontido.

## Acceptance criteria

- [x] A regra de quem executa `get_extern_issue.py` esta declarada sem
      ambiguidade.
- [x] O runbook emitido por `yoda_intake.py` reflete essa regra.
- [x] `yoda/yoda.md` nao contem mais delegacao incondicional ao lado da
      descricao do fallback publico.
- [x] `project/specs/11-yoda-intake.md` e
      `project/specs/25-yoda-intake-script.md` estao alinhadas ao runbook.
- [x] A documentacao distingue execucao pelo agente de dispensa de credenciais.
- [x] O texto orienta reportar o transporte retornado ao humano.
- [x] A opcao de o humano executar o comando permanece documentada.
- [x] Ha teste de contrato que falha se a orientacao sair do runbook externo.
- [x] `yoda/scripts/tests` e `project/tests` permanecem passando.

## Entry points

- `yoda/scripts/yoda_intake.py`
- `yoda/yoda.md`
- `project/specs/11-yoda-intake.md`
- `project/specs/25-yoda-intake-script.md`
- `yoda/scripts/tests/test_yoda_intake.py`

## Implementation notes

A origem desta issue e observacional, nao uma issue externa: a contradicao
apareceu durante execucoes reais de Intake nesta sessao, quando o agente
apresentou ao humano um comando que ele mesmo podia executar, e depois o
executou com o transporte `authenticated-cli`.

O Study deve decidir entre pelo menos tres formas: manter a delegacao como
padrao e permitir execucao pelo agente mediante autorizacao; inverter, deixando
o agente executar e delegando apenas quando a coleta falhar por autenticacao; ou
tornar a escolha explicita no runbook, apresentando as duas opcoes ao humano.

Vale considerar que o `get_extern_issue.py` ja produz a informacao necessaria
depois do fato, ao reportar o transporte. Uma regra que dependa de conhecer a
visibilidade antes da coleta exigiria uma verificacao previa que o Out of scope
desta issue exclui.

## Tests

- Adicionar teste de contrato sobre o texto do runbook externo em
  `yoda/scripts/tests/test_yoda_intake.py`.
- Executar `python3 -m pytest yoda/scripts/tests`.
- Executar `python3 -m pytest project/tests`. As duas suites nao podem ser
  executadas na mesma invocacao.

## Risks and edge cases

- Trocar a delegacao por execucao automatica e fazer o agente consumir a sessao
  autenticada do humano sem que ele perceba.
- Corrigir apenas o runbook e deixar manual e specs divergentes, ou o inverso.
- Escrever uma regra que dependa de saber a visibilidade do repositorio antes da
  coleta.
- Tornar o runbook longo a ponto de o agente ignorar o passo seguinte.

## Study findings

A delegacao ao humano nao e residuo de limitacao de autenticacao. Ela foi
introduzida junto do proprio `get_extern_issue.py` como separacao deliberada de
responsabilidades: o agente orquestra o fluxo e decompoe em micro issues; o
humano executa a integracao externa. Autenticacao aparecia ali apenas como risco
registrado, nao como motivo da regra. Portanto o fallback publico enfraqueceu um
argumento secundario, nao o argumento que sustentava a decisao.

A contradicao no manual e real e independe dessa origem. `yoda/yoda.md` delega a
execucao de forma incondicional no passo 1 e, no passo 2, descreve coleta sem
credenciais para issue publica de `github.com`. As duas regras convivem sem
precedencia declarada.

O texto vive em quatro lugares: o runbook emitido por `yoda_intake.py`, a secao
`External source path` de `yoda/yoda.md`, e as specs de YODA Intake e do
`yoda_intake.py`.

Duas restricoes tecnicas delimitam as opcoes:

1. Nao existe forma de forcar o transporte publico. Quando o CLI esta pronto, a
   coleta usa o transporte autenticado; o fallback so entra quando a
   autenticacao esta ausente ou falha. Nao ha flag de transporte, e cria-la
   exigiria alterar `get_extern_issue.py`, fora do escopo desta issue. Logo,
   "o agente executa" implica "a sessao autenticada do humano e usada quando
   estiver disponivel".
2. Este e o unico ponto do framework que delega a execucao de um comando YODA.
   Todos os demais pedidos ao humano solicitam informacao: slug, descricao,
   proximo passo, continuidade do flow. A delegacao de execucao e um outlier
   estrutural.

Impacto pratico de o agente executar com a sessao do humano: a operacao e de
leitura e o agente nunca ve o token, mas o acesso e atribuido a conta do humano,
consumindo seu rate limit e aparecendo em seu registro de auditoria.

Decisao aprovada no encerramento do Study:

O agente passa a executar a coleta e transfere a responsabilidade ao humano
apenas quando a execucao falhar. Isso revisa deliberadamente a separacao de
responsabilidades original, que deixa de valer como regra incondicional.

## Document contract

O Implement deve seguir esta ordem document-first e nao introduzir decisoes
novas fora deste contrato.

### 1. Regra de execucao

Regra unica, valida para runbook, manual e specs:

- O agente MUST executar `get_extern_issue.py` quando o Intake externo indicar
  coleta pendente.
- Se o comando terminar com sucesso, o agente MUST apresentar ao humano o
  transporte retornado, `authenticated-cli` ou `public-http`, junto do caminho
  do arquivo salvo.
- Se o comando falhar, o agente MUST apresentar a mensagem de erro retornada e
  transferir a execucao ao humano, oferecendo o mesmo comando para execucao
  local.
- O agente MUST NOT tentar contornar a falha por outro caminho, nem inferir
  visibilidade de repositorio antes da coleta.
- O humano MAY executar o comando por conta propria a qualquer momento; essa
  possibilidade permanece documentada.

Qualquer codigo de saida diferente de zero conta como falha, incluindo CLI
ausente com repositorio nao publico, autenticacao indisponivel para repositorio
privado, GitHub Enterprise, GitLab, falha de rede e rate limit. A delegacao usa
a mensagem acionavel que o proprio comando ja produz; o runbook nao deve
duplicar diagnostico.

### 2. Runbook emitido por yoda_intake.py

Reescrever `_extern_fetch_runbook` em `yoda/scripts/yoda_intake.py`:

- passo 1 deixa de ser "Ask the human to run this command locally" e passa a
  instruir o agente a executar o comando;
- acrescentar o passo de apresentar transporte e caminho salvo em caso de
  sucesso;
- acrescentar o passo de apresentar o erro e transferir a execucao ao humano em
  caso de falha, mantendo o mesmo comando visivel para execucao local;
- preservar os passos existentes de leitura do JSON e de rerun do
  `yoda_intake.py`;
- manter o runbook compacto: a fronteira de fase permite mais de uma linha, mas
  o texto nao deve crescer a ponto de o agente perder o passo seguinte.

### 3. Manual embarcado

Em `yoda/yoda.md`, secao `External source path`:

- inverter o passo 1 para execucao pelo agente;
- eliminar a contradicao com o passo que descreve o fallback publico,
  reposicionando-o como explicacao do transporte que o agente vai observar e
  reportar, nao como regra concorrente;
- declarar que a coleta pode consumir a sessao autenticada do humano quando o
  CLI estiver disponivel, e que o agente reporta o transporte por isso;
- registrar que o humano pode executar o comando por conta propria.

### 4. Specs

- `project/specs/11-yoda-intake.md`: substituir "Ask the human to run
  `get_extern_issue.py`" pela regra de execucao pelo agente com delegacao em
  caso de falha.
- `project/specs/25-yoda-intake-script.md`: no caminho de arquivo ausente,
  substituir "runbook instructing the agent to ask the human to run" pela
  instrucao de execucao com delegacao em caso de falha.
- As duas specs MUST registrar de forma autocontida que a separacao de
  responsabilidades anterior foi revista e por que, sem citar issue concreta por
  link, numero ou ID, sob pena de reprovacao no lint de independencia.
- O contrato de saida do `yoda_intake.py` nao muda: arquivo ausente continua
  retornando runbook e encerrando com sucesso.

### 5. Verificacao fechada

- Adicionar teste de contrato em `yoda/scripts/tests/test_yoda_intake.py` sobre
  o runbook de arquivo ausente, cobrindo a instrucao de execucao pelo agente, o
  reporte de transporte e a delegacao em caso de falha.
- Adicionar assercao negativa que falhe se "ask the human to run" voltar ao
  runbook externo.
- Executar `python3 -m pytest yoda/scripts/tests`.
- Executar `python3 -m pytest project/tests`. As duas suites nao podem ser
  executadas na mesma invocacao.
- Confirmar por varredura que nenhuma das quatro fontes mantem a delegacao
  incondicional.

Proxima acao deterministica apos aprovacao deste Document: entrar em Implement,
atualizando primeiro as specs, depois `yoda/yoda.md`, depois o runbook do
`yoda_intake.py` e por fim os testes.

## Result log

docs(intake): executar coleta externa antes de delegar

Alinha specs, manual embarcado e runbook para que o agente execute
`get_extern_issue.py`, reporte ao humano o transporte e o caminho salvo quando
houver sucesso, e transfira a execucao ao humano somente depois de uma falha.
Preserva a possibilidade de execucao voluntaria pelo humano e registra de forma
autocontida a revisao da separacao anterior de responsabilidades.

Adiciona teste de contrato contra o retorno da delegacao incondicional. Evaluate
confirmou a saida real do CLI, `102 passed` em `yoda/scripts/tests`, `17 passed`
em `project/tests` e `git diff --check` sem erros, sem achados remanescentes.

- **Issue**: `yoda-0070`

- **Path**: `yoda/project/issues/yoda-0070-rever-quem-executa-get-extern-issue-py-no-runbook-de-intake-externo.md`

## Flow log

- 2026-09-01T08:37:32-03:00 issue_add created title=Rever quem executa get_extern_issue.py no runbook de Intake externo; priority=5
- 2026-09-01T08:38:10-03:00 Intake concluido sem fonte externa: contradicao observada entre delegar a coleta e descrever o fallback publico
- 2026-09-01T08:40:06-03:00 transition to-do->doing/study
- 2026-09-01T08:44:30-03:00 transition doing/study->doing/document | Study aprovado: agente executa a coleta e delega ao humano quando falhar; separacao da yoda-0039 revista
- 2026-09-01T08:46:24-03:00 transition doing/document->doing/implement | Document aprovado: agente executa a coleta, reporta transporte e delega ao humano em caso de falha
- 2026-09-01T08:50:34-03:00 transition doing/implement->doing/evaluate | Evaluate autorizado: revisar regra de execucao da coleta externa, documentacao, runbook e testes
- 2026-09-01T08:54:37-03:00 transition doing/evaluate->done | Evaluate aprovado: agente coleta, reporta transporte e delega apenas apos falha
