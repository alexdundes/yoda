from __future__ import annotations

from conftest import run_script


def test_help_contains_agent_guidance_for_all_scripts() -> None:
    scripts = [
        "get_extern_issue.py",
        "init.py",
        "issue_add.py",
        "log_add.py",
        "todo_list.py",
        "todo_next.py",
        "todo_update.py",
        "update.py",
        "yoda_flow_next.py",
        "yoda_intake.py",
    ]
    for script in scripts:
        result = run_script(script, ["--help"])
        assert result.returncode == 0, f"{script}: {result.stderr}"
        assert "Agent " in result.stdout, script


def test_yoda_flow_next_help_exposes_log_message_flag() -> None:
    result = run_script("yoda_flow_next.py", ["--help"])
    assert result.returncode == 0, result.stderr
    assert "--log-message" in result.stdout


def test_commands_require_explicit_dev_without_env_or_prompt(monkeypatch) -> None:
    monkeypatch.delenv("YODA_DEV", raising=False)

    commands = [
        ("get_extern_issue.py", ["--extern-issue", "1"]),
        ("init.py", []),
        ("issue_add.py", ["--title", "T", "--description", "D"]),
        ("log_add.py", ["--issue", "test-0001", "--message", "test-0001: note"]),
        ("todo_list.py", []),
        ("todo_next.py", []),
        ("todo_update.py", ["--issue", "test-0001"]),
        ("yoda_flow_next.py", []),
    ]
    for script, args in commands:
        result = run_script(script, args)
        assert result.returncode == 2, f"{script}: {result.stdout} | {result.stderr}"
        assert "--dev is required" in result.stderr, script


def test_yoda_intake_without_dev_returns_human_prompt() -> None:
    result = run_script("yoda_intake.py", [])
    assert result.returncode == 0, result.stderr
    assert "What is your YODA slug?" in result.stdout


def test_update_keeps_dev_optional(tmp_path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    yoda_dir = root / "yoda"
    yoda_dir.mkdir(parents=True, exist_ok=True)
    (yoda_dir / "PACKAGE_MANIFEST.yaml").write_text("version: 1.0.0\nbuild: 20260101.abc1234\n", encoding="utf-8")
    latest = tmp_path / "latest.json"
    latest.write_text(
        '{"version":"1.0.0","build":"20260101.abc1234","package_url":"file:///unused","sha256":"deadbeef"}',
        encoding="utf-8",
    )
    result = run_script("update.py", ["--check", "--root", str(root), "--latest", str(latest)])
    # Fails on checksum/metadata validation paths if needed, but must not fail due to missing --dev.
    assert "--dev is required" not in result.stderr
    assert result.returncode in {0, 2}
