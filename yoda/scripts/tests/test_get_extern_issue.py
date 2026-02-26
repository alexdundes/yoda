from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = REPO_ROOT / "yoda" / "scripts" / "get_extern_issue.py"
EXTERN_DIR = REPO_ROOT / "yoda" / "project" / "extern-issues"
# Canonical external issue reference for manual/integration validation:
# GitHub issue #1 ("Test Issue for External Intake Validation").
LIVE_REFERENCE_EXTERN_ISSUE = "1"
TEST_EXTERN_ISSUE = "900001"


def _load_module():
    scripts_dir = REPO_ROOT / "yoda" / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    spec = importlib.util.spec_from_file_location("get_extern_issue_test_module", SCRIPT_PATH)
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


def test_get_extern_issue_writes_file_and_next_step(monkeypatch, capsys) -> None:
    module = _load_module()
    monkeypatch.setattr(module, "detect_origin_url", lambda: "https://github.com/acme/proj.git")
    monkeypatch.setattr(module, "ensure_cli_and_auth", lambda provider: None)
    monkeypatch.setattr(
        module,
        "_fetch_external",
        lambda provider, repo_slug, issue_number: {
            "provider": provider,
            "number": issue_number,
            "title": "Title",
            "description": "Body",
            "state": "open",
            "author": "alex",
            "url": f"https://github.com/acme/proj/issues/{TEST_EXTERN_ISSUE}",
            "labels": ["enhancement"],
        },
    )

    code = module.run(["--dev", "test", "--extern-issue", TEST_EXTERN_ISSUE])
    captured = capsys.readouterr()
    assert code == 0
    out_file = EXTERN_DIR / f"github-{TEST_EXTERN_ISSUE}.json"
    assert out_file.exists()
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["number"] == TEST_EXTERN_ISSUE
    assert (
        f"Next step: python3 yoda/scripts/yoda_intake.py --dev test --extern-issue {TEST_EXTERN_ISSUE}"
        in captured.out
    )


def test_get_extern_issue_requires_dev(caplog) -> None:
    module = _load_module()
    code = module.run(["--extern-issue", "1"])
    assert code == 2
    assert "--dev is required" in caplog.text
