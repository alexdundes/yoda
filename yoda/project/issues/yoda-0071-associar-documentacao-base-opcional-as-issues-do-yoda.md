---
schema_version: '2.01'
status: done
title: Associar documentacao-base opcional as issues do YODA
description: O YODA nao tem forma estruturada de declarar que uma issue nasceu de
  uma documentacao ja existente no projeto consumidor. Hoje essa relacao aparece informalmente
  na descricao, no contexto, nos entry points ou em notas, obrigando o agente a inferir
  o papel do caminho e permitindo que a referencia seja esquecida em Study e Document.
  Introduzir uma associacao opcional e estruturada, capaz de apontar para um arquivo
  ou uma pasta do projeto consumidor, distinta de extern_issue_file, depends_on e
  entry points, e fazer os runbooks de Intake, Study e Document considerarem essa
  documentacao como contexto qualificado. Issues sem a associacao mantem o comportamento
  atual sem fricao adicional.
priority: 5
extern_issue_file: ../extern_issues/github-012.json
created_at: '2026-09-01T10:35:26-03:00'
updated_at: '2026-09-01T14:15:08-03:00'
---

# yoda-0071 - Associar documentacao-base opcional as issues do YODA

## Summary

O YODA nao possui forma explicita de declarar que uma issue nasceu de uma
documentacao ja existente no projeto consumidor. Quando essa relacao existe, ela
aparece informalmente na descricao, no contexto, nos entry points ou em notas, e
o agente precisa inferir o papel do caminho. Introduzir uma associacao opcional
e estruturada, capaz de apontar para um arquivo ou uma pasta do projeto
consumidor, e fazer os runbooks de Intake, Study e Document trata-la como
contexto qualificado. Issues sem a associacao mantem o comportamento atual.

## Context

O YODA e usado por desenvolvedores com formas distintas de organizar o trabalho.
Um padrao observado e documentar primeiro um problema amplo e, so depois,
derivar dessa documentacao uma ou mais issues executaveis. Nesse fluxo a
documentacao antecede a issue e explica por que ela existe, como se relaciona
com um trabalho maior e quais decisoes ja foram tomadas antes da abertura da
demanda.

A analise que originou a issue externa identificou cinco formas recorrentes de
fundamentacao documental: um documento unico originando varias issues; uma pasta
reunindo especificacao distribuida (arquitetura, contratos, eventos, exemplos);
artefatos nao textuais usados como fonte funcional, como planilhas ou colecoes
de requisicoes; registros de reuniao transformados em trabalho executavel; e
casos em que a issue possui simultaneamente demanda externa e artefato local de
referencia.

Hoje o YODA representa bem tres relacoes vizinhas e nenhuma delas cobre esta:

- `extern_issue_file` identifica uma demanda mantida em outro sistema.
- `depends_on` organiza precedencia de execucao entre issues.
- `Entry points` lista lugares relevantes para comecar a investigacao.

A ausencia de uma quarta relacao produz quatro problemas concretos. A relacao
depende de interpretacao: um caminho em `Entry points` pode ser codigo a
alterar, teste relevante, exemplo ou a propria fonte da demanda, e o agente
precisa adivinhar. A referencia pode ser omitida nas fases seguintes, porque
nada garante que uma mencao feita no Intake sera reconsiderada no Study ou no
Document. A informacao e duplicada quando varias issues derivam do mesmo
documento, produzindo variacoes de caminho e divergencias entre issues irmas. E
nao ha distincao entre fonte e destino documental, entre o que fundamentou a
issue e o que sera produzido ou alterado por ela.

Ha ainda o envelhecimento silencioso: documentacao viva e movida, renomeada ou
removida, e uma referencia invalida escondida no corpo da issue so aparece
quando um agente tenta usa-la.

## Objective

Fazer o YODA reconhecer a documentacao anterior a issue como fonte de contexto
de primeira classe: uma associacao opcional, estruturada e distinguivel das
demais relacoes, registrada na issue e efetivamente considerada pelos runbooks
de Intake, Study e Document, sem alterar o comportamento das issues que nao a
utilizarem.

## Scope

- Declarar `source_doc` como campo opcional de front matter, na ordem canonica
  e entre os opcionais omitidos quando vazios, em `issue_metadata.py`.
- Criar helper compartilhado de normalizacao e validacao de escrita, e de
  calculo do alerta de leitura.
- Aceitar como referencia um arquivo ou uma pasta do projeto consumidor,
  informada como caminho absoluto ou relativo e gravada sempre relativa a raiz.
- Implementar `--source-doc` em `issue_add.py`.
- Implementar `--source-doc` e `--clear-source-doc` em `todo_update.py`,
  incluindo o campo no diff de alteracao.
- Carregar `source_doc` em `issue_index.py`, sem validacao.
- Criar modulo compartilhado de runbook consumido por `yoda_flow_next.py` e
  `yoda_prep_flow.py`, com linhas condicionais em Study e Document.
- Expor `source_doc` e `extern_issue_file` nas saidas de `yoda_flow_next.py`,
  `yoda_prep_flow.py`, `todo_list.py` e `todo_next.py`, corrigindo a
  invisibilidade atual de `extern_issue_file`.
