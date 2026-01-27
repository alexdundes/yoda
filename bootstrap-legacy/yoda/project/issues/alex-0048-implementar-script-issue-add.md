---
schema_version: "1.0"
id: alex-0048
title: Implementar script de inclusao de issue (issue_add.py)
slug: implementar-script-issue-add
description: Implementar o issue_add.py conforme a spec project/specs/18-issue-add-script.md.
status: done
priority: 3
lightweight: false
agent: Human
depends_on: [alex-0037]
pending_reason: ""
created_at: "2026-01-27T07:07:49-03:00"
updated_at: "2026-01-27T08:11:10-03:00"
entrypoints: []
tags: [scripts, issue, python]
origin:
  system: "user"
  external_id: ""
  requester: "alexdundes"
---

# alex-0048 - Implementar script de inclusao de issue (issue_add.py)

## Summary
Implementar o `issue_add.py` seguindo a spec definida em `project/specs/18-issue-add-script.md`.

## Context
A especificacao do `issue_add.py` sera criada em `project/specs/18-issue-add-script.md`. Esta issue cobre apenas a implementacao baseada naquela spec.

## Objective
Entregar o script `yoda/scripts/issue_add.py` conforme a spec, com validacao e saidas padronizadas.

## Scope
- Implementar o script `yoda/scripts/issue_add.py` conforme a spec.
- Garantir que o script atualize o TODO e gere o arquivo de issue a partir do template.
- Manter compatibilidade com a estrutura definida em `project/specs/15-scripts-python-structure.md`.

## Out of scope
- Alterar a spec do `issue_add.py`.
- Implementar outros scripts v1.

## Requirements
- Implementacao deve seguir `project/specs/18-issue-add-script.md` sem divergencias.
- Validacao deve bloquear escrita em caso de erro.
- Suporte a `--dev`, `--dry-run`, `--format` e codigos de saida conforme spec.

## Acceptance criteria
- [x] `yoda/scripts/issue_add.py` existe e segue a spec `project/specs/18-issue-add-script.md`.
- [x] O script gera `yoda/project/issues/<id>-<slug>.md` a partir do template.
- [x] O script atualiza o TODO correto e respeita `--dry-run`.
- [x] Validacao embutida impede escrita em caso de erro.

## Dependencies
- alex-0037

## Entry points
- path: project/specs/18-issue-add-script.md
  type: doc
- path: project/specs/13-yoda-scripts-v1.md
  type: doc
- path: project/specs/05-scripts-and-automation.md
  type: doc
- path: project/specs/15-scripts-python-structure.md
  type: doc
- path: yoda/templates/issue.md
  type: doc
- path: yoda/scripts/README.md
  type: doc

## Implementation notes
- Seguir o layout de pacotes e padroes de saida descritos em `project/specs/15-scripts-python-structure.md`.

## Tests
Not applicable.

## Risks and edge cases
- Divergencias com a spec podem quebrar a compatibilidade dos scripts v1.
- Conflitos de arquivo/slug devem ser tratados conforme a spec.

## Result log
Implementado `yoda/scripts/issue_add.py` com estrutura base em `yoda/scripts/lib/` e suporte a criacao de TODO, issues e logs conforme a spec.

feat(yoda): implementar issue_add.py

Issue: alex-0048
Path: `yoda/project/issues/alex-0048-implementar-script-issue-add.md`
