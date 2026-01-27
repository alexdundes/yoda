---
agent: Human
created_at: '2026-01-27T13:32:13-03:00'
depends_on: []
description: Existem conflitos nas regras de entrada do agente e manutencao de TODO
  entre yoda/yoda.md e as specs. Esta issue propõe ajustes pontuais para deixar o
  fluxo de bootstrap e as regras de edicao consistentes e sem ambiguidade, explicitando
  que o bootstrap e provisório e que a documentacao foca a fase nao-bootstrap.
entrypoints: []
id: yoda-0027
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 6
schema_version: '1.0'
slug: resolver-ambiguidades-entrada-todo
status: done
tags: []
title: Resolver ambiguidades de entrada e atualizacao de TODO
updated_at: '2026-01-27T13:32:38-03:00'
---

# yoda-0027 - Resolver ambiguidades de entrada e atualizacao de TODO

## Summary
Existem conflitos nas regras de entrada do agente e manutencao de TODO entre yoda/yoda.md e as specs. Esta issue propõe ajustes pontuais para deixar o fluxo de bootstrap e as regras de edicao consistentes e sem ambiguidade, explicitando que o bootstrap e provisório e que a documentacao foca a fase nao-bootstrap.

## Context
O repositorio opera em bootstrap, com TODO em Markdown e sem scripts. Hoje, ha regras concorrentes: fallback automatico vs perguntar ao usuario quando falta TODO, e proibicao de editar TODO vs obrigacao de atualizar status. Alem disso, o fluxo de entrada em `project/specs/07-agent-entry-and-root-file.md` aponta apenas para `TODO.<dev>.yaml`, enquanto o bootstrap define `TODO.<dev>.md`. As specs precisam reforcar que bootstrap e provisório e que a documentacao aponta para a fase futura nao-bootstrap.

## Objective
Definir uma regra unica e explicita para fallback/consulta do TODO em bootstrap, alinhar a politica de edicao de TODO com a obrigacao de atualizar status, reforcar que o bootstrap e provisório e que a documentacao e focada na fase nao-bootstrap, e refletir essas regras tanto em yoda/yoda.md quanto nas specs relevantes.

## Scope
- Ajustar a regra de fallback/consulta do TODO em `yoda/yoda.md`.
- Alinhar a regra de edicao/atualizacao do TODO em `yoda/yoda.md`.
- Tornar explicita a regra condicional de bootstrap em `project/specs/07-agent-entry-and-root-file.md`.
- Se necessario, ajustar `project/specs/15-bootstrap.md` para reforcar a regra escolhida.
- Explicitar nas specs que bootstrap e provisório e que a documentacao foca a fase nao-bootstrap.
- Revisar `README.md` para manter alinhamento com as regras e evitar conflitos.

## Out of scope
- Migrar TODOs ou logs para YAML.
- Criar ou executar scripts de automacao.
- Alterar a estrutura de pastas do repositorio.

## Requirements
- A regra de fallback/consulta do TODO deve ser unica e nao conflitante entre docs.
- A politica de edicao do TODO deve permitir atualizar status sem contradicao com "nao editar".
- O fluxo de entrada deve explicitar o comportamento em bootstrap quando `TODO.<dev>.yaml` nao existe.
- As specs devem declarar que bootstrap e provisório e que a documentacao foca o futuro nao-bootstrap.
- O `README.md` deve refletir as regras atualizadas e nao conflitar com as specs.

## Acceptance criteria
- [ ] `yoda/yoda.md` tem uma regra unica para fallback/consulta do TODO em bootstrap.
- [ ] `yoda/yoda.md` nao conflita entre "nao editar TODO" e "atualizar status".
- [ ] `project/specs/07-agent-entry-and-root-file.md` explicita o comportamento quando o repositorio esta em bootstrap.
- [ ] Se necessario, `project/specs/15-bootstrap.md` reforca a regra escolhida sem contradicoes.
- [ ] As specs deixam claro que bootstrap e provisório e que a documentacao foca a fase nao-bootstrap.
- [ ] `README.md` fica consistente com as specs e sem regras conflitantes.

## Dependencies
None

## Entry points
- path: yoda/yoda.md
  type: other
- path: project/specs/07-agent-entry-and-root-file.md
  type: other
- path: project/specs/15-bootstrap.md
  type: other
- path: README.md
  type: other
- path: yoda/todos/TODO.alex.md
  type: other

## Implementation notes
- Preservar a regra de bootstrap e a nao coexistencia entre `TODO.<dev>.md` e `TODO.<dev>.yaml`.
- Garantir que a regra escolhida seja consistente com REPO_INTENT.md.
- Regra proposta para TODO ausente: perguntar ao usuario qual TODO usar; `yoda/todos/TODO.alex.md` pode ser sugerido como padrao.
- Regra proposta para edicao de TODO: permitir atualizacao de status/pending como parte do fluxo; qualquer outra edicao exige solicitacao explicita do usuario.
- Anotacoes de bootstrap devem explicitar que sao provisórias e que a documentacao foca a fase nao-bootstrap.

## Tests
Not applicable.

## Risks and edge cases
- Manter compatibilidade com o fluxo de entrada descrito em `README.md`.

## Result log
Alinhei regras de entrada e bootstrap em `yoda/yoda.md` e nas specs, explicitei a natureza provisoria do bootstrap e ajustei o README para evitar conflitos. Tambem defini a regra de fallback do TODO e o limite de edicao (status/pending) sem solicitacao explicita. Revisei o README para seguir a voz tecnica e terminologia das specs, priorizando "agent" e termos canonicos, e normalizei ocorrencias restantes. Ajustei trechos finais para consistencia entre "agent" e "agents".

docs: align bootstrap rules and entry flow

Issue: `yoda-0027`
Path: `yoda/project/issues/yoda-0027-resolver-ambiguidades-entrada-todo.md`