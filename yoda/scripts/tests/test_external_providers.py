from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = REPO_ROOT / "yoda" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from lib.provider_github import fetch_issue as fetch_github_issue
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
