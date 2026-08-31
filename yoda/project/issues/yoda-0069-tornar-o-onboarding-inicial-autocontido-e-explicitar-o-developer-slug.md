---
schema_version: '2.01'
status: to-do
title: Tornar o onboarding inicial autocontido e explicitar o developer slug
description: Explicar o developer slug antes do primeiro uso no README, com formato
  aceito, exemplos validos e invalidos, comando concreto e copiavel, convencao de
  placeholders e o proximo passo apos o init. Ajustar a ajuda compartilhada de --dev
  para metavar SLUG com formato e exemplo, alcancando todos os comandos, e tornar
  compreensiveis as descricoes de --root, --force e --reconcile-layout no init.py.
  Unificar a terminologia entre README, manual embarcado, README de scripts, helps
  e site.
priority: 5
extern_issue_file: ../extern_issues/github-011.json
created_at: '2026-08-31T18:13:47-03:00'
updated_at: '2026-08-31T18:13:47-03:00'
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
  agora; `--force` diz apenas "Overwrite existing files", sem alertar que
  sobrescreve arquivos gerenciados pelo YODA; `--reconcile-layout` nao indica
  que serve a migracao e nao ao primeiro uso.

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
- Melhorar as descricoes de `--root`, `--force` e `--reconcile-layout` no
  `init.py`.
- Unificar a terminologia de developer slug entre `README.md`, `yoda/yoda.md`,
  `yoda/scripts/README.md`, as ajudas dos comandos e o site em `docs/`.
- Adicionar testes de contrato para o texto essencial do help.

## Out of scope

- Alterar o formato aceito do developer slug ou sua validacao.
- Alterar o comportamento de `init.py`, `--root`, `--force` ou
  `--reconcile-layout`.
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
  caixa alta, e MUST informar formato e exemplo.
- A mudanca de `--dev` MUST ser feita no ponto compartilhado, alcancando todos
  os comandos sem divergencia entre eles.
- As descricoes de `--root`, `--force` e `--reconcile-layout` MUST ser
  compreensiveis para quem usa o YODA pela primeira vez; `--force` MUST alertar
  que sobrescreve arquivos gerenciados pelo YODA.
- A terminologia MUST ser consistente entre README, manual embarcado, README de
  scripts, ajudas e site, evitando o placeholder generico `<slug>`, que colide
  com o slug de issue em `<dev>-<NNNN>-<slug>.md`.
- Testes de contrato MUST falhar se o texto essencial do help for removido.
- Textos ja escritos em ingles MUST permanecer em ingles.
- Nenhum texto em `project/specs/` pode citar a issue externa por link, numero
  ou ID; o rationale entra autocontido.

## Acceptance criteria

- [ ] O `README.md` explica o developer slug antes de utiliza-lo.
- [ ] O formato aceito esta documentado em linguagem simples.
- [ ] Existem exemplos de valores validos e invalidos.
- [ ] O primeiro comando usa um valor concreto e copiavel.
- [ ] A documentacao explica que placeholders entre `<...>` devem ser
      substituidos e que os sinais nao sao digitados.
- [ ] O help apresenta `--dev` sem sugerir que o valor seja `DEV` ou maiusculo.
- [ ] O help de `--dev` informa formato e exemplo.
- [ ] `--root`, `--force` e `--reconcile-layout` possuem descricoes
      compreensiveis, e `--force` alerta sobre sobrescrita.
- [ ] A documentacao informa o que acontece apos o `init` e qual e o proximo
      passo.
- [ ] README, manual embarcado, README de scripts, helps e site usam
      terminologia consistente para developer slug.
- [ ] A mudanca de `--dev` alcanca os doze comandos, sem texto divergente.
- [ ] Ha teste de contrato CLI validando o texto essencial do help.
- [ ] `yoda/scripts/tests` e `project/tests` permanecem passando.

## Entry points

- `README.md`
- `yoda/scripts/lib/cli.py`
- `yoda/scripts/init.py`
- `yoda/yoda.md`
- `yoda/scripts/README.md`
- `docs/index.html`
- `yoda/scripts/tests/test_cli_contracts.py`
- `yoda/scripts/tests/test_init.py`
- `yoda/project/extern_issues/github-011.json`

## Implementation notes

O ponto de maior alavanca e `add_global_flags` em `yoda/scripts/lib/cli.py`:
`--dev` e declarado uma unica vez e herdado pelos doze comandos. Definir
`metavar` e texto ali corrige todos simultaneamente, seguindo o mesmo padrao ja
usado para a regra de saida dos comandos.

Verificar no Study se algum teste vigente depende da string `--dev DEV`, do
texto `Developer slug`, ou do formato atual de usage, antes de alterar o
`metavar`.

O site em `docs/` e a fonte publicada referenciada pelo README. Alinhar
terminologia sem redesenhar conteudo visual.

Ao escolher o placeholder canonico, preferir uma forma que nao colida com o slug
de issue. O termo `developer slug` ja e usado no manual e nas specs.

## Tests

- Adicionar teste de contrato sobre o help de `--dev`, cobrindo `metavar`,
  formato e exemplo.
- Adicionar ou ajustar teste do help de `init.py` para `--root`, `--force` e
  `--reconcile-layout`.
- Executar `python3 -m pytest yoda/scripts/tests`.
- Executar `python3 -m pytest project/tests`. As duas suites nao podem ser
  executadas na mesma invocacao.

## Risks and edge cases

- Alterar o `metavar` e quebrar teste que compare a linha de usage.
- Corrigir apenas o `init.py` e deixar os demais comandos com texto divergente.
- Melhorar o README e esquecer o site em `docs/`, que e a porta de entrada
  publica.
- Trocar um placeholder ambiguo por outro igualmente ambiguo.
- Expandir o texto do help a ponto de poluir a saida dos comandos.

## Result log

## Flow log

- 2026-08-31T18:13:47-03:00 issue_add created title=Tornar o onboarding inicial autocontido e explicitar o developer slug; priority=5
- 2026-08-31T18:14:32-03:00 Intake concluido a partir da GitHub #11: onboarding autocontido e --dev corrigido no ponto compartilhado
