---
schema_version: '2.01'
status: done
title: Garantir independencia entre specs e produto YODA
description: 'Definir e aplicar o principio de independencia bidirecional: project/specs
  deve ser autocontido e suficiente para um agente de AI reconstruir o YODA sem depender
  do historico de issues ou da arvore do projeto; o produto YODA empacotado deve permanecer
  autocontido sem depender de project/specs. Remover ou substituir links de specs
  para issues, estabelecer uma forma de rastreabilidade que nao crie dependencia normativa
  e descrever esse conceito explicitamente nas proprias specs.'
priority: 5
created_at: '2026-08-31T15:11:42-03:00'
updated_at: '2026-08-31T16:11:40-03:00'
---

# yoda-0065 - Garantir independencia entre specs e produto YODA

## Summary

Formalizar e aplicar a independencia bidirecional entre o conjunto normativo
`project/specs/` e o produto YODA distribuido. As specs devem ser autocontidas o
suficiente para orientar a reconstrucao do framework sem consultar o historico
do projeto; o pacote YODA deve funcionar sem conter nem consultar as specs.

## Context

A yoda-0064 sincronizou as specs com o estado atual, mas introduziu em
`project/specs/23-distribution-and-packaging.md` um link direto para a issue
yoda-0016 e registrou decisoes por IDs de issues. Ja existiam referencias
historicas semelhantes em `project/specs/05-scripts-and-automation.md` e na
propria spec 23.

Essas referencias confundem dois artefatos com ciclos de vida diferentes:

- `project/specs/` e o contrato portavel e autocontido a partir do qual um
  agente de AI deve conseguir reconstruir o comportamento do YODA;
- o produto em `yoda/` e seu pacote de distribuicao devem ser autocontidos em
  runtime, pois as specs nao fazem parte do pacote;
- issues sao historico, planejamento e rastreabilidade do repositorio de
  desenvolvimento. Podem apontar para specs, mas nao devem ser necessarias para
  interpretar uma regra normativa.

Referencias ao conceito e ao caminho operacional de issues, como
`yoda/project/issues/<dev>-<NNNN>-<slug>.md`, continuam legitimas quando fazem
parte do comportamento especificado. O acoplamento indevido e com uma issue
concreta do historico deste repositorio, por link ou por ID usado como fonte da
regra.

## Objective

Definir nas proprias specs uma arquitetura de dois artefatos independentes e
eliminar dependencias cruzadas que impecam cada lado de cumprir sua finalidade:
specs suficientes para reconstrucao e produto empacotado suficiente para uso.

## Scope

- Adicionar a `project/specs/` uma regra normativa clara de independencia,
  portabilidade, direcao de rastreabilidade e autocontencao.
- Auditar todas as specs por links, IDs e justificativas dependentes de issues
  especificas do repositorio.
- Remover links de specs para arquivos em `yoda/project/issues/` e reescrever o
  contexto normativo necessario dentro da propria spec.
- Substituir referencias historicas como "decidido por yoda-NNNN" por regras,
  rationale ou notas de compatibilidade autocontidas.
- Definir quais referencias internas ao conjunto de specs sao permitidas e
  quais referencias a artefatos externos sao apenas informativas.
- Preservar a rastreabilidade no sentido issue -> spec, sem exigir o sentido
  spec -> issue.
- Auditar codigo, scripts, templates, manual embarcado e empacotamento para
  garantir que o produto nao leia nem dependa de `project/specs/`.
- Adicionar verificacoes automatizadas para prevenir a reintroducao dos dois
  tipos de acoplamento.

## Out of scope

- Alterar o comportamento funcional do YODA que ja esta normatizado.
- Incluir `project/specs/` no pacote de distribuicao.
- Remover das specs o modelo operacional de issues Markdown ou seus caminhos
  genericos, pois eles fazem parte do produto especificado.
- Proibir links entre arquivos pertencentes ao proprio conjunto portavel de
  specs.
- Migrar ou apagar issues historicas.

## Requirements

- As specs MUST conter todas as regras e justificativas necessarias para sua
  interpretacao sem acesso a `yoda/project/issues/`, Flow logs ou Git history.
- Nenhuma spec MUST usar uma issue concreta como autoridade normativa, seja por
  hyperlink, caminho relativo ou ID textual.
- Quando uma decisao historica for relevante para compatibilidade, a decisao e
  seu rationale MUST ser descritos de forma autocontida na spec.
