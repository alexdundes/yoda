---
schema_version: '2.01'
status: done
title: Tornar o onboarding inicial autocontido e explicitar o developer slug
description: Explicar o developer slug antes do primeiro uso no README, com formato
  aceito, exemplos validos e invalidos, comando concreto e copiavel, convencao de
  placeholders e o proximo passo apos o init. Ajustar a ajuda compartilhada de --dev
  para metavar <developer-slug> com formato e exemplo, alcancando todos os comandos,
  e tornar compreensiveis as descricoes de --root e --reconcile-layout no init.py,
  removendo por completo a flag --force obsoleta e sem efeito. Unificar a terminologia
  entre README, manual embarcado, README de scripts, runbooks, helps, specs e site.
priority: 5
extern_issue_file: ../extern_issues/github-011.json
created_at: '2026-08-31T18:13:47-03:00'
updated_at: '2026-08-31T19:25:42-03:00'
---

# yoda-0069 - Tornar o onboarding inicial autocontido e explicitar o developer slug

## Summary

Fazer com que o primeiro contato com o YODA funcione como tutorial minimo. Hoje
o `init.py` e a porta de entrada, mas o usuario precisa consultar codigo ou
documentacao secundaria para entender o primeiro argumento obrigatorio.

## Context

A issue externa GitHub #11 registrou um teste real de documentacao: um usuario
novo nao conseguiu entender como iniciar o YODA nem o significado de `--dev`.

A auditoria dos textos vigentes localiza o problema em duas frentes.

Documentacao:

- `README.md` apresenta `python yoda/scripts/init.py --dev <slug> --root .` sem
  nenhuma explicacao anterior sobre o que e um developer slug, que formato ele
  aceita, ou que `<...>` indica um placeholder a substituir.
- A secao `First run / Init` descreve o que o init NAO faz, mas nao informa o
  resultado esperado nem o proximo passo do fluxo.
- O placeholder `<slug>` e ambiguo: pode ser confundido com o slug de uma issue,
  que aparece no padrao `<dev>-<NNNN>-<slug>.md`.

Ajuda operacional:

- `--dev` e declarado uma unica vez em `add_global_flags`, em
  `yoda/scripts/lib/cli.py`, com `help="Developer slug"` e sem `metavar`. O
  argparse renderiza `--dev DEV`, o que sugere que `DEV` e literal ou que o
  valor deve ser maiusculo. O formato real e `^[a-z][a-z0-9-]*$`.
- No `init.py`, `--root` descreve o padrao como `cwd`, jargao para quem chega
  agora; `--reconcile-layout` nao indica que serve a migracao e nao ao primeiro
  uso. A flag `--force` diz "Overwrite existing files", mas o Study confirmou
  que ela nunca e lida pelo programa e nao possui efeito algum.

Como `--dev` e compartilhado, corrigir `metavar` e texto no ponto unico alcanca
os doze comandos de uma vez e evita divergencia entre eles. As demais flags sao
exclusivas do `init.py` e ficam no proprio script.

## Objective

Permitir que alguem sem conhecimento previo entenda o developer slug, escolha um
valor valido, inicialize o YODA, entenda o resultado e saiba qual e o proximo
passo, sem sair da documentacao de entrada.

## Scope

- Explicar o developer slug no `README.md` antes do primeiro uso, com formato,
  exemplos validos e invalidos e um comando concreto e copiavel.
- Documentar a convencao de placeholders `<...>` e que os sinais nao devem ser
  digitados.
- Descrever no `README.md` o fluxo de primeira execucao ate o proximo passo
  recomendado.
- Ajustar `--dev` em `yoda/scripts/lib/cli.py` para `metavar` explicito e texto
  com formato e exemplo, alcancando todos os comandos.
- Melhorar as descricoes de `--root` e `--reconcile-layout` no `init.py`.
- Remover completamente a flag obsoleta `--force` do parser, da ajuda, dos
  exemplos e dos testes; nao manter documentacao ou compatibilidade para um
  comportamento que nunca existiu no `init.py` atual.
