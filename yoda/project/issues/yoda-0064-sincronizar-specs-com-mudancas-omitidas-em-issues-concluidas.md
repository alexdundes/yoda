---
schema_version: '2.01'
status: done
title: Sincronizar specs com mudancas omitidas em issues concluidas
description: 'Consolidar e corrigir divergencias entre project/specs e o estado atual,
  rastreadas ate as issues que introduziram ou deveriam ter documentado cada mudanca:
  baseline 0.4.0, YODA Prep Flow e flow_prepared_until ([yoda-0062](./yoda-0062-adicionar-fluxo-antecipado-de-study-e-document.md));
  contrato sem id no front matter ([yoda-0060](./yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md),
  [yoda-0061](./yoda-0061-corrigir-scripts-para-remover-id-do-front-matter-e-aplicar-saneamento-no-init.md));
  ordenacao markdown-first do todo_list ([yoda-0011](./yoda-0011-specify-todo-list-py.md),
  [yoda-0012](./yoda-0012-implement-todo-list-py.md), [yoda-0060](./yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md));
  init, update e instalacao ([yoda-0026](./yoda-0026-implement-yoda-install-sh-one-liner-installer.md),
  [yoda-0027](./yoda-0027-implement-update-command-for-embedded-yoda.md), [yoda-0030](./yoda-0030-allow-one-liner-install-without-explicit-version.md),
  [yoda-0047](./yoda-0047-spec-0-3-0-e-estrategia-de-migracao-breaking.md), [yoda-0063](./yoda-0063-tornar-init-py-n-o-intrusivo-para-arquivos-de-agente.md));
  inventario e deprecacoes de scripts ([yoda-0053](./yoda-0053-atualizar-playbook-yoda-md-e-deprecacoes-operacionais.md),
  [yoda-0062](./yoda-0062-adicionar-fluxo-antecipado-de-study-e-document.md)); package
  e changelog ([yoda-0016](./yoda-0016-specs-empacotamento-e-distribui-o-do-yoda-framework.md),
  [yoda-0018](./yoda-0018-comando-de-empacote-do-yoda-package.md), [yoda-0035](./yoda-0035-remover-conceito-de-lightweight-do-yoda.md));
  outputs de log_add e todo_update ([yoda-0002](./yoda-0002-document-log-add-slug-resolution.md),
  [yoda-0003](./yoda-0003-define-json-output-minimums.md), [yoda-0052](./yoda-0052-migracao-de-legado-todo-e-logs-yaml-para-issue-markdown.md));
  validacao do indice markdown ([yoda-0049](./yoda-0049-camada-de-leitura-deterministica-baseada-apenas-em-issues-markdown.md));
  posicionamento Markdown-first ([yoda-0047](./yoda-0047-spec-0-3-0-e-estrategia-de-migracao-breaking.md),
  [yoda-0053](./yoda-0053-atualizar-playbook-yoda-md-e-deprecacoes-operacionais.md),
  [yoda-0060](./yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md));
  README com link para o site oficial em https://alexdundes.github.io/yoda/ e indicacao
  de que sua fonte esta em docs/ ([yoda-0028](./yoda-0028-set-up-github-pages-docs-hosting-for-installer-and-metadata.md));
  e versionamento do schema ([yoda-0038](./yoda-0038-definir-politica-de-versionamento-do-layout-yaml-do-yoda.md),
  [yoda-0062](./yoda-0062-adicionar-fluxo-antecipado-de-study-e-document.md)).'
priority: 5
created_at: '2026-08-31T10:13:04-03:00'
updated_at: '2026-08-31T15:06:40-03:00'
---

# yoda-0064 - Sincronizar specs com mudancas omitidas em issues concluidas

## Summary

Uma auditoria cruzada entre `project/specs/`, scripts, testes, manual e historico
das issues encontrou contratos congelados em 0.3.0 ou com trechos legados depois
de mudancas concluidas. Esta issue consolida a correcao das specs e preserva a
rastreabilidade para as issues que introduziram a mudanca ou declararam uma
convergencia documental incompleta.

## Context

A auditoria foi executada em 2026-08-31 contra a release 0.4.0. Os runbooks de
`--help`, a implementacao e a suite vigente (`68 passed`) foram usados como
evidencia, sem assumir que toda divergencia deva ser resolvida rebaixando uma
regra normativa da spec.

