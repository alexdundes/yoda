from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT_PATH = REPO_ROOT / "yoda" / "scripts" / "get_extern_issue.py"
EXTERN_DIR = REPO_ROOT / "yoda" / "project" / "extern_issues"
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
    monkeypatch.setattr(
        module,
        "_fetch_external",
        lambda provider, host, repo_slug, issue_number: (
            {
                "provider": provider,
                "number": issue_number,
                "title": "Title",
                "description": "Body",
                "state": "open",
                "author": "alex",
                "url": f"https://github.com/acme/proj/issues/{TEST_EXTERN_ISSUE}",
                "labels": ["enhancement"],
            },
            "public-http",
        ),
    )

    code = module.run(["--dev", "test", "--extern-issue", TEST_EXTERN_ISSUE])
    captured = capsys.readouterr()
    assert code == 0
    out_file = EXTERN_DIR / f"github-{TEST_EXTERN_ISSUE}.json"
    assert out_file.exists()
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data["number"] == TEST_EXTERN_ISSUE
    assert "transport" not in data
    assert "Transport: public-http" in captured.out
    assert (
        f"Next step: python3 yoda/scripts/yoda_intake.py --dev test --extern-issue {TEST_EXTERN_ISSUE}"
        in captured.out
    )


def test_get_extern_issue_requires_dev(caplog) -> None:
    module = _load_module()
    code = module.run(["--extern-issue", "1"])
    assert code == 2
    assert "--dev is required" in caplog.text


def test_github_prefers_authenticated_transport(monkeypatch) -> None:
    module = _load_module()
    expected = {"provider": "github", "number": "7"}
    monkeypatch.setattr(
        module,
        "check_cli_and_auth",
        lambda provider: SimpleNamespace(ready=True, error=None),
    )
    monkeypatch.setattr(module, "fetch_github_issue", lambda repo, number: expected)
    monkeypatch.setattr(
        module,
        "fetch_public_github_issue",
        lambda repo, number: pytest.fail("public fallback must not run"),
    )

    issue, transport = module._fetch_external("github", "github.com", "acme/proj", "7")
    assert issue == expected
    assert transport == "authenticated-cli"


def test_github_uses_public_fallback_when_cli_auth_is_unavailable(monkeypatch) -> None:
    module = _load_module()
    auth_error = module.YodaError("gh authentication is not ready", exit_code=3)
    monkeypatch.setattr(
        module,
        "check_cli_and_auth",
        lambda provider: SimpleNamespace(ready=False, error=auth_error),
    )
    monkeypatch.setattr(
        module,
        "fetch_public_github_issue",
        lambda repo, number: {"provider": "github", "number": number},
    )

    issue, transport = module._fetch_external("github", "github.com", "acme/proj", "8")
    assert issue["number"] == "8"
    assert transport == "public-http"


def test_github_permission_failure_uses_public_fallback(monkeypatch) -> None:
    module = _load_module()
    monkeypatch.setattr(
        module,
        "check_cli_and_auth",
        lambda provider: SimpleNamespace(ready=True, error=None),
    )

    def denied(repo, number):
        raise module.GitHubAPIError("denied", status_code=403, kind="permission")

    monkeypatch.setattr(module, "fetch_github_issue", denied)
    monkeypatch.setattr(
        module,
        "fetch_public_github_issue",
        lambda repo, number: {"provider": "github", "number": number},
    )

    _, transport = module._fetch_external("github", "github.com", "acme/proj", "9")
    assert transport == "public-http"


def test_github_enterprise_does_not_use_public_fallback(monkeypatch) -> None:
    module = _load_module()
    auth_error = module.YodaError("Run: gh auth login", exit_code=3)
    monkeypatch.setattr(
        module,
        "check_cli_and_auth",
        lambda provider: SimpleNamespace(ready=False, error=auth_error),
    )
    monkeypatch.setattr(
        module,
        "fetch_public_github_issue",
        lambda repo, number: pytest.fail("github.com fallback must not run for Enterprise"),
    )

    with pytest.raises(module.YodaError, match="gh auth login"):
        module._fetch_external("github", "github.example.com", "acme/proj", "10")