- Emitir alerta nao bloqueante quando um `source_doc` existente apontar para
  caminho inexistente.
- Atualizar o runbook de `yoda_intake.py` para perguntar explicitamente pela
  documentacao-base, aceitar arquivo ou pasta, inventariar pasta e orientar a
  leitura antes de concluir a issue.
- Atualizar `yoda/yoda.md`, `yoda/scripts/README.md` e as specs afetadas.
- Adicionar testes de contrato, incluindo coexistencia entre `source_doc`,
  `extern_issue_file`, `depends_on` e entry points.

## Out of scope

- Tornar obrigatoria a criacao de documentacao antes de uma issue.
- Exigir esse fluxo de todos os desenvolvedores.
- Migrar automaticamente issues antigas.
- Transformar entry points existentes em documentacao-base.
- Inferir silenciosamente que um arquivo citado e a fonte da demanda.
- Copiar o conteudo da documentacao para dentro da issue.
- Substituir a conversa de Intake ou a investigacao do Study pela leitura da
  documentacao.
- Atualizar automaticamente a documentacao-base durante o Document.
- Sincronizar automaticamente varias issues derivadas do mesmo documento.
- Criar um sistema geral de gestao documental dentro do YODA.
- Alterar o contrato de `extern_issue_file`, de `depends_on` ou da secao
  `Entry points`.

## Requirements

- O uso de documentacao-base MUST ser opcional; a ausencia nao e erro nem sinal
  de issue incompleta.
- O Intake MUST perguntar explicitamente se existe documentacao-base, e uma
  resposta negativa MUST preservar o fluxo atual sem perguntas adicionais nas
  fases seguintes.
- A referencia MUST poder representar um arquivo e MUST poder representar uma
  pasta.
- O valor MUST representar uma localizacao dentro do projeto consumidor, e nao
  dentro do repositorio publico do YODA.
- A validacao MUST impedir referencias que escapem do projeto consumidor.
- O agente MUST ler a documentacao informada antes de concluir o Intake; quando
  a referencia apontar para uma pasta, MUST identificar os materiais relevantes
  dentro dela.
- O Intake MUST usar a documentacao como fonte de contexto, sem assumir que todo
  o seu conteudo pertence ao escopo da issue.
- A associacao MUST ser registrada de forma estruturada na issue e MUST
  permanecer distinguivel de entry points, de `depends_on` e de
  `extern_issue_file`.
- Uma issue MUST poder possuir simultaneamente documentacao-base e issue
  externa.
- O runbook de Study MUST orientar a leitura da documentacao-base quando ela
  estiver presente, MUST permitir identificar divergencias entre a documentacao
  e o estado atual do projeto, e MUST diferenciar decisoes ja documentadas de
  questoes ainda em aberto.
- O Study MUST tratar a documentacao como contexto qualificado, nao como
  instrucao incontestavel; a existencia da referencia nao elimina a analise de
  codigo, testes e configuracoes.
- O Document MUST considerar a documentacao-base ao consolidar as decisoes
  aprovadas, e MUST NOT interpretar a associacao como autorizacao automatica
  para edita-la.
- Qualquer atualizacao da documentacao-base MUST depender do escopo e das
  decisoes aprovadas da propria issue.
- Issues sem a associacao MUST manter o comportamento atual, e issues antigas
  MUST permanecer validas.
- O caminho informado MUST ser normalizado para a forma relativa a raiz do
  projeto antes de ser gravado; o caminho da maquina MUST NOT chegar ao front
  matter.
- Na escrita, um caminho fora da raiz do projeto ou inexistente MUST ser
  rejeitado.
- Na leitura, um `source_doc` inexistente MUST produzir alerta e MUST NOT fazer
  qualquer comando falhar.
- Uma fonte declarada MUST NOT ser ignorada silenciosamente.
- Os textos MUST permanecer em ingles onde o documento existente estiver em
  ingles.
- Nenhum texto em `project/specs/` pode citar issue concreta por link, numero ou
  ID; o rationale entra autocontido.

## Acceptance criteria

- [x] O campo se chama `source_doc`, e opcional, e e omitido do front matter
      quando vazio, sob `schema_version` `2.01`.
- [x] Durante o Intake, o agente pergunta se existe uma documentacao-base.
- [x] O desenvolvedor pode recusar a associacao sem impedir a criacao da issue,
      e o fluxo segue identico ao atual.
- [x] O desenvolvedor pode informar um arquivo existente no projeto como
      documentacao-base.
- [x] O desenvolvedor pode informar uma pasta existente no projeto como
      documentacao-base.
- [x] A documentacao informada e lida antes da conclusao da issue, com
      inventario dos materiais relevantes no caso de pasta.
- [x] A associacao e preservada de forma estruturada na issue criada e nao
      precisa ser repetida manualmente para que as fases seguintes a conhecam.
- [x] `source_doc` e `extern_issue_file` aparecem nas saidas de
      `yoda_flow_next.py`, `yoda_prep_flow.py`, `todo_list.py` e `todo_next.py`,
      corrigindo a invisibilidade atual de `extern_issue_file`.
