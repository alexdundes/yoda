# Entrada do agente e arquivo raiz

## Problema

Nao existe consenso entre ferramentas de agentes sobre qual arquivo ler (AGENTS.md, gemini.md, etc.).

## Proposta YODA

- Arquivo raiz: yoda/yoda.md.
- Esse arquivo contem as instrucoes do agente no projeto.
- O init cria AGENTS.md ou gemini.md apontando para yoda/yoda.md.

## Interoperabilidade

- AGENTS.md (Codex) e gemini.md (Gemini CLI / anti-gravity) apenas encaminham para yoda/yoda.md.

## Fluxo de entrada simplificado

1) Usuario inicia o agente com contexto zero.
2) Usuario digita uma frase natural indicando entrar no YODA Flow e pegar a issue prioritaria sem dependencias.
3) Agente le yoda/yoda.md.
4) Agente carrega o TODO.dev.yaml correspondente e segue o fluxo.
