---
created_at: '2026-01-28T19:02:03-03:00'
depends_on: []
description: Especificar no project/specs como o YODA será empacotado/embutido, o
  que entra e sai do artefato, comandos de build/init e alinhamento com meta-implementação.
id: yoda-0016
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 10
schema_version: '1.01'
slug: specs-empacotamento-e-distribui-o-do-yoda-framework
status: done
title: 'Specs: empacotamento e distribuição do YODA Framework'
updated_at: '2026-02-25T20:02:28-03:00'
---

# yoda-0016 - Specs: empacotamento e distribuição do YODA Framework
<!-- AGENT: Replace yoda-0016 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Specs: empacotamento e distribuição do YODA Framework with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Clarificar no `project/specs` como o YODA Framework será empacotado e embutido em outros projetos, definindo o que entra/sai do artefato, layout, versionamento e comandos de build/init. As specs atuais focam na meta-implementação e não guiam a distribuição prática, gerando confusão.

## Context
`project/specs` é a fonte de verdade da meta-implementação, mas não documenta o artefato instalável. O pacote final deve conter apenas o necessário da pasta `yoda/`, excluindo `project/specs`, porém falta norma sobre conteúdo, formato e relação com comandos futuros (`package`, `init`). Sem essa diretriz, há risco de pacote inconsistente e dependência tácita de materiais verbosos.

## Objective
Produzir uma ou mais specs em `project/specs/` que normatizem o empacotamento e distribuição do YODA Framework, descrevendo artefato, inclusões/exclusões, formato, versionamento, compatibilidade e como os comandos de build/init se apoiam nessas regras.

## Scope
- Definir seção ou arquivo(s) em `project/specs` para "Distribuição/Empacote".
- Especificar lista de inclusão/exclusão do artefato (ex.: apenas `yoda/` necessário; excluir `project/specs` e materiais de bootstrap).
- Definir layout do pacote (estrutura de pastas, nomes, versão no filename).
- Documentar requisitos de versionamento/compatibilidade (semver ou similar) e como identificar build (checksum opcional).
- Descrever interface esperada dos comandos de empacote e init (entradas/saídas, flags essenciais) sem implementá-los.
- Atualizar referências cruzadas em `project/specs/summary.md` ou outros capítulos para refletir o novo fluxo.

## Out of scope
- Implementar os comandos de empacote ou init.
- Alterar código em `yoda/` ou scripts existentes.
- Decidir detalhes de UX ou CLI final além do que for necessário para especificação.

## Requirements
- Criar documento(s) em `project/specs/` com seções claras: artefato, inclusões, exclusões, layout, versionamento, interface de comandos.
- Referenciar explicitamente que `project/specs` não vai no pacote e justificar.
- Definir como futuras atualizações do pacote devem tratar compatibilidade (ex.: breaking vs minor).
- Registrar premissas de build (ferramentas permitidas, ambiente mínimo) e de consumo (projeto host).
- Incluir contrato de changelog estruturado (`yoda/CHANGELOG.yaml`) e validação pelo comando `package`.
- Atualizar sumário/índice das specs para incluir o novo material.

## Acceptance criteria
- [x] Novas specs adicionadas em `project/specs/` descrevem artefato, inclusões/exclusões e layout do pacote.
- [x] Seções de versionamento/compatibilidade e interface mínima dos comandos de empacote/init estão documentadas.
- [x] Manifesto do pacote e contrato de changelog estruturado são descritos (incluindo validação pelo `package`).
- [x] `project/specs/summary.md` (ou equivalente) referencia o novo conteúdo.
- [x] Nenhuma dependência obrigatória de `project/specs` permanece no pacote final (apontada explicitamente na spec).

## Dependencies
None.

## Entry points
- path: project/specs/summary.md
  type: doc
- path: project/specs/23-distribution-and-packaging.md
  type: doc
- path: project/specs/02-yoda-flow-process.md
  type: doc
- path: project/specs/06-agent-playbook.md
  type: doc
- path: yoda/yoda.md
  type: doc

## Implementation notes
- Manter linguagem concisa (orientada a agentes), mas dentro do padrão das specs atuais.
- Explicitar relação entre meta-implementação (repo atual) e artefato distribuível.
- Considerar futura automação de build/init para garantir que os campos de interface sejam factíveis.
- Desdobrar follow-ups para LICENSE e README curtos do pacote (issues separadas).

## Tests
- Not applicable (documentação); revisar formatação/lint se houver.

## Risks and edge cases
- Ambiguidade entre o que é "artefato final" e "workspace de desenvolvimento".
- Divergência futura entre specs e implementação se escopo de exclusões não for preciso.
- Necessidade de compatibilidade retroativa pode exigir ajustes adicionais no layout.

## Result log
- Added `project/specs/23-distribution-and-packaging.md` with contrato de artefato (tar.gz), manifesto, changelog estruturado e regras de compatibilidade/upgrade.
- Atualizado `project/specs/summary.md` para referenciar a nova decisão.

Commit suggestion:
```
docs: define distribution and packaging contract

Issue: yoda-0016
Path: project/specs/23-distribution-and-packaging.md
```