- Unificar a terminologia de developer slug entre `README.md`, `yoda/yoda.md`,
  `yoda/scripts/README.md`, runbooks, mensagens operacionais, specs, as ajudas
  dos comandos e o site em `docs/`.
- Adicionar testes de contrato para o texto essencial do help.

## Out of scope

- Alterar o formato aceito do developer slug ou sua validacao.
- Alterar o comportamento de inicializacao, `--root` ou `--reconcile-layout`.
- Renomear a flag `--dev` ou introduzir alias.
- Redesenhar o site em `docs/` alem do alinhamento terminologico.
- Alterar o fluxo de instalacao ou empacotamento.

## Requirements

- O `README.md` MUST explicar o developer slug antes do primeiro comando que o
  utiliza.
- A explicacao MUST descrever o formato aceito em linguagem simples: letras
  ASCII minusculas, digitos e hifens, comecando por letra.
- O `README.md` MUST apresentar exemplos validos e invalidos.
- O primeiro comando de `init` MUST usar um valor concreto e copiavel, deixando
  claro que e um exemplo a substituir.
- A documentacao MUST declarar que `<...>` marca placeholder e que os sinais nao
  fazem parte do comando.
- A documentacao MUST informar o que o `init` produz e qual e o proximo passo.
- O help MUST apresentar `--dev` com `metavar` que nao sugira valor literal nem
  caixa alta. O formato canonico MUST ser `--dev <developer-slug>` e o help MUST
  informar formato e exemplo.
- A mudanca de `--dev` MUST ser feita no ponto compartilhado, alcancando todos
  os comandos sem divergencia entre eles.
- A descricao de `--root` MUST usar `current directory`, sem o jargao `cwd`.
- A descricao de `--reconcile-layout` MUST identifica-la como operacao avancada
  de migracao/reconciliacao, nao necessaria no primeiro uso, e informar que ela
  toca arquivos Markdown sob o project root.
- `--force` MUST ser removida integralmente do `init.py`, da ajuda e dos exemplos.
- A terminologia MUST ser consistente entre README, manual embarcado, README de
  scripts, runbooks, mensagens operacionais, specs, ajudas e site, usando
  `<developer-slug>` para `--dev`. O placeholder `<slug>` permanece apenas onde
  significa o slug de issue em `<dev>-<NNNN>-<slug>.md`.
- Testes de contrato MUST falhar se o texto essencial do help for removido.
- Textos ja escritos em ingles MUST permanecer em ingles.
- Nenhum texto em `project/specs/` pode citar a issue externa por link, numero
  ou ID; o rationale entra autocontido.

## Acceptance criteria

- [x] O `README.md` explica o developer slug antes de utiliza-lo.
- [x] O formato aceito esta documentado em linguagem simples.
- [x] Existem exemplos de valores validos e invalidos.
- [x] O primeiro comando usa um valor concreto e copiavel.
- [x] A documentacao explica que placeholders entre `<...>` devem ser
      substituidos e que os sinais nao sao digitados.
- [x] O help apresenta `--dev <developer-slug>` sem sugerir que o valor seja
      `DEV` ou maiusculo.
- [x] O help de `--dev` informa formato e exemplo.
- [x] `--root` e `--reconcile-layout` possuem descricoes compreensiveis e
      `--reconcile-layout` e identificado como operacao avancada que toca
      Markdown sob o project root.
- [x] `--force` nao existe mais no parser, na ajuda ou nos exemplos.
- [x] A documentacao informa o que acontece apos o `init` e qual e o proximo
      passo.
- [x] README, manual embarcado, README de scripts, runbooks, mensagens, specs,
      helps e site usam terminologia consistente para developer slug.
- [x] A mudanca de `--dev` alcanca os doze comandos, sem texto divergente.
- [x] Ha teste de contrato CLI validando o texto essencial do help.
- [x] `yoda/scripts/tests` e `project/tests` permanecem passando.

## Entry points

