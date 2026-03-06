---
schema_version: '2.00'
id: yoda-0057
status: to-do
depends_on:
- yoda-0048
title: Remover id do front matter e derivar ID pelo nome do arquivo
description: Eliminar o campo id do front matter no modelo 0.3.0 e definir o nome
  do arquivo da issue como fonte canonica para derivacao do ID.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:58:43-03:00'
updated_at: '2026-03-04T20:59:15-03:00'
---

# yoda-0057 - Remover id do front matter e derivar ID pelo nome do arquivo

## Summary
No modelo atual, o identificador da issue aparece no nome do arquivo e no front matter (`id`), gerando redundancia. Esta issue define o nome do arquivo como fonte canonica do ID e remove o campo `id` do front matter no 0.3.0.

## Context
A duplicidade de ID aumenta chance de divergencia em renomeacoes, migracoes e edicoes manuais.

## Objective
Simplificar o schema da issue e eliminar inconsistencias mantendo derivacao deterministica do ID pelo path.

## Scope
- Atualizar specs para definir ID derivado do nome do arquivo.
- Remover `id` do template/front matter 0.3.0.
- Ajustar scripts e validacoes para nao exigir `id` no front matter.
- Definir regras de erro para arquivos com nome invalido.

## Out of scope
- Alterar o formato canonico do nome de arquivo `<id>-<slug>.md`.
- Mudar semantica de slug alem do necessario para derivacao do ID.

## Requirements
- Scripts devem extrair ID do nome do arquivo com validacao forte.
- Front matter nao deve conter `id` no modelo 0.3.0.
- Mensagens de erro devem apontar arquivo e regra violada.

## Acceptance criteria
- [ ] Specs 0.3.0 declaram ID derivado do nome do arquivo.
- [ ] Template de issue remove o campo `id` do front matter.
- [ ] Testes cobrem parse de ID, nomes invalidos e ausencia de `id`.

## Dependencies
Depende de `yoda-0048`.

## Entry points
- `project/specs`
- `yoda/templates/issue.md`
- `yoda/scripts`
- `yoda/project/issues`

## Implementation notes
Padronizar funcao unica de derivacao de ID para evitar divergencia entre scripts.

## Tests
Adicionar casos de fixture para nomes validos/invalidos e backward compatibility durante migracao.

## Risks and edge cases
- Rename manual de arquivo pode quebrar rastreabilidade se nao houver validacao.
- Integracoes externas podem assumir `id` no front matter e precisar ajuste.

## Result log

## Flow log
2026-03-04T20:58:43-03:00 | [yoda-0057] issue_add created | title: Remover id do front matter e derivar ID pelo nome do arquivo | description: Eliminar o campo id do front matter no modelo 0.3.0 e definir o nome do arquivo da issue como fonte canonica para derivacao do ID. | slug: remover-id-do-front-matter-e-derivar-id-pelo-nome-do-arquivo | extern_issue_file: external issue linked
2026-03-04T20:59:15-03:00 | [yoda-0057] todo_update | depends_on:  -> yoda-0048
