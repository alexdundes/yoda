"""Guard the portability of the specification set.

A spec must be interpretable from `project/specs/` alone. These tests fail when
a spec starts depending on this repository's development history, either by
citing a concrete issue or by linking outside the portable unit.

Contract: `project/specs/28-spec-independence-and-portability.md`.
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

from conftest import (
    SPECS_ROOT,
    known_dev_slugs,
    known_issue_ids,
    normative_spec_files,
    origin_repo,
    spec_files,
)


# Inline destination, tolerating `<...>` wrapping and a trailing title.
INLINE_LINK_RE = re.compile(r"\[[^\]]*\]\(\s*(<[^>]*>|[^\s)]+)[^)]*\)")
# Reference definition: `[id]: destination "optional title"`.
REFERENCE_DEFINITION_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]*>|\S+)")
EXTERNAL_SCHEMES = ("http://", "https://", "mailto:")

URL_RE = re.compile(r"https?://[^\s)\]\"'`>]+", re.IGNORECASE)
TRACKER_PATH_RE = re.compile(
    r"^/(?P<slug>.+?)/(?:-/)?(?:issues|pull|pulls|merge_requests)/\d+",
    re.IGNORECASE,
)

# Hexadecimal is case-insensitive, and Git supports SHA-1 and SHA-256 OIDs.
# Requiring at least one hex letter keeps calendar build stamps such as
# `20260129` from being mistaken for abbreviated commit hashes.
COMMIT_SHA_RE = re.compile(r"\b(?=[0-9a-f]*[a-f])[0-9a-f]{7,64}\b", re.IGNORECASE)


def _link_destinations(text: str) -> list[tuple[int, str]]:
    """Return `(line_number, destination)` for inline and reference-style links."""
    destinations: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in (INLINE_LINK_RE, REFERENCE_DEFINITION_RE):
            for match in pattern.finditer(line):
                raw = match.group(1).strip()
                if raw.startswith("<") and raw.endswith(">"):
                    raw = raw[1:-1].strip()
                if raw:
                    destinations.append((line_number, raw))
    return destinations


def _issue_id_pattern(dev_slugs: set[str]) -> re.Pattern[str] | None:
    """Match `<dev>-<NNNN>` only for slugs this repository actually uses.

    Restricting the prefix keeps unrelated hyphen-plus-digits tokens such as
    `iso-8601` from being reported.
    """
    if not dev_slugs:
        return None
    alternatives = "|".join(re.escape(slug) for slug in sorted(dev_slugs))
    return re.compile(rf"\b(?:{alternatives})-\d{{4}}\b")


def find_forbidden_issue_references(
    text: str,
    issue_ids: set[str],
    dev_slugs: set[str],
) -> list[tuple[int, str, str]]:
    """Return `(line_number, fragment, reason)` for each prohibited reference."""
    pattern = _issue_id_pattern(dev_slugs)
    if pattern is None:
        return []

    findings: list[tuple[int, str, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in pattern.finditer(line):
            fragment = match.group(0)
            if fragment in issue_ids:
                reason = "concrete issue of this repository's backlog"
            else:
                reason = "issue-shaped identifier of this repository"
            findings.append((line_number, fragment, reason))
    return findings


def find_tracker_urls(
    text: str,
    origin: tuple[str, str] | None,
) -> list[tuple[int, str, str]]:
    """Return `(line_number, url, reason)` for issue-tracker links.

    Layer one names this repository's own tracker when the git origin resolves.
    Layer two is origin-independent, so an unresolvable origin degrades the
    message rather than disabling detection.
    """
    findings: list[tuple[int, str, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in URL_RE.finditer(line):
            url = match.group(0).rstrip(".,;:")
            parsed = urlsplit(url)
            path_match = TRACKER_PATH_RE.match(parsed.path)
            if not path_match:
                continue
            host = parsed.netloc.lower()
            slug = path_match.group("slug").lower()
            if origin is not None and (host, slug) == origin:
                reason = "link to this repository's own issue tracker"
            else:
                reason = "link to an external issue tracker"
            findings.append((line_number, url, reason))
    return findings


def find_commit_shas(text: str) -> list[tuple[int, str]]:
    """Return `(line_number, fragment)` for commit-hash-shaped tokens."""
    findings: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        for match in COMMIT_SHA_RE.finditer(line):
            findings.append((line_number, match.group(0)))
    return findings


def find_escaping_links(path: Path, text: str) -> list[tuple[int, str]]:
    """Return `(line_number, target)` for links resolving outside the spec set."""
    specs_root = SPECS_ROOT.resolve()
    findings: list[tuple[int, str]] = []
    for line_number, destination in _link_destinations(text):
        target = destination.split("#")[0].strip()
        if not target or target.lower().startswith(EXTERNAL_SCHEMES):
            continue
        resolved = (path.parent / target).resolve()
        if resolved != specs_root and specs_root not in resolved.parents:
            findings.append((line_number, target))
    return findings


def test_specs_do_not_cite_concrete_issues() -> None:
    issue_ids = known_issue_ids()
    dev_slugs = known_dev_slugs()
    assert issue_ids, "expected a populated backlog to derive issue IDs from"

    problems: list[str] = []
    for path in spec_files():
        text = path.read_text(encoding="utf-8")
        for line_number, fragment, reason in find_forbidden_issue_references(
            text, issue_ids, dev_slugs
        ):
            problems.append(
                f"{path.relative_to(SPECS_ROOT.parent.parent)}:{line_number}: "
                f"'{fragment}' is a {reason}. Specs must be self-contained: move the "
                f"rule and its rationale into the spec text. See "
                f"project/specs/28-spec-independence-and-portability.md."
            )

    assert not problems, "Prohibited issue references found:\n" + "\n".join(problems)


def test_specs_have_no_links_escaping_the_portable_unit() -> None:
    problems: list[str] = []
    for path in spec_files():
        text = path.read_text(encoding="utf-8")
        for line_number, target in find_escaping_links(path, text):
            problems.append(
                f"{path.relative_to(SPECS_ROOT.parent.parent)}:{line_number}: "
                f"link '{target}' resolves outside project/specs/. The specification "
                f"set must stay copyable on its own. See "
                f"project/specs/28-spec-independence-and-portability.md."
            )

    assert not problems, "Links escaping project/specs/ found:\n" + "\n".join(problems)


def test_specs_do_not_link_to_issue_trackers() -> None:
    origin = origin_repo()

    problems: list[str] = []
    for path in spec_files():
        text = path.read_text(encoding="utf-8")
        for line_number, url, reason in find_tracker_urls(text, origin):
            problems.append(
                f"{path.relative_to(SPECS_ROOT.parent.parent)}:{line_number}: "
                f"'{url}' is a {reason}. A spec must not cite a concrete tracker "
                f"issue as authority; write the rule and its rationale into the "
                f"spec text. See "
                f"project/specs/28-spec-independence-and-portability.md."
            )

    assert not problems, "Issue tracker links found:\n" + "\n".join(problems)


def test_normative_specs_do_not_cite_commit_hashes() -> None:
    problems: list[str] = []
    for path in normative_spec_files():
        text = path.read_text(encoding="utf-8")
        for line_number, fragment in find_commit_shas(text):
            problems.append(
                f"{path.relative_to(SPECS_ROOT.parent.parent)}:{line_number}: "
                f"'{fragment}' looks like a commit hash. Specs must not depend on "
                f"Git history; state the rule and its rationale instead. See "
                f"project/specs/28-spec-independence-and-portability.md."
            )

    assert not problems, "Commit hash references found:\n" + "\n".join(problems)


def test_escaping_link_detection_covers_every_markdown_link_form() -> None:
    spec = SPECS_ROOT / "00-conventions.md"
    forms = {
        "inline": "[t](../../README.md)",
        "inline with title": '[t](../../README.md "Title")',
        "inline in angle brackets": "[t](<../../README.md>)",
        "reference definition": "[t][x]\n\n[x]: ../../README.md",
        "reference in angle brackets": "[t][x]\n\n[x]: <../../README.md>",
    }

    for label, text in forms.items():
        assert len(find_escaping_links(spec, text)) == 1, f"{label} was not detected"


def test_escaping_link_detection_allows_internal_and_remote_targets() -> None:
    spec = SPECS_ROOT / "00-conventions.md"
    allowed = "\n".join(
        [
            "[t](./28-spec-independence-and-portability.md)",
            "[t](influences/03-docs-as-code.md)",
            "[t](https://alexdundes.github.io/yoda/)",
            "[t](HTTPS://alexdundes.github.io/yoda/)",
            "[t](mailto:someone@example.com)",
        ]
    )

    assert find_escaping_links(spec, allowed) == []


def test_tracker_detection_is_scheme_case_insensitive() -> None:
    origin = ("github.com", "alexdundes/yoda")

    findings = find_tracker_urls("HTTPS://github.com/alexdundes/yoda/issues/7", origin)

    assert len(findings) == 1
    assert "own issue tracker" in findings[0][2]


def test_tracker_detection_covers_reference_and_angle_bracket_forms() -> None:
    origin = ("github.com", "alexdundes/yoda")
    forms = {
        "inline": "[t](https://github.com/alexdundes/yoda/issues/64)",
        "bare": "see https://github.com/alexdundes/yoda/issues/64",
        "angle brackets": "see <https://github.com/alexdundes/yoda/issues/64>",
        "reference definition": "[t][x]\n\n[x]: https://github.com/alexdundes/yoda/issues/64",
    }

    for label, text in forms.items():
        assert len(find_tracker_urls(text, origin)) == 1, f"{label} was not detected"


def test_commit_detection_covers_case_and_oid_lengths() -> None:
    sha256_oid = "9f" * 32

    assert find_commit_shas("commit 5cd734b") == [(1, "5cd734b")]
    assert find_commit_shas("commit 5CD734B") == [(1, "5CD734B")]
    assert find_commit_shas(f"commit {sha256_oid}") == [(1, sha256_oid)]


def test_tracker_detection_separates_own_and_external_trackers() -> None:
    origin = ("github.com", "alexdundes/yoda")
    text = "\n".join(
        [
            "see https://github.com/alexdundes/yoda/issues/7",
            "and https://gitlab.com/someone/other/-/issues/12",
        ]
    )

    findings = find_tracker_urls(text, origin)

    assert [(line, url) for line, url, _ in findings] == [
        (1, "https://github.com/alexdundes/yoda/issues/7"),
        (2, "https://gitlab.com/someone/other/-/issues/12"),
    ]
    assert "own issue tracker" in findings[0][2]
    assert "external issue tracker" in findings[1][2]


def test_tracker_detection_survives_unresolvable_origin() -> None:
    findings = find_tracker_urls("see https://github.com/alexdundes/yoda/issues/7", None)

    assert len(findings) == 1
    assert "external issue tracker" in findings[0][2]


def test_tracker_detection_allows_ordinary_documentation_links() -> None:
    allowed = "\n".join(
        [
            "https://docs.github.com/articles/about-pull-requests",
            "https://news.ycombinator.com/item?id=1627246",
            "https://alexdundes.github.io/yoda/",
            "https://swagger.io/blog/code-first-vs-design-first-api/",
        ]
    )

    assert find_tracker_urls(allowed, ("github.com", "alexdundes/yoda")) == []


def test_commit_detection_allows_build_stamps_and_checksum_wording() -> None:
    allowed = "Generate `build` as `YYYYMMDD.<short-commit>`; example stamp 20260129, sha256 digest."

    assert find_commit_shas(allowed) == []


def test_detection_reports_both_reference_kinds() -> None:
    issue_ids = {"yoda-0001"}
    dev_slugs = {"yoda"}

    findings = find_forbidden_issue_references(
        "decided by yoda-0001\nsee yoda-9999 too\n", issue_ids, dev_slugs
    )

    assert [(line, fragment) for line, fragment, _ in findings] == [
        (1, "yoda-0001"),
        (2, "yoda-9999"),
    ]
    assert "backlog" in findings[0][2]
    assert "issue-shaped" in findings[1][2]


def test_detection_allows_generic_issue_model_and_unrelated_tokens() -> None:
    allowed = "\n".join(
        [
            "Issue path: `yoda/project/issues/<dev>-<NNNN>-<slug>.md`",
            "Timestamps use iso-8601 with an explicit offset.",
            "See `project/specs/00-conventions.md` for the canonical order.",
            "Name pattern: `<dev>-<NNNN>-<slug>.md`.",
        ]
    )

    findings = find_forbidden_issue_references(allowed, known_issue_ids(), known_dev_slugs())

    assert findings == []
