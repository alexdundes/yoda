"""Slug helpers."""

from __future__ import annotations

import re


def generate_issue_slug(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    if not slug:
        slug = "issue"
    if not slug[0].isalpha():
        slug = f"issue-{slug}"
    return slug

