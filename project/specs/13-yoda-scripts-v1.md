# YODA Framework - Scripts v1 Specification

This document defines the minimum script interface for YODA v1. Scripts live in yoda/scripts and are executed by their file name (file name = command).

## Naming

- Script path: yoda/scripts/`<name>.py`
- Command name: `<name>.py`

## Developer selection

Scripts that read TODO files MUST resolve the developer slug using:

1) --dev `<slug>` flag
2) YODA_DEV environment variable
3) Interactive prompt when not defined

Slug format:
- Lowercase ASCII, digits, and hyphens only.
- Must start with a letter and contain no spaces.

## Required scripts

### init.py

Purpose:
- Create the minimum YODA project structure.

Behavior (minimum):
- Ensure required folders exist.
- Create yoda/yoda.md if missing (template placeholder or instructions).
- Create templates folder and issue templates if missing.
- Create logs folder.

Inputs:
- Optional project name or output root.

Outputs:
- Created folders and files.

---

### issue_add.py

Purpose:
- Create a new issue entry in `TODO.<dev>.yaml` and generate the issue Markdown from the template.

Behavior (minimum):
- Generate the next sequential id.
- Create `TODO.<dev>.yaml` entry with basic fields.
- Create the issue Markdown file from the template.
- Fill basic fields in the template (id, title, summary) based on agent-provided inputs.

Inputs:
- Title, description or summary, labels, priority, agent, entrypoints.

Outputs:
- Updated `TODO.<dev>.yaml` and new issue Markdown file.

---

### issue_render.py

Purpose:
- Render or re-render an issue Markdown file from the template.

Behavior (minimum):
- Load the issue data from `TODO.<dev>.yaml` or provided inputs.
- Apply the selected template.
- Preserve or re-apply required fields (id, title, summary).

Inputs:
- Issue id.
- Template path (optional).

Outputs:
- Updated issue Markdown file.

---

### todo_list.py

Purpose:
- List TODO items from `TODO.<dev>.yaml`.

Behavior (minimum):
- Filter by status, priority, agent, or labels.
- Output a human-readable summary and a machine-friendly list.

Inputs:
- TODO file path (default: `TODO.<dev>.yaml`).
- --dev `<slug>` (optional, see Developer selection).
- Optional filters.

Outputs:
- Structured list of issues.

---

### todo_update.py

Purpose:
- Update `TODO.<dev>.yaml` fields.

Behavior (minimum):
- Update status, priority, labels, depends_on, pending_reason.
- Update updated_at.

Inputs:
- Issue id.
- Field updates (flags or key=value).
- --dev `<slug>` (optional, see Developer selection).

Outputs:
- Updated `TODO.<dev>.yaml`.

---

### todo_next.py

Purpose:
- Return the next actionable issue.

Behavior (minimum):
- Select highest priority issue without dependencies.
- Tie-breaker: position in the YAML list (top to bottom).
- Skip issues with pending status.

Inputs:
- TODO file path.
- --dev `<slug>` (optional, see Developer selection).

Outputs:
- Issue id and path.

---

### todo_reorder.py

Purpose:
- Reorder TODO items.

Behavior (minimum):
- Move issue up/down or set explicit order.
- Update updated_at.

Inputs:
- Issue id and target position.
- --dev `<slug>` (optional, see Developer selection).

Outputs:
- Updated `TODO.<dev>.yaml`.

---

### pending_resolve.py

Purpose:
- Resolve a pending issue.

Behavior (minimum):
- Clear pending_reason.
- Set status to the next chosen status (e.g., to-do or doing).
- Update updated_at.

Inputs:
- Issue id.
- New status.
- --dev `<slug>` (optional, see Developer selection).

Outputs:
- Updated `TODO.<dev>.yaml`.

---

### log_add.py

Purpose:
- Append a log entry for an issue.

Behavior (minimum):
- Add a timestamped entry to the issue log.

Inputs:
- Issue id.
- Message text.

Outputs:
- Updated log file.

## Notes

- Scripts must avoid destructive actions without explicit user confirmation.
- Scripts should fail loudly on missing paths or invalid data.
- Output formats should be minimal and consistent for agents.
