---
agent: Human
created_at: '2026-01-28T19:02:09-03:00'
depends_on:
- yoda-0016
description: Implementar comando/script que gera artefato instalável contendo apenas
  os arquivos necessários de yoda/, com versão e checklist de inclusão/exclusão.
entrypoints: []
id: yoda-0018
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 8
schema_version: '1.0'
slug: comando-de-empacote-do-yoda-package
status: to-do
tags: []
title: Comando de empacote do YODA (package)
updated_at: '2026-01-28T19:05:18-03:00'
---

# yoda-0018 - Comando de empacote do YODA (package)
<!-- AGENT: Replace yoda-0018 with the canonical issue id (dev-id, e.g., dev-0001) from `yoda/todos/TODO.<dev>.yaml` and Comando de empacote do YODA (package) with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
Criar comando/script de empacotamento que gere um artefato instalável contendo apenas o necessário de `yoda/`, com nome versionado e checklist de inclusão/exclusão. O pacote será usado para embarcar o YODA Framework em outros projetos.

## Context
Hoje não existe forma automatizada de gerar o artefato distribuível; dependemos do workspace completo e de `project/specs`, que não devem ir para o pacote. Precisamos de um comando reprodutível que siga as futuras specs de distribuição (yoda-0016) e produza um único pacote pronto para consumo pelo comando de init.

## Objective
Implementar um comando (ex.: `yoda/scripts/package.py`) que cria o pacote do YODA Framework com lista de inclusão/exclusão conforme specs, nome versionado e saída documentada.

## Scope
- Implementar script de empacote (CLI) usando stdlib (zip/tar) ou ferramenta já permitida no repo.
- Configurar lista de arquivos/pastas a incluir (manual, scripts, templates, todos necessários) e excluir (`project/specs`, bootstrap, artefatos de build).
- Produzir arquivo com versão no nome (ex.: `yoda-framework-<version>.tar.gz`) e opcional checksum.
- Gerar log/listagem dos arquivos incluídos para conferência.
- Documentar uso básico (ex.: comando, flags, output) no README de scripts ou no manual.

## Out of scope
- Implementar comando de init (yoda-0019).
- Mudar conteúdo funcional do manual (yoda-0017) além do necessário para inclusão.
- Publicar em registries externos.

## Requirements
- CLI com flags mínimas: `--output/--dir`, `--format` (tar.gz/zip), `--version` (fallback padrão), `--dry-run`.
- Usa lista de inclusão/exclusão baseada na spec (yoda-0016) e falha se item obrigatório ausente.
- Salva manifesto de conteúdo (ex.: `PACKAGE_MANIFEST.txt`) dentro do pacote ou ao lado.
- Não deve incluir arquivos temporários, logs ou `project/specs`.
- Saída clara de sucesso/erro; exit codes padronizados.

## Acceptance criteria
- [ ] Rodar o comando gera pacote único com nome versionado e manifesto de conteúdo.
- [ ] Conteúdo do pacote corresponde à lista de inclusão/exclusão definida na spec (sem `project/specs`).
- [ ] `--dry-run` lista o que seria empacotado sem gerar arquivo.
- [ ] Documentação de uso (com exemplo) atualizada em repo.

## Dependencies
Depends on: yoda-0016.

## Entry points
- path: project/specs (nova seção de distribuição de yoda-0016)
  type: doc
- path: yoda/scripts/README.md
  type: doc
- path: yoda/yoda.md
  type: doc
- path: yoda/scripts
  type: code

## Implementation notes
- Preferir stdlib (`tarfile`/`zipfile`) para evitar dependências novas.
- Considerar arquivo de configuração simples (lista de inclusão/exclusão) para facilitar manutenção.
- Garantir compatibilidade com execução via `python3 yoda/scripts/package.py` na raiz do repo.

## Tests
- Adicionar teste simples (ex.: em `yoda/scripts/tests`) que gera pacote em diretório temporário e valida inclusão/exclusão chave; se inviável, documentar manual check.

## Risks and edge cases
- Inclusão acidental de arquivos grandes/privados (logs, caches).
- Nome de versão não fornecido levando a artefatos indistinguíveis.
- Execução em SOs diferentes (paths e permissões) afetar conteúdo.

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->