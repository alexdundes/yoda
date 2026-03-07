---
schema_version: '2.00'
id: yoda-0019
status: done
depends_on:
- yoda-0016
- yoda-0018
title: "Comando de init p\xF3s-embutido"
description: "Criar script que prepara um projeto host ap\xF3s receber o pacote YODA:\
  \ ajusta AGENTS.md, estrutura m\xEDnima, TODO.<dev>.yaml, idempotente e com dry-run."
priority: 7
created_at: '2026-01-28T19:02:12-03:00'
updated_at: '2026-03-03T14:36:08-03:00'
---

# yoda-0019 - Comando de init pós-embutido

## Summary
Criar comando de inicialização para projetos que recebem o pacote do YODA, configurando estrutura mínima (AGENTS.md, pastas, TODO.<dev>.yaml) de forma idempotente e segura, com opção de dry-run.

## Context
Após empacote, o projeto host precisa configurar arquivos de agente e TODO sem depender do workspace de desenvolvimento. Atualmente não existe ferramenta para preparar esse ambiente; é necessário automatizar para reduzir erros manuais e garantir consistência com o manual embarcado.

## Objective
Implementar script de init que, ao rodar no projeto host, crie/ajuste estrutura e arquivos mínimos para rodar o YODA Framework embarcado, respeitando idempotência e segurança (não sobrescrever sem consentimento).

## Scope
- Implementar CLI (ex.: `yoda/scripts/init.py`) chamada a partir do pacote.
- Criar/atualizar arquivos de entrada de agents (`AGENTS.md`, `gemini.md`, `CLAUDE.md`, `agent.md`) com referência ao manual embarcado, preservando conteúdo existente.
- Criar pastas necessárias (`yoda/todos`, `yoda/logs`, `yoda/project/issues`) e seed de `TODO.<dev>.yaml` se ausente.
- Fornecer flags de dry-run e opções de sobrescrita/merge de arquivos existentes.
- Registrar resumo das ações executadas (stdout e/ou log).

## Out of scope
- Gerar o pacote em si (yoda-0018).
- Redigir manual completo (yoda-0017) além do necessário para referência.
- Configurar CI/CD do projeto host.

## Requirements
- CLI com flags: `--dev` (slug), `--dry-run`, `--force` (sobrescrita segura), `--root` (destino opcional).
- Não sobrescrever conteúdo existente dos arquivos de agent; anexar bloco YODA ao final quando necessário.
- Idempotente: rodar duas vezes não corrompe nem duplica entradas.
- Usa caminhos relativos ao diretório onde o pacote foi extraído.
- Mensagens claras de sucesso/erro e códigos de saída apropriados.
- Arquivos de agent suportados por padrão: `AGENTS.md`, `gemini.md`, `CLAUDE.md`, `agent.md` (lista fácil de expandir no script).
- `AGENTS.md`/`gemini.md`/etc. devem apenas apontar para `yoda/yoda.md`.
- `--force` pode sobrescrever `TODO.<dev>.yaml`; arquivos de agent não devem perder conteúdo (apenas atualizar o bloco YODA).
- `TODO.<dev>.yaml` seed deve conter `schema_version: 1.0`, `developer_name/slug` = dev, `timezone` local, `updated_at` e `issues: []`.
- Quando `TODO.<dev>.yaml` já existe e é válido, não modificar; reportar quantidade de issues.
- Conflitos (TODO inválido ou arquivo de agent ilegível) retornam exit code 4 com diff/resumo quando aplicável.

## Acceptance criteria
- [ ] Em projeto vazio, comando cria `AGENTS.md`, estrutura `yoda/` e `TODO.<dev>.yaml` válida.
- [ ] Em projeto com `AGENTS.md` (ou `gemini.md`, `CLAUDE.md`, `agent.md`) existente, o conteúdo é preservado e o bloco YODA é anexado/atualizado no fim.
- [ ] Reexecutar com os mesmos parâmetros não duplica o bloco YODA nem altera o restante do arquivo (salvo se `--force` para TODO).
- [ ] `--dry-run` mostra ações sem escrever no disco.
- [ ] Documentação de uso e exemplos atualizada (manual ou README de scripts).

## Dependencies
Depends on: yoda-0016, yoda-0018.

## Entry points
- path: yoda/scripts
  type: code
- path: yoda/templates
  type: asset
- path: yoda/yoda.md
  type: doc
- path: project/specs (distribuição definida em yoda-0016)
  type: doc

## Implementation notes
- Reutilizar utilitários existentes (`lib.paths`, `lib.dev`, etc.) para consistência.
- Fornecer texto mínimo em `AGENTS.md` apontando para o manual embarcado.
- Considerar modo interativo simples caso arquivos existam (perguntar/confirmar).
- `--root` default é o diretório atual; o manual deve existir em `<root>/yoda/yoda.md`.
- Usar bloco delimitado para idempotência: `<!-- YODA:BEGIN -->` ... `<!-- YODA:END -->`; substituir o bloco se já existir.
- Atualizar `project/specs/07-agent-entry-and-root-file.md` se necessário para refletir múltiplos arquivos de agent.

## Tests
- Preferir teste automatizado criando tempdir e verificando que arquivos são gerados e idempotentes; se inviável, documentar roteiro manual.

## Risks and edge cases
- Sobrescrever configurações existentes do projeto host.
- Permissões de arquivo ou path relativo incorreto ao executar fora da raiz.
- Falta de slug de dev levando a TODO inválido.

## Result log
- Added `yoda/scripts/init.py` to initialize host projects, appending a YODA block to supported agent files and seeding TODO structure with idempotent behavior.
- Updated agent entry spec and script docs; added tests covering creation, idempotency, dry-run, and agent-file conflicts.

Commit suggestion:
```
feat: add init command for embedded yoda

Issue: yoda-0019
Path: yoda/project/issues/yoda-0019-comando-de-init-p-s-embutido.md
```

## Flow log
2026-01-28T19:02:12-03:00 | [yoda-0019] issue_add created | title: Comando de init pós-embutido | description: Criar script que prepara um projeto host após receber o pacote YODA: ajusta AGENTS.md, estrutura mínima, TODO.<dev>.yaml, idempotente e com dry-run. | slug: comando-de-init-p-s-embutido | priority: 7 | agent: Human
2026-01-28T19:05:21-03:00 | [yoda-0019] todo_update | depends_on: [] -> yoda-0016, yoda-0018
2026-02-02T08:35:18-03:00 | [yoda-0019] todo_update | status: to-do -> doing
2026-02-02T08:57:07-03:00 | [yoda-0019] Implemented init command with YODA block append for agent files, updated specs/docs, and added tests.
2026-02-02T08:57:11-03:00 | [yoda-0019] todo_update | status: doing -> done
