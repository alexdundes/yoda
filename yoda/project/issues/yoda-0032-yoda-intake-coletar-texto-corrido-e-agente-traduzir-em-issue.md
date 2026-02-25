---
agent: Human
created_at: '2026-02-25T15:19:59-03:00'
depends_on: []
description: 'No modo YODA Intake, o agente deve pedir ao dev a descrição da issue
  em texto corrido e assumir a responsabilidade de traduzir esse conteúdo para issue
  estruturada e para atualização do markdown da issue. Revisar e ajustar o playbook
  em yoda/yoda.md (seção de Intake). Regra transversal: primeiro atualizar a documentação
  em project/specs/, e somente depois aplicar mudanças em yoda/.'
entrypoints:
- path: yoda/yoda.md
  type: doc
- path: project/specs/
  type: doc
id: yoda-0032
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 3
schema_version: '1.0'
slug: yoda-intake-coletar-texto-corrido-e-agente-traduzir-em-issue
status: to-do
tags:
- release-0.1.2
- intake
- playbook
- docs-first
title: 'YODA Intake: coletar texto corrido e agente traduzir em issue'
updated_at: '2026-02-25T15:19:59-03:00'
---

# yoda-0032 - YODA Intake: coletar texto corrido e agente traduzir em issue
<!-- AGENT: Replace yoda-0032 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and YODA Intake: coletar texto corrido e agente traduzir em issue with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Ajustar o modo YODA Intake para que o agente solicite ao dev a descricao da issue em texto corrido e seja responsavel por traduzir isso para uma issue estruturada. A mesma base textual deve ser usada para preencher/atualizar o markdown da issue. Esta issue tambem segue a regra transversal do ciclo `0.1.2`: atualizar primeiro `project/specs/` e depois `yoda/`.

## Context
Hoje o fluxo de Intake pode induzir o dev a formatar demais o input antes da abertura da issue. O objetivo e reduzir friccao no levantamento e padronizar a responsabilidade do agente em transformar texto livre em estrutura com Definition of Ready.

## Objective
Definir e documentar no playbook que o Intake parte de texto corrido fornecido pelo dev, com estruturacao feita pelo agente ao criar e atualizar a issue.

## Scope
- Atualizar as specs de Intake em `project/specs/` para refletir o novo comportamento.
- Revisar `yoda/yoda.md` na secao de YODA Intake para instruir coleta em texto corrido e traducao estruturada pelo agente.
- Garantir que o procedimento mencione uso dessa traducao ao preencher o markdown da issue.

## Out of scope
- Implementar mudancas de parser/CLI para NLP automatico fora do fluxo atual.
- Redesenhar completo de YODA Flow fora do Intake.
- Alterar regras de priorizacao/reordenacao de TODO que nao dependam desse ajuste.

## Requirements
- Ordem obrigatoria: `project/specs/` antes de `yoda/`.
- O playbook deve instruir o agente a pedir descricao livre ao dev.
- O playbook deve explicitar que o agente converte texto livre em issue estruturada.
- O mesmo conteudo estruturado deve orientar a atualizacao do markdown da issue.

## Acceptance criteria
- [ ] As specs em `project/specs/` descrevem Intake com coleta em texto corrido.
- [ ] `yoda/yoda.md` contem instrucao explicita de traducao do texto corrido para issue estruturada.
- [ ] O fluxo documentado conecta abertura da issue e atualizacao do markdown da issue a partir da mesma base textual.
- [ ] Nao ha contradicao entre specs e manual embutido para o comportamento de Intake.

## Dependencies
None.

## Entry points
- path: project/specs/
  type: doc
- path: yoda/yoda.md
  type: doc

## Implementation notes
A revisao deve focar o playbook de Intake, evitando expandir escopo para outras fases sem necessidade. Preservar linguagem operacional e objetiva para agentes.

## Tests
Revisao documental: validar consistencia textual entre specs e `yoda/yoda.md`. Se houver testes de conformidade documental no repositorio, atualizar conforme necessario.

## Risks and edge cases
- Ambiguidade sobre o nivel de detalhe esperado do texto corrido enviado pelo dev.
- Risco de manter instrucoes antigas em pontos secundarios e gerar conflito de orientacao.
- Excessiva liberdade na traducao pode perder requisitos se os criterios nao estiverem explicitos.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