- `README.md`
- `yoda/scripts/lib/cli.py`
- `yoda/scripts/init.py`
- `yoda/scripts/lib/dev.py`
- `yoda/scripts/yoda_intake.py`
- `yoda/scripts/yoda_flow_next.py`
- `yoda/scripts/yoda_prep_flow.py`
- `yoda/yoda.md`
- `yoda/scripts/README.md`
- `docs/index.html`
- `docs/install/yoda-install.sh`
- `project/specs/02-yoda-flow-process.md`
- `project/specs/06-agent-playbook.md`
- `project/specs/07-agent-entry-files.md`
- `project/specs/11-yoda-intake.md`
- `project/specs/13-yoda-scripts-v1.md`
- `project/specs/15-scripts-python-structure.md`
- `project/specs/16-todo-list-script.md`
- `project/specs/18-issue-add-script.md`
- `project/specs/21-yoda-flow-next-script.md`
- `project/specs/25-yoda-intake-script.md`
- `project/specs/26-get-extern-issue-script.md`
- `project/specs/27-yoda-prep-flow-script.md`
- `yoda/scripts/tests/test_cli_contracts.py`
- `yoda/scripts/tests/test_init.py`
- `yoda/project/extern_issues/github-011.json`

## Implementation notes

O ponto de maior alavanca e `add_global_flags` em `yoda/scripts/lib/cli.py`:
`--dev` e declarado uma unica vez e herdado por onze scripts em `yoda/scripts/`
e pelo `package.py`, totalizando doze comandos. Definir
`metavar="<developer-slug>"` e o texto ali corrige todos simultaneamente. O
Study confirmou que nenhum teste depende de `--dev DEV` ou de `Developer slug`.

Runbooks e mensagens que montam seus proprios exemplos nao recebem o metavar do
argparse e devem ser alinhados separadamente. A limpeza substitui `<slug>` apenas
quando ele representa developer slug; o slug de titulo no padrao de filename
continua sendo `<slug>`.

O site em `docs/` e a fonte publicada referenciada pelo README. Alinhar
terminologia sem redesenhar conteudo visual.

Ao escolher o placeholder canonico, preferir uma forma que nao colida com o slug
de issue. O termo `developer slug` ja e usado no manual e nas specs.

## Tests

- Adicionar teste de contrato sobre o help de `--dev`, cobrindo `metavar`,
  formato e exemplo nos doze comandos.
- Adicionar ou ajustar teste do help de `init.py` para `--root`, ausencia de
  `--force` e descricao avancada de `--reconcile-layout`.
- Executar `python3 -m pytest yoda/scripts/tests`.
- Executar `python3 -m pytest project/tests`. As duas suites nao podem ser
  executadas na mesma invocacao.

## Risks and edge cases

- Alterar o `metavar` e deixar runbooks hardcoded com `<slug>` ou `<DEV>`.
- Corrigir apenas o `init.py` e deixar os demais comandos com texto divergente.
- Melhorar o README e esquecer o site em `docs/`, que e a porta de entrada
  publica.
- Trocar um placeholder ambiguo por outro igualmente ambiguo.
- Expandir o texto do help a ponto de poluir a saida dos comandos.
- Remover `--force` de forma incompleta e deixa-lo em exemplos ou documentacao.

## Study findings

- `add_global_flags()` declara `--dev` para onze scripts sob `yoda/scripts/` e
  para `package.py`; a correcao central alcanca os doze comandos.
- Nenhum teste vigente depende da string `--dev DEV`, do texto curto
  `Developer slug` ou da linha de usage atual.
- O placeholder `<slug>` tambem possui um significado legitimo e diferente: o
  slug do titulo no filename `<dev>-<NNNN>-<slug>.md`. Substituicao global cega
  corromperia esse contrato.
- `yoda_intake.py`, `lib/dev.py`, `yoda_flow_next.py` e `yoda_prep_flow.py`
  constroem exemplos ou mensagens proprias e nao herdarao automaticamente o
  novo metavar.
