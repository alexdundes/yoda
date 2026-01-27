# Dicas do ChatGPT (refinamentos sugeridos)

Este arquivo registra refinamentos sugeridos apos revisar o ZIP mais recente. Nao sao pendencias, mas melhorias para reduzir edge cases e ambiguidades no YODA Framework.

## Contexto geral

- O `project/specs/` esta consistente e agent-ready.
- Correcoes de id canonico (`<dev>-<NNNN>`), naming `<id>-<slug>`, paths (`yoda/todos/...`), regra deterministica do `todo_next`, contrato CLI e templates estao alinhadas.
- Um agente ja consegue implementar os scripts v1 sem inferencia excessiva.

## Refinamentos sugeridos (nao implementar agora)

1) Imutabilidade do `slug`
- Definir explicitamente que o `slug` nao muda depois que a issue e criada, mesmo se o `title` mudar.
- Justificativa: evita renames de arquivos/logs e inconsistencias.
- Onde: `project/specs/04-todo-dev-yaml-issues.md` e `project/specs/13-yoda-scripts-v1.md` (impacto em `issue_render`).

2) Como o `log_add.py` descobre o `<slug>`
- Especificar que `log_add.py` deve buscar o `slug` no TODO a partir do issue id.
- Se nao encontrar, deve retornar erro `3`.
- Onde: `project/specs/13-yoda-scripts-v1.md` (secao `log_add.py`).

3) Definir o formato JSON minimo por script
- O contrato ja aceita `--format md|json`, mas falta definir campos minimos do JSON.
- Adicionar um exemplo por script (especialmente `todo_next`, `todo_list`, `todo_update`).
- Onde: `project/specs/13-yoda-scripts-v1.md` (subsecao "JSON output (minimal)").

4) Adicionar um "Happy path" end-to-end (1 pagina)
- Sequencia sugerida: `init -> issue_add -> todo_next -> (Document/Implement) -> todo_update -> log_add -> todo_update done`.
- Ajuda agentes a entenderem o fluxo sem inferencia.
- Onde: novo arquivo `project/specs/17-examples-happy-path.md` ou dentro de `project/specs/06-agent-playbook.md`.

5) Pequeno ajuste de Markdown
- Em `project/specs/02-yoda-flow-process.md` ha um bullet indentado errado ("Next issue selection...").
- Ajuste apenas de renderizacao/leitura.


## Observacao final

Aplicar apenas os itens 1 a 3 ja elimina praticamente todos os edge cases que costumam gerar divergencia em agentes e scripts.