Pontos encontrados e issues relacionadas:

- **Baseline 0.4.0, Prep Flow e `flow_prepared_until`:** ausentes das specs de
  processo, schema e scripts. Mudanca de
  [yoda-0062](./yoda-0062-adicionar-fluxo-antecipado-de-study-e-document.md).
- **Ordem canonica do front matter:** faltam `flow_prepared_until` e a posicao de
  `pending_reason`. Relacionado a
  [yoda-0043](./yoda-0043-omitir-campos-opcionais-vazios-nos-arquivos.md),
  [yoda-0044](./yoda-0044-padronizar-front-matter-sem-defaults-no-template.md),
  [yoda-0060](./yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md)
  e [yoda-0062](./yoda-0062-adicionar-fluxo-antecipado-de-study-e-document.md).
- **`id` no front matter:** `00-conventions` proibe, mas a spec de `issue_add.py`
  ainda manda incluir. Contrato de
  [yoda-0057](./yoda-0057-remover-id-do-front-matter-e-derivar-id-pelo-nome-do-arquivo.md),
  revisado em [yoda-0060](./yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md)
  e implementado em
  [yoda-0061](./yoda-0061-corrigir-scripts-para-remover-id-do-front-matter-e-aplicar-saneamento-no-init.md).
- **Papel de `todo_next.py`:** specs sugerem remocao/deprecacao, mas manual,
  script e testes o mantem como helper fora do Flow principal. Historico em
  [yoda-0007](./yoda-0007-specify-todo-next-command.md),
  [yoda-0008](./yoda-0008-implement-todo-next-with-single-issue-rule.md),
  [yoda-0047](./yoda-0047-spec-0-3-0-e-estrategia-de-migracao-breaking.md) e
  [yoda-0053](./yoda-0053-atualizar-playbook-yoda-md-e-deprecacoes-operacionais.md).
- **Ordenacao de `todo_list.py`:** ainda usa ordem YAML como desempate, enquanto
  o caminho atual usa ID/ordem dos arquivos. Contrato original de
  [yoda-0011](./yoda-0011-specify-todo-list-py.md) e
  [yoda-0012](./yoda-0012-implement-todo-list-py.md), migracao em
  [yoda-0049](./yoda-0049-camada-de-leitura-deterministica-baseada-apenas-em-issues-markdown.md)
  e convergencia incompleta em
  [yoda-0060](./yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md).
- **Flags de `init.py`/`update.py`:** specs atribuem `--check`/`--apply` ao init;
  hoje pertencem ao update. Relacionado a
  [yoda-0019](./yoda-0019-comando-de-init-p-s-embutido.md),
  [yoda-0027](./yoda-0027-implement-update-command-for-embedded-yoda.md),
  [yoda-0047](./yoda-0047-spec-0-3-0-e-estrategia-de-migracao-breaking.md),
  [yoda-0052](./yoda-0052-migracao-de-legado-todo-e-logs-yaml-para-issue-markdown.md)
  e [yoda-0063](./yoda-0063-tornar-init-py-n-o-intrusivo-para-arquivos-de-agente.md).
- **Inventario Python:** omite comandos/modulos atuais e mantem TODO/log YAML como
  caminhos principais. Relacionado a
  [yoda-0039](./yoda-0039-integrar-backlog-externo-via-glab-e-prever-github.md),
  [yoda-0050](./yoda-0050-criar-yoda-flow-next-py-com-selecao-e-runbook-por-fase.md),
  [yoda-0052](./yoda-0052-migracao-de-legado-todo-e-logs-yaml-para-issue-markdown.md),
  [yoda-0053](./yoda-0053-atualizar-playbook-yoda-md-e-deprecacoes-operacionais.md)
  e [yoda-0062](./yoda-0062-adicionar-fluxo-antecipado-de-study-e-document.md).
- **Timezone de `issue_add.py`:** spec ainda le o TODO root; o script detecta o
  timezone local. Relacionado a
  [yoda-0052](./yoda-0052-migracao-de-legado-todo-e-logs-yaml-para-issue-markdown.md)
  e a revisao de spec 18 declarada em
  [yoda-0060](./yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md).