- [x] `yoda_flow_next.py` e `yoda_prep_flow.py` compartilham a composicao de
      runbook em vez de duplicar o texto condicional.
- [x] A associacao nao e confundida com uma dependencia entre issues, com um
      entry point nem com uma issue externa.
- [x] Uma issue pode possuir documentacao-base e issue externa simultaneamente.
- [x] O valor gravado e sempre relativo a raiz do projeto, POSIX, sem `./` e sem
      barra final, mesmo quando o desenvolvedor informa caminho absoluto ou
      relativo ao diretorio atual.
- [x] Um caminho absoluto e convertido para a forma relativa a raiz; o caminho
      da maquina nunca chega ao front matter.
- [x] Uma referencia que aponte para fora da raiz do projeto e rejeitada na
      escrita.
- [x] Um caminho inexistente e rejeitado na escrita.
- [x] Uma issue ja criada cujo `source_doc` deixou de existir produz alerta na
      saida e nao faz nenhum comando falhar.
- [x] A associacao pode ser informada, atualizada e removida apos a criacao.
- [x] `init.py` preserva a associacao em saneamento e reconstrucao.
- [x] Ao iniciar o Study de uma issue associada, o runbook orienta o agente a
      ler a documentacao-base.
- [x] O runbook de Study orienta confrontar a documentacao com o estado atual do
      projeto e separar decisoes ja estabelecidas de questoes em aberto.
- [x] Ao executar o Document, o runbook orienta considerar a documentacao-base e
      declara que a associacao nao autoriza altera-la automaticamente.
- [x] Uma issue sem documentacao-base continua percorrendo o fluxo habitual, e
      as issues existentes permanecem validas.
- [x] `yoda/yoda.md`, `yoda/scripts/README.md` e as specs afetadas estao
      alinhados ao contrato implementado, e mantem documentacao-base e entry
      point como conceitos separados.
- [x] Ha testes de contrato cobrindo criacao com e sem a associacao, arquivo e
      pasta, normalizacao de caminho, coexistencia com `extern_issue_file` e
      `depends_on`, e o texto dos runbooks de Intake, Study e Document.
- [x] Os criterios que descrevem comportamento do agente estao verificados como
      contrato de texto de runbook, e o Evaluate registra essa natureza de forma
      explicita.
- [x] `yoda/scripts/tests` e `project/tests` permanecem passando.

## Entry points

- `yoda/scripts/issue_add.py`
- `yoda/scripts/todo_update.py`
- `yoda/scripts/yoda_intake.py`
- `yoda/scripts/yoda_flow_next.py`
- `yoda/scripts/yoda_prep_flow.py`
- `yoda/scripts/init.py`
- `yoda/scripts/lib/issue_index.py`
- `yoda/scripts/lib/issue_metadata.py`
- `yoda/scripts/todo_next.py`
- `yoda/scripts/lib/output.py`
- `yoda/yoda.md`
- `yoda/scripts/README.md`
- `project/specs/00-conventions.md`
- `project/specs/04-todo-dev-yaml-issues.md`
- `project/specs/11-yoda-intake.md`
- `project/specs/14-issue-templates-usage.md`
- `project/specs/16-todo-list-script.md`
- `project/specs/18-issue-add-script.md`
- `project/specs/20-todo-update-script.md`
- `project/specs/21-yoda-flow-next-script.md`
- `project/specs/25-yoda-intake-script.md`
- `project/specs/27-yoda-prep-flow-script.md`
- `yoda/scripts/tests/test_issue_add.py`
- `yoda/scripts/tests/test_yoda_intake.py`
- `yoda/scripts/tests/test_yoda_flow_next.py`
- `yoda/scripts/tests/test_todo_update.py`
- `yoda/scripts/tests/test_init.py`
- `yoda/scripts/tests/conftest.py`

## Implementation notes

Esta issue foi criada por decisao explicita do humano como unidade unica de
execucao, cobrindo contrato, implementacao, runbooks, manual, specs e testes. A
issue externa recomendava um Study dedicado de implementacao antes do desenho; o
Study desta issue absorve esse papel e nao pode ser tratado como formalidade.

O precedente mais proximo e `extern_issue_file`: campo opcional no front matter,
com caminho relativo, omitido quando ausente. O Study deve avaliar se a
documentacao-base segue a mesma forma ou se difere, considerando que
`extern_issue_file` aponta para um artefato gerado pelo proprio YODA dentro de
`yoda/project/extern_issues/`, enquanto a documentacao-base aponta para material
preexistente e arbitrario do projeto consumidor. As duas referencias nao tem a
mesma natureza de confiabilidade nem o mesmo ciclo de vida.

As questoes herdadas da issue externa foram fechadas no Study e estao
registradas em `## Approved decisions` e `## Document contract`. Duas delas
deixaram de ser problema de codigo: selecao de arquivos em pasta grande e
tratamento de formatos nao textuais sao texto de runbook, porque nenhum script
do YODA le a documentacao; quem le e o agente.

