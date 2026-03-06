---
schema_version: '2.00'
id: yoda-0053
status: to-do
depends_on:
- yoda-0051
title: Atualizar playbook yoda md e deprecacoes operacionais
description: Reescrever yoda/yoda.md para o novo fluxo guiado por runbooks compactos
  e definir deprecacoes de scripts antigos no modo de compatibilidade.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:33:42-03:00'
updated_at: '2026-03-04T20:34:08-03:00'
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
- Definir novo fluxo com `yoda_flow_next.py` e transicoes guiadas.
- Remover `log_add.py` do caminho padrao de execucao.
- Registrar politica de compatibilidade/deprecacao de scripts antigos.
- Atualizar orientacao para tratar dependencias apenas via `depends_on` no front matter (sem secao `## Dependencies` no corpo).

## Out of scope
- Implementacao tecnica dos scripts.
- Migracao de dados.
- Mudancas de escopo fora de operacao do fluxo.

## Requirements
- Instrucoes devem ser curtas e sem ambiguidade.
- Deve existir orientacao clara sobre quando usar comandos legados.
- Playbook deve manter alinhamento com specs e scripts vigentes.

## Acceptance criteria
- [ ] `yoda/yoda.md` descreve o fluxo 0.3.0 com runbooks compactos.
- [ ] `log_add.py` nao aparece como passo obrigatorio do fluxo padrao.
- [ ] Secao de deprecacao/compatibilidade esta explicita.
- [ ] O playbook nao orienta uso de secao `## Dependencies` no corpo e referencia apenas `depends_on`.

## Dependencies
Depende de `yoda-0051`.

## Entry points
- path: yoda/yoda.md
  type: doc
- path: project/specs
  type: doc
- path: yoda/scripts/yoda_flow_next.py
  type: code

## Implementation notes
Executar apenas apos comportamento de script estar estavel para evitar churn documental.

## Tests
Revisao de consistencia documental e verificacao cruzada com runbooks emitidos por script.

## Risks and edge cases
- Divergencia entre doc e codigo gera regressao operacional.
- Deprecacao sem janela clara pode quebrar fluxos de quem nao migrou.

## Result log

## Flow log
2026-03-04T20:33:42-03:00 | [yoda-0053] issue_add created | title: Atualizar playbook yoda md e deprecacoes operacionais | description: Reescrever yoda/yoda.md para o novo fluxo guiado por runbooks compactos e definir deprecacoes de scripts antigos no modo de compatibilidade. | slug: atualizar-playbook-yoda-md-e-deprecacoes-operacionais | extern_issue_file: external issue linked
2026-03-04T20:34:08-03:00 | [yoda-0053] todo_update | depends_on:  -> yoda-0051
