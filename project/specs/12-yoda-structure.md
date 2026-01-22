# YODA Framework - Minimum Structure

This document defines the minimum folder and file structure for a YODA Framework project.

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
│  │  └─ TODO.<dev>.yaml       # Canonical TODO format (bootstrap may use Markdown)
│  └─ project/
│     └─ issues/              # Issue files (dev-id-slug.md)
└─ project/
   └─ specs/                  # YODA framework specs (source of truth)
```

## Path purposes

- yoda/yoda.md: root entry for agents in this repository.
- yoda/templates/: issue templates used by agents.
- yoda/scripts/: scripts that manage TODOs, logs, and scaffolding.
- yoda/logs/: per-issue logs (YAML by default).
- yoda/todos/: canonical TODO storage (YAML by default; bootstrap may use Markdown).
- yoda/project/issues/: issue files, one per issue, named dev-id-slug.md.
- project/specs/: official specs and decision source of truth.

## Notes

- In the general framework, TODOs are YAML (TODO.<dev>.yaml).
- In this meta-implementation, TODOs are Markdown until scripts exist.
