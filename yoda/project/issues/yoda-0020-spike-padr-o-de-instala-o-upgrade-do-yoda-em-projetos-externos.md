---
created_at: '2026-01-28T19:02:16-03:00'
depends_on:
- yoda-0016
description: Explorar opções para embutir/atualizar o YODA Framework em repositórios
  externos, cobrindo pacote+init, versionamento, upgrade/rollback e riscos.
id: yoda-0020
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 6
schema_version: '1.01'
slug: spike-padr-o-de-instala-o-upgrade-do-yoda-em-projetos-externos
status: done
title: 'Spike: padrão de instalação/upgrade do YODA em projetos externos'
updated_at: '2026-02-25T20:02:28-03:00'
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
- Documentar fluxo de instalação inicial com um one-liner (`curl|sh`) como primeira opção (com alertas), seguido de roteiro manual recomendado.

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
- Especificar `latest.json` como metadata remota para update (`version`, `build`, `package_url`, `sha256`).
- O update deve substituir apenas o subtree `yoda/` (scripts/templates/manual/manifest/changelog), preservando `yoda/todos`, `yoda/logs`, `yoda/project/issues`.
- Não sobrescrever `README.md` na raiz do host; `yoda/scripts/README.md` pode ser sobrescrito.
- Licença do YODA deve existir em `yoda/LICENSE` (sobrescrevível em updates); deve ser igual à LICENSE da raiz deste repo.
- Definir local de rollback: `yoda/_previous/<version>`.
- Listar opção “submódulo git” como alternativa não recomendada (explicitar por quê).

## Acceptance criteria
- [ ] Documento de decisão criado e versionado, contendo opções avaliadas e recomendação escolhida.
- [ ] Fluxo de instalação e upgrade descrito passo a passo, citando comandos previstos.
- [ ] Riscos principais e mitigação registrados.
- [ ] Follow-ups claros (novas issues) identificados.
- [ ] Inclui fluxo “one-liner” primeiro (com alertas), e fluxo manual recomendado em seguida.
- [ ] Define comportamento de update/rollback, metadata `latest.json`, e regras de preservação de arquivos.

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
- Documento como spec normativa em `project/specs/` (proposto: `project/specs/24-installation-and-upgrade.md`).
- Manter linguagem concisa, orientada a decisão; evitar detalhamento de implementação.
- Considerar constraints de segurança (assinatura/checksum) e de ambientes offline.
- Fluxo recomendado: download + verify + replace parcial + rollback seguro.
- Fluxo one-liner: `curl -fsSL <url>/yoda-install.sh | sh -s -- --version <semver+build> --root .` com alertas.

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
- Added installation/upgrade spec covering one-liner install (with warnings), manual flow, update/rollback, and `latest.json` metadata; aligned packaging spec for `yoda/LICENSE` and updated summary.

Commit suggestion:
```
docs: define installation and upgrade strategy

Issue: yoda-0020
Path: yoda/project/issues/yoda-0020-spike-padr-o-de-instala-o-upgrade-do-yoda-em-projetos-externos.md
```