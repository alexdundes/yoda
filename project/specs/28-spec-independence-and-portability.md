# Spec independence and portability

## Objective

Define the bidirectional independence between the normative specification set
in `project/specs/` and the distributed YODA product under `yoda/`.

The two artifacts have different lifecycles and different audiences:

- `project/specs/` is the portable contract from which an implementer can
  rebuild YODA behavior.
- The product in `yoda/` and its distribution package must operate on their own,
  because the specification set is not part of the package.
- Development issues are history, planning, and traceability of one repository.
  They may point to specs, but they must never be required to interpret a
  normative rule.

## Self-containment

- A normative rule MUST be interpretable by reading `project/specs/` alone,
  without access to an issue backlog, Flow logs, or Git history.
- When a historical decision still matters for compatibility, the rule and its
  rationale MUST be written into the spec itself.
- A spec MUST NOT delegate normative authority to an artifact outside the
  specification set.

## Portability

- `project/specs/` MUST remain copyable as a standalone unit.
- No relative link inside `project/specs/` may resolve outside that directory.
- Files under `project/specs/` MAY link to each other freely.

## Reference taxonomy

Three kinds of reference must not be confused.

### 1. Reference to the YODA issue domain — allowed

Generic references to the issue model that the product implements, expressed as
path patterns or directory names:

- `yoda/project/issues/<dev>-<NNNN>-<slug>.md`
- `yoda/project/issues/`

These describe the specified product. They are part of the contract and MUST
remain documented.

### 2. Reference internal to the specification set — allowed

References to sibling specs, such as `project/specs/00-conventions.md`. These
keep the set coherent without leaving the portable unit.

### 3. Reference to this repository's development history — prohibited

A concrete issue identifier (`<dev>-<NNNN>`), a link or relative path to an
issue file, a Flow log entry, or a commit SHA MUST NOT be used as normative
authority or as indispensable context.

The prohibition is about the reference, not its notation. It covers equally:

- relative paths and links into an issue directory;
- plain textual issue identifiers;
- absolute URLs into an issue tracker, including the hosted tracker of the
  project itself, which YODA otherwise supports as an external issue source;
- commit hashes and Flow log excerpts.

Reference material that is part of the specification set, such as summaries of
external practices, MAY cite third-party sources; that material is background,
not a normative rule.

## Traceability direction

- `issue -> spec` is the permitted and recommended direction: an issue records
  which specs it changed.
- `spec -> issue` is prohibited: a spec must not depend on the backlog to be
  understood.

Removing a reference of the third kind never means removing the rule it
explained. The rule and its rationale move into the spec; only the dependency
on the development history disappears.

## Product independence

- The distribution package MUST NOT contain `project/specs/`.
- No packaged artifact may open, import, or resolve a path under
  `project/specs/` at runtime.
- The distributed product MUST initialize, operate, and update with
  `project/specs/` absent.

## Preventive verification

- An automated check MUST fail when a spec reintroduces either coupling
  direction.
- Its error MUST identify the file, the line, and the offending fragment.
- The check MUST NOT flag references of the first or second kind.

This spec states the requirement. The location and the runner of that check
belong to the repository that develops YODA, not to this normative contract.
