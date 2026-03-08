---
schema_version: '2.00'
status: done
depends_on:
- yoda-0051
title: Atualizar playbook yoda md e deprecacoes operacionais
description: Reescrever yoda/yoda.md para o novo fluxo guiado por runbooks compactos
  e definir deprecacoes de scripts antigos no modo de compatibilidade.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:42-03:00'
updated_at: '2026-03-06T21:03:24-03:00'
---

# yoda-0053 - Atualizar playbook yoda md e deprecacoes operacionais

## Summary
Atualizar o manual operacional para refletir o novo YODA Flow orientado por runbooks compactos de script. Definir deprecacoes explicitas de comandos legados no fluxo padrao.

## Context
O playbook atual descreve passos manuais que nao representam o alvo 0.3.0 e aumentam chance de erro do agente.

## Objective
Garantir que a documentacao operacional esteja alinhada ao comportamento real dos scripts 0.3.0.

## Scope
- Revisar secao de YODA Flow em `yoda/yoda.md`.
- Definir novo fluxo com `yoda_flow_next.py` como entrada deterministica de fase.
- Remover `log_add.py` do caminho padrao de execucao (manter como script auxiliar fora do flow).
- Registrar politica de compatibilidade/deprecacao de scripts antigos.
- Atualizar orientacao para tratar dependencias apenas via `depends_on` no front matter (sem secao `## Dependencies` no corpo).
- Atualizar caminhos oficiais para modelo markdown-only (`yoda/project/issues/*.md`) e schema `2.00`.

## Out of scope
- Implementacao tecnica dos scripts.
- Migracao de dados.
- Mudancas de escopo fora de operacao do fluxo.

## Requirements
- Instrucoes devem ser curtas e sem ambiguidade.
- Deve existir orientacao clara sobre quando usar comandos legados/deprecados.
- Playbook deve manter alinhamento com specs e scripts vigentes.
- YODA Flow deve orientar uso de `yoda_flow_next.py --dev <slug>` como comando principal por fase.
- Playbook deve explicitar que `TODO.<dev>.yaml` e `yoda/logs/*.yaml` sao legados removidos apos migracao.
- Deve incluir formato oficial do `Result log` alinhado ao runbook de Evaluate.
- `yoda/yoda.md` deve focar apenas no estado operacional atual e nao deve conter conteudo de migracao nem versionamento.

## Acceptance criteria
- [x] `yoda/yoda.md` descreve o fluxo 0.3.0 com runbooks compactos.
- [x] `log_add.py` nao aparece como passo obrigatorio do fluxo padrao.
- [x] Secao de deprecacao/compatibilidade esta explicita.
- [x] O playbook nao orienta uso de secao `## Dependencies` no corpo e referencia apenas `depends_on`.
- [x] O playbook remove referencias a `TODO.<dev>.yaml` e `yoda/logs/*.yaml` como fonte ativa.
- [x] Entrada de YODA Flow no playbook usa `yoda_flow_next.py` como comando deterministico principal.
- [x] O texto final de `yoda/yoda.md` e estritamente operacional (estado atual), sem topicos de migracao ou historico de versao.


## Entry points
- `yoda/yoda.md`
- `project/specs`
- `yoda/scripts/yoda_flow_next.py`

## Implementation notes
Documentar apenas estado atual de operacao: entrada, modos, fases e comandos vigentes. Evitar texto historico (migracao/versionamento) no `yoda/yoda.md`.

## Tests
Revisao de consistencia documental e verificacao cruzada com:
- saida atual de `yoda_flow_next.py`;
- contratos de `todo_update.py` e `log_add.py` como scripts permanentes auxiliares;
- ausencia de instrucoes legadas conflitantes no `yoda/yoda.md`.

## Risks and edge cases
- Divergencia entre doc e codigo gera regressao operacional.
- Deprecacao sem janela clara pode quebrar fluxos de quem nao migrou.

## Result log
docs(playbook): reescrever yoda.md para fluxo operacional atual de intake e flow

Foi reescrito o `yoda/yoda.md` com foco estritamente operacional no estado atual: entrada e politicas de YODA Intake e YODA Flow, comando principal `yoda_flow_next.py` para execucao por fase, formato oficial de `Result log` e mapa de autoridade dos scripts. O caminho padrao deixou de exigir `log_add.py`, mantendo-o como auxiliar fora do fluxo automatico, e foi incluida nota explicita de compatibilidade operacional sem conteudo de migracao/versionamento.

- **GitHub Issue** :   #3

- **Issue**: `yoda-0053`

- **Path**: `yoda/project/issues/yoda-0053-atualizar-playbook-yoda-md-e-deprecacoes-operacionais.md`

## Flow log
- 2026-03-04T20:33:42-03:00 issue_add created | title: Atualizar playbook yoda md e deprecacoes operacionais | description: Reescrever yoda/yoda.md para o novo fluxo guiado por runbooks compactos e definir deprecacoes de scripts antigos no modo de compatibilidade. | slug: atualizar-playbook-yoda-md-e-deprecacoes-operacionais | extern_issue_file: external issue linked
- 2026-03-04T20:34:08-03:00 todo_update | depends_on: -> yoda-0051
- 2026-03-06T19:02:01-03:00 todo_update status: to-do -> doing
- 2026-03-06T19:02:06-03:00 Study iniciado; playbook atual lido e divergencias 0.3.0 mapeadas (TODO/log YAML, fluxo manual antigo e deprecacoes).
- 2026-03-06T19:09:33-03:00 Document concluido com contrato 0.3.0 para playbook (flow via yoda_flow_next, markdown-only schema 2.00 e deprecacoes explicitas).
- 2026-03-06T19:13:34-03:00 diretriz confirmada no Document: yoda.md sera somente operacional do estado atual, sem migracao/versionamento.
- 2026-03-06T20:54:51-03:00 Implement concluido com reescrita operacional do yoda.md para Intake/Flow atuais, sem migracao/versionamento, e testes 51 passed.
- 2026-03-06T21:03:24-03:00 Evaluate concluido com ACs validados, yoda.md final operacional e testes 51 passed.
- 2026-03-06T21:03:24-03:00 todo_update status: doing -> done
