# Documentation-Driven Development (DocDD)

## What it is

**Documentation-Driven Development (DocDD)** is an approach where you **write user-facing documentation before implementation** and treat that documentation as the **primary contract** for what the feature is and how it behaves.

A commonly cited framing is:

* If a feature is **not documented**, then (from a user perspective) it effectively **doesn’t exist**.
* If a feature is **documented incorrectly**, it’s **broken**. ([Gist][1])

DocDD is not “write docs at the end”. It is “define the feature in the language of the user first”, then implement to match the documented behavior. ([Gist][1])

---

## What “documentation” means in DocDD

DocDD emphasizes **consumer-oriented** documentation—what someone needs to successfully use the feature. That usually includes:

* **How-to / guides** (happy-path tasks)
* **Reference docs** (inputs/outputs, constraints, exact semantics)
* **Examples** (1 happy path + a few realistic edge cases)
* **Error behavior** (failures, invalid inputs, precondition violations)
* **Vocabulary / glossary** (consistent terms across docs, UI, API, logs)

The key is that documentation should be **actionable** and **testable**: a reader can follow it and know whether the feature works as described. ([Gist][1])

---

## Core principles

### 1) Documentation is the feature contract

Docs are treated as the **canonical description of behavior** (what it does, what it does not do, what errors look like). Implementation should converge to the documentation, not the opposite. ([Gist][1])

### 2) Feedback before code

Because docs are cheap to change, DocDD encourages review **before development begins**—ideally by users, stakeholders, or a representative group who can validate clarity and usefulness. ([Gist][2])

### 3) Tests should validate what the docs promise

DocDD often pairs naturally with TDD/BDD: tests become a way to ensure the implementation remains consistent with the documented contract. Some practitioners explicitly describe “documentation tests” or integration tests as “the executable form of your docs’ promises.” ([&yet Blog][3])

### 4) Version docs with the software

Documentation is part of the shipped product and should evolve with it. Versioning the docs alongside the code reduces drift and supports multiple versions in the wild. ([Gist][1])

---

## Typical workflow (feature slice)

A commonly described DocDD flow looks like:

1. **Draft docs** for the feature (from the user’s perspective)
2. **Review docs** (feedback loop: clarity, scope, missing cases)
3. **Implement** (often with TDD/BDD style)
4. **Validate** (staging/QA; ensure behavior matches docs)
5. **Ship**
6. **Publish/merge docs**
7. **Increment version** (if your process requires it) ([Gist][1])

**Important:** DocDD works best when applied in **thin slices** (small deliverables). Otherwise, it can degrade into “big upfront writing” (waterfall-like) and lose agility. (The practical mitigation is: document only what you intend to deliver in the next increment.) ([&yet Blog][3])

---

## How DocDD relates to adjacent ideas

### DocDD and “Docs-as-Code”

DocDD becomes much more scalable when combined with **Docs-as-Code**: documentation lives in version control, uses plain text formats, is reviewed via PRs, and can be validated via automation. ([Write the Docs][4])

### DocDD and API-first / contract-first

For APIs, DocDD overlaps with **contract-first** thinking: define the interface/behavior first (often with a spec), then implement against it. Even when you don’t use formal contracts (like OpenAPI), the DocDD mindset is similar: the “consumer contract” is written first and reviewed. ([Gist][1])

### DocDD and BDD

BDD can be seen as a close cousin: scenarios (“Given/When/Then”) are a human-readable contract that can be automated. DocDD isn’t limited to BDD syntax, but both share a “describe behavior first” worldview. ([&yet Blog][3])

---

## Benefits (why teams adopt it)

* **Clarity before complexity:** if you can’t explain it, you likely don’t understand it yet. ([&yet Blog][3])
* **Cheaper iteration:** changing wording is cheaper than rewriting code. ([Gist][2])
* **Better alignment:** docs are reviewable by dev, product, support, and users. ([Gist][2])
* **Reduced drift:** when docs are maintained with code, “stale docs” becomes a process failure you can catch early. ([Write the Docs][4])