O achado que mais condiciona a implementacao: hoje `extern_issue_file` e
carregado pelo indice e nunca aparece em nenhuma saida de comando. Reproduzir
esse padrao para `source_doc` faria a associacao falhar o proprio criterio que
motiva a issue. Por isso a correcao da visibilidade de `extern_issue_file` entra
no mesmo escopo.

## Tests

- Estender `yoda/scripts/tests/test_issue_add.py`: criacao sem `--source-doc`
  (front matter sem o campo), com arquivo, com pasta, com caminho absoluto
  dentro da raiz, com caminho fora da raiz (rejeitado), com caminho inexistente
  (rejeitado) e com `extern_issue_file` simultaneo.
- Adicionar teste do helper de normalizacao: `~`, caminho absoluto, caminho
  relativo ao diretorio atual, `..`, symlink, barra final e separador; forma
  gravada sempre POSIX relativa a raiz, sem `./`.
- Estender `yoda/scripts/tests/test_todo_update.py`: informar, atualizar e
  remover `source_doc`; presenca do campo no diff; rejeicao de
  `--source-doc` combinado com `--clear-source-doc`.
- Adicionar teste do alerta de leitura: issue com `source_doc` apontando para
  caminho removido produz alerta e o comando continua com codigo de sucesso.
- Estender `yoda/scripts/tests/test_yoda_intake.py`: presenca da pergunta sobre
  documentacao-base no runbook e das instrucoes de leitura e inventario.
- Estender `yoda/scripts/tests/test_yoda_flow_next.py` e adicionar cobertura em
  `test_yoda_prep_flow.py`: runbooks de Study e Document com e sem
  `source_doc`, ausencia de linha condicional em Implement e Evaluate, e a
  declaracao de que a associacao nao autoriza edicao automatica.
- Estender `yoda/scripts/tests/test_todo_list.py` e `test_todo_next.py`:
  exposicao de `source_doc` e `extern_issue_file`.
- Estender `yoda/scripts/tests/test_init.py`: preservacao do campo em saneamento,
  sem migracao de `schema_version`.
- Adicionar teste de coexistencia entre `source_doc`, `extern_issue_file`,
  `depends_on` e entry points.
- Executar `python3 -m pytest yoda/scripts/tests`.
- Executar `python3 -m pytest project/tests`. As duas suites nao podem ser
  executadas na mesma invocacao.

## Risks and edge cases

- Tornar o fluxo opcional apenas nominalmente, introduzindo fricao para quem nao
  trabalha a partir de documentacao previa.
- Tratar a documentacao como especificacao definitiva, ignorando que ela pode
  conter hipoteses, decisoes provisorias e informacao desatualizada.
- Confundir documentacao-base com entry point, ou com issue externa, ao escrever
  os runbooks; um mesmo arquivo pode exercer os dois papeis sem que os conceitos
  sejam equivalentes.
- Permitir que o Document altere documentacao compartilhada por varias issues
  sem autorizacao, antecipando decisoes ou produzindo inconsistencias.
- Referencia que envelhece: caminho movido, renomeado ou removido apos a criacao
  da issue, com risco de a fonte ser ignorada silenciosamente.
- Pasta muito grande, ou com arquivos binarios e formatos nao textuais, tornando
  a leitura do Intake impraticavel.
- Referencia apontando para fora do projeto consumidor, por caminho relativo
  ascendente ou absoluto.
- Duplicar a documentacao dentro da issue, dificultando identificar qual versao
  e a fonte vigente.
- Alongar os runbooks a ponto de o agente perder os passos seguintes.
- Escopo unico grande: risco de o Implement comecar antes de o contrato estar
  fechado no Document.

## Study findings

### 1. O precedente estrutural existe e e menor do que parece

`extern_issue_file` foi introduzido pelo mesmo caminho que esta associacao
precisa percorrer: campo opcional no front matter, omitido quando vazio,
declarado em `CANONICAL_ISSUE_FIELD_ORDER` e `OPTIONAL_EMPTY_KEYS` em
`yoda/scripts/lib/issue_metadata.py`, lido em `yoda/scripts/lib/issue_index.py`,
escrito por `issue_add.py` e mutavel por `todo_update.py`.

Alem disso, `project/specs/00-conventions.md` registra que o schema `2.01`
"adds an optional field" em relacao ao `2.00`. Ou seja, acrescentar um campo
opcional ja tem politica de versionamento estabelecida e um precedente
executado: readers aceitam a versao anterior durante a janela de migracao,
writers persistem a nova, e `init.py` atualiza o marcador sem inventar valores.

### 2. O campo nao precisa ser lido por nenhum script

Nenhum script do YODA precisa abrir a documentacao-base. Quem le e interpreta o
material e o agente, orientado pelo runbook. Os scripts precisam apenas
armazenar o caminho, valida-lo, expo-lo nas saidas e condicionar o texto dos
runbooks a sua presenca.

Isso reduz drasticamente a superficie de implementacao. As questoes herdadas da
issue externa sobre "como o agente deve selecionar arquivos quando a referencia
apontar para uma pasta grande" e "como lidar com formatos que nao podem ser
lidos diretamente como texto" nao sao problemas de codigo: sao texto de runbook.

