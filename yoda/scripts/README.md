# yoda/scripts

Scripts for YODA TODO, issue, and log automation. See `project/specs/13-yoda-scripts-v1.md`.

## Quickstart

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r yoda/scripts/requirements.txt
python yoda/scripts/issue_add.py --title "Example issue" --description "Short description"
python yoda/scripts/todo_update.py --id dev-0001 --status doing
python yoda/scripts/log_add.py --id dev-0001 --message "Started work"
```

## Tests

```bash
pytest yoda/scripts/tests
```
