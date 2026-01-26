# YODA Framework

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="yoda/favicons/yoda-dark.svg">
  <img src="yoda/favicons/yoda-light.svg" alt="YODA Framework Logo" width="256" height="256">
</picture>

> **YODA Framework — YAML-Oriented Documentation & Agents**  
> Framework document-first para desenvolvimento assistido por agents, com documentacao em YAML/Markdown como fonte de verdade.

## O que e o YODA Framework?

O **YODA Framework** organiza projetos (codigo, documentacao e automacoes) em torno de tres ideias:

1. **Documentacao como fonte de verdade**  
   Antes do codigo, um documento descreve o que fazer, por que e em qual ordem.

2. **YAML como camada estrutural**  
   Arquivos YAML mantem o estado estruturado do projeto: TODOs, issues, flows, agents e contextos.  
   Sao legiveis por humanos, scripts e agents.

3. **Agents e flows que agem sobre a documentacao**  
   Scripts e agents leem esses arquivos, decidem e atualizam codigo e docs.  
   O agent le o contexto no YODA.

O objetivo:

- Humanos escrevem e ajustam a visao do projeto em arquivos simples.
- Agents e scripts usam essa visao como input confiavel.
- O fluxo de trabalho permanece repetivel, auditavel e compartilhavel.

## Por que o nome YODA?

### Versao oficial da sigla

> **YODA = YAML-Oriented Documentation & Agents**

- **Y - YAML**  
  O projeto e YAML-first: o estado operacional fica em arquivos `.yaml`.

- **O - Oriented**  
  Tudo e orientado por esses arquivos, sem limitar o framework a apenas YAML.

- **D - Documentation**  
  A documentacao e o centro. Codigo e agents giram em torno dela.

- **A - Agents**  
  Agents, scripts ou servicos que leem/alteram os docs e executam acoes.

## Filosofia do YODA Framework

### 1. Document-First Design

- Tudo comeca em um documento: feature, fluxo, regra de negocio, decisao tecnica.
- A documentacao define objetivos, restricoes, criterios de aceitacao e contexto historico.
- O codigo e consequencia, nao o primeiro passo.

### 2. YAML como camada de controle

- YAML e usado para representar:
  - `TODO.<dev>.yaml` por pessoa (backlog e metadados)
  - Metadados de issues (no `TODO.<dev>.yaml`)
  - Flows de agents (quem faz o que, em qual ordem)
  - Configuracoes de contexto (escopos, tenants, ambientes)
- Scripts e agents leem esses YAMLs para:
  - Gerar/atualizar Markdown
  - Sugerir codigo
  - Orquestrar issues

### 3. Markdown como camada narrativa

- Markdown e usado para:
  - Explicar a interface (UI/UX)
  - Documentar decisoes (estilo ADR)
  - Escrever issues em linguagem natural
  - Manuais e guias
- Uma issue pode ter:
  - Metadados centralizados no `TODO.<dev>.yaml`
  - Descricao detalhada em um arquivo `.md` separado

### 4. Agent como copiloto, nao como oraculo

- O agent nao inventa contexto; ele le do YODA.
- O YODA Framework organiza o contexto (docs + YAML) e define como ler e escrever nesses arquivos.
- Isso reduz alucinacoes e aumenta repetibilidade e auditabilidade.

### 5. Multi-agent, multi-ferramenta

- O YODA nao depende de um unico agent ou modelo.
- Voce pode ter agents especialistas (backend, frontend, docs), todos lendo e escrevendo estruturas padronizadas.

## YODA Flow

O ciclo basico e:

1) Study (Estudar): entender o contexto e as restricoes.  
2) Document (Documentar): capturar intencao e estrutura em YAML/Markdown.  
3) Implement (Implementar): executar com base no plano documentado.  
4) Evaluate (Avaliar): validar resultados e refinar os docs (iterar quando necessario).

O YODA Flow e simples, repetivel e scriptavel.

## Artefatos e fonte de verdade

A direcao atual define um backlog YAML por pessoa como fonte canonica de metadados, com Markdown para detalhe narrativo.

- `TODO.<dev>.yaml` guarda metadados estruturados, ordem de execucao e contexto de planejamento.
- Issues ficam em `yoda/project/issues/dev-id-slug.md` (um arquivo por issue).
- O arquivo Markdown da issue usa o ID no titulo.

Scripts podem gerar esqueletos Markdown a partir do YAML e produzir resumos para agents quando necessario.

## Estado atual desta meta-implementacao

- `project/specs/` descreve o YODA Framework futuro e e a fonte da verdade.
- `yoda/` e a implementacao em construcao desses specs e pode estar incompleta.
- Enquanto os scripts nao existem, este repo usa Markdown como excecao temporaria:
  - TODOs em `yoda/todos/TODO.<dev>.md`
  - Logs em `yoda/logs/dev-id-slug.md`
- Bootstrap e provisório; a documentacao e os specs focam a fase futura nao-bootstrap, com excecoes marcadas como bootstrap.

## Entrada do agent

- Arquivo raiz do agent: `yoda/yoda.md`.
- `AGENTS.md` ou `gemini.md` apontam para esse arquivo.
- A entrada pode ser uma frase natural indicando entrar no YODA Flow e pegar a issue prioritaria sem dependencias.
  - A frase deve mencionar "YODA Flow" (ou "YODA") e a intencao de pegar a issue de maior prioridade sem dependencias.
- Se o TODO esperado nao existir, o agent pergunta qual TODO usar (padrao: `yoda/todos/TODO.alex.md`).

## Automacao (conceitual)

O YODA espera scripts leves que:

- leiam `TODO.<dev>.yaml` e gerem Markdown ou resumos para agents
- validem estrutura e status dos itens
- padronizem a estrutura do projeto antes de humanos ou agents editarem

Os scripts ficam em `yoda/scripts`, sao feitos em Python e o nome do arquivo e o comando (ex.: `init.py`).
Logs do ciclo ficam em `yoda/logs/dev-id-slug.yaml` no framework final.
Nesta meta-implementacao, usamos `yoda/logs/dev-id-slug.md` ate os scripts existirem.

## Formato de commit

- Primeira linha: conventional commit message.
- Corpo:
  - Issue: `<ID>`
  - Path: `<issue path>`

Detalhes de CLI e tooling estao definidos em `project/specs/13-yoda-scripts-v1.md` e `project/specs/05-scripts-and-automation.md`.

## Escopo e posicionamento

Audiencia primaria: solo devs (1 humano + 1 agent) usando o YODA Flow.  
Posicionamento: framework de apoio ao desenvolvimento assistido por agents, com issues versionadas junto ao codigo do projeto.  
Escopo: framework de processos de uso geral para quem precisa de maior controle no desenvolvimento apoiado por agents.  
Limites de escopo (v1) estao definidos em `project/specs/16-out-of-scope.md`.

Detalhes de implementacao (CI/CD, padroes de arquitetura, etc.) ficam fora deste README e sao definidos por projeto.

## Status

O framework esta em definicao ativa, com decisoes consolidadas em `project/specs` e resumidas em `project/specs/summary.md`.
MCP esta previsto como implementacao futura (v2).