### 3. O ponto critico: hoje `extern_issue_file` e invisivel para as fases

`grep` por `extern_issue_file` em `todo_list.py`, `todo_next.py`,
`yoda_flow_next.py` e `yoda_prep_flow.py` nao retorna nenhuma ocorrencia. O
campo e carregado no registro do indice por `issue_index.py` e nunca aparece em
nenhuma saida de comando.

Consequencia pratica: quando o agente entra no Study, a saida do
`yoda_flow_next.py` nao informa que existe uma issue externa. O agente so
descobre se abrir o markdown por conta propria.

Este e exatamente o problema que a issue externa descreve como "a referencia
pode ser omitida nas fases seguintes". Se a documentacao-base for implementada
copiando o padrao de `extern_issue_file`, ela reproduz o mesmo defeito e o
criterio "a referencia nao precisa ser repetida manualmente apenas para que as
fases seguintes saibam que ela existe" nao e atendido.

Conclusao: armazenar o campo e condicao necessaria e insuficiente. A associacao
precisa aparecer na saida do comando que entra na fase.

### 4. Os runbooks de fase sao constantes estaticas

`RUNBOOK_BY_STEP` e um `dict` literal em `yoda/scripts/yoda_flow_next.py`
(linhas 32-53) e um segundo `dict` literal, com textos diferentes, em
`yoda/scripts/yoda_prep_flow.py` (linhas 33-44). O texto e selecionado por
`RUNBOOK_BY_STEP[next_step]`, sem qualquer parametro da issue.

Tornar o runbook condicional a presenca da documentacao-base exige trocar o
acesso por indice por uma funcao que receba a issue. Isso e uma mudanca
arquitetural pequena mas real, e precisa acontecer nos dois scripts, que hoje
duplicam o conceito sem compartilhar codigo.

Facilitador: `runbook_md_lines` em `yoda/scripts/lib/output.py` ja tolera
runbooks de multiplas linhas e indenta continuacoes dentro do mesmo item de
lista. Acrescentar linhas condicionais nao quebra a renderizacao.

Restricao: `project/specs/00-conventions.md` exige que `runbook_line` seja
"imperative and as compact as the instruction". Isso limita quanto texto
condicional pode ser acrescentado, e conversa diretamente com o risco de
alongar o runbook a ponto de o agente perder os passos seguintes.

### 5. Existem duas camadas de validacao e a viva nao valida nada

`yoda/scripts/lib/validate.py` possui `validate_issue_item`, que valida
`extern_issue_file` contra a regex
`^\.\./extern_issues/[a-z0-9-]+-\d+\.json$`. Essa funcao e alcancada apenas por
`init.py` e por `lib/todo_utils.py`, ambos no caminho legado do TODO YAML.

O caminho vivo, de leitura de issues markdown, e `issue_index.py`, que faz
apenas `str(metadata.get("extern_issue_file", "") or "")`, sem validacao
nenhuma.

Portanto a decisao "onde validar o caminho da documentacao-base" nao tem
resposta obvia por analogia. Seguir o precedente literalmente significa validar
no lugar que nao executa. A validacao util precisa entrar em `issue_index.py`,
que e fail-fast em todo o conjunto de issues do desenvolvedor.

Isso cria uma tensao concreta: `issue_index.py` falha o carregamento inteiro
quando uma issue e invalida. Se um caminho de documentacao que deixou de existir
for tratado como erro de validacao ali, uma unica referencia quebrada derruba
todos os comandos YODA para aquele desenvolvedor. O requisito de nao ignorar
silenciosamente uma fonte declarada colide com o modelo fail-fast do indice.

Nota lateral: `validate.py` ainda carrega `ALLOWED_ENTRY_TYPES` com o valor
`doc`, residuo dos `entrypoints` tipados removidos do YAML. E codigo morto no
caminho markdown, mas e uma colisao de nomenclatura a evitar ao batizar o campo
novo.

### 6. O precedente de caminho relativo nao serve

`extern_issue_file` vale `../extern_issues/<provider>-<NNN>.json`, relativo ao
diretorio do arquivo da issue (`yoda/project/issues/`). Aplicar a mesma
convencao a documentacao-base produziria valores como
`../../../docs/arquitetura.md`, ilegiveis e frageis.

`repo_root()` em `yoda/scripts/lib/paths.py` e `parents[3]` do proprio arquivo,
o que resolve exatamente para a raiz do projeto consumidor quando o YODA esta
embarcado. Existe, portanto, uma ancora bem definida para caminhos relativos a
raiz do projeto, e ela e diferente da ancora usada por `extern_issue_file`.

Divergir do precedente aqui parece correto, mas e uma decisao explicita: passa a
haver dois campos de caminho no mesmo front matter com ancoras diferentes.

### 7. `init.py` ja preserva campos desconhecidos, mas fora de ordem

`_reconcile_issue_front_matter` em `yoda/scripts/init.py` remove apenas `id` e
atualiza `schema_version`; nao apaga chaves que nao conhece.
`canonicalize_issue_metadata` reordena pelos campos canonicos e reanexa ao final
qualquer chave nao listada.

