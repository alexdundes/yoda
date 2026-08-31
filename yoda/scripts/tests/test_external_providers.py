from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
import urllib.error

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = REPO_ROOT / "yoda" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lib.provider_github import (
    GitHubAPIError,
    fetch_issue as fetch_github_issue,
    fetch_issue_public as fetch_public_github_issue,
)
from lib.provider_gitlab import fetch_issue as fetch_gitlab_issue


def _ok(payload: object) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=0, stdout=json.dumps(payload), stderr="")


def test_provider_github_fetches_issue_comments_and_timeline(monkeypatch) -> None:
    def fake_run(cmd, capture_output, text):
        path = cmd[-1]
        if path.endswith("/issues/12"):
            return _ok(
                {
                    "number": 12,
                    "title": "Issue title",
                    "body": "Issue body",
                    "state": "open",
                    "user": {"login": "alice"},
                    "html_url": "https://github.com/acme/repo/issues/12",
                    "labels": [{"name": "bug"}],
                }
            )
        if "/issues/12/comments" in path:
            return _ok(
                [
                    {
                        "id": 101,
                        "user": {"login": "bob"},
                        "created_at": "2026-03-01T10:00:00Z",
                        "updated_at": "2026-03-01T10:00:00Z",
                        "body": "first comment",
                        "html_url": "https://github.com/acme/repo/issues/12#issuecomment-101",
                    }
                ]
            )
        if "/issues/12/timeline" in path:
            return _ok(
                [
                    {
                        "id": 999,
                        "event": "closed",
                        "actor": {"login": "alice"},
                        "created_at": "2026-03-01T11:00:00Z",
                        "updated_at": "2026-03-01T11:00:00Z",
                        "html_url": "https://github.com/acme/repo/issues/12#event-999",
                    },
                    {
                        "id": 101,
                        "event": "commented",
                        "actor": {"login": "bob"},
                        "created_at": "2026-03-01T10:00:00Z",
                        "updated_at": "2026-03-01T10:00:00Z",
                        "body": "first comment",
                        "html_url": "https://github.com/acme/repo/issues/12#issuecomment-101",
                    }
                ]
            )
        raise AssertionError(f"unexpected command path: {path}")

    monkeypatch.setattr("lib.provider_github.subprocess.run", fake_run)

    issue = fetch_github_issue("acme/repo", "12")
    assert set(issue) == {
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
    assert issue["provider"] == "github"
    assert issue["number"] == "12"
    assert issue["labels"] == ["bug"]
    assert isinstance(issue["log"], list)
    assert issue["log"] == [
        {
            "type": "comment",
            "id": "101",
            "author": "bob",
            "created_at": "2026-03-01T10:00:00Z",
            "updated_at": "2026-03-01T10:00:00Z",
            "body": "first comment",
            "url": "https://github.com/acme/repo/issues/12#issuecomment-101",
        },
        {
            "type": "timeline:closed",
            "id": "999",
            "author": "alice",
            "created_at": "2026-03-01T11:00:00Z",
            "updated_at": "2026-03-01T11:00:00Z",
            "body": "event: closed",
            "url": "https://github.com/acme/repo/issues/12#event-999",
        },
    ]


def test_provider_gitlab_fetches_issue_and_notes(monkeypatch) -> None:
    def fake_run(cmd, capture_output, text):
        path = cmd[-1]
        if "/issues/34" in path and "/notes" not in path:
            return _ok(
                {
                    "iid": 34,
                    "title": "Issue title",
                    "description": "Issue body",
                    "state": "opened",
                    "author": {"username": "carol"},
                    "web_url": "https://gitlab.com/acme/repo/-/issues/34",
                    "labels": ["feature"],
                }
            )
        if "/issues/34/notes" in path:
            return _ok(
                [
                    {
                        "id": 202,
                        "author": {"username": "dave"},
                        "created_at": "2026-03-02T08:00:00Z",
                        "updated_at": "2026-03-02T08:30:00Z",
                        "body": "first note",
                        "system": False,
                        "url": "https://gitlab.com/acme/repo/-/issues/34#note_202",
                    }
                ]
            )
        raise AssertionError(f"unexpected command path: {path}")

    monkeypatch.setattr("lib.provider_gitlab.subprocess.run", fake_run)

    issue = fetch_gitlab_issue("acme/repo", "34")
    assert issue["provider"] == "gitlab"
    assert issue["number"] == "34"
    assert issue["labels"] == ["feature"]
    assert isinstance(issue["log"], list)
    assert issue["log"] == [
        {
            "type": "note",
            "id": "202",
            "author": "dave",
            "created_at": "2026-03-02T08:00:00Z",
            "updated_at": "2026-03-02T08:30:00Z",
            "body": "first note",
            "url": "https://gitlab.com/acme/repo/-/issues/34#note_202",
        }
    ]


class _HttpResponse:
    def __init__(self, payload: object) -> None:
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        return None

    def read(self) -> bytes:
        return self.payload


def test_provider_github_public_uses_required_headers_and_shared_normalization() -> None:
    requests = []

    def fake_open(request, timeout):
        requests.append((request, timeout))
        path = request.full_url
        if path.endswith("/issues/12"):
            return _HttpResponse(
                {
                    "number": 12,
                    "title": "Public title",
                    "body": "Public body",
                    "state": "open",
                    "user": {"login": "alice"},
                    "html_url": "https://github.com/acme/repo/issues/12",
                    "labels": [{"name": "public"}],
                }
            )
        if "/comments?per_page=100" in path:
            return _HttpResponse(
                [
                    {
                        "id": 101,
                        "user": {"login": "bob"},
                        "created_at": "2026-03-01T10:00:00Z",
                        "updated_at": "2026-03-01T10:00:00Z",
                        "body": "public comment",
                        "html_url": "https://github.com/acme/repo/issues/12#issuecomment-101",
                    }
                ]
            )
        if "/timeline?per_page=100" in path:
            return _HttpResponse([])
        raise AssertionError(f"unexpected URL: {path}")

    issue = fetch_public_github_issue("acme/repo", "12", opener=fake_open)

    assert set(issue) == {
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
    assert issue["provider"] == "github"
    assert issue["labels"] == ["public"]
    assert issue["log"][0]["body"] == "public comment"
    assert len(requests) == 3
    for request, timeout in requests:
        headers = {name.lower(): value for name, value in request.header_items()}
        assert headers["accept"] == "application/vnd.github+json"
        assert headers["x-github-api-version"] == "2022-11-28"
        assert headers["user-agent"] == "yoda-get-extern-issue"
        assert "authorization" not in headers
        assert timeout == 15


def test_provider_github_public_reports_rate_limit() -> None:
    def rate_limited(request, timeout):
        raise urllib.error.HTTPError(
            request.full_url,
            403,
            "rate limited",
            {"X-RateLimit-Remaining": "0", "Retry-After": "60"},
            None,
        )

    with pytest.raises(GitHubAPIError, match="rate limit") as caught:
        fetch_public_github_issue("acme/repo", "12", opener=rate_limited)
    assert caught.value.kind == "rate_limit"
    assert "60" in str(caught.value)


def test_provider_github_public_404_is_ambiguous_and_actionable() -> None:
    def not_found(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 404, "not found", {}, None)

    with pytest.raises(GitHubAPIError) as caught:
        fetch_public_github_issue("acme/private", "12", opener=not_found)
    assert caught.value.exit_code == 3
    assert caught.value.kind == "not_found"
    assert "not publicly accessible" in str(caught.value)
    assert "gh auth login" in str(caught.value)


def test_provider_github_public_network_failure_is_distinct() -> None:
    def offline(request, timeout):
        raise urllib.error.URLError("offline")

    with pytest.raises(GitHubAPIError, match="network failure") as caught:
        fetch_public_github_issue("acme/repo", "12", opener=offline)
    assert caught.value.kind == "network"


def test_provider_github_timeline_does_not_hide_permission_error(monkeypatch) -> None:
    def fake_run(cmd, capture_output, text):
        path = cmd[-1]
        if path.endswith("/issues/12"):
            return _ok({"number": 12, "labels": []})
        if "/comments?per_page=100" in path:
            return _ok([])
        if "/timeline?per_page=100" in path:
            return subprocess.CompletedProcess(
                args=[],
                returncode=1,
                stdout="",
                stderr="gh: Resource not accessible (HTTP 403)",
            )
        raise AssertionError(f"events fallback must not hide permission failure: {path}")

    monkeypatch.setattr("lib.provider_github.subprocess.run", fake_run)

    with pytest.raises(GitHubAPIError) as caught:
        fetch_github_issue("acme/repo", "12")
    assert caught.value.kind == "permission"
    assert caught.value.status_code == 403


def test_provider_github_timeline_falls_back_when_endpoint_is_unavailable(monkeypatch) -> None:
    def fake_run(cmd, capture_output, text):
        path = cmd[-1]
        if path.endswith("/issues/12"):
            return _ok({"number": 12, "labels": []})
        if "/comments?per_page=100" in path:
            return _ok([])
        if "/timeline?per_page=100" in path:
            return subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="HTTP 404")
        if "/events?per_page=100" in path:
            return _ok([])
        raise AssertionError(f"unexpected command path: {path}")

    monkeypatch.setattr("lib.provider_github.subprocess.run", fake_run)
    assert fetch_github_issue("acme/repo", "12")["log"] == []
