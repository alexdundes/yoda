---
agent: Human
created_at: '2026-01-28T19:02:06-03:00'
depends_on:
- yoda-0016
description: Produzir manual mínimo para agentes (YODA Flow e Intake) que funcione
  sem project/specs, com playbooks claros e referências às ferramentas/scripts.
entrypoints: []
id: yoda-0017
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 9
schema_version: '1.0'
slug: manual-embarcado-reescrever-yoda-yoda-md-independente-das-specs
status: to-do
tags: []
title: 'Manual embarcado: reescrever yoda/yoda.md independente das specs'
updated_at: '2026-01-28T19:05:16-03:00'
---

# yoda-0017 - Manual embarcado: reescrever yoda/yoda.md independente das specs
<!-- AGENT: Replace yoda-0017 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Manual embarcado: reescrever yoda/yoda.md independente das specs with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Reescrever o manual do YODA (`yoda/yoda.md`, podendo dividir em arquivos) para que agentes executem YODA Flow e YODA Intake sem depender de `project/specs`. O conteúdo deve ser enxuto, com playbooks claros, comandos e caminhos práticos para entrada, fluxo e encerramento.

## Context
`yoda/yoda.md` atual referencia `project/specs` como fonte de verdade e presume o repositório de meta-implementação. No pacote embarcado, `project/specs` não estará presente; sem manual autossuficiente, agentes ficarão sem orientação mínima.

## Objective
Produzir manual embarcado que cubra entrada, fluxos (Flow/Intake), scripts `todo_*`, `issue_add`, `log_add`, deliverables e regras de lightweight, usando apenas recursos inclusos no pacote.

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
- [ ] `yoda/yoda.md` (ou conjunto equivalente) funciona sem consultar `project/specs`.
- [ ] Playbooks de YODA Flow e Intake estão descritos com passos acionáveis e exemplos de frases.
- [ ] Uso dos scripts `todo_*`, `issue_add.py`, `log_add.py` está documentado com caminhos corretos.
- [ ] Referências a `project/specs` não são necessárias para operar o framework embarcado.
- [ ] Links internos/âncoras funcionam após empacote.

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
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->