Logo, um campo novo sobrevive ao saneamento mesmo sem alteracao, mas fica fora
da ordem canonica ate ser declarado em `CANONICAL_ISSUE_FIELD_ORDER`. E preciso
declara-lo tambem em `OPTIONAL_EMPTY_KEYS` para que seja omitido quando vazio,
conforme a politica de campos opcionais.

### 8. O Intake nao tem estado por issue

O runbook de Intake e montado por `_full_runbook(dev, external, external_file)`
em `yoda/scripts/yoda_intake.py`, a partir de um booleano. No momento do Intake
a issue ainda nao existe, entao nao ha onde consultar a associacao.

Consequencia: a pergunta sobre documentacao-base e apenas mais um passo numerado
no texto do runbook, de baixo custo. Mas a resposta so pode ser gravada se
`issue_add.py` receber uma flag nova, hoje inexistente.

### 9. Boa parte dos criterios de aceite so e testavel como texto de runbook

Criterios como "a documentacao informada e lida antes da conclusao da issue" ou
"o Study confronta a documentacao com o estado atual do projeto" descrevem
comportamento do agente, nao do script. A suite so consegue verificar que a
instrucao correspondente esta presente no runbook emitido.

O repositorio ja usa esse padrao: existem testes de contrato sobre o texto de
runbooks. E preciso reconhecer explicitamente que a verificacao e indireta, para
que o Evaluate nao prometa mais do que a suite entrega.

### 10. Linha de base

`python3 -m pytest yoda/scripts/tests` passa com 102 testes.
`python3 -m pytest project/tests` passa com 17 testes.

## Approved decisions

Decisoes fechadas com o humano no encerramento do Study. O Implement nao pode
introduzir decisao nova fora deste conjunto.

1. **Nome do campo**: `source_doc`. Escolhido sobre `spec_source` porque a fonte
   pode ser planilha, JSON, colecao de requisicoes, diagrama ou nota de reuniao,
   e nao apenas especificacao; e porque `spec` ja nomeia `project/specs/` neste
   repositorio, que e outro conceito.
2. **Ancora do caminho**: raiz do projeto consumidor. O valor gravado nunca pode
   carregar o caminho da maquina, sob pena de perder portabilidade.
3. **Cardinalidade**: caminho unico, capaz de representar arquivo ou pasta.
   Multiplas fontes se resolvem agrupando o material em uma pasta. A
   simplificacao e deliberada.
4. **Onde validar**: forma e existencia sao validadas na escrita, em
   `issue_add.py` e `todo_update.py`, e bloqueiam. `issue_index.py` nao valida
   `source_doc`; apenas carrega o valor.
5. **Caminho invalido apos a criacao**: alerta na saida, nunca bloqueio. Nenhum
   script pode falhar porque um `source_doc` deixou de existir.
6. **Surface**: linha condicional no runbook para `source_doc`, e correcao da
   invisibilidade de `extern_issue_file` no mesmo passo. Os dois campos tem
   pesos diferentes: `extern_issue_file` importa sobretudo no Intake, enquanto
   `source_doc` importa em varias fases. O tratamento nao e o mesmo texto
   aplicado duas vezes.
7. **Duplicacao de runbook**: extrair para modulo compartilhado entre
   `yoda_flow_next.py` e `yoda_prep_flow.py`.
8. **Schema**: permanece `2.01`. Como o campo e opcional e omitido quando vazio,
   issues existentes seguem validas sem migracao e `init.py` nao precisa agir.
   Consequencia aceita: a ordem canonica descrita para `2.01` passa a incluir
   `source_doc`, e nao havera como distinguir issues escritas antes e depois.
   Nada no framework depende dessa distincao.
9. **Backlog**: expor a associacao tambem em `todo_list.py` e `todo_next.py`.
10. **Superficie de teste**: criterios que descrevem comportamento do agente sao
    verificados como contrato de texto de runbook. O Evaluate MUST registrar
    essa natureza de forma explicita, em vez de afirmar comportamento verificado.

Nao decidido pelo humano, assumido e apresentado sem objecao: caminho relativo
informado na linha de comando resolve contra o diretorio atual, nao contra a
raiz do projeto. As duas leituras coincidem no uso normal, porque os comandos
YODA sao executados da raiz.

## Document contract

O Implement deve seguir esta ordem e nao introduzir decisoes fora deste
contrato.

### 1. Contrato do campo

- Nome: `source_doc`. Tipo: string. Opcional.
- Declarado em `OPTIONAL_EMPTY_KEYS` e em `CANONICAL_ISSUE_FIELD_ORDER` em
  `yoda/scripts/lib/issue_metadata.py`, imediatamente apos `extern_issue_file`.
- Omitido do front matter quando vazio, conforme a politica de campos opcionais.
- `schema_version` permanece `2.01`.
- Valor gravado: caminho relativo a raiz do projeto, com separador POSIX, sem
  `./` inicial e sem barra final. Pode denotar arquivo ou pasta.

### 2. Normalizacao e validacao na escrita

