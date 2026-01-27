---
schema_version: "1.0"
id: [ID]
title: [TITLE]
slug: [SLUG]
description: [SUMMARY]
status: to-do
priority: 5
lightweight: false
agent: Human
depends_on: []
pending_reason: ""
created_at: "[CREATED_AT]"
updated_at: "[UPDATED_AT]"
entrypoints: []
tags: []
origin:
  system: ""
  external_id: ""
  requester: ""
---

# [ID] - [TITLE]
<!-- AGENT: Replace [ID] with the canonical issue id (dev-id, e.g., alex-0001) from `yoda/todos/TODO.<dev>.yaml` and [TITLE] with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
<!-- AGENT: Provide a short summary of the problem and the intended change (2-4 sentences). -->

## Context
<!-- AGENT: Describe the current situation, pain points, and why this work is needed. -->

## Objective
<!-- AGENT: State the clear objective and expected outcome. -->

## Scope
<!-- AGENT: List what is in scope for this issue. -->
- 

## Out of scope
<!-- AGENT: List what is explicitly NOT part of this issue. -->
- 

## Requirements
<!-- AGENT: List functional requirements as bullet points. -->
- 

## Acceptance criteria
<!-- AGENT: List testable acceptance criteria. Use checkboxes. -->
- [ ] 

## Dependencies
<!-- AGENT: List dependencies and related issues (IDs). If none, write "None". -->

## Entry points
<!-- AGENT: List relevant files or artifacts used as references for implementation. -->
- path: 
  type: doc|code|config|schema|data|asset|other

## Implementation notes
<!-- AGENT: Add technical notes, constraints, or decisions needed to implement. -->

## Tests
<!-- AGENT: Describe tests to be added or updated. If not applicable, write \"Not applicable\". -->

## Risks and edge cases
<!-- AGENT: List risks, edge cases, or failure scenarios to consider. -->
- 

## Result log
<!-- AGENT: After implementation, summarize what was done and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
<!-- AGENT: In this repo's meta-implementation, logs are Markdown (`yoda/logs/<id>-<slug>.md`) until scripts exist. -->
