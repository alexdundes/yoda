---
schema_version: '2.00'
id: yoda-0060
status: to-do
title: Convergencia 0.3.1 de contrato entre specs, scripts e docs
description: 'Executar uma rodada curta de convergencia final pos-0.3.0: validar e
  alinhar contratos de issue markdown, Flow log, Entry points e documentos estruturais
  (README, REPO_INTENT, repo.intent.yaml e specs centrais) para eliminar drift residual.'
priority: 5
created_at: '2026-03-07T20:36:29-03:00'
updated_at: '2026-03-07T20:36:29-03:00'
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
- Definir tratamento para `yoda/project/issues/other-0001-beta.md` (fixture, legado ou backlog oficial).

## Out of scope
- Migracao em massa de todas as issues antigas nesta mesma entrega.
- Reescrita ampla de arquitetura ou criacao de novos comandos.
- Mudancas de release/packaging fora do que for necessario para consistencia documental.

## Requirements
- Cada contrato potencialmente ambiguo deve ficar com uma unica regra oficial documentada.
- A documentacao revisada deve indicar com clareza itens de compatibilidade e itens de legado.
- Quando houver divergencia nao resolvida nesta issue, abrir follow-up explicito no backlog.
- Registrar no corpo da issue as premissas adotadas por nao haver fonte externa vinculada.

## Acceptance criteria
- [ ] `project/specs/07-agent-entry-and-root-file.md`, `11-yoda-intake.md`, `16-todo-list-script.md` e `18-issue-add-script.md` estao consistentes com o contrato vigente.
- [ ] `README.md`, `REPO_INTENT.md` e `repo.intent.yaml` deixam explicito o papel de canonico/compatibilidade/legado.
- [ ] Existe decisao registrada para `other-0001-beta.md` com impacto documentado.
- [ ] Qualquer gap remanescente foi convertido em issue(s) de follow-up com rastreabilidade clara.

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
- `yoda/project/issues/yoda-0060-convergencia-0-3-1-de-contrato-entre-specs-scripts-e-docs.md`

## Implementation notes
Executar em ordem document-first: decidir contrato, atualizar docs estruturais, depois ajustar backlog/follow-ups.
Evitar apagar contexto historico: preferir marcar legado explicitamente quando a remocao nao trouxer ganho objetivo.

## Tests
Nao aplicavel para testes automatizados de codigo.
Validar por varredura manual orientada (grep/checklist) para confirmar que nao ha instrucoes conflitantes entre arquivos de entrada e specs centrais.

## Risks and edge cases
- Tratar conclusoes de revisao externa como fato sem revalidacao local.
- Ajustar docs sem refletir comportamento real de scripts.
- Criar texto muito generico e manter ambiguidades operacionais.

## Result log

## Flow log
2026-03-07T20:36:29-03:00 issue_add created title=Convergencia 0.3.1 de contrato entre specs, scripts e docs; priority=5