---

## Common pitfalls (and mitigations)

### Pitfall: “Docs-first becomes waterfall”

**Mitigation:** write docs only for the next shippable slice; keep the doc scope small and iterative. ([&yet Blog][3])

### Pitfall: “Docs become stale”

**Mitigation:** adopt Docs-as-Code practices and make doc updates part of the PR definition-of-done. ([Write the Docs][4])

### Pitfall: “Docs are too aspirational / vague”

**Mitigation:** require concrete examples, explicit errors, constraints, and acceptance checks. (A good heuristic: could a new engineer or an agent implement this without guessing?) ([Gist][1])

---

## Why DocDD is especially useful with AI agents

In AI-assisted development, **context quality** dominates outcomes: agents are fast, but can diverge or hallucinate when the constraints and vocabulary are fuzzy. DocDD’s emphasis on “describe it for the user first” produces a stable, shared context that reduces guesswork and improves consistency across iterations. ([Doc Driven Development][5])

---

## Spec implications for YODA (normative hints)

These are **guidance-level norms** to shape YODA Framework specs and agent behavior (not a full YODA spec).

### MUST

* **MUST** create or update the **Issue Markdown** (user-facing description + acceptance criteria) *before* implementing code. ([Gist][1])
* **MUST** treat the Issue (and referenced spec docs) as the **contract**; implementation that contradicts docs is considered wrong until docs are updated. ([Gist][1])
* **MUST** include **explicit acceptance criteria** (even if small) for any implementable issue. ([Gist][1])
* **MUST** record **error behavior** and constraints when relevant (inputs, preconditions, failure modes). ([Gist][1])
* **MUST** keep docs in version control and review changes via PR-style workflow (Docs-as-Code), **quando houver fluxo PR/CI**. ([Write the Docs][4])

### SHOULD

* **SHOULD** document work in **thin slices** (small, shippable increments) to avoid “waterfall docs.” ([&yet Blog][3])
* **SHOULD** have tests that reflect the documented contract (“documentation tests” / integration checks aligned with docs). ([&yet Blog][3])
* **SHOULD** define and enforce a shared **vocabulary** across YAML metadata, Issue Markdown, UI labels, and logs. ([Write the Docs][4])
* **SHOULD** require doc review (human or stakeholder) for high-impact behaviors before coding. ([Gist][2])

### MAY

* **MAY** generate documentation skeletons/templates automatically (to reduce friction), as long as the human-readable contract remains clear and editable. ([Write the Docs][4])
* **MAY** introduce “doc linting” (automation that checks required sections/fields) to prevent incomplete specs from entering the main branch. ([Write the Docs][4])

---

## References

* Zach Supalla — “Documentation-Driven Development (DDD)” (foundational DocDD framing, workflow, review-before-code, tests/versions alignment). ([Gist][1])
* Write the Docs — “Docs as Code” (docs in git, PR review, automation). ([Write the Docs][4])
* &yet blog — “documentation-driven-development… integration tests as documentation tests” (practitioner framing). ([&yet Blog][3])
* DocDD.ai / Ryan Vice — “Context is King… DocDD for AI-assisted development” (DocDD as context-first discipline). ([Doc Driven Development][5])

---

[1]: https://gist.github.com/zsup/9434452?utm_source=chatgpt.com "Documentation-Driven Development (DDD)"
[2]: https://gist.github.com/zsup/9434452?permalink_comment_id=4340435&utm_source=chatgpt.com "Documentation-Driven Development (DDD)"
[3]: https://blog.andyet.com/2014/11/04/your-code-isnt-the-most-important/?utm_source=chatgpt.com "Your code isn't the most important part of your project | &yet blog"
[4]: https://www.writethedocs.org/guide/docs-as-code.html?utm_source=chatgpt.com "Docs as Code"
[5]: https://docdd.ai/events/12th-cto-colloquium-park-city-ut?utm_source=chatgpt.com "Context is King: Boosting Developer Productivity with DocDD"