- A rastreabilidade de implementacao SHOULD residir nas issues, apontando para
  as specs afetadas; ela nao deve introduzir dependencia reversa.
- O produto distribuido MUST operar, inicializar e atualizar sem
  `project/specs/` presente. A prova contratual e um smoke executado sobre o
  conteudo extraido do pacote em diretorio isolado; a suite
  `yoda/scripts/tests/` permanece fora do pacote.
- Codigo e artefatos empacotados MUST NOT abrir, importar ou resolver arquivos
  sob `project/specs/` em runtime.
- A documentacao normativa MUST explicar a diferenca entre: referencia ao
  dominio de issues do YODA, referencia interna entre specs e referencia ao
  historico de desenvolvimento deste repositorio.
- As verificacoes preventivas MUST produzir erro acionavel indicando o arquivo
  e a referencia proibida.

## Acceptance criteria

- [x] O principio de independencia bidirecional esta descrito normativamente em
      uma spec central e resumido no indice `project/specs/README.md`.
- [x] Um leitor com somente `project/specs/` consegue identificar arquitetura,
      comportamento, contratos, formatos e criterios necessarios para
      reconstruir uma implementacao compativel do YODA.
- [x] Nenhum arquivo normativo em `project/specs/` possui link para
      `yoda/project/issues/` nem usa um ID concreto `yoda-NNNN` como fonte de
      regra ou contexto indispensavel.
- [x] As referencias historicas encontradas nas specs 05 e 23 foram removidas
      ou reescritas como texto autocontido, preservando a regra vigente.
- [x] Referencias genericas ao modelo operacional de issues continuam
      documentadas e nao sao confundidas com dependencia do backlog deste
      repositorio.
- [x] A politica estabelece issue -> spec como direcao de rastreabilidade
      permitida, sem exigir spec -> issue.
- [x] O inventario do pacote confirma que `project/specs/` nao e distribuido e
      nenhum arquivo empacotado depende desse caminho.
- [x] Um teste ou lint falha de forma acionavel caso uma spec volte a apontar
      para uma issue concreta do repositorio.
- [x] Um teste de pacote ou ambiente isolado comprova que o YODA funciona sem a
      arvore `project/specs/`.
- [x] A suite completa permanece passando.

## Entry points

- `project/specs/00-conventions.md`
- `project/specs/05-scripts-and-automation.md`
- `project/specs/23-distribution-and-packaging.md`
- `project/specs/README.md`
- `project/specs/28-spec-independence-and-portability.md`
- `project/tests/`
- `README.md`
- `package.py`
- `yoda/scripts/tests/`
- `yoda/project/issues/yoda-0064-sincronizar-specs-com-mudancas-omitidas-em-issues-concluidas.md`

## Implementation notes

Tratar `project/specs/` como uma unidade portavel: referencias entre suas specs
sao validas, mas referencias ao backlog, aos Flow logs ou a arquivos do produto
nao podem ser necessarias para completar o significado normativo. Caminhos e
nomes do produto podem aparecer como objetos especificados, sem implicar que a
spec precise desses arquivos para ser compreendida.

Uma verificacao inicial pode procurar links com `project/issues`, caminhos
relativos que escapem de `project/specs/` e IDs concretos `yoda-[0-9]{4}`. O
lint deve permitir exemplos genericos como `<dev>-<NNNN>-<slug>.md` e evitar
falsos positivos em especificacoes do modelo de issues.

Para a independencia do pacote, validar o manifest produzido por `package.py` e
executar uma prova em diretorio temporario contendo apenas os artefatos
distribuidos. O teste nao deve depender do checkout original por `cwd`, imports
ou caminhos absolutos acidentais.

## Tests

- Adicionar lint/teste de arquitetura para referencias proibidas nas specs.
- Adicionar teste do inventario do pacote garantindo a ausencia de
  `project/specs/`.
- Adicionar teste isolado de smoke/contrato a partir do conteudo empacotado.
- Executar a suite completa de `yoda/scripts/tests` e as validacoes de package.

## Risks and edge cases

- Remover um link sem incorporar na spec a decisao que ele explicava.
- Confundir o caminho generico de issues, parte do contrato do produto, com uma
  dependencia no historico real do repositorio.
- Criar um lint amplo demais que bloqueie IDs usados em fixtures ou exemplos
  validos.
- Um teste de pacote passar por importar arquivos do checkout original sem
  perceber o acoplamento.
