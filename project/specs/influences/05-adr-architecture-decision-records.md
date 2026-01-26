# Architecture Decision Records (ADR)

## What it is

An **Architecture Decision Record (ADR)** is a **short, text-based document** that captures **one important decision**, along with its **context** and **consequences**. The practice was popularized by Michael Nygard’s 2011 “Documenting Architecture Decisions”, which describes ADRs as lightweight records stored in the repository (e.g., `doc/arch/adr-NNN.md`). ([Cognitect.com][1])

A useful vocabulary used by ADR practitioners:

* **AD (Architecture Decision):** a significant design choice that addresses an important requirement.
* **ADR:** the record for one AD.
* **ADL (Architecture Decision Log):** the collection of ADRs for a project (the “decision history”). ([GitHub][2])

---

## Why ADRs exist

Teams make “big” decisions constantly (tech choices, data models, integration patterns, naming conventions, compatibility policies). Over time, the *why* fades, people leave, and decisions get re-litigated. ADRs reduce that churn by preserving:

* **Context** (forces/constraints, what problem existed),
* **Decision** (what was chosen),
* **Consequences** (tradeoffs, follow-up work, risks). ([Cognitect.com][1])

AWS describes ADRs as a way to streamline technical decision-making and maintain a **decision log** that helps newcomers get project context quickly. ([Documentação AWS][3])

---

## What makes a decision “ADR-worthy”

Create an ADR when the decision is likely to be:

* **Hard to reverse** (or costly to change),
* **Cross-cutting** (affects many parts of the system),
* **A long-term constraint** (standards, compatibility rules, security posture),
* **Frequently questioned** (decisions that keep resurfacing). ([Thoughtworks][4])

Keep ADRs **lightweight**: Thoughtworks explicitly promotes “Lightweight Architecture Decision Records” as a technique for capturing essential decisions without heavy documentation overhead. ([Thoughtworks][4])

---

## Typical ADR structure (templates)

### The “Nygardian” ADR (classic minimal template)

Nygard’s widely adopted format focuses on a few essential sections:

* **Title**
* **Date**
* **Status**
* **Context**
* **Decision**
* **Consequences** ([Cognitect.com][1])

### MADR (Markdown Architectural Decision Records)

**MADR** is a streamlined Markdown template designed to capture ADRs “in a lean way” while keeping structure consistent and easy to review. It’s commonly used when teams want more guidance and optional sections without making ADRs heavy. ([Architectural Decision Records][5])

### Multiple templates are normal

There’s no single global standard—ADR templates vary (Nygard, MADR, Y-Statements, etc.). The key is to choose one template and keep it consistent inside the project. ([Architectural Decision Records][6])

---

## ADR lifecycle and states

ADRs usually have **states** and follow a **lifecycle**. AWS guidance explicitly calls out that ADRs have states and describes the ADR process as producing a decision log that helps provide project context. ([Documentação AWS][7])

Common status set (practical and widely compatible):

* **Proposed** (draft, under discussion)
* **Accepted** (decision approved and active)
* **Superseded** (replaced by a newer ADR)
* **Deprecated** (no longer recommended; may be replaced or sunset)

> Tip: prefer **Superseded** over editing history. If a decision changes, write a new ADR and link them.

---

## Process (how ADRs work in practice)

A lightweight, effective process (aligned with AWS + common ADR practice):

1. **Create** a new ADR in *Proposed* state
2. **Review** with relevant stakeholders (async in PR comments works well)
3. **Accept** (update status to *Accepted*)
4. **Implement** and link the ADR in the related PR/issue
5. **Supersede** with a new ADR if the decision changes later ([Documentação AWS][8])

AWS also emphasizes “ownership” (an ADR owner/author shepherds the document to acceptance) and that the ADR log gives newcomers an at-a-glance understanding of project context. ([Documentação AWS][9])

---

## Tooling (optional, but helpful)

### adr-tools (Nat Pryce)

**adr-tools** is a command-line tool to manage an ADR log (initialize, create new ADRs, keep numbering consistent). It exists specifically to keep ADRs lightweight and easy to maintain in-repo. ([GitHub][10])

### Viewers / publishing

Some teams add a viewer or static site for ADR browsing, but this is optional—Git + PR review is often sufficient for v1 workflows. (For example, tools like ADR viewers exist to present ADRs as navigable web pages.) ([PyPI][11])

---

## Common pitfalls (and how to avoid them)

1. **ADR sprawl (too many trivial ADRs)**

   * Keep ADRs for *architecturally significant* decisions only. ([Open Practice Library][12])