Um helper compartilhado, novo, resolve o valor informado. Ele nao pertence a
`yoda/scripts/lib/validate.py`, que serve ao caminho legado do TODO YAML e nao
executa na leitura de issues markdown.

Ordem obrigatoria:

1. Expandir `~`.
2. Se o caminho for absoluto, usa-lo; caso contrario, resolver contra o
   diretorio atual.
3. Resolver `..` e symlinks.
4. Verificar contencao na raiz do projeto, comparando com `repo_root()` tambem
   resolvido. Fora da raiz: erro de validacao, nao grava.
5. Verificar existencia, arquivo ou pasta. Inexistente: erro de validacao, nao
   grava.
6. Gravar a forma relativa a raiz, POSIX, sem `./` e sem barra final.

Os passos 4 e 5 bloqueiam apenas na escrita. Nenhum deles roda na leitura.

### 3. Superficie de CLI

- `issue_add.py`: `--source-doc <path>`.
- `todo_update.py`: `--source-doc <path>` e `--clear-source-doc`, seguindo a
  forma ja usada por `--extern-issue-file` e `--clear-extern-issue-file`,
  incluindo a rejeicao de combinacao contraditoria entre definir e limpar.
- `source_doc` entra na lista de campos de `_diff_fields` em `todo_update.py`,
  para aparecer no log de alteracao.

### 4. Leitura

- `issue_index.py` carrega `source_doc` como string, sem validar, espelhando o
  tratamento atual de `extern_issue_file`.
- Um helper de leitura calcula o alerta: `source_doc` nao vazio cujo caminho,
  resolvido a partir da raiz do projeto, nao existe.
- O helper retorna informacao; ele MUST NOT levantar excecao.

### 5. Surface nas saidas

`yoda_flow_next.py` e `yoda_prep_flow.py`, nas linhas de cabecalho da saida md,
quando o valor existir:

- `External issue file: <valor>`
- `Source doc: <valor>`
- `Alert: source_doc path not found: <valor>` quando o caminho nao existir.

`todo_list.py` e `todo_next.py` expoem os dois campos na visao de backlog.

O payload JSON ja carrega os campos onde o registro do indice e serializado;
onde nao carregar, incluir.

### 6. Runbooks condicionais

Modulo compartilhado novo, consumido por `yoda_flow_next.py` e
`yoda_prep_flow.py`, substituindo o acesso direto a `RUNBOOK_BY_STEP[step]` por
uma composicao que recebe o registro da issue.

Linhas acrescentadas apenas quando `source_doc` estiver preenchido:

- Em `study`: instruir a ler `source_doc` como contexto qualificado, confrontar
  com o estado atual do projeto, e separar decisoes ja estabelecidas de questoes
  ainda em aberto.
- Em `document`: instruir a considerar `source_doc` ao consolidar as decisoes
  aprovadas, e declarar que a associacao nao autoriza edita-la; qualquer
  atualizacao depende do escopo aprovado da issue.
- Em `implement` e `evaluate`: nenhuma linha condicional. O valor permanece
  visivel no cabecalho, sem obrigacao associada.

`extern_issue_file` nao recebe linha condicional de runbook nas fases. Sua
correcao e de visibilidade, pelas linhas de cabecalho da secao 5, coerente com
o peso maior que ele tem no Intake.

Os textos MUST permanecer em ingles e MUST respeitar a regra de
`project/specs/00-conventions.md` de manter `runbook_line` imperativo e compacto.

### 7. Intake

`yoda_intake.py` acrescenta, nos dois runbooks montados por `_full_runbook`, um
passo perguntando se existe documentacao-base, instruindo a aceitar arquivo ou
pasta, a inventariar o conteudo quando for pasta, e a ler o material antes de
concluir a issue. Resposta negativa MUST manter o fluxo atual sem passo extra
nas fases seguintes.

### 8. Documentacao

- `yoda/yoda.md`: registrar `source_doc` e sua distincao frente a
  `extern_issue_file`, `depends_on` e entry points.
- `yoda/scripts/README.md`: incluir `source_doc` na lista de front matter.
- `project/specs/00-conventions.md`: ordem canonica.
- `project/specs/04-todo-dev-yaml-issues.md`: listas de campos.
- `project/specs/11-yoda-intake.md` e `project/specs/25-yoda-intake-script.md`:
  passo de Intake.
- `project/specs/18-issue-add-script.md` e
  `project/specs/20-todo-update-script.md`: flags e normalizacao.
- `project/specs/21-yoda-flow-next-script.md` e
  `project/specs/27-yoda-prep-flow-script.md`: runbooks condicionais e cabecalho.
- `project/specs/16-todo-list-script.md`: exposicao no backlog.
- `project/specs/14-issue-templates-usage.md`: apenas se a descricao da ordem
  canonica exigir ajuste.

`yoda/templates/issue.md` NAO muda. Seu front matter e vazio e o front matter
real e gerado pelos scripts; a associacao nao ganha secao no corpo, porque
duplicar a referencia no corpo e explicitamente fora de escopo.

