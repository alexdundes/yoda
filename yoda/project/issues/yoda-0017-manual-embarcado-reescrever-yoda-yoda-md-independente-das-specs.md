---
created_at: '2026-01-28T19:02:06-03:00'
depends_on:
- yoda-0016
description: Produzir manual mínimo para agentes (YODA Flow e Intake) que funcione
  sem project/specs, com playbooks claros e referências às ferramentas/scripts.
id: yoda-0017
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 9
schema_version: '1.01'
slug: manual-embarcado-reescrever-yoda-yoda-md-independente-das-specs
status: done
title: 'Manual embarcado: reescrever yoda/yoda.md independente das specs'
updated_at: '2026-02-25T20:02:28-03:00'
---

# yoda-0017 - Manual embarcado: reescrever yoda/yoda.md independente das specs
<!-- AGENT: Replace yoda-0017 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Manual embarcado: reescrever yoda/yoda.md independente das specs with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Rewrite the YODA manual (`yoda/yoda.md`) so agents can run YODA Flow and YODA Intake without relying on `project/specs`. Deliver a concise, standalone playbook with practical steps, commands, and paths for entry, execution, and exit.

## Context
The previous `yoda/yoda.md` pointed to `project/specs`, which will not ship in the embedded package. Agents need a self-contained manual inside `yoda/` to operate both cycles with only the packaged assets.

## Objective
Provide an English, single-file manual covering Flow/Intake entry phrases, developer slug resolution, playbooks (Study/Document/Implement/Evaluate, lightweight), blocking handling, script usage, paths, and handoff—using only packaged resources.

## Scope
- Reestruturar `yoda/yoda.md` (ou dividir em poucos arquivos sob `yoda/`) para ser standalone.
- Descrever triggers e passos de YODA Flow e YODA Intake, incluindo frases de entrada/saída e validações (issue doing, dependências).
- Documentar uso dos scripts (`todo_list/next/update/reorder`, `issue_add`, `log_add`) e caminhos relevantes (`yoda/todos`, `yoda/logs`, `yoda/project/issues`).
- Cobrir regras de lightweight, deliverables por fase e tratamento de bloqueios/pending.
- Ajustar referências internas para não exigir leitura de `project/specs`.

## Out of scope
- Implementar ou alterar scripts de empacote/init.
- Atualizar `project/specs` (coberto por yoda-0016).
- Definir formato final do pacote (coberto por yoda-0016/0018).

## Requirements
- Manual deve ser legível em isolamento (sem `project/specs`).
- Exemplos de entrada no fluxo e mensagens de confirmação traduzidas ao idioma do usuário.
- Seções concisas para: resolução de dev, seleção de issue, ciclos (Study/Document/Implement/Evaluate), Intake, lightweight, bloqueios e logging.
- Referenciar apenas arquivos/pastas que estarão no artefato empacotado.
- Se subdividido, incluir índice claro e links relativos funcionais.

## Acceptance criteria
- [x] `yoda/yoda.md` (single-file) works without consulting `project/specs`.
- [x] YODA Flow and Intake playbooks are described with actionable steps and example phrasing.
- [x] Usage of scripts (`todo_*`, `issue_add.py`, `log_add.py`) is documented with correct paths.
- [x] No `project/specs` references are required to operate the embedded framework.
- [x] Internal links/anchors function after packaging.

## Dependencies
Depends on: yoda-0016.

## Entry points
- path: yoda/yoda.md
  type: doc
- path: project/specs/02-yoda-flow-process.md
  type: doc
- path: project/specs/11-yoda-intake.md
  type: doc
- path: project/specs/06-agent-playbook.md
  type: doc

## Implementation notes
- Manter linguagem concisa e operacional, com foco em ações e comandos.
- Considerar dividir em seções: Entrada, Flow, Intake, Scripts, Deliverables, Glossário rápido.
- Garantir que instruções reflitam o layout que será empacotado (ver yoda-0016).

## Tests
- Not applicable (documentação); validar links e lint se disponível.

## Risks and edge cases
- Duplicar lógica das specs e gerar divergência futura.
- Manual ficar grande demais e perder clareza.
- Mudanças posteriores nos scripts quebrarem referências se não forem mantidas.

## Result log
- Rewrote `yoda/yoda.md` as a standalone, English manual with Flow/Intake playbooks, slug resolution, scripts quick reference, file map, and handoff steps; removed dependency on `project/specs`.

Commit suggestion:
```
docs: rewrite embedded yoda manual

Issue: yoda-0017
Path: yoda/yoda.md
```