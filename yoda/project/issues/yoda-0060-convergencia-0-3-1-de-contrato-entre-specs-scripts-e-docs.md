---
schema_version: '2.00'
status: done
title: Convergencia 0.3.1 de contrato entre specs, scripts e docs
description: 'Executar uma rodada curta de convergencia final pos-0.3.0: validar e
  alinhar contratos de issue markdown, Flow log, Entry points e documentos estruturais
  (README, REPO_INTENT, repo.intent.yaml e specs centrais) para eliminar drift residual.'
priority: 5
created_at: '2026-03-07T20:36:29-03:00'
updated_at: '2026-03-07T21:04:30-03:00'
---

# yoda-0060 - Convergencia 0.3.1 de contrato entre specs, scripts e docs

## Summary
Ha sinais de drift residual entre specs, scripts, backlog historico e documentos de entrada do repositorio apos a release 0.3.0.
Esta issue organiza uma rodada curta de convergencia 0.3.1 para consolidar contrato canonico e marcar explicitamente o que e compatibilidade ou legado.
O foco e reduzir ambiguidade para agentes e humanos antes de novas evolucoes funcionais.

## Context
A demanda veio de uma revisao tecnica consolidada em texto livre (sem `extern_issue_file`), com apontamentos de inconsistencias entre narrativas e artefatos.
Parte dos temas ja teve tratamento forward-only, mas ainda e necessario validar de ponta a ponta se a documentacao estrutural e os contratos centrais estao alinhados com o comportamento atual dos scripts.
Sem esta convergencia final, o projeto permanece funcional, porem com custo cognitivo alto e risco de interpretacao divergente.

## Objective
Entregar um baseline 0.3.1 semanticamente coerente, com contrato unico e explicito sobre issue markdown, logs de fluxo, entry points e documentos de onboarding/repositorio.

## Scope
- Revalidar contrato vigente nos scripts e nas specs centrais (`07`, `11`, `16`, `18`).
- Revisar e alinhar `README.md`, `REPO_INTENT.md` e `repo.intent.yaml` com o modelo canonico atual.
- Declarar explicitamente, em texto, o que e canonico, o que e compatibilidade e o que e legado.
- Verificar se existe drift residual no backlog historico e definir estrategia (manter legacy, migrar, ou registrar excecoes).
- Remover `yoda/project/issues/other-0001-beta.md` do backlog ativo e tratar o caso apenas como fixture de teste.
- Ajustar testes para nao depender de artefato fixo no repositório de issues e garantir limpeza no teardown.

## Out of scope
- Migracao em massa de todas as issues antigas nesta mesma entrega.
- Reescrita ampla de arquitetura ou criacao de novos comandos.
- Mudancas de release/packaging fora do que for necessario para consistencia documental.

## Requirements
- Cada contrato potencialmente ambiguo deve ficar com uma unica regra oficial documentada.
- A documentacao revisada deve indicar com clareza itens de compatibilidade e itens de legado.
- Quando houver divergencia nao resolvida nesta issue, abrir follow-up explicito no backlog.
- Registrar no corpo da issue as premissas adotadas por nao haver fonte externa vinculada.
- `other-0001-beta.md` nao deve permanecer como issue ativa em `yoda/project/issues`.
- O caso de teste relacionado deve operar com arquivo temporario e limpar residuos ao final.

## Acceptance criteria
- [x] `project/specs/07-agent-entry-and-root-file.md`, `11-yoda-intake.md`, `16-todo-list-script.md` e `18-issue-add-script.md` estao consistentes com o contrato vigente.
- [x] `README.md`, `REPO_INTENT.md` e `repo.intent.yaml` deixam explicito o papel de canonico/compatibilidade/legado.
- [x] `other-0001-beta.md` foi removido de `yoda/project/issues` e seu papel foi convertido para fixture temporaria de teste.
- [x] Suite de testes confirma que nao ha residuos (`other-*.md`) apos execucao dos testes afetados.
- [x] Qualquer gap remanescente foi convertido em issue(s) de follow-up com rastreabilidade clara.

## Entry points
- `README.md`
- `REPO_INTENT.md`
- `repo.intent.yaml`
- `project/specs/07-agent-entry-and-root-file.md`
- `project/specs/11-yoda-intake.md`
- `project/specs/16-todo-list-script.md`
- `project/specs/18-issue-add-script.md`
- `yoda/yoda.md`
- `yoda/project/issues`
- `yoda/scripts/tests/test_issue_index.py`
- `yoda/scripts/tests/conftest.py`
- `yoda/project/issues/yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md`

## Implementation notes
Executar em ordem document-first: decidir contrato, atualizar docs estruturais, depois ajustar backlog/follow-ups.
Evitar apagar contexto historico: preferir marcar legado explicitamente quando a remocao nao trouxer ganho objetivo.
Para `other-0001-beta.md`, preferir fixture gerada durante o teste (e removida no cleanup) em vez de manter artefato estatico dentro de `yoda/project/issues`.

## Tests
Executar `python3 -m pytest yoda/scripts/tests/test_issue_index.py` apos ajuste de fixture/cleanup.
Executar `python3 -m pytest yoda/scripts/tests` para regressao geral e confirmar ausencia de residuos em `yoda/project/issues`.

## Risks and edge cases
- Tratar conclusoes de revisao externa como fato sem revalidacao local.
- Ajustar docs sem refletir comportamento real de scripts.
- Criar texto muito generico e manter ambiguidades operacionais.
- Remover `other-0001-beta.md` sem adaptar teste pode quebrar cobertura de filtro por `dev`.

## Result log
docs(specs): convergir contrato 0.3.1 para modelo markdown-first

Foi concluida a rodada de convergencia documental e contratual da 0.3.1 com alinhamento entre specs, docs raiz e comportamento dos scripts. Foram atualizados `README.md`, `REPO_INTENT.md` e `repo.intent.yaml` para explicitar `issue markdown` como caminho canonico e YAML como compatibilidade/legado. As specs `07`, `11`, `16` e `18` foram revisadas para refletir a operacao atual baseada em `yoda/project/issues/*` e `## Flow log` embutido.

Tambem foi removido `yoda/project/issues/other-0001-beta.md` do backlog ativo e o cleanup de testes foi ajustado para limpar `other-*.md`, evitando residuos no repositorio. A validacao foi executada com sucesso em `python3 -m pytest yoda/scripts/tests/test_issue_index.py` (6 passed) e `python3 -m pytest yoda/scripts/tests` (57 passed), sem gaps remanescentes que exigissem follow-up adicional nesta entrega.

- **Issue**: `yoda-0060`

- **Path**: `yoda/project/issues/yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md`

## Flow log
- 2026-03-07T20:36:29-03:00 issue_add created title=Convergencia 0.3.1 de contrato entre specs, scripts e docs; priority=5
- 2026-03-07T20:50:56-03:00 transition to-do->doing/study
- 2026-03-07T20:55:15-03:00 transition doing/study->doing/document | Study aprovado: alinhar contratos e tratar other-0001-beta como artefato de teste com limpeza e remocao do projeto ativo
- 2026-03-07T20:57:02-03:00 transition doing/document->doing/implement | Document aprovado: implementar convergencia markdown-first e remover other-0001-beta do backlog ativo
- 2026-03-07T21:03:48-03:00 transition doing/implement->doing/evaluate | Implement concluido: convergencia docs/specs markdown-first, remocao de other-0001-beta e testes verdes
- 2026-03-07T21:04:30-03:00 transition doing/evaluate->done | Evaluate aprovado: convergencia 0.3.1 validada e result log finalizado