- **CLI de package:** spec anuncia `--version`, `--output`, `--archive-format` e
  `--changelog`; o comando atual exige `--next-version` e usa `--dir`. Contrato de
  [yoda-0016](./yoda-0016-specs-empacotamento-e-distribui-o-do-yoda-framework.md)
  e [yoda-0018](./yoda-0018-comando-de-empacote-do-yoda-package.md); reescrita
  relevante ocorreu junto de
  [yoda-0035](./yoda-0035-remover-conceito-de-lightweight-do-yoda.md).
- **Manifesto/changelog/versionamento:** spec diz que `package_sha256` vai ao
  changelog e que init valida version/build; hoje checksum fica no
  manifesto/`latest.json` e a validacao pertence ao update. Relacionado a
  [yoda-0016](./yoda-0016-specs-empacotamento-e-distribui-o-do-yoda-framework.md),
  [yoda-0018](./yoda-0018-comando-de-empacote-do-yoda-package.md) e
  [yoda-0027](./yoda-0027-implement-update-command-for-embedded-yoda.md).
- **Instalacao/upgrade:** spec nao cobre integralmente `latest.json`, latest/pinned
  e one-liner, e chama update de legado. Relacionado a
  [yoda-0023](./yoda-0023-document-one-liner-install-flow.md),
  [yoda-0026](./yoda-0026-implement-yoda-install-sh-one-liner-installer.md),
  [yoda-0027](./yoda-0027-implement-update-command-for-embedded-yoda.md),
  [yoda-0030](./yoda-0030-allow-one-liner-install-without-explicit-version.md) e
  [yoda-0063](./yoda-0063-tornar-init-py-n-o-intrusivo-para-arquivos-de-agente.md).
- **Outputs:** `log_add.py` retorna `issue_path`, nao `log_path`, e
  `todo_update.py` nao retorna `timestamp`. Contratos de
  [yoda-0002](./yoda-0002-document-log-add-slug-resolution.md),
  [yoda-0003](./yoda-0003-define-json-output-minimums.md) e migracao de
  [yoda-0052](./yoda-0052-migracao-de-legado-todo-e-logs-yaml-para-issue-markdown.md).
- **Markdown-first:** overview ainda chama YAML de centro de gravidade. Mudanca de
  [yoda-0047](./yoda-0047-spec-0-3-0-e-estrategia-de-migracao-breaking.md),
  [yoda-0049](./yoda-0049-camada-de-leitura-deterministica-baseada-apenas-em-issues-markdown.md),
  [yoda-0052](./yoda-0052-migracao-de-legado-todo-e-logs-yaml-para-issue-markdown.md),
  [yoda-0053](./yoda-0053-atualizar-playbook-yoda-md-e-deprecacoes-operacionais.md)
  e [yoda-0060](./yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md).
- **Schema:** `flow_prepared_until` foi classificado como `subtle`, mas o schema
  permaneceu `2.00`. Reconciliar
  [yoda-0038](./yoda-0038-definir-politica-de-versionamento-do-layout-yaml-do-yoda.md)
  com [yoda-0062](./yoda-0062-adicionar-fluxo-antecipado-de-study-e-document.md).
- **Validacao normativa:** specs exigem timestamp, fase, `pending_reason` e IDs de
  dependencia validos, mas o indice atual e mais permissivo e considera dependencia
  ausente resolvida. Decisao de
  [yoda-0049](./yoda-0049-camada-de-leitura-deterministica-baseada-apenas-em-issues-markdown.md)
  nao reconciliada por
  [yoda-0060](./yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md).
- **Out-of-scope de distribuicao:** ainda trata ferramentas de distribuicao como
  futuras, apesar de package/installer/update existirem. Relacionado a
  [yoda-0016](./yoda-0016-specs-empacotamento-e-distribui-o-do-yoda-framework.md),
  [yoda-0018](./yoda-0018-comando-de-empacote-do-yoda-package.md),
  [yoda-0026](./yoda-0026-implement-yoda-install-sh-one-liner-installer.md) e
  [yoda-0027](./yoda-0027-implement-update-command-for-embedded-yoda.md).
