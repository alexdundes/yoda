# MCP no YODA Framework (v2)

## O que e MCP

Model Context Protocol (MCP) e um protocolo para conectar agentes a ferramentas e dados externos.

## Encaixe no YODA (futuro)

- MCP pode expor os scripts do YODA como ferramentas padronizadas.
- Um MCP server de workspace permite ler docs, TODOs e aplicar patches.
- Qualquer agente compatível pode usar essas ferramentas sem integracao especifica.

## Beneficios

- Interoperabilidade entre agentes e plataformas.
- Padronizacao de tools e schemas.
- Facilita governanca e segurança em ambientes multi-tenant.

## Riscos

- Aumenta a complexidade inicial.
- Exige cuidado com permissao e escopo das tools.

## MVP sugerido (v2)

- Tools minimas: todos.list, docs.read, workspace.apply_patch.
- Adicionar tools de negocio depois (fidc, cnpj, etc.).
