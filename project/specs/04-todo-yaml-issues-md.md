# TODO.dev.yaml e issues em Markdown

## Objetivo

Separar o backlog e metadados das descricoes ricas das issues.

## Direcao preferida

- Um TODO por pessoa, no formato TODO.dev.yaml (dev = slug do desenvolvedor).
- Cada issue possui um arquivo Markdown proprio em yoda/project/issues/.
- O TODO.dev.yaml referencia o caminho do arquivo Markdown de cada issue.
- Os arquivos de issue contem apenas descricao livre (contexto, criterios, notas).
- Um script cria a issue e o esqueleto inicial do Markdown.

## Local e padrao de nome

- Pasta de issues: yoda/project/issues/
- Nome do arquivo: dev-id-slug.md
  - dev = slug do desenvolvedor
  - id = sequencial gerado pelo script do TODO
  - slug = slug do title

## Schema minimo do TODO.dev.yaml

Cada item de issue deve conter:

- id: sequencial gerado pelo script
- title: titulo da issue
- slug: slug do title (usado no nome do arquivo)
- description: breve descricao do que precisa ser feito
- entrypoints: array de objetos com:
  - path: caminho do arquivo (issue ou outro artefato)
  - type: tipo do entrypoint (issue, code, outros no futuro)
- status: to-do | doing | do-it | pending
- priority: 0 a 10 (10 = mais prioritario)
- labels: lista de rotulos
- agent: Human | Codex | Antigravity | ...
- depends_on: lista de ids
- pending_reason: motivo da pendencia (quando status = pending)
- created_at, updated_at

Observacao: nao existe owner, pois cada dev possui seu proprio TODO.

## Status (definicoes)

- to-do: criado, ainda nao iniciado
- doing: iniciado no YODA Flow da issue
- do-it: ciclo do YODA Flow finalizado
- pending: impedimento identificado durante o YODA Flow; registrar o motivo em pending_reason e manter em stand-by ate resolver

## Vantagens

- Fonte unica de verdade para o estado do trabalho.
- Operacoes em massa ficam simples (listar, filtrar, reordenar).
- Economia de tokens ao enviar apenas TODO.dev.yaml para planejamento.
- Markdown livre para escrita de qualidade.

## Identificador minimo

O arquivo Markdown da issue deve ter um identificador minimo para ligar ao TODO.dev.yaml, por exemplo:

- Usar o ID no titulo do arquivo Markdown.

## Observacoes

- A IA nao deve editar TODO.dev.yaml diretamente; deve chamar scripts.
- A IA pode editar livremente o texto da issue.
