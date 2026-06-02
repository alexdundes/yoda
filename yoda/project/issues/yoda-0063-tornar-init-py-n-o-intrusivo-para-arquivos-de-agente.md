---
schema_version: '2.00'
status: done
title: "Tornar init.py n\xE3o intrusivo para arquivos de agente"
description: "Alterar o YODA para deixar de criar ou modificar arquivos de agente\
  \ e intent na raiz do projeto host. As instru\xE7\xF5es de agente do YODA devem\
  \ ficar autocontidas dentro de yoda/ e ser tratadas pelo pacote/update do pr\xF3\
  prio framework."
priority: 5
extern_issue_file: ../extern_issues/github-007.json
created_at: '2026-06-02T09:09:50-03:00'
updated_at: '2026-06-02T10:19:33-03:00'
---

# yoda-0063 - Tornar init.py não intrusivo para arquivos de agente

## Summary
Alterar a abordagem de inicializacao do YODA para que o framework nao crie nem
modifique arquivos de agente ou intent na raiz do projeto host. As instrucoes de
agente do YODA devem ser autocontidas dentro de `yoda/` (`yoda/AGENTS.md`,
`yoda/GEMINI.md`, `yoda/CLAUDE.md` e `yoda/yoda.md`), seguir no pacote/update do
proprio framework e poder ser substituidas pelo mecanismo de distribuicao do YODA.

## Context
Hoje `yoda/scripts/init.py` atua sobre arquivos markdown e YAML na raiz do
projeto host, incluindo `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`, `REPO_INTENT.md`
e `repo.intent.yaml`. Esse comportamento foi util para onboarding, mas torna o
YODA intrusivo nas instrucoes proprias do projeto consumidor.

A issue externa GitHub #7 define uma mudanca de abordagem: o YODA deve ser
autocontido e nao interferir nas instrucoes do projeto host. Arquivos voltados a
agentes do YODA devem morar dentro de `yoda/`, fazer parte do artefato
distribuivel e ser atualizados/substituidos pelo fluxo normal de update/package.

## Objective
Fazer `init.py` deixar de criar, anexar ou atualizar arquivos de agente/intent na
raiz do projeto host e consolidar as instrucoes de agente do YODA dentro da
pasta `yoda/`, mantendo o framework autocontido e nao intrusivo.

## Scope
- Remover de `init.py` a criacao/alteracao de `AGENTS.md`, `GEMINI.md`,
  `CLAUDE.md`, `REPO_INTENT.md` e `repo.intent.yaml` na raiz do projeto host.
- Criar arquivos autocontidos de entrada para agentes em `yoda/AGENTS.md`,
  `yoda/GEMINI.md` e `yoda/CLAUDE.md`, apontando para `yoda/yoda.md`.
- Nao criar equivalentes autocontidos de `REPO_INTENT.md` ou `repo.intent.yaml`.
- Garantir que os arquivos autocontidos em `yoda/` entram no pacote e no fluxo de
  update, quando aplicavel.
- Atualizar `yoda/yoda.md` para remover a dependencia de leitura de
  `REPO_INTENT.md` e passar a ser autocontido.
- Atualizar README, manuais, runbooks dos scripts e documentacao operacional para
  refletir que `init.py` nao e mais intrusivo.
- Revisar e alinhar as especificacoes em `project/specs/` afetadas pela mudanca,
  especialmente entrada de agentes, empacotamento e instalacao/update.
- Atualizar testes de `init.py`, package/update e contratos CLI conforme
  necessario.

## Out of scope
- Migrar ou remover automaticamente arquivos de agente ja existentes na raiz de
  projetos consumidores.
- Editar instrucoes proprietarias do projeto host.
- Fechar ou atualizar automaticamente a issue externa no GitHub.
- Alterar o modelo canonico de issues markdown (`yoda/project/issues/*.md`).

## Requirements
- `init.py` nao deve escrever, criar, anexar bloco ou fazer merge em arquivos de
  agente/intent na raiz do projeto host.
- Em modo `--dry-run`, `init.py` tambem nao deve reportar escrita planejada
  nesses arquivos raiz.
- O YODA deve manter sua documentacao operacional autocontida dentro de `yoda/`,
  incluindo `yoda/AGENTS.md`, `yoda/GEMINI.md`, `yoda/CLAUDE.md` e
  `yoda/yoda.md`.
- `yoda/AGENTS.md`, `yoda/GEMINI.md` e `yoda/CLAUDE.md` devem ser curtos e devem
  orientar a leitura de `yoda/yoda.md`, sem duplicar playbooks extensos.
- `yoda/yoda.md` nao deve orientar leitura de `REPO_INTENT.md`.
- A lista de arquivos empacotados deve incluir os novos arquivos autocontidos.
- O update/package deve continuar substituindo arquivos de framework sob `yoda/`
  sem tocar dados de projeto preservados.
- A documentacao deve explicar que projetos host podem manter seus proprios
  arquivos de agente e, se desejarem, apontar manualmente para `yoda/yoda.md`.
- `project/specs/07-agent-entry-files.md` deve refletir que os arquivos
  de entrada de agentes sao autocontidos sob `yoda/` e que `init.py` nao toca a
  raiz do host.
- `project/specs/23-distribution-and-packaging.md` deve incluir os arquivos de
  agente autocontidos no contrato do artefato e remover expectativa de skeleton
  raiz com `AGENTS.md`.
- `project/specs/24-installation-and-upgrade.md` e runbooks de scripts devem ser
  revisados para nao sugerir mutacao de arquivos raiz de agente/intent.

