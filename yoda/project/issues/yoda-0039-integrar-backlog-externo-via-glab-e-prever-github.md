---
created_at: '2026-02-25T15:36:45-03:00'
depends_on:
- yoda-0038
description: 'Redefinir o uso de origin para mapear e traduzir backlog externo em
  issues YODA usando glab (GitLab CLI), permitindo que uma issue externa gere uma
  ou varias issues YODA. Prever tambem operacao equivalente com issues do GitHub (gh).
  Regra transversal: atualizar primeiro project/specs/ e depois yoda/.'
id: yoda-0039
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 1
schema_version: '1.01'
slug: integrar-backlog-externo-via-glab-e-prever-github
status: done
title: Integrar backlog externo via glab e prever GitHub
updated_at: '2026-02-26T17:12:16-03:00'
---

# yoda-0039 - Integrar backlog externo via glab e prever GitHub

## Summary
Introduzir o comando `yoda_intake.py` como entrada operacional do YODA Intake e separar a coleta externa no novo `get_extern_issue.py`. O intake passa a consumir JSON local em `yoda/project/extern-issues/`, mantendo o agente no fluxo de runbook e o humano responsável pela execução de integração externa.

## Context
Hoje o Intake estava descrito diretamente em `yoda/yoda.md`, sem um comando dedicado para guiar o agente. A ingestao externa tambem precisava separar responsabilidades entre humano (execucao de CLI externa) e agente (orquestracao do fluxo e decomposicao em micro issues locais).

## Objective
Padronizar o Intake via `yoda_intake.py` com fluxo em duas etapas e mover a coleta externa para `get_extern_issue.py`, mantendo rastreabilidade de origem externa e documentacao consistente em `project/specs/`.

## Scope
- Criar `yoda/scripts/yoda_intake.py`.
- Criar `yoda/scripts/get_extern_issue.py` para ser executado pelo humano.
- Suportar execucao inicial com `--dev` para devolver runbook curto de decisao.
- Suportar execucao com `--dev --extern-issue <NNN>` para devolver:
  - runbook completo do Intake para o agente;
  - resumo amigavel (Markdown) da issue externa.
- Suportar execucao com `--dev --no-extern-issue` para devolver runbook completo sem ingestao externa.
- Detectar provedor pelo `origin` do repositorio (`.git/config` / remote URL) para decidir entre `glab` e `gh`.
- Implementar cliente por provedor em modulos dedicados em `yoda/scripts/lib/` (ex.: `provider_gitlab.py`, `provider_github.py`).
- Atualizar `yoda/yoda.md`: retirar detalhes operacionais de Intake e instruir que a entrada no Intake deve chamar `yoda_intake.py` e seguir o runbook.
- Revisar e alinhar toda documentacao relevante em `project/specs/` para manter consistencia de contrato.
- Criar specs dedicadas para os novos scripts (`25-yoda-intake-script.md` e `26-get-extern-issue-script.md`).
- Manter classificacao da issue como **subtle**.

## Out of scope
- Sincronizacao bidirecional completa de estado entre plataformas.
- Cobrir todos provedores de issue tracker alem de GitLab/GitHub.
- Fechar automaticamente issues externas via texto de commit.

## Requirements
- Ordem obrigatoria: `project/specs/` antes de `yoda/`.
- Ao entrar no YODA Intake, o agente deve chamar `yoda_intake.py --dev <slug>` como primeiro passo.
- O retorno inicial (`--dev` apenas) deve orientar:
  - perguntar ao humano se existe issue externa;
  - se sim: executar `yoda_intake.py --dev <slug> --extern-issue <NNN>`;
  - se nao: executar `yoda_intake.py --dev <slug> --no-extern-issue`.
- Em modo `--extern-issue <NNN>`, `yoda_intake.py` deve orientar o agente a pedir ao humano a execucao de `get_extern_issue.py`.
- `get_extern_issue.py` deve detectar provedor pelo `origin`, consultar issue externa via CLI correspondente e salvar JSON em `yoda/project/extern-issues/`.
- Depois do JSON salvo, `yoda_intake.py --extern-issue <NNN>` retorna runbook completo + resumo Markdown com base no arquivo local.
- Se o provedor detectado nao estiver suportado, `get_extern_issue.py` retorna erro explicito.
- Se CLI necessario nao estiver instalado ou auth falhar, `get_extern_issue.py` retorna instrucao acionavel ao humano.
- O YODA deve associar commit a issue externa usando `#NNN`, sem usar termos de fechamento automatico (`Closes/Fixes/Resolves`).
- Deve existir rastreabilidade entre issue YODA criada e `origin` da issue externa.
- Classificacao confirmada: **subtle**.