`yoda/scripts/lib/validate.py` NAO muda. O valor `doc` em `ALLOWED_ENTRY_TYPES`
permanece como esta; e residuo do caminho legado e nao conflita com
`source_doc`. As specs MUST manter documentacao-base e entry point como
conceitos separados.

### 9. Ordem de execucao do Implement

1. `issue_metadata.py`: campo na ordem canonica e nos opcionais vazios.
2. Helper compartilhado de normalizacao, validacao de escrita e alerta de
   leitura.
3. `issue_add.py` e `todo_update.py`: flags e gravacao.
4. `issue_index.py`: carga do campo.
5. Modulo compartilhado de runbook; `yoda_flow_next.py` e `yoda_prep_flow.py`.
6. `todo_list.py` e `todo_next.py`.
7. `yoda_intake.py`.
8. Testes.
9. `yoda/yoda.md`, `yoda/scripts/README.md` e specs.

## Evaluation findings

- 25 de 26 criterios de aceite foram comprovados por revisao do diff, testes de
  contrato e execucao das suites.
- Os criterios que descrevem comportamento do agente foram verificados como
  contrato de texto dos runbooks. Isso comprova a presenca e a estabilidade da
  instrucao, nao a execucao material do comportamento por um agente.
- Achado do primeiro Evaluate, agora corrigido: a suite cobria criacao com e sem
  `source_doc`, arquivo, pasta, normalizacao e coexistencia com
  `extern_issue_file` em testes separados, mas nao exercitava as quatro relacoes
  ao mesmo tempo. Foram adicionados dois testes conjuntos em
  `yoda/scripts/tests/test_source_doc.py`:
  - `test_all_four_relations_coexist_and_stay_distinct`: uma issue carrega
    `source_doc`, `extern_issue_file`, `depends_on` e uma secao `Entry points`
    simultaneamente; nenhuma relacao vaza para outra; um mesmo arquivo pode
    figurar como `source_doc` e como entry point sem que os conceitos se
    confundam; e o bloqueio por dependencia continua decidido apenas por
    `depends_on`.
  - `test_relations_are_independently_mutable`: limpar `source_doc`,
    `extern_issue_file` ou `depends_on` nao afeta as outras duas relacoes.
- Segundo achado, nao bloqueante, tambem corrigido: na primeira versao de
  `test_relations_are_independently_mutable`, o terceiro caso limpava
  `depends_on` quando `extern_issue_file` ja havia sido removido pelo caso
  anterior. A assercao comprovava a preservacao de uma relacao, nao das duas
  que o nome do teste promete. O teste passou a restaurar `extern_issue_file`
  antes do terceiro caso e a afirmar explicitamente a preservacao das duas
  relacoes restantes. A correcao foi confirmada por mutacao: forcar
  `--clear-depends-on` a limpar tambem `extern_issue_file` faz o teste falhar,
  o que prova que a assercao nao e vazia.
- Com isso, os 26 criterios de aceite estao atendidos.
- Verificacoes executadas apos a correcao:
  `python3 -m pytest yoda/scripts/tests` (151 passed),
  `python3 -m pytest project/tests` (17 passed) e `git diff --check` limpo.
  O primeiro Evaluate havia registrado 149 passed e tambem
  `python3 -m compileall -q yoda/scripts`.

## Result log

feat(yoda): associate base documentation with issues

Adiciona `source_doc` opcional com normalizacao e validacao na escrita, alerta
na leitura, visibilidade nas saidas, orientacao condicional nos runbooks e
contrato alinhado em manual, specs e testes. Corrige tambem a invisibilidade de
`extern_issue_file` nas saidas dos comandos de fase e de backlog. O Evaluate
confirmou os 26 criterios de aceite. Os criterios que descrevem comportamento do
agente foram verificados como contrato de texto dos runbooks: isso comprova a
presenca e a estabilidade da instrucao, nao a execucao material do
comportamento.

- **GitHub Issue** :   #12

- **Issue**: `yoda-0071`

- **Path**: `yoda/project/issues/yoda-0071-associar-documentacao-base-opcional-as-issues-do-yoda.md`

## Flow log
- 2026-09-01T10:35:26-03:00 issue_add created title=Associar documentacao-base opcional as issues do YODA; priority=5
- 2026-09-01T10:46:31-03:00 transition to-do->doing/study
- 2026-09-01T11:15:56-03:00 transition doing/study->doing/document | study closed: 10 decisions settled; source_doc normalized to project root, blocking on write, alert on read
- 2026-09-01T11:33:18-03:00 transition doing/document->doing/implement | document contract closed: source_doc field, shared normalization helper, shared runbook module, extern_issue_file visibility
- 2026-09-01T11:57:46-03:00 transition doing/implement->doing/evaluate
- 2026-09-01T13:58:59-03:00 evaluate remediation: added joint coexistence tests for source_doc, extern_issue_file, depends_on and entry points; 26/26 criteria met
- 2026-09-01T14:13:16-03:00 evaluate remediation 2: third mutability case now starts with all three relations set; assertion mutation-checked
- 2026-09-01T14:15:08-03:00 transition doing/evaluate->done | evaluate approved: 26/26 criteria met; source_doc shipped with runbook, spec and test coverage
