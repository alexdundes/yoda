---
agent: Human
created_at: '2026-01-28T19:02:16-03:00'
depends_on:
- yoda-0016
description: Explorar opções para embutir/atualizar o YODA Framework em repositórios
  externos, cobrindo pacote+init, versionamento, upgrade/rollback e riscos.
entrypoints: []
id: yoda-0020
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 6
schema_version: '1.0'
slug: spike-padr-o-de-instala-o-upgrade-do-yoda-em-projetos-externos
status: to-do
tags: []
title: 'Spike: padrão de instalação/upgrade do YODA em projetos externos'
updated_at: '2026-01-28T19:05:24-03:00'
---

# yoda-0020 - Spike: padrão de instalação/upgrade do YODA em projetos externos
<!-- AGENT: Replace yoda-0020 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Spike: padrão de instalação/upgrade do YODA em projetos externos with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Investigar e propor padrão de instalação e upgrade do YODA em projetos externos, avaliando opções (pacote + init, submódulo, vendoring, gestor de pacotes), versionamento, upgrade/rollback e riscos. Entrega será um documento de decisão com recomendações e próximos passos.

## Context
Estamos criando o pacote e o comando de init, mas ainda não existe estratégia consolidada para como times vão instalar/atualizar o YODA nos próprios repositórios. Sem diretriz, cada adoção pode inventar um fluxo diferente, dificultando suporte, upgrades e rollback.

## Objective
Produzir análise curta e recomendação prática sobre como embutir e atualizar o YODA Framework em repositórios externos, incluindo versões, verificação de integridade e rollback seguro.

## Scope
- Levantar pelo menos três opções de distribuição (ex.: pacote + init, submódulo git, gestor de pacotes zip/tar).
- Avaliar cada opção em critérios: simplicidade, reprodutibilidade, controle de versão, segurança, atualização e rollback.
- Propor caminho recomendado (MVP) e condições para revisitar alternativas.
- Definir requisitos para upgrade/rollback (ex.: manter cópia anterior, sem quebrar TODO/AGENTS existentes).
- Listar follow-ups (issues) necessários para implementar a recomendação.

## Out of scope
- Implementar comandos de empacote ou init (coberto por outras issues).
- Criar pipeline de publicação.
- Decidir sobre licenciamento ou branding.

## Requirements
- Documento curto (1-2 páginas) em `project/specs/` ou subpasta de decisões, com opções, prós/contras e recomendação.
- Descrever fluxo de upgrade/rollback recomendado e como validar versão/integração (checksum/assinatura opcional).
- Indicar como o comando de init/pacote serão usados no fluxo recomendado.
- Listar riscos e medidas de mitigação.
- Enumerar tarefas derivadas com prioridade sugerida.

## Acceptance criteria
- [ ] Documento de decisão criado e versionado, contendo opções avaliadas e recomendação escolhida.
- [ ] Fluxo de instalação e upgrade descrito passo a passo, citando comandos previstos.
- [ ] Riscos principais e mitigação registrados.
- [ ] Follow-ups claros (novas issues) identificados.

## Dependencies
Depends on: yoda-0016 (usar specs de distribuição como base).

## Entry points
- path: project/specs (distribuição, yoda-0016)
  type: doc
- path: yoda/yoda.md
  type: doc
- path: yoda/scripts
  type: code

## Implementation notes
- Escolher localização do documento alinhada ao padrão atual (ex.: `project/specs/decisions/` ou `project/specs/spikes/`).
- Manter linguagem concisa, orientada a decisão; evitar detalhamento de implementação.
- Considerar constraints de segurança (assinatura/checksum) e de ambientes offline.

## Tests
- Not applicable (spike/decisão).

## Risks and edge cases
- Escolha inadequada dificultar upgrades futuros.
- Ignorar restrições de ambientes corporativos (sem internet, proxies).
- Recomendação depender de ferramentas não disponíveis no pacote.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->