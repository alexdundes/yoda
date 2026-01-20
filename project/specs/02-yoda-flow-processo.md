# YODA Flow (processo)

## Ciclo base

O YODA Flow e o ciclo de trabalho padrao do framework:

1) Estudar
2) Documentar
3) Implementar
4) Avaliar e iterar

## Detalhamento por etapa

### 1) Estudar

- Conversa livre entre humano e IA.
- Foco em entendimento de contexto, regras e restricoes.
- Nenhuma entrega formal e gerada nesta etapa.
- Ao final, a IA deve estar pronta para documentar uma issue (arquivo Markdown).

### 2) Documentar

- A IA cria ou atualiza o arquivo Markdown da issue, conforme o que foi discutido.
- O humano revisa e corrige o texto para eliminar ambiguidades.
- A issue (arquivo Markdown) vira o contrato oficial para a implementacao.

### 3) Implementar

- A IA implementa apenas o que esta definido no arquivo Markdown da issue.
- Se algo mudar, volta-se a etapa de documentar para atualizar o arquivo Markdown da issue.

### 4) Avaliar e iterar

- O humano valida o resultado.
- A IA corrige codigo e documentacao conforme o feedback.
- Ao final, a issue recebe um resumo do que foi feito e uma sugestao de mensagem de commit.

## Observacoes

- O ciclo e pensado para ser iterativo e nao waterfall.
- Processo leve: nao inclui a etapa Estudar; a IA segue a issue preliminar diretamente.