## Acceptance criteria
- [x] `yoda_intake.py --dev <slug>` retorna runbook inicial com decisao externa vs sem externa.
- [x] `yoda_intake.py --dev <slug> --extern-issue <NNN>` retorna runbook para coleta externa quando JSON nao existe e runbook completo quando JSON existe.
- [x] `yoda_intake.py --dev <slug> --no-extern-issue` retorna runbook completo sem consulta externa.
- [x] `get_extern_issue.py --dev <slug> --extern-issue <NNN>` salva `yoda/project/extern-issues/<provider>-<NNN>.json` e imprime proximo comando do loop.
- [x] Provedor e CLI sao escolhidos pela origem (`origin`): GitLab -> `glab`, GitHub -> `gh`.
- [x] Sem CLI requerido instalado ou sem auth, `get_extern_issue.py` retorna instrucao acionavel.
- [x] Sem suporte para o provedor detectado, `get_extern_issue.py` retorna erro explicito.
- [x] Fluxo documentado em `project/specs/` e `yoda/yoda.md` atualizado para delegar Intake ao script.
- [x] Regras de commit externo documentadas: associar com `#NNN`, sem fechamento automatico.
- [x] Fluxo suporta uma issue externa originando uma ou multiplas issues YODA com rastreabilidade via `origin`.
- [x] Specs dedicadas criadas para `yoda_intake.py` e `get_extern_issue.py`.

## Dependencies
`yoda-0038` caso haja alteracao de layout YAML/origin.

## Entry points
- path: project/specs/
  type: doc
- path: yoda/scripts/yoda_intake.py
  type: code
- path: yoda/scripts/get_extern_issue.py
  type: code
- path: yoda/scripts/lib/provider_gitlab.py
  type: code
- path: yoda/scripts/lib/provider_github.py
  type: code
- path: project/specs/25-yoda-intake-script.md
  type: doc
- path: project/specs/26-get-extern-issue-script.md
  type: doc
- path: yoda/yoda.md
  type: doc
- path: .git/config
  type: config

## Implementation notes
- Decisao de planejamento: tratar esta issue como `subtle`.
- Primeiro passo operacional do Intake passa a ser comando (`yoda_intake.py`) e nao bloco textual embutido no manual.
- Provedor deve ser inferido da URL de `origin` (sem parametro adicional no MVP).
- Nao fechar automaticamente issue externa; apenas associar por `#NNN` quando aplicavel no texto sugerido de commit.
- `yoda_intake.py` nao consulta API externa; ele consome arquivo local de `extern-issues`.
- Coleta externa fica explicitamente no `get_extern_issue.py` (execucao humana).

## Tests
- Testes de CLI para tres modos: `--dev`, `--extern-issue`, `--no-extern-issue`.
- Testes de deteccao de provedor a partir de `origin` em `get_extern_issue.py`.
- Testes de erros acionaveis: CLI ausente, auth ausente, provedor nao suportado em `get_extern_issue.py`.
- Testes de renderizacao do resumo Markdown da issue externa.
- Testes de mapeamento de `origin` para uma e multiplas issues YODA.

## Risks and edge cases
- Limitacoes de autenticacao/escopo de token no `glab` e `gh`.
- Diferencas de modelo de dados entre GitLab e GitHub.
- Duplicacao de issues se nao houver controle de idempotencia na importacao.
- Repositorios com multiplos remotes ou `origin` ausente.
- Ambientes sem rede/CLI disponivel durante Intake.

## Result log
Implementado o fluxo completo de Intake externo com separacao de responsabilidade: `get_extern_issue.py` realiza a coleta externa e persiste JSON local em `yoda/project/extern-issues/`, enquanto `yoda_intake.py` orquestra runbooks e consome o arquivo local para apoiar a decomposicao em micro issues. Tambem foram adicionadas specs dedicadas (`25` e `26`) e ajustes de documentacao cruzada nos contratos de scripts.

feat(yoda): add external-intake handoff with get_extern_issue and local source files
Issue: `yoda-0039`
Path: `yoda/project/issues/yoda-0039-integrar-backlog-externo-via-glab-e-prever-github.md`