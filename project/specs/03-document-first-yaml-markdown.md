# Document-first, YAML, and Markdown

## Document-first

- Documentation comes before implementation.
- Code is the consequence of what is documented.
- The AI must follow the documentation, not informal conversation.

## YAML

- Used for metadata and structures that scripts must read.
- Example: backlog in `yoda/todos/TODO.<dev>.yaml`, agent configuration.
- Enables automation and structured queries.

## Markdown

- Used for rich free text.
- Example: issues in Markdown (one file per issue), UI specs, business explanations.
- It is the main reading layer for humans and AI.
- Issue files must include YAML front matter for metadata (mirrors TODO issue fields).

## Adopted direction

- YAML is the source of truth for metadata.
- Markdown for narrative and details.
- Scripts generate skeletons and keep consistency.
 
## Guardrails

- If the issue is ambiguous, return to Document before coding.
- Do not invent files or paths; verify the repo structure first.
- Any change to project/specs must be tracked by an issue.