def test_github_double_failure_preserves_both_actionable_causes(monkeypatch) -> None:
    module = _load_module()
    auth_error = module.YodaError(
        "Required CLI 'gh' is not installed. Install GitHub CLI.",
        exit_code=3,
    )
    monkeypatch.setattr(
        module,
        "check_cli_and_auth",
        lambda provider: SimpleNamespace(ready=False, error=auth_error),
    )

    def public_network_failure(repo, number):
        raise module.GitHubAPIError(
            "GitHub public API network failure. Check connectivity and retry.",
            kind="network",
        )

    monkeypatch.setattr(module, "fetch_public_github_issue", public_network_failure)

    with pytest.raises(module.YodaError) as caught:
        module._fetch_external("github", "github.com", "acme/proj", "11")
    message = str(caught.value)
    assert "Authenticated transport: Required CLI 'gh' is not installed" in message
    assert "Public transport: GitHub public API network failure" in message
    assert "Install GitHub CLI" in message
    assert "Check connectivity and retry" in message


def test_cli_missing_returns_actionable_auth_state(monkeypatch) -> None:
    module = _load_module()
    monkeypatch.setattr("lib.external_issue_utils.shutil.which", lambda cli: None)

    state = module.check_cli_and_auth("github")
    assert not state.ready
    assert state.error is not None
    assert "Required CLI 'gh' is not installed" in str(state.error)
    assert "Install GitHub CLI" in str(state.error)


def test_cli_auth_failure_does_not_expose_cli_output(monkeypatch) -> None:
    module = _load_module()
    secret = "secret-token-from-cli"
    monkeypatch.setattr("lib.external_issue_utils.shutil.which", lambda cli: f"/usr/bin/{cli}")
    monkeypatch.setattr(
        "lib.external_issue_utils.subprocess.run",
        lambda cmd, capture_output, text: SimpleNamespace(
            returncode=1,
            stdout="",
            stderr=f"authentication failed for token {secret}",
        ),
    )

    state = module.check_cli_and_auth("github")
    assert not state.ready
    assert state.error is not None
    assert secret not in str(state.error)
    assert "gh auth login" in str(state.error)


def test_public_fallback_persists_exact_intake_schema(monkeypatch, capsys) -> None:
    module = _load_module()
    auth_error = module.YodaError("gh authentication is not ready", exit_code=3)
    expected_keys = {
        "provider",
        "number",
        "title",
        "description",
        "state",
        "author",
        "url",
        "labels",
        "log",
    }
    public_issue = {
        "provider": "github",
        "number": TEST_EXTERN_ISSUE,
        "title": "Public issue",
        "description": "Public body",
        "state": "open",
        "author": "alex",
        "url": f"https://github.com/acme/proj/issues/{TEST_EXTERN_ISSUE}",
        "labels": ["documentation"],
        "log": [],
    }
    monkeypatch.setattr(module, "detect_origin_url", lambda: "https://github.com/acme/proj.git")
    monkeypatch.setattr(
        module,
        "check_cli_and_auth",
        lambda provider: SimpleNamespace(ready=False, error=auth_error),
    )
    monkeypatch.setattr(module, "fetch_public_github_issue", lambda repo, number: public_issue)

    code = module.run(["--dev", "test", "--extern-issue", TEST_EXTERN_ISSUE, "--json"])
    output = json.loads(capsys.readouterr().out)
    persisted = json.loads((EXTERN_DIR / f"github-{TEST_EXTERN_ISSUE}.json").read_text(encoding="utf-8"))

    assert code == 0
    assert set(persisted) == expected_keys
    assert persisted == public_issue
    assert "transport" not in persisted
    assert output["transport"] == "public-http"
