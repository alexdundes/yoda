# Bootstrap (temporary)

## Purpose

Document the bootstrap mode used by this meta-implementation while scripts are not available.

## Definition

Bootstrap is a temporary documentation-only mode for the YODA Framework meta-implementation.

## Rules

- Use `TODO.<dev>.md` instead of `TODO.<dev>.yaml`.
- Use Markdown logs at `yoda/logs/<id>-<slug>.md` instead of YAML logs.
- Agent entry checks for `TODO.<dev>.md` when YAML is not available.
- Scripts are optional during bootstrap and may be missing.
- Manual updates to `TODO.<dev>.md` are allowed in bootstrap, but YAML updates must use scripts once available.
- Bootstrap does not allow coexistence of `TODO.<dev>.md` and `TODO.<dev>.yaml`; only one format exists at a time.
- Any mention of bootstrap in specs must explicitly state that it is temporary and will be removed.
- Unless explicitly marked as bootstrap, documentation targets the future non-bootstrap phase.

## Exit and removal

- When scripts exist, bootstrap mode ends and this document is removed from the specs.
- The canonical framework uses YAML for TODOs and logs.
- All bootstrap-specific documentation is temporary and must be removed when bootstrap ends.
