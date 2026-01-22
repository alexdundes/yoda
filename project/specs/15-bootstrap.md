# Bootstrap (temporary)

## Purpose

Document the bootstrap mode used by this meta-implementation while scripts are not available.

## Definition

Bootstrap is a temporary documentation-only mode for the YODA Framework meta-implementation.

## Rules

- Use `TODO.<dev>.md` instead of `TODO.<dev>.yaml`.
- Use Markdown logs at `yoda/logs/dev-id-slug.md` instead of YAML logs.
- Agent entry checks for `TODO.<dev>.md` when YAML is not available.
- Scripts are optional during bootstrap and may be missing.
- Manual updates to `TODO.<dev>.md` are allowed in bootstrap, but YAML updates must use scripts once available.

## Exit and removal

- When scripts exist, bootstrap mode ends and this document is removed from the specs.
- The canonical framework uses YAML for TODOs and logs.
