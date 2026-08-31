---
schema_version: '2.01'
status: to-do
title: Adicionar fallback publico para coleta de issues externas
description: Permitir que get_extern_issue.py consulte APIs publicas sem autenticacao
  quando a issue pertence a um repositorio publico e o CLI autenticado estiver indisponivel
  ou sem sessao valida, preservando o acesso autenticado atual para repositorios privados
  e mantendo o mesmo contrato JSON do YODA Intake.
priority: 5
created_at: '2026-08-31T16:36:09-03:00'
updated_at: '2026-08-31T16:36:09-03:00'
---

# yoda-0067 - Adicionar fallback publico para coleta de issues externas

## Summary

Adicionar ao `get_extern_issue.py` uma rota de leitura sem autenticacao para
issues de repositorios publicos. O transporte autenticado atual deve continuar
preferencial e obrigatorio quando o repositorio ou seus dados forem privados,
enquanto a API publica funciona como fallback seguro e transparente.

## Context

Durante o Intake da GitHub #9, o `gh auth status` falhou porque o token local
estava invalido. A issue e publica e pôde ser obtida com sucesso pela API HTTP
publica do GitHub, incluindo a confirmacao de que nao havia comentarios nem
eventos de timeline, e normalizada no mesmo contrato JSON consumido pelo YODA
Intake.

Hoje `get_extern_issue.py` executa `ensure_cli_and_auth(provider)` antes de
qualquer leitura. Isso transforma autenticacao em requisito mesmo quando o
provedor oferece os dados publicamente. Ao mesmo tempo, remover o caminho
autenticado quebraria repositorios privados, limites de acesso e dados que
dependem das credenciais do operador.

## Objective

Permitir Intake de issues publicas sem login, com degradacao previsivel quando
o CLI ou a autenticacao nao estiverem disponiveis, sem reduzir a capacidade de
coletar issues privadas pelo transporte autenticado existente.

## Scope

- Especificar a estrategia de selecao entre transporte autenticado e publico.
- Implementar fallback HTTP publico para o provider GitHub.
- Preservar o caminho atual por `gh api` para repositorios privados.
- Manter o provider GitLab e sua autenticacao atual sem regressao.
- Normalizar issue, labels, comentarios e timeline/eventos no mesmo schema JSON.
- Manter nome do arquivo, rastreabilidade e consumo pelo YODA Intake.
- Tratar rate limit, indisponibilidade, 401, 403 e 404 com mensagens acionaveis.
- Atualizar help, manual, specs e testes sem exigir rede real na suite.
- Avaliar e documentar separadamente a paridade futura de fallback publico para
  GitLab, sem inclui-la implicitamente nesta entrega.

## Out of scope

- Remover ou substituir o suporte autenticado de GitHub ou GitLab.
- Tornar uma issue privada acessivel sem credenciais validas.
- Armazenar tokens no JSON de issue externa ou em arquivos do YODA.
- Criar, editar, comentar ou fechar issues no provedor externo.
- Depender de navegador, sessao grafica ou scraping de HTML.
- Exigir chamadas reais a internet nos testes automatizados.
- Implementar fallback publico para GitLab sem decisao explicita de contrato e
  verificacao de paridade do provider.

## Requirements

- Quando o CLI e a autenticacao estiverem validos, o coletor SHOULD preservar o
  transporte autenticado atual, inclusive para repositorios privados.
- Quando `gh` estiver ausente ou `gh auth status` falhar, o coletor MUST tentar
  a API publica do GitHub antes de encerrar com erro.
- Uma falha autenticada de acesso a uma issue publica MAY acionar o mesmo
  fallback, desde que erros de permissao e rate limit nao sejam ocultados.
- O fallback MUST usar endpoints oficiais de issue, comentarios e
  timeline/eventos, com headers de API apropriados.
- Os dois transportes MUST produzir o mesmo schema persistido: `provider`,
  `number`, `title`, `description`, `state`, `author`, `url`, `labels` e `log`.
- A ordenacao e deduplicacao de comentarios/timeline MUST permanecer
  deterministicas e equivalentes ao provider autenticado.
- Para repositorio privado, 401/403/404 no transporte publico MUST resultar em
  orientacao para instalar/autenticar o CLI, sem afirmar incorretamente que a
  issue nao existe.
- Rate limit publico MUST ter mensagem distinta, incluindo orientacao para usar
  o caminho autenticado.
- O fallback MUST NOT imprimir, persistir ou solicitar tokens por argumentos de
  linha de comando.
- O arquivo `github-<NNN>.json` e a flag `--extern-issue` MUST manter
  compatibilidade.
