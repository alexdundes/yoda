# Playbook do agente

## Objetivo

Definir como a IA deve agir no YODA Framework em cada etapa do fluxo.

## Fases

### Estudar

- Fazer perguntas e entender contexto.
- Nao gerar codigo nem editar arquivos.
- Produzir resumos quando solicitado.

### Documentar

- Criar ou atualizar o arquivo Markdown da issue.
- Gerar esqueleto via script, se existir.
- Priorizar clareza, escopo e criterios.

### Implementar

- Ler o arquivo Markdown da issue e o codigo existente.
- Implementar apenas o que esta documentado.
- Usar scripts para criar estrutura quando necessario.

### Avaliar

- Receber feedback humano.
- Corrigir codigo e atualizar o arquivo Markdown da issue.
- Sugerir mensagem de commit ao final.
- Incluir o texto do commit na issue e exibir em tela.
- Registrar log do ciclo em yoda/logs/dev-id-slug.yaml.
- Excecao neste projeto (meta-implementacao): usar yoda/logs/dev-id-slug.md.
- Se surgir impedimento, marcar status como pending e registrar o motivo no TODO.dev.yaml; usar o script de resolucao de pendencia quando liberado.

## Regras gerais

- Sempre manter a issue (arquivo Markdown) como fonte de verdade.
- Nunca editar TODO.dev.yaml diretamente.
- Preferir perguntas quando houver ambiguidade.
