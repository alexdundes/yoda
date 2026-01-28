# YODA Framework - Specs (en)

This README organizes the topics discussed so far. Each topic has a dedicated file in this folder. The **human entrypoint** for a YODA-enabled project is the repo `README.md`; the **agent entrypoint** is `yoda/yoda.md`.

## Language policy

- project/specs is always in English to improve agent interoperability.
- Other repo content may be in Portuguese during development.
- The final YODA Framework will be published in English; Portuguese content is provisional.

## Topics

00. Conventions (normative language and shared rules)
    - file: `00-conventions.md`
01. YODA Framework overview and principles
    - file: `01-yoda-overview.md`
02. YODA Flow (cycle: Study -> Document -> Implement -> Evaluate)
    - file: `02-yoda-flow-process.md`
03. Document-first, YAML, and Markdown (role of each)
    - file: `03-document-first-yaml-markdown.md`
04. `yoda/todos/TODO.<dev>.yaml` and issues in Markdown (centralized metadata)
    - file: `04-todo-dev-yaml-issues.md`
05. Scripts and automation (`yoda/scripts/`, Python)
    - file: `05-scripts-and-automation.md`
06. Agent playbook and operating rules
    - file: `06-agent-playbook.md`
07. Agent entry and root files (`yoda/yoda.md`, `AGENTS.md`, `gemini.md`)
    - file: `07-agent-entry-and-root-file.md`
08. MCP in the YODA Framework (tool integration)
    - file: `08-mcp-in-yoda.md`
09. Visual identity and logo (minimal favicon)
    - file: `09-visual-identity-logo.md`
10. Approaches and references (DocDD, Docs-as-Code, RDD, ADRs, etc.)
    - file: `10-approaches-and-references.md`
10. Influences (details for each approach)
    - folder: `influences/` (one file per influence)
12. YODA minimum structure
    - file: `12-yoda-structure.md`
13. YODA scripts v1 specification
    - file: `13-yoda-scripts-v1.md`
14. Issue templates usage guide
    - file: `14-issue-templates-usage.md`
15. Python structure for YODA scripts
    - file: `15-scripts-python-structure.md`
16. `todo_list.py` specification
    - file: `16-todo-list-script.md`
17. `todo_reorder.py` specification
    - file: `17-todo-reorder-script.md`
18. `issue_add.py` specification
    - file: `18-issue-add-script.md`
19. `log_add.py` specification
    - file: `19-log-add-script.md`
20. `todo_update.py` specification
    - file: `20-todo-update-script.md`
21. `todo_next.py` specification
    - file: `21-todo-next-script.md`
22. Out of scope (v1)
    - file: `22-out-of-scope.md`
99. Decision summary (not part of the numbered spec sequence)
    - file: `summary.md`