2. **“Aspirational ADRs” that don’t match reality**

   * Ensure acceptance happens before implementation (or immediately alongside it), and treat ADRs as part of the deliverable. ([Documentação AWS][8])

3. **Editing old ADRs instead of superseding**

   * Prefer “Superseded by ADR-XXXX” with a new ADR to preserve history. ([Documentação AWS][8])

4. **No clear ownership**

   * Assign an owner for Proposed ADRs so they don’t rot in draft state. ([Documentação AWS][9])

---

## How ADRs inspire YODA Framework

YODA is itself a “framework of contracts” (schemas, CLI behavior, file conventions, agent rules). ADRs are ideal to record decisions like:

* “Why YAML-first for metadata?”
* “Why this TODO schema and status model?”
* “Why these CLI outputs and exit codes?”
* “Why this repository layout and entrypoint precedence?”

In other words: ADRs help YODA stay coherent as it evolves, especially when multiple agents (and humans) propose changes.

---

## Spec implications for YODA (normative hints)

These are guidance-level norms to shape YODA’s design and agent behavior.

### MUST

* **MUST** record an ADR for any decision that changes YODA’s **public contracts** (schemas, CLI outputs, artifact paths, compatibility policy). ([Cognitect.com][1])
* **MUST** keep ADRs as plain-text, version-controlled files (reviewed like code). ([Cognitect.com][1])
* **MUST** include at least: **Status, Context, Decision, Consequences** (Nygard/MADR minimal core). ([Cognitect.com][1])
* **MUST** supersede decisions with a new ADR when the decision changes, rather than rewriting history. ([Documentação AWS][8])

### SHOULD

* **SHOULD** keep ADRs lightweight (1 decision per ADR; short, scannable). ([Thoughtworks][4])
* **SHOULD** standardize on one ADR template (e.g., Nygard or MADR) and apply it consistently. ([Architectural Decision Records][6])
* **SHOULD** link ADRs to the issues/PRs that implement them (“decision ↔ implementation” traceability). ([Documentação AWS][8])
* **SHOULD** define a small status lifecycle and enforce it (Proposed → Accepted → Superseded). ([Documentação AWS][7])

### MAY

* **MAY** use a helper tool (e.g., adr-tools) to keep numbering and structure consistent. ([GitHub][10])
* **MAY** publish/browse ADRs with a viewer if the ADR log grows large. ([PyPI][11])

---

## References

* Michael Nygard — “Documenting Architecture Decisions” (origin/popularization; ADR format and in-repo storage). ([Cognitect.com][1])
* AWS Prescriptive Guidance — ADR process, lifecycle/state concept, decision log outcomes. ([Documentação AWS][3])
* Thoughtworks Technology Radar — “Lightweight Architecture Decision Records” technique. ([Thoughtworks][4])
* adr.github.io — ADR templates overview and landscape. ([Architectural Decision Records][6])
* MADR (Markdown ADR template) — rationale and templates. ([Architectural Decision Records][5])
* Nat Pryce — adr-tools (CLI for ADR logs). ([GitHub][10])

[1]: https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions?utm_source=chatgpt.com "Documenting Architecture Decisions - Cognitect.com"
[2]: https://github.com/joelparkerhenderson/architecture-decision-record?utm_source=chatgpt.com "Architecture decision record (ADR) examples for software ..."
[3]: https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/welcome.html?utm_source=chatgpt.com "Using architectural decision records to streamline technical ..."
[4]: https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records?utm_source=chatgpt.com "Lightweight Architecture Decision Records"
[5]: https://adr.github.io/madr/?utm_source=chatgpt.com "About MADR"
[6]: https://adr.github.io/adr-templates/?utm_source=chatgpt.com "ADR Templates | Architectural Decision Records"
[7]: https://docs.aws.amazon.com/pt_br/prescriptive-guidance/latest/architectural-decision-records/adr-process.html?utm_source=chatgpt.com "Processo de ADR - AWS Orientação prescritiva"
[8]: https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html?utm_source=chatgpt.com "ADR process - AWS Prescriptive Guidance"
[9]: https://docs.aws.amazon.com/pdfs/prescriptive-guidance/latest/architectural-decision-records/architectural-decision-records.pdf?utm_source=chatgpt.com "architectural-decision-records.pdf"
[10]: https://github.com/npryce/adr-tools?utm_source=chatgpt.com "npryce/adr-tools: Command-line tools for working ..."
[11]: https://pypi.org/project/adr-viewer/?utm_source=chatgpt.com "adr-viewer"
[12]: https://openpracticelibrary.com/practice/architectural-decision-records-adr/?utm_source=chatgpt.com "Architectural Decision Records (ADR)"
