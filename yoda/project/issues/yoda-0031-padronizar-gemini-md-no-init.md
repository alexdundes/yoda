---
agent: Human
created_at: '2026-02-25T15:18:57-03:00'
depends_on: []
description: 'Ajustar o script yoda/scripts/init.py para criar/referenciar o arquivo
  GEMINI.md em caixa alta, substituindo a variação gemini.md. Regra transversal deste
  backlog: primeiro atualizar a documentação em project/specs/, e somente depois aplicar
  mudanças em yoda/. Neste item, não considerar compatibilidade com legado; o único
  consumidor atual é ../fibu.'
entrypoints:
- path: yoda/scripts/init.py
  type: code
- path: project/specs/
  type: doc
id: yoda-0031
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 3
schema_version: '1.0'
slug: padronizar-gemini-md-no-init
status: done
tags:
- release-0.1.2
- init
- docs-first
title: Padronizar GEMINI.md no init
updated_at: '2026-02-25T18:39:01-03:00'
---

# yoda-0031 - Padronizar GEMINI.md no init
<!-- AGENT: Replace yoda-0031 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Padronizar GEMINI.md no init with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Padronizar o nome do arquivo `GEMINI.md` em caixa alta no fluxo de init do YODA. O ajuste deve remover o uso de `gemini.md` no script de inicializacao e manter o comportamento idempotente. Esta issue segue a regra transversal do ciclo `0.1.2`: atualizar primeiro `project/specs/` e apenas depois `yoda/`.

## Context
Foi identificado em uso real (`../fibu`) que a variacao de caixa no nome do arquivo gera inconsistencia e friccao operacional. Como o YODA esta sendo usado atualmente apenas nesse contexto, nao ha necessidade de compatibilidade com legado para este ponto.

## Objective
Garantir que o init do YODA trate `GEMINI.md` como nome canonico, sem referencias ativas a `gemini.md`.

## Scope
- Atualizar a especificacao em `project/specs/` para definir `GEMINI.md` como padrao.
- Atualizar `yoda/scripts/init.py` para criar/referenciar `GEMINI.md`.
- Ajustar documentacao diretamente relacionada ao comportamento do init, se necessario.

## Out of scope
- Implementar migracao automatica de projetos antigos com `gemini.md`.
- Fazer hardening amplo de compatibilidade retroativa para este tema.
- Outras refatoracoes nao relacionadas ao nome do arquivo.

## Requirements
- A ordem de trabalho deve ser: `project/specs/` primeiro, `yoda/` depois.
- O init deve usar apenas `GEMINI.md` como alvo canonico.
- O comportamento deve continuar idempotente em execucoes repetidas.

## Acceptance criteria
- [x] Existe definicao explicita em `project/specs/` do uso de `GEMINI.md`.
- [x] `yoda/scripts/init.py` nao depende de `gemini.md` para o caminho principal.
- [x] Uma execucao de init em projeto limpo gera/referencia `GEMINI.md`.
- [x] Execucoes repetidas nao criam efeitos colaterais indevidos.

## Dependencies
None.

## Entry points
- path: project/specs/
  type: doc
- path: yoda/scripts/init.py
  type: code

## Implementation notes
Decisao explicita deste backlog: nao priorizar legado nesse item. Validar impacto apenas no fluxo atual usado por `../fibu`.

## Tests
Validar init em cenario limpo e em reexecucao para confirmar idempotencia. Atualizar/adicionar testes automatizados apenas se houver cobertura para `init.py` no repositorio.

## Risks and edge cases
- Ambiente com filesystem case-insensitive pode mascarar erros de padronizacao.
- Documentacao e implementacao podem divergir se a ordem docs-first nao for respeitada.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
Padronizacao aplicada para `GEMINI.md` no fluxo de init: specs atualizadas para nome canonico, `yoda/scripts/init.py` ajustado para gerar/referenciar `GEMINI.md`, e arquivo do repositorio renomeado no Git para manter consistencia de case. Validacao de idempotencia executada em diretorio temporario com dois runs consecutivos.

fix(init): padronizar GEMINI.md como arquivo canonico de entrada
Issue: `yoda-0031`
Path: `yoda/project/issues/yoda-0031-padronizar-gemini-md-no-init.md`