# YODA Framework - Minimum Structure

Defines the minimum folder and file structure for a YODA Framework project.

## Required structure

```
.
├─ yoda/
│  ├─ yoda.md                 # Root agent instructions
│  ├─ templates/
│  │  ├─ issue.md             # Standard issue template
│  │  └─ issue-lightweight-process.md
│  ├─ scripts/                # Python scripts (file name = command)
│  ├─ logs/                   # One log per issue
│  ├─ todos/
│  │  └─ TODO.<dev>.yaml       # Canonical TODO at yoda/todos/TODO.<dev>.yaml (bootstrap may use Markdown)
│  └─ project/
│     └─ issues/              # Issue files (<id>-<slug>.md)
└─ project/
   └─ specs/                  # YODA framework specs (source of truth)
```

## Path purposes

- `yoda/yoda.md`: root entry for agents in this repository.
- `yoda/templates/`: issue templates used by agents.
- `yoda/scripts/`: scripts that manage TODOs, logs, and scaffolding.
- `yoda/logs/`: one log per issue (YAML by default, named `<id>-<slug>.yaml`).
- `yoda/todos/`: canonical TODO storage (YAML by default; bootstrap may use Markdown).
- `yoda/project/issues/`: issue files, one per issue, named `<id>-<slug>.md`.
- `project/specs/`: official specs and decision source of truth.

## Notes

- In the general framework, TODOs are YAML (`yoda/todos/TODO.<dev>.yaml`).
- In this meta-implementation, TODOs are Markdown until scripts exist (see Appendix: Bootstrap in `project/specs/15-bootstrap.md`).
- Each developer edits only their own TODO file; conflicts are resolved manually if they occur.
- Log files use YAML in the framework and follow the required fields in `project/specs/05-scripts-and-automation.md`.
