---
schema_version: '2.01'
status: done
title: Adicionar fallback publico para coleta de issues externas
description: Permitir que get_extern_issue.py consulte APIs publicas sem autenticacao
  quando a issue pertence a um repositorio publico e o CLI autenticado estiver indisponivel
  ou sem sessao valida, preservando o acesso autenticado atual para repositorios privados
  e mantendo o mesmo contrato JSON do YODA Intake.
priority: 5
created_at: '2026-08-31T16:36:09-03:00'
updated_at: '2026-08-31T17:54:32-03:00'
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
- Quando uma leitura autenticada do GitHub falhar por autenticacao ou permissao,
  o coletor MUST tentar o mesmo fallback publico e MUST preservar contexto
  acionavel sobre os dois transportes caso nenhum deles tenha sucesso.
- Falhas de rede, payload invalido e rate limit no transporte autenticado MUST
  NOT ser convertidas silenciosamente em fallback publico.
- O fallback MUST usar endpoints oficiais de issue, comentarios e
  timeline/eventos, enviando `User-Agent`,
  `Accept: application/vnd.github+json` e versao explicita da API.
- O fallback publico desta entrega MUST ser limitado a `github.com`; hosts de
  GitHub Enterprise continuam dependendo do transporte autenticado por `gh`.
- Os dois transportes MUST produzir o mesmo schema persistido: `provider`,
  `number`, `title`, `description`, `state`, `author`, `url`, `labels` e `log`.
- A ordenacao e deduplicacao de comentarios/timeline MUST permanecer
  deterministicas e equivalentes ao provider autenticado.
- Os dois transportes MUST manter nesta entrega o limite atual de ate 100 itens
  por endpoint. Paginacao completa exige uma mudanca futura aplicada aos dois
  transportes para nao criar contratos divergentes.
- O fallback entre os endpoints de timeline e events MUST ignorar apenas a
  indisponibilidade especifica do endpoint. Falhas de rede, autenticacao,
  permissao e rate limit MUST permanecer visiveis.
- Para repositorio privado, 401/403/404 no transporte publico MUST resultar em
  orientacao para instalar/autenticar o CLI, sem afirmar incorretamente que a
  issue nao existe.
- Rate limit publico MUST ter mensagem distinta, incluindo orientacao para usar
  o caminho autenticado.
- O fallback MUST NOT imprimir, persistir ou solicitar tokens por argumentos de
  linha de comando.
- O arquivo `github-<NNN>.json` e a flag `--extern-issue` MUST manter
  compatibilidade.
- A saida normal e o modo verbose MUST informar `authenticated-cli` ou
  `public-http` no payload do comando, sem acrescentar esse detalhe ao JSON
  persistido da issue externa.
- A implementacao MUST usar `urllib` da biblioteca padrao, com timeout e pontos
  de injecao para testes, sem introduzir dependencia em `curl`.

## Acceptance criteria

- [x] Uma issue GitHub publica e importada quando `gh` nao esta instalado.
- [x] Uma issue GitHub publica e importada quando `gh auth status` falha.
- [x] O JSON gerado pelo fallback possui o mesmo contrato do caminho
      autenticado e e aceito por `yoda_intake.py`.
- [x] Comentarios e timeline/eventos publicos sao normalizados, ordenados e
      deduplicados de forma deterministica.
- [x] Os dois transportes preservam o limite atual de ate 100 itens por
      endpoint, sem implementar paginacao parcial em apenas um deles.
- [x] O caminho autenticado continua funcionando para repositorios publicos e
      privados.
- [x] Uma tentativa publica que nao consegue distinguir privado de inexistente
      orienta autenticacao em vez de emitir conclusao enganosa.
- [x] Rate limit e falhas de rede possuem erros distintos e acionaveis.
- [x] Falhas de timeline/events nao ocultam rate limit, rede ou permissao.
- [x] Nenhuma credencial aparece em logs, JSON ou mensagens de erro.
- [x] O help explica o fallback publico e a necessidade de autenticacao para
      repositorios privados.
- [x] Specs, manual embarcado e README de scripts refletem a estrategia.
- [x] Testes usam respostas simuladas e nao dependem de internet ou credenciais.
- [x] Suites de GitHub, GitLab, Intake e scripts permanecem passando.

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

Fluxo aprovado:

1. detectar provider e repositorio pelo `remote.origin.url` ou
   `YODA_ORIGIN_URL`;
2. se CLI + autenticacao estiverem prontos, usar o provider autenticado atual;
3. se o provider for `github.com` e o bloqueio for ausencia do CLI, falha de
   autenticacao ou permissao, tentar os endpoints publicos;
