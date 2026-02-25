---
created_at: '2026-01-28T19:02:09-03:00'
depends_on:
- yoda-0016
description: Implementar comando/script que gera artefato instalável contendo apenas
  os arquivos necessários de yoda/, com versão e checklist de inclusão/exclusão.
id: yoda-0018
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 8
schema_version: '1.01'
slug: comando-de-empacote-do-yoda-package
status: done
title: Comando de empacote do YODA (package)
updated_at: '2026-02-25T20:02:28-03:00'
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
- Ajustar a spec de empacotamento para refletir README.md obrigatório e exclusão de testes em `yoda/scripts/tests`.

## Out of scope
- Implementar comando de init (yoda-0019).
- Mudar conteúdo funcional do manual (yoda-0017) além do necessário para inclusão.
- Publicar em registries externos.

## Requirements
- CLI com flags mínimas: `--output/--dir`, `--archive-format` (tar.gz/zip), `--version` (obrigatório), `--dry-run`.
- Usa lista de inclusão/exclusão baseada na spec (yoda-0016) e falha se item obrigatório ausente.
- Salva manifesto de conteúdo (ex.: `PACKAGE_MANIFEST.txt`) dentro do pacote ou ao lado.
- Não deve incluir arquivos temporários, logs ou `project/specs`.
- Saída clara de sucesso/erro; exit codes padronizados.
- `README.md` (não `README`) é obrigatório no pacote e na spec.
- `--archive-format` suporta apenas `tar.gz` por enquanto; qualquer outro valor deve falhar.
- Excluir `yoda/scripts/tests` do pacote.
- Campo `built_by` do manifesto deve usar o slug `--dev` atual.
- `package_sha256` deve ser o hash do artefato final (auto-referencial).

## Acceptance criteria
- [ ] Rodar o comando gera pacote único com nome versionado e manifesto de conteúdo.
- [ ] Conteúdo do pacote corresponde à lista de inclusão/exclusão definida na spec (sem `project/specs`).
- [ ] `--dry-run` lista o que seria empacotado sem gerar arquivo.
- [ ] Documentação de uso (com exemplo) atualizada em repo.
- [ ] `README.md` incluído e `yoda/scripts/tests` excluído.
- [ ] `--archive-format` rejeita formatos além de `tar.gz`.

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
- Atualizar `project/specs/23-distribution-and-packaging.md` (e referências) para refletir `README.md` obrigatório e exclusão de `yoda/scripts/tests`.

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
- Added `yoda/scripts/package.py` with deterministic tar.gz packaging, include/exclude rules, manifest/changelog validation, and dry-run output; added tests and docs for the new command.
- Updated packaging spec to require `README.md`, exclude `yoda/scripts/tests`, and clarify tar.gz-only/manifest hashing rules.

Commit suggestion:
```
feat: add package command for yoda artefact

Issue: yoda-0018
Path: yoda/project/issues/yoda-0018-comando-de-empacote-do-yoda-package.md
```