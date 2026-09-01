"""Contract tests for the optional `source_doc` issue association.

Write path validation blocks; read path validation only alerts. Several
acceptance criteria of this feature describe agent behavior, so they are
verified here as runbook text contracts: the assertion is that the instruction
is present and cannot silently disappear in a refactor, not that an agent
actually followed it.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import frontmatter
import pytest

from conftest import REPO_ROOT, TEST_DEV, cleanup_test_files, run_script

sys.path.insert(0, str(REPO_ROOT / "yoda" / "scripts"))

from lib.errors import YodaError  # noqa: E402
from lib.phase_runbook import compose_runbook, reference_lines  # noqa: E402
from lib.source_doc import normalize_source_doc, source_doc_alert  # noqa: E402


ISSUES_DIR = REPO_ROOT / "yoda" / "project" / "issues"


def _issue_file(issue_id: str) -> Path:
    matches = list(ISSUES_DIR.glob(f"{issue_id}-*.md"))
    assert len(matches) == 1
    return matches[0]


def setup_function() -> None:
    cleanup_test_files()


def teardown_function() -> None:
    cleanup_test_files()


# --- normalization -------------------------------------------------------


def test_normalize_accepts_project_relative_file() -> None:
    assert normalize_source_doc("yoda/yoda.md") == "yoda/yoda.md"


def test_normalize_accepts_directory() -> None:
    assert normalize_source_doc("yoda/templates") == "yoda/templates"


def test_normalize_strips_dot_slash_and_trailing_slash() -> None:
    assert normalize_source_doc("./yoda/templates/") == "yoda/templates"


def test_normalize_converts_absolute_path_to_project_relative() -> None:
    absolute = str((REPO_ROOT / "yoda" / "yoda.md").resolve())
    normalized = normalize_source_doc(absolute)
    assert normalized == "yoda/yoda.md"
    assert not Path(normalized).is_absolute()
    assert str(REPO_ROOT) not in normalized


def test_normalize_resolves_parent_traversal_inside_project() -> None:
    assert normalize_source_doc("yoda/scripts/../yoda.md") == "yoda/yoda.md"


def test_normalize_resolves_relative_against_given_base_dir() -> None:
    base = REPO_ROOT / "yoda" / "scripts"
    assert normalize_source_doc("../yoda.md", base_dir=base) == "yoda/yoda.md"


def test_normalize_empty_value_is_allowed_and_empty() -> None:
    assert normalize_source_doc("") == ""
    assert normalize_source_doc("   ") == ""


def test_normalize_rejects_path_outside_project_root() -> None:
    with pytest.raises(YodaError):
        normalize_source_doc("/etc")


def test_normalize_rejects_parent_traversal_escaping_project() -> None:
    with pytest.raises(YodaError):
        normalize_source_doc("../../..")


def test_normalize_rejects_missing_path() -> None:
    with pytest.raises(YodaError):
        normalize_source_doc("yoda/does-not-exist.md")


def test_normalize_rejects_project_root_itself() -> None:
    with pytest.raises(YodaError):
        normalize_source_doc(str(REPO_ROOT))


# --- read path alert -----------------------------------------------------


def test_alert_is_empty_for_existing_path() -> None:
    assert source_doc_alert("yoda/yoda.md") == ""


def test_alert_is_empty_when_unset() -> None:
    assert source_doc_alert("") == ""


def test_alert_reports_missing_path_without_raising() -> None:
    assert "source_doc path not found" in source_doc_alert("gone/removed.md")


# --- issue_add -----------------------------------------------------------


def test_issue_add_without_source_doc_omits_the_field() -> None:
    result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "No source doc", "--description", "Desc"],
    )
    assert result.returncode == 0, result.stderr
    metadata = frontmatter.load(_issue_file("test-0001")).metadata
    assert "source_doc" not in metadata


def test_issue_add_stores_file_source_doc() -> None:
    result = run_script(
        "issue_add.py",
        [
            "--dev", TEST_DEV, "--title", "With file", "--description", "Desc",
            "--source-doc", "yoda/yoda.md",
        ],
    )
    assert result.returncode == 0, result.stderr
    assert frontmatter.load(_issue_file("test-0001")).metadata["source_doc"] == "yoda/yoda.md"


def test_issue_add_stores_directory_source_doc() -> None:
    result = run_script(
        "issue_add.py",
        [
            "--dev", TEST_DEV, "--title", "With dir", "--description", "Desc",
            "--source-doc", "yoda/templates",
        ],
    )
    assert result.returncode == 0, result.stderr
    assert frontmatter.load(_issue_file("test-0001")).metadata["source_doc"] == "yoda/templates"


def test_issue_add_normalizes_absolute_source_doc() -> None:
    absolute = str((REPO_ROOT / "yoda" / "yoda.md").resolve())
    result = run_script(
        "issue_add.py",
        [
            "--dev", TEST_DEV, "--title", "Absolute", "--description", "Desc",
            "--source-doc", absolute,
        ],
    )
    assert result.returncode == 0, result.stderr
    stored = frontmatter.load(_issue_file("test-0001")).metadata["source_doc"]
    assert stored == "yoda/yoda.md"
    assert str(REPO_ROOT) not in stored


def test_issue_add_rejects_source_doc_outside_project() -> None:
    result = run_script(
        "issue_add.py",
        [
            "--dev", TEST_DEV, "--title", "Outside", "--description", "Desc",
            "--source-doc", "/etc",
        ],
    )
    assert result.returncode != 0
    assert not list(ISSUES_DIR.glob(f"{TEST_DEV}-*.md"))


def test_issue_add_rejects_missing_source_doc() -> None:
    result = run_script(
        "issue_add.py",
        [
            "--dev", TEST_DEV, "--title", "Missing", "--description", "Desc",
            "--source-doc", "yoda/does-not-exist.md",
        ],
    )
    assert result.returncode != 0
    assert not list(ISSUES_DIR.glob(f"{TEST_DEV}-*.md"))


def test_source_doc_and_extern_issue_file_coexist() -> None:
    result = run_script(
        "issue_add.py",
        [
            "--dev", TEST_DEV, "--title", "Both", "--description", "Desc",
            "--source-doc", "yoda/yoda.md", "--extern-issue", "12",
        ],
    )
    assert result.returncode == 0, result.stderr
    metadata = frontmatter.load(_issue_file("test-0001")).metadata
    assert metadata["source_doc"] == "yoda/yoda.md"
    assert metadata["extern_issue_file"].endswith("-12.json")


def test_source_doc_follows_extern_issue_file_in_canonical_order() -> None:
    result = run_script(
        "issue_add.py",
        [
            "--dev", TEST_DEV, "--title", "Order", "--description", "Desc",
            "--source-doc", "yoda/yoda.md", "--extern-issue", "12",
        ],
    )
    assert result.returncode == 0, result.stderr
    keys = list(frontmatter.load(_issue_file("test-0001")).metadata.keys())
    assert keys.index("source_doc") == keys.index("extern_issue_file") + 1
    assert keys.index("source_doc") < keys.index("created_at")


def test_source_doc_does_not_change_schema_version() -> None:
    result = run_script(
        "issue_add.py",
        [
            "--dev", TEST_DEV, "--title", "Schema", "--description", "Desc",
            "--source-doc", "yoda/yoda.md",
        ],
    )
    assert result.returncode == 0, result.stderr
    assert frontmatter.load(_issue_file("test-0001")).metadata["schema_version"] == "2.01"


# --- todo_update ---------------------------------------------------------


def _create_issue(*extra: str) -> Path:
    result = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Update target", "--description", "Desc", *extra],
    )
    assert result.returncode == 0, result.stderr
    return _issue_file("test-0001")


def test_todo_update_sets_source_doc_after_creation() -> None:
    _create_issue()
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0001", "--source-doc", "yoda/yoda.md"],
    )
    assert result.returncode == 0, result.stderr
    assert frontmatter.load(_issue_file("test-0001")).metadata["source_doc"] == "yoda/yoda.md"


def test_todo_update_normalizes_absolute_source_doc() -> None:
    _create_issue()
    absolute = str((REPO_ROOT / "yoda" / "templates").resolve())
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0001", "--source-doc", absolute],
    )
    assert result.returncode == 0, result.stderr
    assert frontmatter.load(_issue_file("test-0001")).metadata["source_doc"] == "yoda/templates"


def test_todo_update_clears_source_doc() -> None:
    _create_issue("--source-doc", "yoda/yoda.md")
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0001", "--clear-source-doc"],
    )
    assert result.returncode == 0, result.stderr
    assert "source_doc" not in frontmatter.load(_issue_file("test-0001")).metadata


def test_todo_update_rejects_set_and_clear_together() -> None:
    _create_issue()
    result = run_script(
        "todo_update.py",
        [
            "--dev", TEST_DEV, "--issue", "test-0001",
            "--source-doc", "yoda/yoda.md", "--clear-source-doc",
        ],
    )
    assert result.returncode != 0


def test_todo_update_reports_source_doc_in_diff() -> None:
    _create_issue()
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0001", "--source-doc", "yoda/yoda.md"],
    )
    assert result.returncode == 0, result.stderr
    assert "source_doc" in result.stdout


def test_todo_update_rejects_source_doc_outside_project() -> None:
    _create_issue()
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0001", "--source-doc", "/etc"],
    )
    assert result.returncode != 0


# --- runbook composition (agent-behavior criteria as text contracts) -----


def test_study_runbook_gains_source_doc_instruction() -> None:
    composed = compose_runbook("BASE", "study", {"source_doc": "docs/a.md"})
    assert composed.startswith("BASE")
    assert "docs/a.md" in composed
    assert "qualified context" in composed
    assert "confront it with the current project state" in composed
    assert "still open" in composed


def test_document_runbook_forbids_automatic_edit_of_source_doc() -> None:
    composed = compose_runbook("BASE", "document", {"source_doc": "docs/a.md"})
    assert "does not authorize editing it" in composed
    assert "approved issue scope" in composed


def test_implement_and_evaluate_get_no_conditional_line() -> None:
    for step in ("implement", "evaluate"):
        assert compose_runbook("BASE", step, {"source_doc": "docs/a.md"}) == "BASE"


def test_runbook_is_unchanged_without_source_doc() -> None:
    for step in ("study", "document", "implement", "evaluate"):
        assert compose_runbook("BASE", step, {}) == "BASE"
        assert compose_runbook("BASE", step, {"source_doc": ""}) == "BASE"


def test_flow_and_prep_share_the_runbook_module() -> None:
    import yoda_flow_next
    import yoda_prep_flow
    from lib import phase_runbook

    assert yoda_flow_next.RUNBOOK_BY_STEP is phase_runbook.FLOW_RUNBOOK_BY_STEP
    assert yoda_prep_flow.RUNBOOK_BY_STEP is phase_runbook.PREP_RUNBOOK_BY_STEP
    assert yoda_flow_next.compose_runbook is phase_runbook.compose_runbook
    assert yoda_prep_flow.compose_runbook is phase_runbook.compose_runbook


# --- reference visibility ------------------------------------------------


def test_reference_lines_expose_both_fields() -> None:
    lines = reference_lines(
        {"extern_issue_file": "../extern_issues/github-12.json", "source_doc": "yoda/yoda.md"}
    )
    assert "External issue file: ../extern_issues/github-12.json" in lines
    assert "Source doc: yoda/yoda.md" in lines


def test_reference_lines_are_empty_without_references() -> None:
    assert reference_lines({}) == []


def test_reference_lines_alert_on_stale_source_doc() -> None:
    lines = reference_lines({"source_doc": "gone/removed.md"})
    assert any("source_doc path not found" in line for line in lines)


def test_stale_source_doc_does_not_break_commands() -> None:
    _create_issue()
    issue_path = _issue_file("test-0001")
    post = frontmatter.load(issue_path)
    post.metadata["source_doc"] = "gone/removed.md"
    issue_path.write_text(frontmatter.dumps(post), encoding="utf-8")

    for script in ("todo_list.py", "todo_next.py"):
        result = run_script(script, ["--dev", TEST_DEV])
        assert result.returncode == 0, f"{script}: {result.stderr}"

    result = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--dry-run"])
    assert result.returncode == 0, result.stderr
    assert "Alert: source_doc path not found: gone/removed.md" in result.stdout


def test_flow_next_exposes_extern_issue_file() -> None:
    _create_issue("--extern-issue", "12")
    result = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--dry-run"])
    assert result.returncode == 0, result.stderr
    assert "External issue file:" in result.stdout


def test_todo_list_shows_source_doc_column_only_when_present() -> None:
    _create_issue()
    without = run_script("todo_list.py", ["--dev", TEST_DEV])
    assert without.returncode == 0, without.stderr
    assert "source_doc" not in without.stdout

    run_script("todo_update.py", ["--dev", TEST_DEV, "--issue", "test-0001", "--source-doc", "yoda/yoda.md"])
    with_field = run_script("todo_list.py", ["--dev", TEST_DEV])
    assert with_field.returncode == 0, with_field.stderr
    assert "source_doc" in with_field.stdout


# --- intake runbook ------------------------------------------------------


def _assert_asks_for_source_doc(text: str) -> None:
    assert "base documentation" in text
    assert "--source-doc" in text
    assert "one file or one directory" in text
    assert "inventory the directory contents" in text
    assert "read the material before completing" in text
    assert "not an entry point" in text
    # Optionality must stay explicit, or the question becomes friction for
    # developers who do not work from prior documentation.
    assert "It is optional" in text
    assert "no extra step" in text


def test_intake_runbook_asks_for_source_doc_without_external_source() -> None:
    result = run_script("yoda_intake.py", ["--dev", TEST_DEV, "--no-extern-issue"])
    assert result.returncode == 0, result.stderr
    _assert_asks_for_source_doc(result.stdout)


@pytest.mark.parametrize("external", (False, True))
def test_full_intake_runbook_asks_for_source_doc(external: bool) -> None:
    import yoda_intake

    _assert_asks_for_source_doc(yoda_intake._full_runbook(TEST_DEV, external))


# --- joint coexistence of all four relations -----------------------------


def _entry_points_section(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    start = text.index("## Entry points")
    end = text.index("## ", start + len("## Entry points"))
    return text[start:end]


def test_all_four_relations_coexist_and_stay_distinct() -> None:
    """`source_doc`, `extern_issue_file`, `depends_on` and Entry points are four
    different relations. They must be storable at once, never derived from one
    another, and independently mutable.
    """
    first = run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Dependency target", "--description", "Desc"],
    )
    assert first.returncode == 0, first.stderr

    second = run_script(
        "issue_add.py",
        [
            "--dev", TEST_DEV, "--title", "All relations", "--description", "Desc",
            "--source-doc", "yoda/yoda.md", "--extern-issue", "12",
        ],
    )
    assert second.returncode == 0, second.stderr

    target = _issue_file("test-0002")
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0002", "--depends-on", "test-0001"],
    )
    assert result.returncode == 0, result.stderr

    # An entry point that repeats the source_doc path, plus one that does not:
    # the same file may play both roles without the concepts collapsing.
    post = frontmatter.load(target)
    post.content = post.content.replace(
        "## Entry points\n",
        "## Entry points\n\n- yoda/yoda.md\n- yoda/scripts/issue_add.py\n",
        1,
    )
    target.write_text(frontmatter.dumps(post), encoding="utf-8")

    metadata = frontmatter.load(target).metadata
    assert metadata["source_doc"] == "yoda/yoda.md"
    assert metadata["extern_issue_file"] == "../extern_issues/github-12.json"
    assert metadata["depends_on"] == ["test-0001"]

    # No relation leaks into another.
    assert metadata["source_doc"] not in metadata["depends_on"]
    assert metadata["source_doc"] != metadata["extern_issue_file"]
    entry_points = _entry_points_section(target)
    assert "yoda/scripts/issue_add.py" in entry_points
    assert "source_doc" not in entry_points

    # Dependency blocking is decided by depends_on alone: an issue carrying a
    # source_doc and an external issue is still blocked only by its dependency.
    listing = run_script("todo_list.py", ["--dev", TEST_DEV, "--format", "json"])
    assert listing.returncode == 0, listing.stderr
    by_id = {item["id"]: item for item in json.loads(listing.stdout)["issues"]}
    assert by_id["test-0002"]["blocked_by"] == ["test-0001"]
    assert by_id["test-0002"]["selectable"] is False
    assert by_id["test-0001"]["selectable"] is True

    # The flow selects the dependency first, and exposes only its own
    # references: test-0001 declares none.
    flow = run_script("yoda_flow_next.py", ["--dev", TEST_DEV, "--dry-run"])
    assert flow.returncode == 0, flow.stderr
    assert "Issue ID: test-0001" in flow.stdout
    assert "Source doc:" not in flow.stdout
    assert "External issue file:" not in flow.stdout


def test_relations_are_independently_mutable() -> None:
    run_script(
        "issue_add.py",
        ["--dev", TEST_DEV, "--title", "Dependency target", "--description", "Desc"],
    )
    run_script(
        "issue_add.py",
        [
            "--dev", TEST_DEV, "--title", "All relations", "--description", "Desc",
            "--source-doc", "yoda/yoda.md", "--extern-issue", "12",
        ],
    )
    run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0002", "--depends-on", "test-0001"],
    )
    target = _issue_file("test-0002")

    # Clearing source_doc leaves the external issue and the dependency intact.
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0002", "--clear-source-doc"],
    )
    assert result.returncode == 0, result.stderr
    metadata = frontmatter.load(target).metadata
    assert "source_doc" not in metadata
    assert metadata["extern_issue_file"] == "../extern_issues/github-12.json"
    assert metadata["depends_on"] == ["test-0001"]

    # Clearing the external issue leaves a restored source_doc and the
    # dependency intact.
    run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0002", "--source-doc", "yoda/templates"],
    )
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0002", "--clear-extern-issue-file"],
    )
    assert result.returncode == 0, result.stderr
    metadata = frontmatter.load(target).metadata
    assert metadata["source_doc"] == "yoda/templates"
    assert "extern_issue_file" not in metadata
    assert metadata["depends_on"] == ["test-0001"]

    # Restore the external issue so the third case also starts with all three
    # relations set; otherwise it would only prove preservation of one.
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0002", "--extern-issue", "12"],
    )
    assert result.returncode == 0, result.stderr
    metadata = frontmatter.load(target).metadata
    assert metadata["source_doc"] == "yoda/templates"
    assert metadata["extern_issue_file"] == "../extern_issues/github-12.json"
    assert metadata["depends_on"] == ["test-0001"]

    # Clearing the dependency leaves both the source_doc and the external issue
    # intact.
    result = run_script(
        "todo_update.py",
        ["--dev", TEST_DEV, "--issue", "test-0002", "--clear-depends-on"],
    )
    assert result.returncode == 0, result.stderr
    metadata = frontmatter.load(target).metadata
    assert metadata["source_doc"] == "yoda/templates"
    assert metadata["extern_issue_file"] == "../extern_issues/github-12.json"
    assert "depends_on" not in metadata
