---
agent: Human
created_at: '2026-01-27T13:32:13-03:00'
depends_on: []
description: Define the official brand voice and terminology guidelines for the YODA
  Framework. This should establish tone, preferred terms, and consistency rules across
  documentation. The goal is to remove ambiguity in how the framework is described.
entrypoints: []
id: yoda-0025
lightweight: false
origin:
  external_id: ''
  requester: ''
  system: ''
pending_reason: ''
priority: 7
schema_version: '1.0'
slug: definir-brand-voice
status: done
tags: []
title: Definir brand voice e terminologia
updated_at: '2026-01-27T13:32:38-03:00'
---

# yoda-0025 - Define brand voice and terminology

## Summary
Define the official brand voice and terminology guidelines for the YODA Framework. This should establish tone, preferred terms, and consistency rules across documentation. The goal is to remove ambiguity in how the framework is described.

## Context
Brand voice is listed as an open decision. Current docs mix informal and formal language without a declared style guide.

## Objective
Decide the brand voice and terminology guidelines and update the canonical specs and summary.

## Scope
- Define tone and terminology rules for docs.
- Document the guidelines in canonical spec file(s).
- Update the summary to close the decision.

## Out of scope
- Visual identity changes.
- Marketing materials or external branding assets.

## Requirements
- Voice and terminology are explicit and consistent.
- The decision is recorded in canonical specs.
- project/specs/summary.md reflects the closure.

## Acceptance criteria
- [ ] Brand voice and terminology guidelines are documented in canonical specs.
- [ ] project/specs/summary.md no longer lists brand voice as open.

## Dependencies
None

## Entry points
- path: project/specs/summary.md
  type: issue
- path: project/specs/00-conventions.md
  type: issue
- path: project/specs/01-yoda-overview.md
  type: issue
- path: README.md
  type: other

## Implementation notes
- Keep terms consistent with existing references like "YODA Flow" and `TODO.<dev>.yaml`.

## Tests
Not applicable.

## Risks and edge cases
- Overly strict guidelines could limit contributions from different audiences.

## Result log
Defined brand voice and terminology in canonical specs, closed the decision in the summary, and removed the open status entry from README.md.

Commit:
docs(specs): define brand voice and terminology

Issue: yoda-0025
Path: yoda/project/issues/yoda-0025-definir-brand-voice.md

Follow-up: aligned YODA Flow phase naming in specs README and summary.
Follow-up: standardized phase naming in README and YODA Flow process spec.
Follow-up: replaced "task" wording with "issue" where it implied the unit of work.
Follow-up: tightened README phrasing to match the brand voice (clear, technical, pragmatic).
Follow-up: tightened language in specs overview and document-first guidance.
Follow-up: tightened language across remaining specs files.
Follow-up: tightened language in YODA structure and influence reference docs.
Follow-up: removed soft adjectives in specs index and YAML docs.
Follow-up: wrapped `<dev>` terms in inline code to avoid Markdown tag parsing.
Follow-up: documented inline-code rule for angle-bracket tokens in conventions.
Follow-up: added inline-code reminder for `<...>` placeholders in issue templates.