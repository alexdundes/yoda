---
schema_version: "1.0"
id: alex-0039
title: Ajustar padrao de logs no repo.intent.yaml
slug: ajustar-padrao-logs-repo-intent-yaml
description: Alinhar target.logs.pattern para yoda/logs/<id>-<slug>.yaml, removendo duplicacao de dev no nome.
status: done
priority: 6
lightweight: false
agent: Codex
depends_on: []
pending_reason: ""
created_at: "2026-01-26T20:51:10-03:00"
updated_at: "2026-01-26T20:51:55-03:00"
entrypoints:
  - path: repo.intent.yaml
    type: doc
  - path: project/specs/05-scripts-and-automation.md
    type: doc
  - path: project/specs/17-scripts-python-structure.md
    type: doc
  - path: project/specs/summary.md
    type: doc
tags: []
origin:
  system: ""
  external_id: ""
  requester: ""
---

# alex-0039 - Ajustar padrao de logs no repo.intent.yaml

## Summary
Corrigir o padrao de logs no repo.intent.yaml para remover a duplicacao do dev no nome do arquivo. O target deve refletir o contrato canonico dos specs: um log por issue em yoda/logs/<id>-<slug>.yaml.

## Context
O repo.intent.yaml define o estado atual (bootstrap) e o alvo do framework. Hoje, target.logs.pattern inclui <dev>-<id>-<slug>.yaml, o que conflita com os specs que estabelecem <id>-<slug>.yaml como nome canonico de logs.

## Objective
Alinhar o target.logs.pattern com o formato canonico dos logs definido nas specs.

## Scope
- Atualizar target.logs.pattern no repo.intent.yaml para yoda/logs/<id>-<slug>.yaml.
- Confirmar alinhamento com os specs que descrevem logs canonicos.

## Out of scope
- Alterar specs de logs ou outros paths no repo.intent.yaml.
- Mudar convencoes de logs no bootstrap.

## Requirements
- Substituir target.logs.pattern para remover o prefixo <dev>-.
- Manter consistencia com os docs existentes em project/specs.

## Acceptance criteria
- [ ] repo.intent.yaml usa yoda/logs/<id>-<slug>.yaml em target.logs.pattern.
- [ ] Nao ha divergencia entre repo.intent.yaml e os specs sobre o nome do log canonico.

## Dependencies
None.

## Entry points
- path: repo.intent.yaml
  type: doc
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: project/specs/17-scripts-python-structure.md
  type: doc
- path: project/specs/summary.md
  type: doc

## Implementation notes
- O bootstrap permanece com logs Markdown em yoda/logs/<id>-<slug>.md; apenas o target YAML deve ser ajustado.

## Tests
Not applicable.

## Risks and edge cases
- Nenhum risco tecnico; cuidado para nao alterar outras chaves do repo.intent.yaml.

## Result log
Atualizado repo.intent.yaml para usar o padrao canonico de logs sem o prefixo <dev>, alinhando com os specs do framework.

chore: ajustar padrao de logs no repo.intent.yaml

Issue: `alex-0039`
Path: `yoda/project/issues/alex-0039-ajustar-padrao-logs-repo-intent-yaml.md`