- Duplicar rationale em varias specs e permitir que as copias divirjam; preferir
  uma regra central com referencias internas ao conjunto normativo.

## Document contract

O Implement deve seguir esta ordem document-first e nao introduzir decisoes
novas fora deste contrato.

### 1. Nova spec 28 com o principio normativo

Criar `project/specs/28-spec-independence-and-portability.md` contendo:

- Independencia bidirecional entre o conjunto normativo `project/specs/` e o
  produto distribuido em `yoda/`.
- Autocontencao: uma regra normativa MUST ser interpretavel lendo apenas
  `project/specs/`, sem acesso a `yoda/project/issues/`, Flow logs ou Git
  history.
- Portabilidade: `project/specs/` MUST poder ser copiado isoladamente; nenhum
  link relativo pode resolver fora do diretorio.
- Taxonomia explicita dos tres tipos de referencia:
  1. Referencia ao dominio de issues do YODA, generica, por padrao de caminho
     como `yoda/project/issues/<dev>-<NNNN>-<slug>.md`: PERMITIDA, pois
     descreve o produto especificado.
  2. Referencia interna ao conjunto de specs, como `project/specs/NN-*.md`:
     PERMITIDA.
  3. Referencia ao historico de desenvolvimento deste repositorio, como ID
     concreto `<dev>-<NNNN>`, link para arquivo de issue, Flow log ou commit:
     PROIBIDA como autoridade normativa ou contexto indispensavel.
- Direcao de rastreabilidade: issue -> spec e permitida e recomendada;
  spec -> issue e proibida.
- Independencia do produto: o pacote MUST NOT conter `project/specs/` e nenhum
  artefato empacotado pode abrir, importar ou resolver esse caminho em runtime.
- Exigencia de verificacao preventiva automatizada com erro acionavel que
  identifique arquivo, linha e o trecho proibido. A spec declara a exigencia; o
  caminho concreto da suite pertence ao repositorio, nao ao contrato normativo.

### 2. Resumo e indice

- `project/specs/00-conventions.md`: adicionar regra curta de independencia e
  autocontencao, apontando para a spec 28 por referencia interna.
- `project/specs/README.md`: indexar `28. Spec independence and portability`.

### 3. Reescrita autocontida das referencias existentes

Sao exatamente quatro pontos, em dois arquivos, confirmados por auditoria:

- `project/specs/05-scripts-and-automation.md`, secao
  `Markdown-index read validation`: remover `By explicit yoda-0049 decisions` e
  manter as duas regras com rationale proprio: `phase` fora de `doing` e
  ignorada, e um alvo de dependencia ausente e tratado como resolvido, por
  compatibilidade com backlogs migrados e com dependencias fora do indice
  carregado.
- `project/specs/23-distribution-and-packaging.md`: remover o paragrafo
  `Classification recorded by yoda-0064` e o hyperlink relativo para
  `../../yoda/project/issues/`. Preservar a regra do aviso de compatibilidade
  de MAJOR/build antigo, com rationale autocontido.
- `project/specs/23-distribution-and-packaging.md`, secao `Cross-references`:
  remover a linha `Related issues`; preservar a orientacao de manter
  referencias cruzadas entre specs atualizadas.

Nenhuma regra vigente pode ser perdida na reescrita. O objetivo e trocar a
autoridade da issue pela regra escrita, nao remover a regra.

### 4. Ajuste de redacao aprovado no Study

O Requirement sobre execucao sem `project/specs/` foi reescrito nesta issue.
Motivo: `yoda/scripts/tests/**` consta em `EXCLUDE_GLOBS` de `package.py` e ha
teste vigente garantindo essa exclusao, entao nao existem testes dentro do
pacote para executar. `EXCLUDE_GLOBS` nao muda neste escopo.

### 5. Verificacoes preventivas em project/tests/

Criar a suite de repositorio `project/tests/`, separada da suite do produto,
espelhando o posicionamento de `package.py` na raiz:

- `project/tests/conftest.py`: `REPO_ROOT` derivado do proprio arquivo, sem
  depender de `cwd`.
- `project/tests/test_specs_independence.py`:
  - falha se algum link Markdown em `project/specs/**` resolver fora de
    `project/specs/`;
  - falha se algum arquivo em `project/specs/**` citar um ID concreto de issue
    deste repositorio;
  - deteccao em duas camadas para evitar falso positivo: comparacao contra os
    IDs reais derivados dos nomes de arquivo em `yoda/project/issues/`, e
    padrao `<slug>-<NNNN>` restrito aos dev slugs efetivamente presentes nesse
    diretorio;
  - o token `iso-8601` e o padrao generico `<dev>-<NNNN>-<slug>.md` NAO podem
    gerar falso positivo; incluir teste negativo provando isso;
  - a mensagem de erro MUST citar arquivo, linha e o trecho proibido.
