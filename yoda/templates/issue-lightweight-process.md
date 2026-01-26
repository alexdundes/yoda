---
schema_version: "1.0"
id: [ID]
title: [TITLE]
slug: [SLUG]
description: [SUMMARY]
status: to-do
priority: 5
lightweight: true
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
<!-- AGENT: Replace [ID] with the canonical issue id (dev-id, e.g., alex-0001) and [TITLE] with the issue title. Fill front matter fields from TODO; scripts must keep them in sync. Keep any <...> placeholders wrapped in inline code when used in prose. -->

## Summary
<!-- AGENT: One short paragraph describing what to build or change. -->

## What to implement
<!-- AGENT: List the exact steps or changes required. -->
- 

## Files to touch
<!-- AGENT: List files you will create or edit. -->
- 

## Acceptance check
<!-- AGENT: Define how the result will be verified. Use checkboxes. -->
- [ ] 

## Result log
<!-- AGENT: After implementation, write a short summary and include the commit message using this format:
First line: conventional commit message.
Body:
Issue: `<ID>`
Path: `<issue path>`
-->
<!-- AGENT: In this repo's meta-implementation, logs are Markdown (`yoda/logs/<id>-<slug>.md`) until scripts exist. -->
