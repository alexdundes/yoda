---
schema_version: '2.01'
status: done
title: Tornar fronteiras de fase do YODA Flow observaveis
description: Explicitar na politica do YODA Flow que cada transicao precede o trabalho
  da fase, que cada interacao humana autoriza apenas uma fase, que o runbook retornado
  deve ser apresentado ao humano e que Study, Document, Implement e Evaluate terminam
  com entregaveis definidos.
priority: 5
extern_issue_file: ../extern_issues/github-009.json
created_at: '2026-08-31T16:36:09-03:00'
updated_at: '2026-08-31T17:14:19-03:00'
---

# yoda-0066 - Tornar fronteiras de fase do YODA Flow observaveis

## Summary

Tornar cada fronteira do YODA Flow observavel pelo humano e verificavel no
historico. A transicao deve anunciar o trabalho que comeca, cada fase deve
terminar com um entregavel apresentado e uma autorizacao humana deve liberar
somente a proxima fase.

## Context

A issue externa [GitHub #9](https://github.com/alexdundes/yoda/issues/9)
registrou uma execucao real em que Study, Document, Implement e Evaluate foram
encadeados em dezenove segundos. Todo o trabalho havia sido feito ainda em
Study; as chamadas seguintes apenas registraram transicoes e suas saidas foram
descartadas, portanto o humano nao recebeu os runbooks nem teve um entregavel
especifico para aprovar.

A politica atual exige uma chamada por passo e autorizacao entre fases, mas nao
define de forma inequívoca a ordem transicao -> trabalho -> entregavel -> pausa.
Assim, o texto permite interpretar a transicao como registro retroativo e
permite que uma autorizacao generica seja consumida por varias chamadas.

## Objective

Definir uma fronteira de fase que o agente nao consiga atravessar corretamente
sem apresentar ao humano o resultado da fase anterior e aguardar nova
autorizacao explicita.

## Scope

- Atualizar primeiro as specs normativas do processo e do orquestrador.
- Alinhar a `Flow policy` do manual embarcado `yoda/yoda.md`.
- Definir a ordem entre transicao e execucao do trabalho.
- Definir uma fase por interacao humana, nao apenas uma fase por chamada.
- Declarar o entregavel de Study, Document, Implement e Evaluate.
- Exigir que a saida/runbook de `yoda_flow_next.py` seja apresentada ao humano.
- Revisar o texto do runbook/help para nao sugerir encadeamento silencioso.
- Estender a mesma fronteira ao YODA Prep Flow: uma etapa de preparo por
  interacao humana, com entregavel apresentado e parada antes da etapa seguinte.
- Registrar uma verificacao manual do comportamento e, quando aplicavel,
  testes de contrato do texto emitido.

## Out of scope

- Alterar quantidade, nomes ou ordem das fases.
- Alterar YODA Intake.
- Alterar os demais contratos do YODA Prep Flow: selecao explicita por issue,
  independencia de ordem/dependencias, estados preparados e retomada no Flow.
- Impor duracao minima entre transicoes.
- Bloquear automaticamente uma transicao com base apenas em timestamps.
- Criar um mecanismo tecnico de prova de autorizacao humana; se a politica e o
  runbook forem insuficientes, essa automacao deve ser tratada em outra issue.

## Requirements

- A transicao MUST acontecer antes do trabalho da fase que ela inicia; nunca
  deve registrar retroativamente trabalho ja concluido.
- Cada interacao humana MUST autorizar no maximo uma transicao de fase.
- Depois de executar a fase, o agente MUST apresentar seu entregavel e parar.
- O runbook retornado por `yoda_flow_next.py` MUST ser apresentado ao humano e
  MUST NOT ser descartado ou ocultado por encadeamento de comandos.
- Study MUST entregar achados, restricoes e decisoes em aberto.
- Document MUST entregar a issue atualizada com as decisoes aprovadas e o
  contrato document-first fechado.
- Implement MUST entregar codigo e artefatos do escopo aprovado, acompanhados
  das verificacoes executadas.
- Evaluate MUST entregar criterios conferidos, findings restantes e, quando
  aprovada, o `Result log` preenchido.
- Uma resposta generica como "siga" MUST valer apenas para a proxima fronteira;
  cada fase posterior exige que seu proprio entregavel seja apresentado.
- YODA Prep Flow MUST executar no maximo uma etapa de preparo por interacao
  humana, apresentar o entregavel de Prep Study ou Prep Document e parar.
- O intervalo entre timestamps MAY ser usado como indício de encadeamento, mas
  MUST NOT ser tratado isoladamente como prova de violacao.
- Specs, manual embarcado e ajuda operacional MUST permanecer consistentes e em
  ingles onde o documento existente estiver em ingles.
- O `--help` de todos os comandos YODA MUST instruir o agente a seguir o runbook
  retornado e a nunca descartar a saida do comando.
- `yoda/yoda.md` e os textos de `--help` MUST ser escritos como instrucao
  imperativa dirigida ao agente, nao como explicacao para o humano.
- `runbook_line` MAY ocupar mais de uma linha quando isso for necessario para
  ser compreendido; deve permanecer compacto sempre que possivel. A regra de
  linha unica das entradas de `## Flow log` permanece inalterada.

## Acceptance criteria

- [x] As specs declaram explicitamente a ordem transicao -> trabalho ->
      entregavel -> pausa/autorizacao.
- [x] A politica define o passo como uma fase por interacao humana.
- [x] Os entregaveis das quatro fases estao definidos sem ambiguidade.
- [x] O manual declara que o runbook e instrucao operacional dirigida ao agente
      e que o agente deve apresenta-la ao humano.
- [x] A formulacao antiga baseada somente em uma chamada por passo foi removida
      ou contextualizada para nao permitir encadeamento.
- [x] O help/runbook de `yoda_flow_next.py` reflete a mesma fronteira.
- [x] Specs e runbooks do YODA Prep Flow definem uma etapa de preparo por
      interacao humana, apresentam o entregavel e param, preservando seus demais
      contratos.
- [x] Uma simulacao documentada apresenta uma fase, para e exige autorizacao
      antes da transicao seguinte.
- [x] A verificacao nao usa intervalo curto como bloqueio automatico.
- [x] Specs, `yoda/yoda.md` e testes de contrato permanecem alinhados.
- [x] O `--help` de todos os comandos YODA instrui a seguir o runbook e a nao
      descartar a saida do comando.
- [x] A restricao de linha unica saiu de `runbook_line` sem afetar a regra de
      linha unica do `## Flow log`.
- [x] A suite relevante passa.

## Entry points

- `project/specs/02-yoda-flow-process.md`
- `project/specs/06-agent-playbook.md`
- `project/specs/21-yoda-flow-next-script.md`
- `project/specs/00-conventions.md`
- `project/specs/27-yoda-prep-flow-script.md`
- `yoda/yoda.md`
- `yoda/scripts/yoda_flow_next.py`
- `yoda/scripts/yoda_prep_flow.py`
- `yoda/scripts/*.py`
- `package.py`
- `yoda/scripts/tests/test_yoda_flow_next.py`
- `yoda/scripts/tests/test_cli_contracts.py`
- `yoda/project/extern_issues/github-009.json`

## Implementation notes

Substituir a regra ambigua "one step per call" por uma regra centrada na
interacao humana. A chamada de script continua sendo atomica, mas isso e uma
propriedade tecnica subordinada a fronteira de processo.

Fluxo esperado:

1. humano autoriza a proxima fase;
2. agente chama `yoda_flow_next.py` e apresenta o runbook retornado;
3. agente executa somente o trabalho daquela fase;
4. agente apresenta o entregavel e para;
5. nova transicao depende de nova autorizacao humana.

O Flow log continua sendo evidencia operacional. Timestamps proximos ajudam a
investigar uma execucao, mas fases legitimamente curtas impedem que o intervalo
seja usado como regra de validade.

## Tests

- Atualizar testes de contrato que verificam o runbook/help da fase.
- Executar `yoda/scripts/tests/test_yoda_flow_next.py` e a suite completa.
- Fazer uma verificacao manual guiada, registrando que cada transicao foi
  precedida por autorizacao e seguida apenas pelo trabalho da fase anunciada.

## Risks and edge cases

- Aumentar o custo de interacao para issues triviais.
- Confundir uma fase curta legitima com encadeamento indevido.
- Atualizar apenas o manual empacotado e deixar as specs divergentes.
- O agente exibir o runbook, mas continuar trabalhando fases posteriores sem
  parar.
- Uma autorizacao ampla do humano ser interpretada como aprovacao de fases cujo
  entregavel ainda nao existe.

## Document contract

O Implement deve seguir esta ordem document-first e nao introduzir decisoes
novas fora deste contrato.

Decisoes aprovadas no encerramento do Study:

1. A regra completa vive em `project/specs/`; `yoda/yoda.md` carrega uma versao
   operacional compacta porem autossuficiente, nao um ponteiro, porque as specs
   nao sao distribuidas com o pacote.
2. `yoda/yoda.md` e os textos de `--help` sao dirigidos ao AGENTE. Devem ser
   instrucao imperativa, nao explicacao para leitor humano.
3. A formulacao "one step per call" e substituida, nao contextualizada.
4. A tabela `Deliverables per phase` da spec 02 e expandida no lugar.
5. Nao ha automacao possivel de prova de autorizacao. O mecanismo de controle e
   o texto imperativo no manual e nos `--help`.
6. Extensao de escopo aprovada: a linha sobre seguir o runbook e nao descartar a
   saida entra no `--help` de TODOS os comandos, nao apenas do `yoda_flow_next`.
7. Extensao de escopo aprovada: a restricao de linha unica sai de
   `runbook_line`.
8. Extensao de escopo aprovada durante Evaluate: a fronteira por interacao
   humana tambem se aplica ao YODA Prep Flow. Essa ampliacao substitui a
   exclusao original sem alterar selecao, dependencias, estados ou retomada.

### 1. Specs normativas

- `project/specs/02-yoda-flow-process.md`: criar uma secao de fronteira de fase
  declarando a ordem `autorizacao -> transicao -> trabalho -> entregavel ->
  pausa`; afirmar que a transicao precede o trabalho e nunca registra
  retroativamente; definir o passo como uma fase por interacao humana;
  substituir `phase advances one step per execution`; expandir
  `Deliverables per phase` com os quatro entregaveis dos Requirements e a regra
  de apresentar o entregavel e parar.
- `project/specs/06-agent-playbook.md`: alinhar a sequencia de entrada do Flow
  com a mesma fronteira e declarar que a saida dos comandos e insumo do passo
  seguinte e nao pode ser descartada.
- `project/specs/21-yoda-flow-next-script.md`: manter
  `each execution resolves exactly one next deterministic step` como propriedade
  tecnica explicitamente subordinada a fronteira de processo; declarar que a
  transicao antecede o trabalho da fase que ela inicia.

Nenhum desses textos pode citar a issue externa por link, numero ou ID: o lint
de independencia reprova a spec. O rationale entra autocontido.

### 2. Manual embarcado

`yoda/yoda.md`, secao `Flow policy`:

- remover `Execute one step per yoda_flow_next.py call`;
- declarar o passo como uma fase por interacao humana;
- declarar a ordem `autorizacao -> transicao -> trabalho -> entregavel -> pausa`;
- declarar que o runbook retornado e instrucao operacional que o agente MUST
  apresentar ao humano;
- proibir descartar, silenciar ou redirecionar a saida dos comandos YODA;
- listar o entregavel das quatro fases;
- manter o texto imperativo e dirigido ao agente.

### 3. Ajuda operacional de todos os comandos

Acrescentar ao epilogo de `--help` de cada comando uma linha equivalente a:
seguir o runbook retornado e nunca descartar a saida do comando.

Comandos alcancados: `yoda_flow_next.py`, `yoda_prep_flow.py`,
`yoda_intake.py`, `issue_add.py`, `todo_update.py`, `todo_list.py`,
`todo_next.py`, `log_add.py`, `get_extern_issue.py`, `init.py`, `update.py` e
`package.py`.

Isso amplia os Entry points originais da issue e foi autorizado no Study.

### 4. Fim da restricao de linha unica em runbook_line

- Ajustar `project/specs/00-conventions.md`, `project/specs/02-yoda-flow-process.md`
  e `project/specs/21-yoda-flow-next-script.md` para exigir `runbook_line`
  compacto e imperativo, permitindo mais de uma linha quando necessario.
- NAO alterar as regras de linha unica das entradas de `## Flow log`, que
  aparecem em `00-conventions`, `04-todo-dev-yaml-issues`,
  `05-scripts-and-automation`, `19-log-add-script` e `21-yoda-flow-next-script`.
  Sao regras distintas e continuam valendo.
- `yoda_flow_next.py` e `yoda_prep_flow.py` renderizam o runbook como item de
  lista Markdown. A renderizacao MUST preservar a legibilidade quando o texto
  ocupar mais de uma linha, sem quebrar a estrutura da saida `md`.
- `project/specs/02-yoda-flow-process.md`,
  `project/specs/13-yoda-scripts-v1.md` e
  `project/specs/27-yoda-prep-flow-script.md` devem substituir a moldura de uma
  etapa por chamada por uma etapa de preparo por interacao humana.
- Os demais contratos do Prep Flow permanecem inalterados: selecao explicita
  por `--issue`, independencia de ordem/dependencias, transicoes
  `none -> study -> document`, persistencia em `to-do` e retomada pelo Flow em
  Implement.

### 5. Textos de runbook por fase

Estender `RUNBOOK_BY_STEP` em `yoda_flow_next.py` para que cada fase instrua
executar apenas aquela fase, apresentar o entregavel e parar para autorizacao.
Preservar os prefixos e trechos ja fixados pelos testes vigentes:
`Run Study:`, `Run Implement:`, `conventional-commit line` e
`Issue moved to done.`.

Alinhar tambem `RUNBOOK_BY_STEP` em `yoda_prep_flow.py` para apresentar o
entregavel e parar, preservando os prefixos `Run Prep Study:` e
`Run Prep Document:`.

### 6. Verificacao fechada

- Teste de contrato garantindo que o `--help` de cada comando alcancado contem a
  instrucao de seguir o runbook e de nao descartar a saida.
- Teste de contrato garantindo que o `runbook_line` de cada fase expressa a
  fronteira e que a saida `md` permanece bem formada com texto multilinha.
- Atualizar `test_yoda_flow_next.py` conforme os textos novos.
- Atualizar `test_yoda_prep_flow.py` para cobrir a fronteira nos dois runbooks.
- Registrar nesta issue uma simulacao manual mostrando uma fase apresentada,
  parada e autorizacao exigida antes da transicao seguinte.
- Nao introduzir bloqueio automatico por intervalo de timestamp.
- Executar `python3 -m pytest yoda/scripts/tests` e
  `python3 -m pytest project/tests`.

Proxima acao deterministica apos aprovacao deste Document: entrar em Implement,
atualizando primeiro as specs, depois `yoda/yoda.md`, depois os `--help` e os
runbooks, e por fim os testes.

## Manual verification

A execucao desta propria issue serve como simulacao documentada da fronteira.
Cada transicao foi precedida por autorizacao humana explicita, o runbook
retornado foi apresentado ao humano, e cada fase terminou com um entregavel
apresentado antes de qualquer nova transicao.

Flow log observado:

| Transicao | Horario | Intervalo | Autorizacao |
| --- | --- | --- | --- |
| to-do -> study | 16:44:17 | - | "entre no yoda flow" |
| study -> document | 16:53:11 | 9 min | decisoes A, B, C e D respondidas |
| document -> implement | 16:56:37 | 3 min | "autorizado" |

Nenhuma transicao registrou trabalho ja concluido: em cada uma delas o trabalho
da fase comecou depois da chamada, e o runbook devolvido foi exibido antes do
trabalho.

Contraste com o padrao que motivou a issue, observado em execucao anterior deste
mesmo repositorio, com cinco transicoes em setenta e tres segundos:

```
08:58:02  to-do     -> study
08:58:23  study     -> document    (21s)
08:58:50  document  -> implement   (27s)
08:58:54  implement -> evaluate    ( 4s)
08:59:15  evaluate  -> done        (21s)
```

O intervalo curto motivou a inspecao, mas nao foi tratado como prova isolada.
Nenhuma verificacao automatica bloqueia transicao por intervalo de tempo, e o
contraste acima esta registrado apenas como evidencia de investigacao.

## Result log

docs: tornar as fronteiras de fase do YODA Flow observaveis

Definiu a fronteira de fase como regra de processo, nao como escrituracao. As
specs, o manual embarcado e a ajuda operacional passam a declarar a ordem
autorizacao -> transicao -> trabalho -> entregavel -> pausa, com o passo medido
por interacao humana e nao por chamada de comando. A formulacao anterior
centrada na chamada foi removida do YODA Flow e, por ampliacao aprovada durante
o Evaluate, tambem do YODA Prep Flow, sem alterar seus contratos de selecao,
estado, dependencia ou retomada.

Declarou o entregavel das quatro fases e tornou explicito que uma autorizacao
generica vale apenas para a proxima fronteira. A regra de nunca descartar,
silenciar ou redirecionar a saida dos comandos foi centralizada em
`lib/cli.py` e repetida nos doze `--help`, de modo a sobreviver a perda de
contexto do agente. A restricao de linha unica saiu de `runbook_line`,
preservada apenas para as entradas de `## Flow log`, e a renderizacao Markdown
passou a manter texto multilinha dentro de um unico item de lista.

Corrigiu tambem `log_add.py`, unico comando sem `RawDescriptionHelpFormatter`,
cujo epilogo vinha refluido e quebrado no meio das frases.

Nenhuma verificacao automatica bloqueia transicao por intervalo de tempo; a
simulacao manual da fronteira esta registrada em `## Manual verification`.

Evaluate: `84 passed` em `yoda/scripts/tests`, `17 passed` em `project/tests`,
`git diff --check` sem erros e zero formulacoes por chamada remanescentes.

- **GitHub Issue** :   #9

- **Issue**: `yoda-0066`

- **Path**: `yoda/project/issues/yoda-0066-tornar-fronteiras-de-fase-do-yoda-flow-observaveis.md`

## Flow log
- 2026-08-31T16:36:09-03:00 issue_add created title=Tornar fronteiras de fase do YODA Flow observaveis; priority=5
- 2026-08-31T16:39:50-03:00 Intake concluido a partir da GitHub #9: fronteiras de fase, entregaveis e autorizacao por interacao definidos
- 2026-08-31T16:44:17-03:00 transition to-do->doing/study
- 2026-08-31T16:53:11-03:00 transition doing/study->doing/document | Study aprovado: regra completa nas specs e yoda.md autossuficiente, passo por interacao humana, help de todos os comandos e fim do limite de uma linha
- 2026-08-31T16:56:37-03:00 transition doing/document->doing/implement | Document aprovado: fronteira de fase nas specs, yoda.md autossuficiente, help dos 12 comandos e fim da linha unica em runbook_line
- 2026-08-31T17:04:05-03:00 transition doing/implement->doing/evaluate | Implement concluido: fronteira nas specs, yoda.md imperativo, regra de output nos 12 helps e fim da linha unica em runbook_line
- 2026-08-31T17:14:19-03:00 transition doing/evaluate->done | Evaluate aprovado: fronteira de fase nas specs, manual e 12 helps, ampliada ao Prep Flow