- **Site oficial no README:** o `README.md` deve incluir um link visivel para
  [https://alexdundes.github.io/yoda/](https://alexdundes.github.io/yoda/) e
  explicar que o site publicado e mantido a partir do conteudo da pasta `docs/`.
  O hosting em GitHub Pages foi introduzido por
  [yoda-0028](./yoda-0028-set-up-github-pages-docs-hosting-for-installer-and-metadata.md).

## Objective

Entregar um conjunto de specs coerente com o estado atual do YODA Framework,
incluindo a release 0.4.0, com rastreabilidade historica e decisao explicita para
cada conflito em que a implementacao atual nao necessariamente deva substituir o
requisito normativo existente.

## Scope

- Revisar todo o conjunto `project/specs/`, nao apenas as specs citadas pela
  ultima issue de convergencia.
- Atualizar baseline, terminologia, schema, ciclos e catalogo de scripts para o
  YODA Prep Flow e o estado 0.4.0.
- Corrigir contratos de `todo_list.py`, `issue_add.py`, `log_add.py`,
  `todo_update.py`, `init.py`, `update.py`, `package.py` e instalador.
- Atualizar estrutura Python, paths canonicos/legados, outputs e responsabilidades.
- Resolver contradicoes internas antes de alinhar texto ao codigo.
- Decidir explicitamente os conflitos de validacao e versionamento de schema e
  alinhar specs, implementacao e testes conforme a decisao aprovada.
- Atualizar `project/specs/README.md` e referencias cruzadas, criando uma spec
  dedicada ao Prep Flow se essa for a estrutura aprovada no Document.
- Atualizar o `README.md` da raiz com o link do site oficial
  `https://alexdundes.github.io/yoda/` e indicar `docs/` como fonte do site.

## Out of scope

- Reescrever o contexto historico dentro de issues concluidas.
- Alterar `bootstrap-legacy/` para parecer compativel com o modelo atual.
- Introduzir funcionalidades sem relacao direta com os contratos divergentes.
- Publicar pacote/release antes da convergencia e validacao.

## Requirements

- Preservar `project/specs/` como fonte de verdade: nao copiar comportamento atual
  para texto normativo sem validar a intencao document-first.
- Classificar cada ponto como `spec stale`, `implementation drift` ou
  `internal spec contradiction`.
- Manter em cada correcao link para ao menos uma issue de origem/convergencia.
- Distinguir claramente canonico, compatibilidade e legado.
- Definir sem ambiguidade `flow_prepared_until`, sua ordem, valores e transicoes.
- Seguir a politica de versionamento de layout para eventual bump/migracao.
- Conferir exemplos de CLI e payload contra `--help`, codigo e testes atuais.
- Nao deixar links relativos quebrados.
- Manter no README um link navegavel para o site oficial e uma descricao correta
  da relacao entre o site publicado e a pasta `docs/`.

## Acceptance criteria

- [x] Specs correntes deixam de se apresentar como baseline operacional 0.3.0.
- [x] Prep Flow, `yoda_prep_flow.py`, `flow_prepared_until` e retomada em Implement
      estao documentados no processo, schema e catalogo.
- [x] Nao ha contradicao sobre `id`, ordem do front matter ou timezone.
- [x] `todo_next.py` e `todo_list.py` refletem seus papeis e ordenacao aprovados,
      sem ordem YAML como desempate canonico.
- [x] Specs de init/update/instalacao e package/changelog refletem flags, outputs,
      checksums, versoes e responsabilidades aprovados.
- [x] Outputs de `log_add.py` e `todo_update.py` possuem campos minimos explicitos.
- [x] Overview descreve issue Markdown como fonte operacional canonica e YAML
      conforme seu papel atual.
- [x] Divergencias de validacao/schema foram decididas e specs, codigo e testes
      ficaram alinhados, sem ocultar o conflito no texto.
- [x] `project/specs/README.md` indexa o conjunto final sem lacunas ambiguas.
- [x] O `README.md` da raiz inclui link navegavel para
      `https://alexdundes.github.io/yoda/` e informa que o site esta contido em
      `docs/`.
- [x] Suite de scripts passa e varredura documental nao encontra os termos/flags
      legados identificados nesta issue fora de contexto historico explicito.

## Entry points

- `project/specs/`
- `project/specs/README.md`
- `README.md`
- `docs/`
- `docs/index.html`
- `yoda/yoda.md`
- `yoda/scripts/README.md`
- `yoda/scripts/*.py`
- `yoda/scripts/lib/`
- `yoda/scripts/tests/`
- `package.py`
- `CHANGELOG.yaml`
- `docs/install/yoda-install.sh`
- `docs/install/latest.json`
- `yoda/project/issues/yoda-0064-sincronizar-specs-com-mudancas-omitidas-em-issues-concluidas.md`

## Implementation notes

Executar em ordem document-first. No Study, validar cada associacao com
`git blame`, commits e corpo das issues. No Document, registrar uma matriz curta
`divergencia -> decisao -> specs afetadas -> issue de origem`. Somente depois
alinhar implementacao/testes quando a decisao normativa exigir.

O backlog estava sem issues abertas neste Intake; por isso foi mantida a
prioridade baseline `5`, sem justificativa comparativa para altera-la.

## Study findings

O Study cruzou o texto das specs com os `--help`, implementacao, testes, corpos
das issues e historico Git. A release operacional e `0.4.0` (`CHANGELOG.yaml`,
`docs/install/latest.json` e tag `v0.4.0`). Os principais marcos que explicam o
drift sao os commits `3d11208` (Markdown/schema 2.00), `573214c` (ordenacao por
ID), `c78589e` (convergencia Markdown-first), `8a2f14b` (YODA Prep Flow) e
`f14ce52` (init nao intrusivo).

Matriz de classificacao e encaminhamento proposto:

| Divergencia | Classificacao | Decisao proposta para Document/Implement |
| --- | --- | --- |
| Baseline operacional ainda descrito como 0.3.0 | `spec stale` | Adotar 0.4.0 como baseline corrente e preservar 0.3.0 apenas onde for contexto historico ou de migracao. |
| YODA Prep Flow e `flow_prepared_until` ausentes | `spec stale` | Criar spec dedicada para `yoda_prep_flow.py`, integrar processo/schema/catalogo e indexar em `project/specs/README.md`. |
| Ordem do front matter sem `flow_prepared_until`/`pending_reason` | `spec stale` | Documentar a ordem efetiva de `issue_metadata.py`, sempre omitindo opcionais vazios e `id` no front matter. |
| Spec de `issue_add.py` ainda manda persistir `id` | `internal spec contradiction` | Manter ID derivado exclusivamente do filename, conforme yoda-0057/yoda-0060/yoda-0061. |
| `todo_next.py` consta como removido, mas segue helper suportado | `internal spec contradiction` | Documenta-lo como helper de inspecao fora do Flow principal; `yoda_flow_next.py` continua entrypoint canonico. |
| `todo_list.py` usa desempate por ordem YAML na spec | `spec stale` | Documentar prioridade + ID e timestamps + ID, conforme codigo/testes introduzidos em `573214c`. |
| Flags de init/update e fluxo de instalacao estao trocados/incompletos | `spec stale` | Atribuir `--check`/`--apply` ao `update.py`; manter `init.py` como reconciliador nao intrusivo; cobrir latest/pinned, checksum, backup e re-sync. |
| Inventario Python omite comandos atuais e preserva caminhos YAML como principais | `spec stale` | Inventariar Flow, Prep Flow, Intake, helpers e modulos atuais; marcar TODO/log YAML somente como compatibilidade de migracao. |
| Timezone de `issue_add.py` ainda aponta para TODO root | `spec stale` | Documentar deteccao do timezone local, sem dependencia de TODO YAML. |
| CLI de `package.py` anuncia modos/flags inexistentes | `spec stale` | Fixar o contrato atual em `--next-version`, notas de release e `--dir`; remover `--version`, `--output`, `--archive-format` e `--changelog` como capacidades vigentes. |
| Checksum, changelog e validacao de versao estao atribuidos aos componentes errados | `spec stale` | Manter checksum no manifesto/latest e verificacao no installer/update; changelog sem `package_sha256`; init apenas finaliza/reconcilia. |
| Outputs de `log_add.py` e `todo_update.py` estao desatualizados | `spec stale` | Especificar os payloads reais, incluindo `issue_path`; nao exigir campos que a CLI nao retorna. |
| Overview ainda coloca YAML no centro operacional | `internal spec contradiction` | Fixar issue Markdown como fonte operacional e YAML apenas como legado/compatibilidade. |
| `flow_prepared_until` foi aprovado como `subtle`, mas o schema ficou 2.00 | `implementation drift` | Aplicar minor bump para 2.01, com leitura transicional de 2.00, emissao/reconciliacao em 2.01 e rollout via init/update. |
| Regras de validacao divergem entre specs e yoda-0049 | `internal spec contradiction` com `implementation drift` parcial | Preservar as decisoes explicitas da yoda-0049 para dependencia ausente como resolvida e `phase` fora de `doing` ignorada; implementar o que segue normativo e nao foi revogado: timestamps com timezone e `pending_reason` obrigatorio/exposto em `pending`. |
| Out-of-scope ainda trata distribuicao como futura | `spec stale` | Reconhecer package/installer/update como capacidades atuais e manter apenas publicacao automatizada como fora de escopo. |
| README nao oferece link editorial para o site em `docs/` | `documentation omission` | Adicionar link navegavel para `https://alexdundes.github.io/yoda/` e informar que o site publicado vem de `docs/`, conforme yoda-0028. |

Associacoes com issues foram confirmadas pelos respectivos corpos/Result logs e
pelos commits que alteraram os entrypoints. Nao foi encontrada evidencia para
criar outra issue: todos os pontos cabem no contrato consolidado desta yoda-0064.

Decisoes aprovadas no encerramento de Study:

1. Adotar o schema `2.01` para corrigir o bump sutil omitido em yoda-0062,
   mantendo compatibilidade de leitura com `2.00` durante o rollout.
2. Adotar a regra hibrida de validacao: preservar as excecoes deliberadas da
   yoda-0049 e endurecer somente timestamps e metadados de `pending`.
3. Criar `project/specs/27-yoda-prep-flow-script.md`, pois o numero 26 ja e usado
   por `get_extern_issue.py`, em vez de diluir todo o contrato apenas nas specs
   gerais de processo e scripts.

## Document contract

O Implement deve seguir esta ordem document-first e nao introduzir decisoes
novas fora deste contrato.

### 1. Specs gerais e baseline

- `project/specs/README.md`: indexar a nova spec 27.
- `project/specs/00-conventions.md`: declarar baseline operacional 0.4.0, schema
  corrente 2.01, compatibilidade 2.00 e ordem canonica com
  `flow_prepared_until` e `pending_reason` antes de `depends_on`.
- `project/specs/01-yoda-overview.md` e
  `project/specs/03-document-first-yaml-markdown.md`: tornar issue Markdown o
  centro operacional e limitar YAML a manifesto, changelog, metadados externos
  e compatibilidade/migracao.
- `project/specs/04-todo-dev-yaml-issues.md`: atualizar o contrato da issue para
  0.4.0/schema 2.01, registrar `flow_prepared_until` e atribuir `--check` e
  `--apply` ao update.
- `project/specs/12-yoda-structure.md` e
  `project/specs/14-issue-templates-usage.md`: refletir a estrutura atual,
  opcionais omitidos, schema 2.01 e reconciliacao por init sem flags de update.

Referencias historicas a 0.3.0 podem permanecer apenas quando descrevem a
migracao breaking que introduziu Markdown-first; titulos operacionais como
"script set", "canonical order" e "current contract" devem usar 0.4.0 ou nao
fixar versao.

### 2. Flow, Prep Flow e catalogo de scripts

- `project/specs/02-yoda-flow-process.md`: incluir o YODA Prep Flow como preparo
  alternativo de Study/Document, mantendo o YODA Flow em quatro fases e uma
  etapa por autorizacao.
- `project/specs/05-scripts-and-automation.md`,
  `project/specs/06-agent-playbook.md`, `project/specs/13-yoda-scripts-v1.md` e
  `project/specs/15-scripts-python-structure.md`: inventariar os entrypoints e
  modulos atuais; definir `todo_next.py`/`todo_list.py` como helpers e
  `yoda_flow_next.py` como driver canonico; retirar TODO/log YAML dos paths
  operacionais correntes.
- `project/specs/21-yoda-flow-next-script.md`: documentar entrada direta em
  Implement para `to-do + flow_prepared_until=document` e compatibilidade de
  schema.
- Criar `project/specs/27-yoda-prep-flow-script.md` com CLI, selecao explicita
  por `--issue`, independencia da ordem/dependencias para preparo, transicoes
  `none -> study -> document`, persistencia em `to-do`, retomada pelo Flow,
  `--dry-run`, outputs e erros.

### 3. Contratos das CLIs existentes

- `project/specs/16-todo-list-script.md`: substituir toda ordem YAML por
  desempate por ID; manter prioridade + ID no default e timestamp + ID nos
  modos alternativos.
- `project/specs/18-issue-add-script.md`: remover `id` do front matter, usar
  schema 2.01, timezone local detectado e payload real com `issue_id`,
  `issue_path`, `template` e `dry_run`.
- `project/specs/19-log-add-script.md`: trocar `log path` por `issue_path` e
  explicitar `issue_id`, `timestamp` e `dry_run`.
- `project/specs/20-todo-update-script.md`: documentar o payload real
  (`issue_id`, `updated_fields`, `issue_path`, `dry_run`) sem prometer timestamp
  de saida; `flow_prepared_until` permanece gerenciado pelo Prep Flow, nao por
  uma nova flag de `todo_update.py`.
- `project/specs/23-distribution-and-packaging.md`: manter apenas o modo atual
  `--next-version`, campos de release, `--dir` e `--dry-run`; remover capacidades
  inexistentes (`--version`, `--output`, `--archive-format`, `--changelog`);
  manter checksum no manifesto/latest e nao no changelog.
- `project/specs/24-installation-and-upgrade.md`: cobrir one-liner latest/pinned,
  `latest.json`, checksum, backup, `update.py --check/--apply`, preservacao de
  dados e chamada nao intrusiva ao init.
- `project/specs/22-out-of-scope.md`: reconhecer package, installer e update
  como capacidades atuais; deixar somente publicacao automatizada fora de
  escopo.

### 4. Schema 2.01 e validacao

- Centralizar em `yoda/scripts/lib/issue_metadata.py` a versao corrente `2.01`
  e o conjunto compativel `{2.00, 2.01}` para evitar novos literais divergentes.
- `issue_add.py` deve criar novas issues em 2.01.
- `issue_index.py` deve ler 2.00 e 2.01; continuar tratando dependencia ausente
  como resolvida e ignorando `phase` fora de `doing`, conforme yoda-0049.
- `issue_index.py` deve validar `created_at`/`updated_at` com timezone e carregar
  `pending_reason`, exigindo valor nao vazio quando `status=pending`.
- `todo_update.py`, `yoda_flow_next.py` e `yoda_prep_flow.py` devem aceitar
  issues 2.00/2.01 e gravar 2.01 quando alterarem front matter.
- `init.py` deve migrar front matter 2.00 para 2.01 no fluxo normal executado
  apos update, sem depender da existencia de TODO YAML e sem tocar arquivos de
  agente/intent na raiz.
- `yoda/scripts/lib/validate.py` deve reconhecer 2.01 nos caminhos legados ainda
  suportados.
- Nao reescrever issues concluidas manualmente neste repositorio; a migracao
  deve ser exercida pelo mecanismo do init e coberta por fixture/teste.

### 5. README e site

- Atualizar o `README.md` raiz com um link editorial navegavel para
  `https://alexdundes.github.io/yoda/`.
- Informar no mesmo trecho que o site publicado e mantido a partir de `docs/`.
- Nao alterar o conteudo visual de `docs/index.html`; ele e somente a fonte do
  site referenciada pelo README neste escopo.

### 6. Verificacao fechada

- Atualizar testes de emissao/migracao para esperar 2.01 e preservar fixtures
  explicitas de compatibilidade 2.00.
- Adicionar testes do indice para schema 2.01, compatibilidade 2.00, timestamps
  invalidos/sem timezone e `pending_reason` ausente/presente.
- Adicionar testes de Flow, Prep Flow e todo_update provando que uma mutacao de
  issue 2.00 persiste 2.01 sem mudar as excecoes da yoda-0049.
- Adicionar teste de init que migra uma issue Markdown 2.00 mesmo sem TODO YAML.
- Executar `python3 -m pytest yoda/scripts/tests`.
- Comparar specs de CLI com os respectivos `--help`, validar links Markdown e
  varrer termos/flags legados; ocorrencias historicas devem estar explicitamente
  qualificadas.
- Confirmar por diff que `docs/.DS_Store` e demais alteracoes preexistentes nao
  foram incorporadas ao trabalho da issue.

Proxima acao deterministica apos aprovacao deste Document: entrar em Implement,
atualizar primeiro `project/specs/` e depois README/scripts/testes, exatamente
nos limites acima.

## Tests

- Executar python3 -m pytest yoda/scripts/tests.
- Conferir comandos afetados com o respectivo --help.
- Usar rg para localizar 0.3.0, ordem YAML, flags inexistentes, outputs antigos
  e papeis legados remanescentes em project/specs/.
- Verificar links Markdown relativos desta issue e das specs alteradas.

## Risks and edge cases

- Transformar bug de implementacao em regra normativa apenas para coincidir texto
  e codigo.
- Atualizar somente specs centrais e manter drift em estrutura Python,
  out-of-scope, packaging ou instalacao.
- Aplicar bump de schema sem rollout compativel ou manter schema 2.00 sem decisao.
- Remover contexto historico em vez de marca-lo claramente como legado.
- Criar uma spec sem atualizar indice e referencias cruzadas.

## Result log

docs: sincronizar specs do YODA com o estado 0.4.0 e schema 2.01

Consolidou o conjunto `project/specs/` com o estado corrente do framework:
baseline operacional 0.4.0, YODA Prep Flow e `flow_prepared_until` documentados
em processo/schema/catalogo, spec dedicada 27 criada e indexada, contratos de
`todo_list.py`, `issue_add.py`, `log_add.py`, `todo_update.py`, `init.py`,
`update.py`, `package.py` e instalador alinhados com `--help`, codigo e testes.

Aplicou o schema 2.01 de forma centralizada em `issue_metadata.py`, com leitura
compativel 2.00/2.01, escrita 2.01 em Flow/Prep Flow/todo_update e migracao pelo
`init.py` sem depender de TODO YAML. A validacao hibrida da yoda-0049 foi
preservada (dependencia ausente resolvida, `phase` fora de `doing` ignorada) e o
endurecimento ficou restrito a timestamps com timezone e `pending_reason`
obrigatorio em `pending`, com mensagens de erro acionaveis e o comportamento
fail-fast declarado explicitamente na spec 05.

Corrigiu tambem o desempate por ID ascendente nos modos `--order` descendentes,
os avisos de compatibilidade MAJOR/build antigo em `update.py`, o guard de
`--version` contra `latest.json` e o link do site oficial no `README.md`.

Suite: `79 passed`.

- **Issue**: `yoda-0064`

- **Path**: `yoda/project/issues/yoda-0064-sincronizar-specs-com-mudancas-omitidas-em-issues-concluidas.md`

## Flow log
- 2026-08-31T10:13:04-03:00 issue_add created title=Sincronizar specs com mudancas omitidas em issues concluidas; priority=5
- 2026-08-31T10:23:22-03:00 Intake completed with consolidated spec divergences and source-issue traceability
- 2026-08-31T11:31:04-03:00 Intake follow-up: incluir no README o link do site oficial publicado a partir de docs/
- 2026-08-31T11:35:58-03:00 transition to-do->doing/study
- 2026-08-31T11:45:21-03:00 transition doing/study->doing/document | Study aprovado: schema 2.01 compativel com 2.00, validacao hibrida conforme yoda-0049 e spec dedicada ao YODA Prep Flow
- 2026-08-31T13:14:37-03:00 transition doing/document->doing/implement | Document aprovado: plano fechado para specs 0.4.0, Prep Flow, schema 2.01, validacao hibrida, CLIs e README do site
- 2026-08-31T14:33:29-03:00 transition doing/implement->doing/evaluate | Evaluate iniciado: auditoria de specs, scripts e testes da yoda-0064
- 2026-08-31T15:06:40-03:00 transition doing/evaluate->done | Evaluate aprovada: 79 testes passaram, contratos CLI conferidos e divergencias documentais resolvidas
