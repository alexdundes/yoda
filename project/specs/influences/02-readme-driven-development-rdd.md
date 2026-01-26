# README-Driven Development (RDD)

## What it is

**README-Driven Development (RDD)** is a practice where you **write the project’s `README.md` first**—before you write code—so that the README becomes the **initial, user-facing contract** for what you’re building and how people will use it.

The idea was popularized by **Tom Preston-Werner** (GitHub co-founder) in his 2010 post “Readme Driven Development”, where he argues that writing the README first forces you to clarify what you’re actually building and how it should be used. ([Tom Preston-Werner][1])

RDD is intentionally pragmatic: the README is the **first contact** for users, contributors, and future maintainers. It is the place where the project must answer: *What is this? Why does it exist? How do I use it?*

---

## Why “README first” works

### It forces an “outside-in” design

When you write the README first, you are forced to think in terms of the **public interface**:

* what the project does (scope),
* how it’s installed,
* what the primary usage looks like,
* what the “happy path” is,
* what people should *not* expect.

This pushes you to make design choices early—especially about **API shape**, CLI commands, configuration surface, terminology, and examples—before implementation inertia makes changes expensive. ([Tom Preston-Werner][1])

### It’s also a reality check

A well-written README can reveal when:

* the problem isn’t compelling,
* the solution is too complex for the value delivered,
* the interface feels awkward,
* the feature list is unclear or incoherent.

This “cheap falsification” is one of RDD’s biggest benefits: you can abandon or reshape an idea before committing code. ([Tom Preston-Werner][1])

### It improves adoption and collaboration

Even early-stage projects benefit from a clear README: it helps people understand why the project matters, how to get started, and how to contribute. Community discussions around the original RDD post highlight that a strong README helps new users engage because it provides a direct path to “try it”. ([Hacker News][2])

---

## What a “RDD-quality” README typically contains

RDD doesn’t mandate a single template, but the README should cover the minimum information that enables a user to succeed quickly. A solid structure is:

1. **Name + one-line pitch**
2. **Problem statement / motivation** (why it exists)
3. **What it does / what it doesn’t** (explicit scope boundaries)
4. **Quickstart** (the shortest path to a working example)
5. **Installation**
6. **Usage** (primary flows with examples)
7. **Configuration** (env vars, config files, defaults)
8. **Interface reference**

   * CLI: commands, options, exit codes
   * Library: main API surface, function signatures, invariants
9. **Errors & troubleshooting** (common failure modes)
10. **Contributing / development** (how to run tests, local setup)
11. **License** / governance (when relevant)

This mirrors general best practices for README content: explain what it does, how to use it, and how to collaborate. ([Appsmith][3])

> Important: RDD does **not** claim that a README is the only documentation you’ll ever need. The README is the *entrypoint* and the “contract summary”; deeper docs can and should exist when complexity demands it. ([Medium][4])

---

## A typical RDD workflow (thin slice)

RDD is most effective when done **iteratively**, in small deliverable slices:

1. **Draft the README first**

   * Quickstart + primary usage + scope boundaries
2. **Review/feedback**

   * Can a new person understand it?
   * Are the examples realistic?
   * Is the interface obvious?
3. **Implement against the README**

   * Treat examples as targets (your code should make them true)
4. **Tighten the README**

   * Update wording, add edge cases you discovered
5. **Repeat**

   * Each new capability starts as a README change (or README + linked docs)

This matches a common RDD framing: writing the README first clarifies the external shape and keeps implementation focused. ([Tom Preston-Werner][1])

---

## Relationship to adjacent practices

### RDD vs DocDD

* **RDD**: “Start with README first” (high-leverage entrypoint; great for small/medium projects, libraries, CLIs).
* **DocDD**: “Start with user documentation first” (broader; includes guides, reference docs, and deeper contracts). RDD can be seen as a *subset* or “minimum viable DocDD”. ([Tom Preston-Werner][1])

### RDD + Docs-as-Code

RDD becomes durable when combined with **Docs-as-Code** workflows: docs in Git, PR review, automation, and tests/checks that keep docs aligned with behavior. ([Write the Docs][5])

### RDD for APIs and CLIs

RDD shines for:

* libraries (public API clarity),
* CLIs (command semantics),
* SDKs and integrations (quickstart + examples).

In these cases, the README is effectively a “human contract” that influences the formal contract you may later adopt (OpenAPI, JSON Schema, etc.).

