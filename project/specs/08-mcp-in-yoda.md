# MCP in the YODA Framework (v2)

## What is MCP

Model Context Protocol (MCP) connects agents to external tools and data.

## Fit in YODA (future)

- MCP can expose YODA scripts as standardized tools.
- A workspace MCP server can read docs, TODOs, and apply patches.
- Any compatible agent can use these tools without custom integration.

## Benefits

- Interoperability across agents and platforms.
- Standardized tools and schemas.
- Easier governance and security in multi-tenant environments.

## Risks

- Adds initial complexity.
- Requires careful permission and tool scope control.

## Suggested MVP (v2)

- Minimal tools: todos.list, docs.read, workspace.apply_patch.
- Add business tools later (fidc, cnpj, etc.).
