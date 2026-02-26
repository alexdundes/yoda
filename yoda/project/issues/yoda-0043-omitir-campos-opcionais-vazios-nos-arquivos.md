---
created_at: '2026-02-26T18:57:50-03:00'
depends_on: []
description: Quando um campo opcional estiver vazio, ele nao deve ser definido/persistido
  nos arquivos gerados ou atualizados.
id: yoda-0043
origin:
  external_id: '2'
  requester: ''
  system: github
pending_reason: ''
priority: 5
schema_version: '1.01'
slug: omitir-campos-opcionais-vazios-nos-arquivos
status: to-do
title: Omitir campos opcionais vazios nos arquivos
updated_at: '2026-02-26T18:57:50-03:00'
---

# yoda-0043 - Omitir campos opcionais vazios nos arquivos

## Summary
Reduzir tamanho e ruido dos artefatos YAML/Markdown omitindo campos opcionais quando estiverem vazios. Em vez de persistir chaves com string vazia, lista vazia ou valor padrao sem informacao util, os scripts devem simplesmente nao escrever essas chaves nos arquivos de saida. A regra deve ser consistente entre criacao, update e reconciliacao.

## Context
Atualmente varios arquivos persistem campos opcionais vazios, o que aumenta volume, dificulta leitura e amplia diferencas em PRs sem ganho funcional. Essa verbosidade tambem eleva o custo de manutencao do schema e dos templates. A padronizacao de omissao para opcionais vazios simplifica artefatos e torna mudancas mais claras.

## Objective
Definir e implementar politica unica de serializacao para que campos opcionais vazios sejam omitidos dos arquivos internos do YODA, preservando compatibilidade operacional e validacao.

## Scope
- Mapear campos opcionais relevantes em TODO, issue front matter e logs aplicaveis.
- Ajustar escrita de arquivos em scripts que criam/atualizam dados para omitir opcionais vazios.
- Ajustar templates para nao forcar emissao de campos opcionais vazios.
- Atualizar validacao para aceitar ausencia desses campos.
- Atualizar/reconciliar artefatos existentes quando aplicavel.

## Out of scope
- Remover campos obrigatorios do schema.
- Alterar significado semantico de campos opcionais quando presentes.
- Mudancas funcionais nao relacionadas a serializacao/compactacao de artefatos.

## Requirements
- Campo opcional vazio nao deve ser persistido em novos arquivos.
- Campo opcional que ficar vazio apos update deve ser removido do arquivo.
- Validadores devem considerar a ausencia de opcional como valida.
- Renderizacao/serializacao deve permanecer deterministica para evitar diffs instaveis.
- Documentacao de scripts deve refletir a regra de omissao de opcionais vazios.

## Acceptance criteria
- [ ] `issue_add.py` nao grava campos opcionais vazios no front matter e no item do TODO.
- [ ] `todo_update.py` remove campo opcional quando atualizado para vazio.
- [ ] `init.py --reconcile-layout` (ou fluxo equivalente) consegue limpar campos opcionais vazios em arquivos legados.
- [ ] Validacao aceita arquivos sem campos opcionais omitidos.
- [ ] Testes automatizados cobrem criacao, update e reconciliacao com omissao de opcionais.

## Dependencies
Relacionada a `yoda-0042` (simplificacao de origem externa) e ao backlog externo `github #2`.

## Entry points
- path: yoda/scripts/issue_add.py
  type: code
- path: yoda/scripts/todo_update.py
  type: code
- path: yoda/scripts/init.py
  type: code
- path: yoda/scripts/lib/validate.py
  type: code
- path: yoda/scripts/lib/front_matter.py
  type: code
- path: yoda/templates/issue.md
  type: template
- path: yoda/todos/TODO.yoda.yaml
  type: data

## Implementation notes
A regra de "opcional vazio = omitido" deve ser centralizada em utilitario compartilhado de serializacao para evitar divergencia entre scripts. Necessario definir com precisao o que e "vazio" por tipo (string vazia, lista vazia, objeto vazio, null) e aplicar de forma uniforme.

## Tests
- Adicionar testes unitarios para serializacao com omissao de opcionais vazios.
- Atualizar fixtures de TODO/issue para novo comportamento.
- Cobrir caminho de migracao/reconciliacao de arquivos existentes.
- Rodar `python3 -m pytest yoda/scripts/tests`.

## Risks and edge cases
- Remocao indevida de campo que parecia opcional, mas e exigido por algum fluxo especifico.
- Mudanca gerar incompatibilidade com ferramentas externas que esperam chave presente vazia.
- Reconciliacao em massa produzir diffs grandes; precisa de criterio claro de rollout.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