- O site publicado instala o YODA, mas nao explica developer slug, inicializacao
  ou Intake. O onboarding publico termina antes da primeira operacao util.
- `init.py` cria os diretorios YODA ausentes, migra dados legados quando
  presentes, reconcilia front matter compativel e relata itens criados,
  escritos ou ignorados.
- `--reconcile-layout` chama `_touch_markdown_files(root)`, que toca todos os
  arquivos Markdown sob o project root, alem de reconciliar metadados legados.
- `--force` e uma flag morta: o parser a aceita, mas `args.force` nunca e lido e
  nao existe contrato normativo para seu comportamento.

## Document contract

O Implement deve seguir este contrato document-first sem alterar a validacao do
developer slug nem o comportamento efetivo de inicializacao e reconciliacao.

Decisoes aprovadas no encerramento do Study:

1. `<developer-slug>` e o placeholder canonico e tambem o metavar de `--dev`.
2. `mynick` e o exemplo concreto de onboarding e deve ser apresentado como
   valor substituivel e reutilizavel.
3. A limpeza terminologica cobre specs, runbooks e mensagens, preservando
   `<slug>` quando ele significa slug de issue.
4. Ampliacao de escopo aprovada: `--force`, por ser obsoleto e sem efeito, e
   removido integralmente do parser, ajuda, exemplos e testes, sem deprecacao ou
   documentacao residual.
5. `--reconcile-layout` e documentado como operacao avancada de migracao que
   toca Markdown sob o project root.
6. O comportamento e o fluxo do instalador publicado permanecem inalterados;
   apenas seu help de `--dev` recebe a terminologia canonica. O site acrescenta
   os passos separados de developer slug, init e Intake.
7. A spec 13 recebe o contrato central e todas as ocorrencias normativas de
   developer placeholder sao alinhadas.
8. Um teste percorre os doze comandos para provar metavar e ajuda identicos;
   testes do init cobrem suas flags exclusivas.

### 1. README e site

- `README.md`: antes do primeiro uso de placeholder, explicar que `<...>` marca
  texto a substituir e que os sinais nao sao digitados. Antes do primeiro
  `--dev`, definir developer slug, formato, exemplos validos (`mynick`,
  `fernando`, `time-backend`) e invalidos (`MeuNick`, `123fernando`,
  `fernando_silva`).
- O primeiro init deve ser copiavel:
  `python3 yoda/scripts/init.py --dev mynick --root .`; explicar o valor, o
  diretorio atual, o resultado e a reutilizacao do slug.
- Completar o primeiro fluxo com conferencia da saida e
  `python3 yoda/scripts/yoda_intake.py --dev mynick`.
- `docs/index.html`: manter o instalador atual e acrescentar uma secao compacta
  de primeira execucao com a mesma definicao, exemplo, init e Intake, sem
  redesenho visual.

### 2. Produto distribuido

- `lib/cli.py`: configurar `--dev` com `metavar="<developer-slug>"` e help em
  ingles contendo o formato simples e `example: mynick`.
- `init.py`: remover `--force`; descrever `--root` como project root com default
  `current directory`; descrever `--reconcile-layout` como migracao avancada,
  desnecessaria no primeiro uso e capaz de tocar Markdown sob o root.
- `yoda/yoda.md` e `yoda/scripts/README.md`: definir/reutilizar developer slug,
  convencao de placeholder e comandos com `<developer-slug>` ou `mynick`, sem
  usar `<slug>` para `--dev`.
- Alinhar exemplos hardcoded e mensagens em `lib/dev.py`, `yoda_intake.py`,
  `yoda_flow_next.py` e `yoda_prep_flow.py`.

### 3. Specs normativas

- `project/specs/13-yoda-scripts-v1.md`: centralizar formato, significado,
  metavar, exemplo e obrigacao da ajuda compartilhada.
- Nas demais specs listadas em Entry points, substituir `--dev <slug>` por
  `--dev <developer-slug>` e textos equivalentes quando representam o
  developer. Preservar padrões de issue como `<dev>-<NNNN>-<slug>.md`.
