from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = REPO_ROOT / "yoda" / "scripts" / "yoda_intake.py"
EXTERN_DIR = REPO_ROOT / "yoda" / "project" / "extern-issues"
# Canonical external issue reference for manual/integration validation:
# GitHub issue #1 ("Test Issue for External Intake Validation").
LIVE_REFERENCE_EXTERN_ISSUE = "1"
TEST_EXTERN_ISSUE = "900123"


def _load_module():
    scripts_dir = REPO_ROOT / "yoda" / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    spec = importlib.util.spec_from_file_location("yoda_intake_test_module", SCRIPT_PATH)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def setup_function() -> None:
    for name in (f"github-{TEST_EXTERN_ISSUE}.json", f"gitlab-{TEST_EXTERN_ISSUE}.json"):
        path = EXTERN_DIR / name
        if path.exists():
            path.unlink()


def teardown_function() -> None:
    setup_function()


def test_yoda_intake_initial_runbook(capsys) -> None:
    module = _load_module()
    code = module.run(["--dev", "test"])
    captured = capsys.readouterr()
    assert code == 0
    assert "AGENT runbook (initial)" in captured.out
    assert "--extern-issue <NNN>" in captured.out
    assert "--no-extern-issue" in captured.out


def test_yoda_intake_missing_dev_returns_question_runbook(monkeypatch, capsys) -> None:
    module = _load_module()
    monkeypatch.delenv("YODA_DEV", raising=False)
    code = module.run([])
    captured = capsys.readouterr()
    assert code == 0
    assert "AGENT runbook (missing dev)" in captured.out
    assert "What is your YODA slug?" in captured.out


def test_yoda_intake_no_external_runbook(capsys) -> None:
    module = _load_module()
    code = module.run(["--dev", "test", "--no-extern-issue"])
    captured = capsys.readouterr()
    assert code == 0
    assert "## AGENT runbook" in captured.out
    assert "No external source was declared" in captured.out


def test_yoda_intake_rejects_non_numeric_external_issue(caplog) -> None:
    module = _load_module()
    code = module.run(["--dev", "test", "--extern-issue", "abc"])
    assert code == 2
    assert "must be numeric" in caplog.text


def test_yoda_intake_missing_external_file_returns_runbook(capsys) -> None:
    module = _load_module()
    code = module.run(["--dev", "test", "--extern-issue", TEST_EXTERN_ISSUE])
    captured = capsys.readouterr()
    assert code == 0
    assert "AGENT runbook (external source required)" in captured.out
    assert f"get_extern_issue.py --dev test --extern-issue {TEST_EXTERN_ISSUE}" in captured.out
    assert "Read the saved `*.json` file details" in captured.out


def test_yoda_intake_external_issue_success_from_saved_file(monkeypatch, capsys) -> None:
    module = _load_module()
    monkeypatch.setenv("YODA_ORIGIN_URL", "https://gitlab.com/acme/proj.git")
    EXTERN_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "provider": "gitlab",
        "number": TEST_EXTERN_ISSUE,
        "title": "External issue",
        "description": "Body",
        "state": "opened",
        "author": "alice",
        "url": f"https://gitlab.com/acme/proj/-/issues/{TEST_EXTERN_ISSUE}",
        "labels": ["bug"],
    }
    (EXTERN_DIR / f"gitlab-{TEST_EXTERN_ISSUE}.json").write_text(json.dumps(payload), encoding="utf-8")

    code = module.run(["--dev", "test", "--extern-issue", TEST_EXTERN_ISSUE])
    captured = capsys.readouterr()
    assert code == 0
    assert "## AGENT runbook" in captured.out
    assert "## External Issue Summary" in captured.out
    assert f"External ID: `#{TEST_EXTERN_ISSUE}`" in captured.out
    assert f"gitlab-{TEST_EXTERN_ISSUE}.json" in captured.out
