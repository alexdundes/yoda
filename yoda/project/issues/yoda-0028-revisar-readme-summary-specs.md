---
agent: Human
created_at: '2026-01-27T13:32:13-03:00'
depends_on: []
description: Revisar o `README.md` e o `project/specs/summary.md` para garantir que
  ambos reflitam a especificacao atual presente em `project/specs`. A tarefa inclui
  remover pendencias obsoletas e ajustar o resumo para refletir decisoes ja formalizadas.
entrypoints: []
id: yoda-0028
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 6
schema_version: '1.0'
slug: revisar-readme-summary-specs
status: done
tags: []
title: Revisar README e summary com specs atuais
updated_at: '2026-01-27T13:32:39-03:00'
---

# yoda-0028 - Revisar README e summary com specs atuais

## Summary
Revisar o `README.md` e o `project/specs/summary.md` para garantir que ambos reflitam a especificacao atual presente em `project/specs`. A tarefa inclui remover pendencias obsoletas e ajustar o resumo para refletir decisoes ja formalizadas.

## Context
O README ainda menciona pendencias ja resolvidas nas issues, enquanto a documentacao em `project/specs` indica que essas implementacoes estao concluidas. O `project/specs/summary.md` pode ter ficado dessincronizado com a documentacao principal, causando divergencias entre os documentos.

## Objective
Manter `README.md` e `project/specs/summary.md` sincronizados com as especificacoes de `project/specs`, removendo itens que nao estao mais em aberto.

## Scope
- Revisar o conteudo de `README.md` frente a `project/specs`.
- Revisar o conteudo de `project/specs/summary.md` frente a `project/specs`.
- Atualizar ambos os documentos para refletir o estado atual das especificacoes.
- Manter o `README.md` em portugues durante o bootstrap.

## Out of scope
- Alterar o conteudo de `project/specs`.
- Implementar mudancas no codigo ou em `yoda/`.

## Requirements
- Remover ou ajustar pendencias do README que ja foram resolvidas.
- Garantir que o summary seja consistente com as especificacoes atuais.
- Registrar referencias claras para as secoes ajustadas, quando necessario.
- Ajustar o README para indicar que as decisoes ja estao especificadas (nao mais em aberto).

## Acceptance criteria
- [x] `README.md` reflete o estado atual das especificacoes em `project/specs`.
- [x] `project/specs/summary.md` reflete o estado atual das especificacoes em `project/specs`.
- [x] Nenhuma pendencia desatualizada permanece nos documentos revisados.
- [x] README permanece em portugues durante o bootstrap.

## Dependencies
None

## Entry points
- path: README.md
  type: other
- path: project/specs/summary.md
  type: other
- path: project/specs
  type: other

## Implementation notes
- Use `project/specs` como fonte da verdade e alinhe o texto sem alterar as especificacoes.

## Tests
Not applicable.

## Risks and edge cases
- Divergencias sutis entre resumo e especificacao principal podem passar despercebidas.
- Alteracoes no README podem omitir referencias a pendencias que ainda existam.

## Result log
README e summary sincronizados com as specs atuais. Removidas pendencias obsoletas do README e registrado o estado atual no summary, incluindo bootstrap e front matter.

docs(yoda): alinhar README e summary com specs atuais

Issue: `yoda-0028`
Path: `yoda/project/issues/yoda-0028-revisar-readme-summary-specs.md`