- A saida MUST informar qual transporte foi usado, ao menos no modo verbose ou
  no payload do comando, sem alterar desnecessariamente o schema da issue
  externa.
- A implementacao MUST usar cliente HTTP disponivel no pacote ou na biblioteca
  padrao, sem introduzir dependencia em `curl`.

## Acceptance criteria

- [ ] Uma issue GitHub publica e importada quando `gh` nao esta instalado.
- [ ] Uma issue GitHub publica e importada quando `gh auth status` falha.
- [ ] O JSON gerado pelo fallback possui o mesmo contrato do caminho
      autenticado e e aceito por `yoda_intake.py`.
- [ ] Comentarios e timeline/eventos publicos sao normalizados, ordenados e
      deduplicados de forma deterministica.
- [ ] O caminho autenticado continua funcionando para repositorios publicos e
      privados.
- [ ] Uma tentativa publica que nao consegue distinguir privado de inexistente
      orienta autenticacao em vez de emitir conclusao enganosa.
- [ ] Rate limit e falhas de rede possuem erros distintos e acionaveis.
- [ ] Nenhuma credencial aparece em logs, JSON ou mensagens de erro.
- [ ] O help explica o fallback publico e a necessidade de autenticacao para
      repositorios privados.
- [ ] Specs, manual embarcado e README de scripts refletem a estrategia.
- [ ] Testes usam respostas simuladas e nao dependem de internet ou credenciais.
- [ ] Suites de GitHub, GitLab, Intake e scripts permanecem passando.

## Entry points

- `project/specs/26-get-extern-issue-script.md`
- `yoda/yoda.md`
- `yoda/scripts/README.md`
- `yoda/scripts/get_extern_issue.py`
- `yoda/scripts/lib/external_issue_utils.py`
- `yoda/scripts/lib/provider_github.py`
- `yoda/scripts/lib/provider_gitlab.py`
- `yoda/scripts/tests/test_get_extern_issue.py`
- `yoda/project/extern_issues/github-009.json`

## Implementation notes

Fluxo inicial recomendado:

1. detectar provider e repositorio pelo `remote.origin.url` ou
   `YODA_ORIGIN_URL`;
2. se CLI + autenticacao estiverem prontos, usar o provider autenticado atual;
3. se o provider for GitHub e o bloqueio for ausencia/falha de autenticacao,
   tentar os endpoints publicos;
4. se a leitura publica falhar por acesso/nao encontrado, explicar que o
   repositorio pode ser privado e orientar `gh auth login`;
5. normalizar a resposta antes de persistir, mantendo um unico contrato para o
   Intake.

Separar transporte de normalizacao evita duplicar regras de labels, log,
timeline e deduplicacao. O cliente publico deve permitir injecao/mocking de
respostas nos testes. Nao usar o sucesso observado manualmente via `curl` como
dependencia do produto; ele e apenas evidencia de viabilidade.

No Study, decidir se a origem do transporte deve aparecer apenas no payload do
comando/verbose ou como metadata opcional fora do JSON normalizado. Evitar uma
mudanca de schema sem necessidade.

## Tests

- Simular CLI ausente, autenticacao invalida e fallback publico bem-sucedido.
- Simular issue privada/404, 401/403, rate limit e falha de rede.
- Testar equivalencia de payload entre transporte autenticado e publico.
- Testar comentarios, timeline, fallback de events e deduplicacao.
- Garantir que GitLab autenticado nao sofreu alteracao comportamental.
- Executar testes de `get_extern_issue.py`, Intake e suite completa.

## Risks and edge cases

- Limite anonimo da API publica ser menor e causar falhas intermitentes.
- GitHub retornar 404 tanto para recurso inexistente quanto privado, impedindo
  diagnostico conclusivo sem autenticacao.
- Timeline publica exigir header especifico ou diferir do retorno autenticado.
- Fallback silencioso esconder token expirado que o usuario gostaria de
  corrigir; a saida deve informar a degradacao.
- Duplicar normalizacao nos dois transportes e gerar JSONs divergentes.
- Introduzir dependencia externa ausente no pacote distribuido.
- Alterar por acidente o comportamento do provider GitLab.
- Tratar HTML publico como API; somente endpoints JSON oficiais sao aceitos.

## Result log

## Flow log
- 2026-08-31T16:36:09-03:00 issue_add created title=Adicionar fallback publico para coleta de issues externas; priority=5
- 2026-08-31T16:39:50-03:00 Intake concluido sem fonte externa: fallback publico definido com preservacao do acesso autenticado privado