4. se a leitura publica falhar por acesso/nao encontrado, explicar que o
   repositorio pode ser privado e orientar `gh auth login`;
5. normalizar a resposta antes de persistir, mantendo um unico contrato para o
   Intake.

Separar transporte de normalizacao evita duplicar regras de labels, log,
timeline e deduplicacao. `provider_github.py` deve oferecer os transportes
autenticado e publico sobre os mesmos helpers de normalizacao; o orquestrador
seleciona o transporte e inclui sua origem no payload do comando. O cliente
publico deve permitir injecao/mocking de respostas nos testes. Nao usar o
sucesso observado manualmente via `curl` como dependencia do produto; ele e
apenas evidencia de viabilidade.

O JSON persistido continua deliberadamente independente do transporte. Isso
preserva o contrato consumido pelo Intake e evita bump de schema por um detalhe
operacional da coleta.

## Tests

- Simular CLI ausente, autenticacao invalida e fallback publico bem-sucedido.
- Simular issue privada/404, 401/403, rate limit e falha de rede.
- Verificar `User-Agent`, `Accept`, versao da API, timeout e ausencia de token
  no transporte publico.
- Testar equivalencia de payload entre transporte autenticado e publico.
- Testar comentarios, timeline, fallback de events e deduplicacao.
- Provar que erros de rate limit, rede e permissao da timeline nao sao
  engolidos pelo fallback de endpoint.
- Provar que GitHub Enterprise nao usa o fallback publico de `github.com`.
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

## Study findings

- O bloqueio atual e anterior ao fetch: `ensure_cli_and_auth()` encerra a
  operacao mesmo quando todos os dados pedidos estao publicamente acessiveis.
- Transporte e normalizacao estao acoplados em `provider_github.py`; duplicar o
  provider para HTTP criaria risco direto de JSONs e logs divergentes.
- A API REST do GitHub permite leitura anonima de issue, comentarios e timeline
  de recursos publicos, mas exige headers adequados e aplica limite anonimo
  significativamente menor que o autenticado.
- Respostas `403` e `429` podem representar rate limit. `404` nao distingue com
  seguranca recurso inexistente de recurso privado sem acesso.
- O fallback atual de timeline para events captura qualquer `YodaError`, o que
  pode esconder rede, permissao e rate limit em vez de apenas degradar quando
  um endpoint nao estiver disponivel.
- O provider autenticado pede `per_page=100`, mas nao percorre paginacao. Dar
  paginacao completa somente ao transporte publico quebraria a equivalencia
  desta entrega.
- O provider GitLab tem transporte e contrato proprios e nao precisa mudar para
  que o fallback publico de `github.com` seja entregue.

## Document contract

O Implement deve seguir este contrato document-first e nao introduzir novas
decisoes de produto sem retornar ao humano.

Decisoes aprovadas no encerramento do Study:

1. O caminho autenticado por `gh` e preferencial. O HTTP publico e fallback
   para CLI ausente, sessao invalida ou falha autenticada de permissao.
2. O cliente publico usa `urllib`, headers oficiais, timeout e nenhum token.
3. O fallback publico fica restrito a `github.com`; GitHub Enterprise e GitLab
   preservam os respectivos caminhos autenticados.
4. O limite existente de 100 itens por endpoint permanece simetrico. Paginacao
   completa fica fora desta entrega.
5. O transporte aparece como `authenticated-cli` ou `public-http` no payload e
   na apresentacao do comando, nunca no JSON persistido da issue externa.
6. `404` publico e reportado como nao encontrado ou nao acessivel publicamente,
   com orientacao para autenticar; rate limit e falhas de rede ficam distintos.
7. Timeline/events so degradam entre endpoints por indisponibilidade especifica
   e nao podem ocultar rede, autenticacao, permissao ou rate limit.
8. Testes simulam subprocesso e HTTP, sem rede real, e demonstram equivalencia
   de normalizacao, ausencia de credenciais e preservacao do GitLab.

### 1. Contrato normativo e documentacao distribuida

- Atualizar `project/specs/26-get-extern-issue-script.md` com selecao de
  transporte, limite de host, headers, erros, visibilidade do transporte e
  preservacao do schema persistido. O texto deve ser autocontido e nao depender
  desta issue como autoridade normativa.
- Atualizar `yoda/yoda.md` e `yoda/scripts/README.md` com a mesma orientacao
  operacional compacta, pois o produto empacotado nao inclui as specs.
