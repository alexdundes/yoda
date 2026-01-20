# Scripts e automacao

## Objetivo

Padronizar tarefas repetitivas e reduzir a necessidade de edicoes manuais.

## Local e linguagem

- Pasta: yoda/scripts
- Linguagem: Python
- Regra: o nome do arquivo .py e o nome do comando

## Scripts minimos (v1)

- init.py: cria a estrutura minima do YODA Framework
- scripts de manutencao do TODO.dev.yaml (listar, atualizar, reordenar, etc.)
- scripts para mostrar o TODO.dev.yaml de forma amigavel para humanos e agentes
- scripts de log (quando aplicavel) para registrar eventos do fluxo
- script de resolucao de pendencia (atualiza pending -> status definido e limpa pending_reason)

## Logs

- Padrao do framework: log por issue em yoda/logs/dev-id-slug.yaml
- Excecao neste projeto (meta-implementacao): logs em Markdown, um por issue, em yoda/logs/dev-id-slug.md

## Principios

- Scripts sao a forma oficial de mudar metadados.
- O humano ou orquestrador executa os comandos.

## Beneficios

- Consistencia de estrutura.
- Menos erros na manipulacao de metadados.
- Facilita auditoria e reproduzibilidade.