## Acceptance criteria
- [x] `init.py` nao cria nem modifica `AGENTS.md`, `GEMINI.md`, `CLAUDE.md`,
      `REPO_INTENT.md` ou `repo.intent.yaml` na raiz do projeto host.
- [x] Testes cobrem projeto vazio e projeto com arquivos de agente existentes,
      validando que eles permanecem ausentes/inalterados.
- [x] Existem `yoda/AGENTS.md`, `yoda/GEMINI.md` e `yoda/CLAUDE.md`, todos
      autocontidos e apontando para `yoda/yoda.md`.
- [x] `yoda/yoda.md` nao instrui agentes a ler `REPO_INTENT.md`.
- [x] Package/update incluem ou preservam corretamente os arquivos autocontidos
      de instrucao, sem depender de arquivos raiz do projeto host.
- [x] README/manual/script help deixam claro que `init.py` e nao intrusivo em
      relacao aos arquivos de agente/intent do projeto host.
- [x] `project/specs/` foi revisado e atualizado nos contratos afetados.
- [x] A suite relevante de testes passa.

## Entry points
- project/specs/07-agent-entry-files.md
- project/specs/23-distribution-and-packaging.md
- project/specs/24-installation-and-upgrade.md
- project/specs/06-agent-playbook.md
- project/specs/12-yoda-structure.md
- yoda/scripts/init.py
- yoda/scripts/tests/test_init.py
- package.py
- yoda/scripts/tests/test_package.py
- yoda/scripts/update.py
- yoda/yoda.md
- yoda/AGENTS.md
- yoda/GEMINI.md
- yoda/CLAUDE.md
- README.md
- yoda/scripts/README.md
- yoda/project/extern_issues/github-007.json

## Implementation notes
Tratar esta mudanca como alteracao de abordagem operacional, nao como migracao
destrutiva. O comportamento novo deve ser forward-only: `init.py` deixa de tocar
arquivos raiz daqui para frente, mas nao remove arquivos ja existentes.

Decisao de Study:

- Criar `yoda/AGENTS.md`, `yoda/GEMINI.md` e `yoda/CLAUDE.md`.
- Nao criar `REPO_INTENT.md` nem `repo.intent.yaml` dentro de `yoda/`.
- Remover integralmente do `init.py` a logica de escrita/merge para arquivos de
  agente e intent da raiz do host.
- Revisar docs/runbooks/scripts e `project/specs/` no mesmo trabalho.
- Revisar empacotamento para incluir os novos arquivos autocontidos.

Evitar duplicar instrucoes longas nos novos arquivos de agente. Eles devem atuar
como roteadores autocontidos para `yoda/yoda.md`.

## Tests
Atualizar testes de `init.py` que hoje esperam criacao/alteracao de arquivos
raiz. Adicionar regressao para garantir que arquivos de agente existentes no host
nao sao alterados e que, em projeto vazio, esses arquivos nao sao criados.

Adicionar ou ajustar testes de empacotamento/update para confirmar que
`yoda/AGENTS.md`, `yoda/GEMINI.md` e `yoda/CLAUDE.md` entram no artefato e sao
tratados como arquivos de framework substituiveis.

## Risks and edge cases
- Projetos host que dependiam do bloco automatico em `AGENTS.md` deixam de
  receber esse onboarding automatico.
- Documentacao pode ficar ambigua se ainda mencionar que `init.py` altera
  arquivos raiz.
- O pacote pode ficar incompleto se novos arquivos autocontidos nao entrarem no
  manifesto/arquivo distribuivel.
- Mudancas em `init.py` nao devem afetar preservacao de dados YODA como
  `yoda/project/issues/` e `yoda/project/extern_issues/`.
- Specs antigas podem continuar descrevendo `init.py` como criador de
  `AGENTS.md` na raiz se a revisao de `project/specs/` nao for completa.

## Result log
fix(yoda): stop init from mutating host agent files

`init.py` deixou de criar, atualizar ou mesclar arquivos de agente/intent na raiz
do projeto host. O YODA agora carrega entradas autocontidas em `yoda/AGENTS.md`,
`yoda/GEMINI.md` e `yoda/CLAUDE.md`, com documentacao operacional apontando para
`yoda/yoda.md`, specs/runbooks alinhados e empacotamento cobrindo os novos
arquivos.

- **GitHub Issue** :   #007

- **Issue**: `yoda-0063`

- **Path**: `yoda/project/issues/yoda-0063-tornar-init-py-n-o-intrusivo-para-arquivos-de-agente.md`

## Flow log
- 2026-06-02T09:09:50-03:00 issue_add created title=Tornar init.py não intrusivo para arquivos de agente; priority=5
- 2026-06-02T09:14:02-03:00 transition to-do->doing/study
- 2026-06-02T09:20:11-03:00 transition doing/study->doing/document | Study approved: create yoda/AGENTS.md GEMINI.md CLAUDE.md, remove host root agent/intent mutations from init.py, update yoda.md, docs/runbooks, project specs, and packaging
- 2026-06-02T09:22:22-03:00 transition doing/document->doing/implement | Document approved: implement non-intrusive init, yoda-local agent files, yoda.md entry update, project specs/docs, packaging, and tests
- 2026-06-02T09:32:54-03:00 transition doing/implement->doing/evaluate | Implement completed: init is non-intrusive for host-root agent/intent files, YODA-local agent entries were added, docs/specs/package/tests were updated, and spec 07 was renamed to agent-entry-files before evaluation
- 2026-06-02T10:19:33-03:00 transition doing/evaluate->done | Evaluate approved: acceptance criteria validated, result log filled, and test suite passed with 68 tests
