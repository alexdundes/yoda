# yoda/scripts

Scripts for YODA TODO, issue, and log automation. See `project/specs/13-yoda-scripts-v1.md`.

## Quickstart

Use a virtual environment, install the requirements from `yoda/scripts/requirements.txt`, and run the scripts as needed.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r yoda/scripts/requirements.txt

python yoda/scripts/issue_add.py --title "Example issue" --description "Short description"
python yoda/scripts/todo_update.py --issue dev-0001 --status doing
python yoda/scripts/log_add.py --issue dev-0001 --message "[dev-0001] Started work"
```

## Tests

```bash
python3 -m pytest yoda/scripts/tests
```