---

## Benefits

* **Faster alignment**: a README can be reviewed by devs, stakeholders, and users with low friction. ([Tom Preston-Werner][1])
* **Better interface design**: encourages designing from the consumer’s perspective. ([Medium][4])
* **Reduced wasted work**: exposes unclear value/complexity before code is written. ([Tom Preston-Werner][1])
* **Improved onboarding**: makes it easier for new contributors to get started. ([Hacker News][2])

---

## Common pitfalls and mitigations

### Pitfall: “The README becomes marketing only”

If the README is only a pitch, it stops being a contract.

**Mitigation:** require a **real Quickstart** and at least one concrete “usage” path that can be validated. ([Appsmith][3])

### Pitfall: “README is not enough documentation”

As the system grows, a single README can become overloaded.

**Mitigation:** keep README as the entrypoint and link to deeper docs/specs; still keep the README updated as the “front door”. ([Medium][4])

### Pitfall: “Docs drift from behavior”

Docs that are not part of the delivery process will go stale.

**Mitigation:** adopt Docs-as-Code (PR reviews, automation, gates). ([Write the Docs][5])

---

## How it inspires YODA Framework

RDD is particularly relevant to YODA because YODA depends on **stable, shared context** for both humans and agents.

RDD suggests that YODA should have:

* a **single, clear entrypoint document** (“front door”) that explains *what YODA is* and *how to use it*,
* a Quickstart that an agent can follow deterministically,
* minimal but explicit contracts for CLI/scripts and repository structure,
* a strong separation between **entrypoint (README)** and **deep specs** (linked and organized).

---

## Spec implications for YODA (normative hints)

These are guidance-level norms to shape YODA’s design and how agents operate.

### MUST

* **MUST** provide a **primary human entrypoint** README for the framework (the “front door”) that answers: *what it is, why it exists, quickstart, and where the specs live*. The **agent entrypoint** is [`yoda/yoda.md`](/yoda/yoda.md). ([Tom Preston-Werner][1])
* **MUST** include a **real Quickstart** in the README (or link to a Quickstart doc) that results in a working minimal flow (even if bootstrap). ([Appsmith][3])
* **MUST** treat README usage examples as **contractual targets**: if examples are present, the implementation must make them true (or the README must be updated). ([Tom Preston-Werner][1])
* **MUST** keep README changes under version control and review them with the same discipline as code (Docs-as-Code). ([Write the Docs][5])

### SHOULD

* **SHOULD** keep the README focused on **user-facing outcomes** (how to use), not internal architecture (which belongs in deeper specs). ([Appsmith][3])
* **SHOULD** document **scope boundaries** explicitly (“YODA does X; YODA does not do Y”) to reduce agent overreach. ([Tom Preston-Werner][1])
* **SHOULD** link from README to deeper specs using a stable structure (so agents can navigate deterministically).
* **SHOULD** prefer **thin-slice README updates** per deliverable (small increments) instead of “big README rewrite” releases. ([Medium][4])

### MAY

* **MAY** use README templates/checklists to enforce minimum sections (Quickstart, Usage, Contracts, Troubleshooting). ([Appsmith][3])
* **MAY** add automated checks (lint/gates) that validate README has required sections and that referenced files/paths exist (Docs-as-Code automation). ([Write the Docs][5])

---

## References

* Tom Preston-Werner — “Readme Driven Development” (origin and core rationale). ([Tom Preston-Werner][1])
* Write the Docs — “Docs as Code” (process discipline to prevent drift). ([Write the Docs][5])
* Elliot Chance — “Readme Driven Development” (benefits framing: focus, clarity, progress indicator). ([Medium][4])
* Appsmith — “How to Write a Great README” (README structure expectations). ([Appsmith][3])

[1]: https://tom.preston-werner.com/2010/08/23/readme-driven-development?utm_source=chatgpt.com "Readme Driven Development - Tom Preston-Werner"
[2]: https://news.ycombinator.com/item?id=1627246&utm_source=chatgpt.com "Readme Driven Development"
[3]: https://www.appsmith.com/blog/write-a-great-readme?utm_source=chatgpt.com "How to Write a Great README"
[4]: https://medium.com/%40elliotchance/readme-driven-development-3a434b7e253c?utm_source=chatgpt.com "Readme Driven Development"
[5]: https://www.writethedocs.org/guide/docs-as-code.html?utm_source=chatgpt.com "Docs as Code"
