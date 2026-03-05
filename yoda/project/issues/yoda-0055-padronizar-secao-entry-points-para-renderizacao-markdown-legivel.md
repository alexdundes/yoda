---
schema_version: '1.02'
id: yoda-0055
status: to-do
depends_on:
- yoda-0048
title: Padronizar secao Entry points para renderizacao markdown legivel
description: Substituir o formato pseudo-YAML da secao Entry points por formato markdown
  legivel no preview humano, mantendo estrutura deterministica para scripts.
priority: 5
extern_issue_file: ../extern_issues/github-3.json
created_at: '2026-03-04T20:42:02-03:00'
updated_at: '2026-03-04T20:42:18-03:00'
---

# yoda-0055 - Padronizar secao Entry points para renderizacao markdown legivel

## Summary
A secao `Entry points` das issues usa um formato pseudo-YAML dentro do markdown, que fica ruim no preview humano. Esta issue define e aplica um formato markdown legivel, sem perder determinismo para leitura por scripts.

## Context
No estado atual, o bloco em estilo YAML dentro do corpo da issue dificulta leitura em interfaces de preview markdown e gera friccao no uso diario.

## Objective
Padronizar `Entry points` em formato markdown nativo (lista ou tabela) com regra clara e previsivel para humanos e automacao.

## Scope
- Definir formato canonico de `Entry points` na spec.
- Atualizar template de issue para o novo formato.
- Ajustar validacoes/script(s) que dependam do formato anterior.
- Atualizar issues abertas do pacote 0.3.0 quando necessario.

## Out of scope
- Redesenhar outras secoes da issue sem relacao com `Entry points`.
- Mudancas em fluxo de estado/fase nao relacionadas.

## Requirements
- O formato deve renderizar corretamente em preview markdown.
- A estrutura deve continuar parseavel de forma deterministica.
- O template nao deve incluir exemplos que causem ambiguidade visual.

## Acceptance criteria
- [ ] `Entry points` possui formato markdown legivel e padronizado.
- [ ] Template de issue reflete o novo formato.
- [ ] Validacoes/testes cobrem o formato adotado.

## Dependencies
Depende de `yoda-0048`.

## Entry points
- `project/specs`
- `yoda/templates/issue.md`
- `yoda/project/issues`

## Implementation notes
Preferir tabela markdown com colunas fixas quando houver necessidade de parse por heuristica simples.

## Tests
Adicionar casos de fixture garantindo renderizacao legivel e consistencia de parse.

## Risks and edge cases
- Formato novo pode exigir ajuste em scripts que assumem padrao antigo.
- Conversao parcial de issues pode gerar inconsistencias temporarias.

## Result log