- Nenhuma spec pode citar a fonte externa ou uma issue concreta por link,
  numero ou ID.

### 4. Verificacao

- Testar os helps de onze scripts e `package.py`, exigindo
  `--dev <developer-slug>`, formato e `example: mynick`.
- Testar no help de `init.py` as descricoes de `--root` e
  `--reconcile-layout`, alem da ausencia total de `--force`.
- Confirmar por busca que nenhum exemplo `--dev <slug>` ou `--dev <DEV>` resta
  nas superficies de onboarding e nas specs; ocorrencias de `<slug>` em padrões
  de filename continuam permitidas.
- Rodar `yoda/scripts/tests` e `project/tests` em invocacoes separadas e
  conferir visualmente README/site e helps.

## Result log

docs: tornar o onboarding inicial autocontido e explicitar o developer slug

Fez do primeiro contato com o YODA um tutorial minimo. O `README.md` passa a
explicar o developer slug antes de qualquer comando que o use, com o formato em
linguagem simples, exemplos validos e invalidos acompanhados do motivo, um
comando concreto e copiavel, a convencao de placeholders entre `<...>` e o fluxo
de primeira execucao ate o proximo passo, que e entrar no YODA Intake. O site em
`docs/` recebeu a mesma orientacao.

Corrigiu a ajuda no ponto compartilhado: `--dev` e declarado uma unica vez em
`lib/cli.py`, entao definir `metavar` e texto ali alcancou os doze comandos de
uma vez, sem divergencia entre eles. O antigo `--dev DEV`, que sugeria valor
literal ou caixa alta, deu lugar a `--dev <developer-slug>` com formato e
exemplo. As mensagens de erro passaram a usar a mesma terminologia, distinguindo
o developer slug do slug de issue presente em `<dev>-<NNNN>-<slug>.md`.

No `init.py`, `--root` deixou de descrever o padrao como `cwd` e
`--reconcile-layout` passou a se identificar como operacao avancada de migracao,
nao necessaria no primeiro uso.

Removeu a flag `--force`, ampliacao de escopo aprovada no Study depois de
confirmar que era codigo morto: o parser a aceitava, mas o valor nunca era lido
e nenhum caminho de execucao dependia dela. Nenhum chamador a utilizava;
`update.py` e o instalador invocam o init apenas com `--dev` e `--root`. Como a
flag nunca teve efeito, sua remocao nao altera comportamento observavel.

Evaluate: `101 passed` em `yoda/scripts/tests`, `17 passed` em `project/tests`,
`--dev <developer-slug>` confirmado nos doze comandos e nenhuma ocorrencia
remanescente de `--force` fora do historico de issues.

- **GitHub Issue** :   #11

- **Issue**: `yoda-0069`

- **Path**: `yoda/project/issues/yoda-0069-tornar-o-onboarding-inicial-autocontido-e-explicitar-o-developer-slug.md`

## Flow log

- 2026-08-31T18:13:47-03:00 issue_add created title=Tornar o onboarding inicial autocontido e explicitar o developer slug; priority=5
- 2026-08-31T18:14:32-03:00 Intake concluido a partir da GitHub #11: onboarding autocontido e --dev corrigido no ponto compartilhado
- 2026-08-31T18:39:29-03:00 transition to-do->doing/study | YODA Flow continuado apos conclusao da yoda-0068
- 2026-08-31T18:47:55-03:00 transition doing/study->doing/document | Study aprovado: onboarding autocontido com developer-slug canonico e remocao completa de --force
- 2026-08-31T18:55:58-03:00 transition doing/document->doing/implement | Document aprovado: implementar onboarding autocontido e remover --force obsoleto
- 2026-08-31T19:21:12-03:00 transition doing/implement->doing/evaluate | Evaluate iniciado: revisao do onboarding, do metavar compartilhado e da remocao do --force
- 2026-08-31T19:25:42-03:00 transition doing/evaluate->done | Evaluate aprovado: onboarding autocontido, --dev explicito nos doze comandos e --force removido
