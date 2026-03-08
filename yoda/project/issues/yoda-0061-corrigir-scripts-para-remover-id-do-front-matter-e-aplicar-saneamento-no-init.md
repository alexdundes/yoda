---
schema_version: '2.00'
status: done
title: Corrigir scripts para remover id do front matter e aplicar saneamento no init
description: 'Alinhar implementacao ao contrato vigente sem id no front matter: issue_add/todo_update/front_matter
  nao devem persistir id, e init deve detectar/remover id em issues existentes quando
  necessario sem alterar o ID derivado do filename.'
priority: 5
created_at: '2026-03-07T21:09:00-03:00'
updated_at: '2026-03-07T21:20:21-03:00'
---

# yoda-0061 - Corrigir scripts para remover id do front matter e aplicar saneamento no init

## Summary
A documentacao vigente define que o ID canonico e derivado do filename e que o front matter nao deve conter `id`.
Hoje, parte dos scripts ainda persiste `id` no metadata, mantendo inconsistência entre contrato e implementacao.
Esta issue alinha os scripts ao contrato e adiciona saneamento no `init` para remover `id` de issues existentes quando aplicavel.

## Context
Specs e template ja foram convergidos para o modelo sem `id` no front matter.
Entretanto, `issue_add.py` e utilitarios de metadata ainda incluem `id`, e o repositorio possui historico com esse campo.
Sem alinhamento tecnico, o projeto continua gerando artefatos fora do contrato oficialmente adotado.

## Objective
Garantir que scripts nao escrevam mais `id` no front matter e que `init` possa normalizar issues legadas removendo esse campo com seguranca.

## Scope
- Remover persistencia de `id` no front matter em `issue_add.py` e fluxos correlatos de escrita.
- Ajustar normalizacao de metadata para manter ordem canonica sem campo `id`.
- Atualizar `init.py` para detectar/remover `id` legado em issues existentes, preservando demais metadados.
- Manter derivacao de ID exclusivamente via filename na leitura/indexacao.
- Atualizar testes afetados e adicionar cobertura para saneamento no `init`.

## Out of scope
- Renomear arquivos de issue ou alterar regra de derivacao de ID.
- Reestruturar fases do YODA Flow.
- Migracao manual em massa fora do que for executado por `init`.

## Requirements
- Nenhum script deve escrever `id` em front matter de novas issues.
- `init.py` deve remover `id` quando presente e manter arquivo valido/idempotente.
- A ausencia de `id` nao pode afetar selecao, dependencias e transicoes do flow.
- `--dry-run` de comandos relevantes deve permanecer sem escrita.
- A normalizacao de front matter deve ser separada da normalizacao de TODO legado para evitar regressao em `validate_todo`.

## Acceptance criteria
- [x] `issue_add.py` cria issue sem campo `id` no front matter.
- [x] Fluxos de update/rewrite de front matter nao reintroduzem `id`.
- [x] `init.py` remove `id` legado de issue existente e mantem arquivo consistente.
- [x] Suite de testes cobre criacao sem `id`, saneamento no `init` e ausencia de regressao no flow/index.
- [x] Fluxo de compatibilidade com TODO YAML legado continua valido quando aplicavel.

## Entry points
- `yoda/scripts/issue_add.py`
- `yoda/scripts/init.py`
- `yoda/scripts/lib/issue_metadata.py`
- `yoda/scripts/lib/front_matter.py`
- `yoda/scripts/lib/issue_index.py`
- `yoda/scripts/tests`
- `yoda/project/issues/yoda-0061-corrigir-scripts-para-remover-id-do-front-matter-e-aplicar-saneamento-no-init.md`

## Implementation notes
A leitura ja deriva ID do filename; manter essa regra como fonte unica.
Durante saneamento no `init`, aplicar escrita apenas quando houver mudanca real para preservar idempotencia.
Decisao de implementacao aprovada:
- Introduzir caminho de normalizacao especifico para front matter de issue que remove `id`.
- Manter normalizacao de TODO legado separada, preservando `id` onde ainda for exigido por validacao de compatibilidade.

## Tests
Adicionar testes em `test_issue_add.py` e `test_init.py` cobrindo ausencia/remoção de `id`.
Executar regressao em `test_issue_index.py` e `test_yoda_flow_next.py` para confirmar comportamento inalterado com metadados sem `id`.
Adicionar cobertura em `test_todo_update.py` para garantir que update de issue nao reintroduz `id`.

## Risks and edge cases
- Remocao de `id` sem atualizar testes pode gerar falhas de expectativa.
- Reescrita de front matter pode alterar ordem/campos opcionais sem necessidade.
- Issues historicas sem `## Flow log` exigem cuidado no mesmo passo de saneamento.

## Result log
fix(metadata): remover id do front matter e sanear legado via init

Foi implementado um caminho dedicado de normalizacao para front matter de issues sem persistir `id`, mantendo o ID canonico derivado exclusivamente do nome do arquivo. A camada de escrita (`front_matter.py`) passou a usar essa normalizacao, evitando que `issue_add` e `todo_update` reintroduzam `id` em metadados de issue markdown.

No `init.py`, foi adicionado saneamento explicito para remover `id` de issues existentes (`<dev>-*.md`), inclusive em cenarios sem TODO legado. A compatibilidade com fluxo legado de TODO YAML foi preservada ao manter separacao entre normalizacao de front matter e normalizacao de dados de reconcile/migracao.

Foram atualizados testes em `test_issue_add.py`, `test_todo_update.py` e `test_init.py`, incluindo caso dedicado de saneamento sem TODO legado, e executada regressao completa com sucesso (`python3 -m pytest yoda/scripts/tests`: 59 passed).

- **Issue**: `yoda-0061`

- **Path**: `yoda/project/issues/yoda-0061-corrigir-scripts-para-remover-id-do-front-matter-e-aplicar-saneamento-no-init.md`

## Flow log
- 2026-03-07T21:09:00-03:00 issue_add created title=Corrigir scripts para remover id do front matter e aplicar saneamento no init; priority=5
- 2026-03-07T21:10:08-03:00 transition to-do->doing/study
- 2026-03-07T21:12:33-03:00 transition doing/study->doing/document | Study aprovado: separar normalizacao de front matter sem id e preservar compatibilidade do TODO legado
- 2026-03-07T21:15:27-03:00 transition doing/document->doing/implement | Document aprovado: implementar escrita de front matter sem id com compatibilidade de TODO legado preservada
- 2026-03-07T21:19:47-03:00 transition doing/implement->doing/evaluate | Implement concluido: scripts sem id no front matter, saneamento no init e suite 59/59
- 2026-03-07T21:20:21-03:00 transition doing/evaluate->done | Evaluate aprovado: ACs e result log validados para encerramento
- 2026-03-07T21:35:33-03:00 flow-log format check