- `project/tests/test_package_independence.py`:
  - falha se algum caminho do tar produzido por `package.py` estiver sob
    `project/`;
  - smoke isolado: extrair o pacote em diretorio temporario que nao contenha
    `project/specs/` e executar `init.py`, `issue_add.py` e
    `yoda_flow_next.py` com `cwd` no diretorio extraido, via `sys.executable`;
  - o smoke MUST falhar se algum comando resolver caminho do checkout original.

`project/tests/` nao entra no pacote: `_collect_files` percorre apenas
`yoda/templates` e `yoda/scripts`, e `project/**` ja consta em `EXCLUDE_GLOBS`.

`yoda/scripts/tests/test_package.py` permanece onde esta. Sua assercao textual
existente sobre `project/specs` nao substitui a verificacao de inventario por
caminho exigida pelos criterios desta issue.

### 6. Documentacao dos comandos

- `README.md` da raiz: documentar as duas suites e seus comandos,
  `python3 -m pytest yoda/scripts/tests` e `python3 -m pytest project/tests`,
  explicando que a primeira valida o produto e a segunda valida a fronteira
  entre repositorio e produto.

### 7. Verificacao fechada

- Executar `python3 -m pytest yoda/scripts/tests` e
  `python3 -m pytest project/tests`.
- Provar que o lint falha: introduzir temporariamente um ID concreto de issue em
  uma spec, confirmar a mensagem acionavel e reverter.
- Confirmar que nenhum link relativo de `project/specs/**` escapa do diretorio.
- Confirmar por varredura que nenhum arquivo de produto referencia
  `project/specs`.
- Nao alterar comportamento funcional ja normatizado, `INCLUDE_GLOBS` nem
  `EXCLUDE_GLOBS`.

Proxima acao deterministica apos aprovacao deste Document: entrar em Implement,
criando primeiro a spec 28, depois as reescritas em 00/05/23/README, depois
`project/tests/` e por fim o `README.md` da raiz.

## Result log

docs: garantir independencia entre specs e produto YODA

Formalizou a independencia bidirecional em uma spec portavel e autocontida,
removeu das specs as referencias ao historico de issues e preservou as regras
vigentes com rationale proprio. Separou a rastreabilidade issue -> spec da
definicao normativa e confirmou que o produto empacotado opera sem
`project/specs/`.

Adicionou verificacoes de repositorio para bloquear IDs concretos, URLs de
trackers, hashes de commit e links Markdown que escapem do conjunto portavel,
incluindo links inline, por referencia, com titulos ou destinos entre angulos.
O smoke extrai e opera o pacote em diretorio isolado sem acessar o checkout.

Evaluate: `17 passed` em `project/tests`, inclusive a partir de `/private/tmp`;
`79 passed` em `yoda/scripts/tests`; `git diff --check` sem erros.

- **Issue**: `yoda-0065`

- **Path**: `yoda/project/issues/yoda-0065-garantir-independencia-entre-specs-e-produto-yoda.md`

## Flow log
- 2026-08-31T15:11:42-03:00 issue_add created title=Garantir independencia entre specs e produto YODA; priority=5
- 2026-08-31T15:15:39-03:00 Intake concluido: independencia bidirecional definida para specs autocontidas e produto empacotado autocontido
- 2026-08-31T15:19:39-03:00 transition to-do->doing/study
- 2026-08-31T15:29:58-03:00 transition doing/study->doing/document | Study aprovado: spec dedicada 28, lint em project/tests e redacao do requisito de testes contratuais ajustada
- 2026-08-31T15:33:42-03:00 transition doing/document->doing/implement | Document aprovado: spec 28, reescrita autocontida em 00/05/23, suite project/tests e smoke isolado do pacote
- 2026-08-31T15:44:23-03:00 transition doing/implement->doing/evaluate | Implement concluido pelo Claude; Evaluate iniciada para revisar independencia das specs e do pacote
- 2026-08-31T16:11:40-03:00 transition doing/evaluate->done | Evaluate aprovado: specs autocontidas, lint de fronteira e smoke isolado do pacote validados