- Alinhar o `--help` de `get_extern_issue.py` ao fallback publico e a exigencia
  de autenticacao para repositorios privados.

### 2. Provider GitHub

- Refatorar `provider_github.py` para compartilhar normalizacao, ordenacao e
  deduplicacao entre o transporte `gh api` e o HTTP publico.
- Implementar o cliente `urllib` injetavel, headers obrigatorios, timeout,
  leitura de erro HTTP e classificacao de rate limit.
- Manter issue/comments/timeline-events com `per_page=100` e impedir que o
  fallback de endpoint engula classes de erro nao recuperaveis.

### 3. Orquestracao e compatibilidade

- Fazer `get_extern_issue.py` preferir autenticacao e selecionar o fallback
  somente nas condicoes aprovadas, retornando o transporte no payload.
- Ajustar `external_issue_utils.py` para que a sondagem de CLI/autenticacao
  informe disponibilidade sem bloquear antecipadamente o fallback GitHub.
- Preservar nome de arquivo, flags, schema persistido, comportamento de pull
  requests aceitos pelo endpoint de issues e provider GitLab.

### 4. Verificacao

- Expandir os testes de provider e comando com clientes simulados para todos os
  cenarios dos Acceptance criteria.
- Rodar a suite de scripts e os testes de projeto, conferir `--help` contra a
  spec 26 e validar a documentacao empacotada sem acesso a `project/specs/`.

## Result log

feat: adicionar fallback publico para coleta de issues externas do GitHub

Permitiu que `get_extern_issue.py` importe issues publicas de `github.com` sem
autenticacao quando o `gh` esta ausente, a sessao nao esta valida, ou uma
leitura autenticada falha especificamente por autenticacao/permissao. O
transporte autenticado continua preferencial e permanece obrigatorio para
repositorios privados, GitHub Enterprise e GitLab.

O fallback usa `urllib` da biblioteca padrao com timeout e ponto de injecao para
testes, enviando `User-Agent`, `Accept: application/vnd.github+json` e versao
explicita da API, sem token. Os dois transportes compartilham a mesma
normalizacao, ordenacao, deduplicacao e o limite de 100 itens por endpoint, de
modo que o JSON persistido e identico e continua aceito pelo YODA Intake.

Falhas de rede, payload invalido e rate limit no transporte autenticado nao sao
convertidas em fallback silencioso. O fallback entre timeline e events ignora
apenas a indisponibilidade do endpoint, mantendo visiveis erros de rede,
permissao e rate limit. Um `401`, `403` ou `404` publico nao afirma ausencia da
issue: orienta autenticar o CLI. Quando os dois transportes falham, a mensagem
relata separadamente a causa de cada um.

Nenhuma credencial aparece em logs, JSON ou mensagens: o `stderr` do CLI passou
a ser usado apenas para classificar o erro, nunca para compor texto exibido. O
payload do comando informa `authenticated-cli` ou `public-http`, sem acrescentar
esse campo ao JSON persistido.

Evaluate: tres achados corrigidos nesta fase, sendo um bloqueante contra o
requisito de preservar contexto acionavel dos dois transportes, mais a cobertura
ausente do ramo de CLI nao instalado e a demonstracao do schema do Intake.
`98 passed` em `yoda/scripts/tests`, `17 passed` em `project/tests` e
`git diff --check` sem erros.

- **Issue**: `yoda-0067`

- **Path**: `yoda/project/issues/yoda-0067-adicionar-fallback-publico-para-coleta-de-issues-externas.md`

## Flow log
- 2026-08-31T16:36:09-03:00 issue_add created title=Adicionar fallback publico para coleta de issues externas; priority=5
- 2026-08-31T16:39:50-03:00 Intake concluido sem fonte externa: fallback publico definido com preservacao do acesso autenticado privado
- 2026-08-31T17:18:09-03:00 transition to-do->doing/study | YODA Flow iniciado para estudar fallback publico com preservacao do acesso autenticado
- 2026-08-31T17:23:38-03:00 transition doing/study->doing/document | Study aprovado: documentar fallback publico GitHub com transporte autenticado preferencial
- 2026-08-31T17:27:16-03:00 transition doing/document->doing/implement | Document aprovado: implementar fallback publico GitHub conforme contrato fechado
- 2026-08-31T17:43:29-03:00 transition doing/implement->doing/evaluate | Evaluate iniciado: revisao do fallback publico, transporte, seguranca e sincronizacao documental
- 2026-08-31T17:54:32-03:00 transition doing/evaluate->done | Evaluate aprovado: fallback publico restrito a github.com, transportes com schema identico e contexto acionavel preservado
