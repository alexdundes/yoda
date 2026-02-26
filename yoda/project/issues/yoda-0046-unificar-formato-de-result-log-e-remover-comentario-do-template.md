---
created_at: '2026-02-26T19:27:28-03:00'
depends_on: []
description: Remover comentario instrucional do Result log no template e alinhar o
  formato do Evaluate no yoda/yoda.md, com linha de issue externa condicional quando
  houver vinculo.
id: yoda-0046
origin:
  external_id: '2'
  requester: ''
  system: github
pending_reason: ''
priority: 5
schema_version: '1.01'
slug: unificar-formato-de-result-log-e-remover-comentario-do-template
status: to-do
title: Unificar formato de Result log e remover comentario do template
updated_at: '2026-02-26T19:27:28-03:00'
---

# yoda-0046 - Unificar formato de Result log e remover comentario do template

## Summary
Remover o comentario instrucional do bloco `Result log` no template de issue para evitar que ele seja mantido acidentalmente por agentes durante Evaluate. Unificar o formato de `Result log` entre template e playbook (`yoda/yoda.md`) para eliminar conflito de instrucoes. Definir regra condicional para a linha de issue externa: so deve aparecer quando a issue interna estiver associada a uma issue externa.

## Context
Foi observado comportamento recorrente em que o comentario HTML do template nao e removido no fechamento da issue. Alem disso, o formato de `Result log` no template e no playbook Evaluate nao esta alinhado, gerando saidas inconsistentes. Essa divergencia aumenta retrabalho e dificulta padronizacao de logs de conclusao.

## Objective
Padronizar `Result log` com um unico formato oficial, remover comentario residual do template e tornar explicita a regra de emissao condicional da linha `GitLab|GitHub Issue`.

## Scope
- Remover comentario instrucional do `Result log` em `yoda/templates/issue.md`.
- Atualizar `yoda/yoda.md` (fase Evaluate) com o formato oficial de `Result log`.
- Garantir que o template e o playbook usem o mesmo formato.
- Definir regra condicional: linha `- **<GitLab|GitHub> Issue** :   #NNN` apenas quando houver associacao externa.
- Ajustar orientacoes de fluxo para manter `#NNN` quando houver issue externa, permitindo vinculacao no provedor.

## Out of scope
- Alterar a estrutura de outras secoes da issue fora de `Result log`.
- Mudar comportamento de scripts de fechamento alem do necessario para respeitar o formato padrao.
- Mudancas de schema nao relacionadas ao tema de log de resultado.

## Requirements
- O template de issue nao deve conter comentario HTML no bloco `Result log`.
- O playbook Evaluate deve declarar este formato unico:
  - `<First line: conventional commit message.>`
  - linha em branco
  - `<descricao do que foi feito>`
  - linha em branco
  - `- **<GitLab|GitHub> Issue** :   #NNN` (somente quando houver issue externa associada)
  - `- **Issue**: \`<ID>\``
  - `- **Path**: \`<issue path>\``
- Quando houver issue externa associada, a linha deve incluir `#NNN` obrigatoriamente.
- Quando nao houver issue externa associada, a linha `GitLab|GitHub Issue` deve ser omitida.
- O formato entre template e playbook deve permanecer consistente e sem duplicidade de regra.

## Acceptance criteria
- [ ] `yoda/templates/issue.md` nao contem mais o comentario instrucional no `Result log`.
- [ ] `yoda/yoda.md` (Evaluate) descreve exatamente o formato oficial definido.
- [ ] O formato no template e no playbook e identico, sem instrucoes conflitantes.
- [ ] Caso com issue externa inclui linha `GitLab|GitHub Issue` com `#NNN`.
- [ ] Caso sem issue externa nao inclui a linha `GitLab|GitHub Issue`.

## Dependencies
Origem externa `github #2`.

## Entry points
- path: yoda/templates/issue.md
  type: template
- path: yoda/yoda.md
  type: doc
- path: yoda/project/issues/
  type: data

## Implementation notes
Classificacao sugerida: `subtle` (ajuste de padronizacao e instrucao operacional, sem quebra de compatibilidade funcional esperada). A regra condicional da issue externa deve ser objetiva e testavel para evitar ambiguidade de output.

## Tests
- Validar manualmente/por teste de fixture que o template nao inclui comentario no `Result log`.
- Validar que o playbook Evaluate contem o formato oficial e a regra condicional da issue externa.
- Adicionar teste/documentacao de exemplo para ambos os cenarios: com e sem issue externa.

## Risks and edge cases
- Agentes antigos podem continuar reproduzindo formato legado se instrucoes cacheadas forem usadas.
- Omissao indevida da linha externa em issue vinculada pode perder automacao de vinculacao por `#NNN`.
- Inclusao indevida da linha externa em issue sem vinculo pode gerar referencia incorreta.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
