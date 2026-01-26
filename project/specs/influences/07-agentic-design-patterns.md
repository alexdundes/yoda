# Agentic Design Patterns

## What it is

**Agentic design patterns** are recurring, reusable solutions for building **LLM-powered agents**—systems that can plan, decide, use tools, collaborate, and iteratively improve outputs.

In this context, *Agentic Design Patterns* also refers to the book **“Agentic Design Patterns: A Hands-On Guide to Building Intelligent Systems”** by **Antonio Gullí**, published by **Springer** (Oct 2025). The book presents a catalog of **21 essential agentic patterns**, with hands-on examples and a framework-agnostic orientation (it explicitly mentions examples using tools like LangChain, CrewAI, and Google ADK). ([Springer Nature][1])

---

## Why patterns matter in agentic systems

Agentic systems fail in predictable ways:

* they wander without a plan,
* they choose the wrong next step,
* they get stuck in loops,
* they hallucinate tool usage or misuse tools,
* they produce outputs without verification.

Patterns exist because these failure modes repeat. A pattern gives you:

* a **known structure** for reasoning + action,
* explicit **boundaries** (inputs/outputs/states),
* and places to add **quality controls**.

This “patterns as reusable blueprints” framing is a common explanation in modern agentic systems discussions. ([philschmid.de][2])

---

## Typical pattern families (how to mentally organize the space)

Different sources group patterns differently, but for practical engineering and for YODA alignment, it’s useful to think in families:

### 1) Decomposition and flow control

Patterns that prevent “one big prompt” from becoming chaos:

* **Prompt Chaining**: break a task into sequential steps (each with clear IO).
* **Routing**: choose a path based on classification/conditions.
* **Parallelization**: run sub-tasks concurrently and then merge.

These are commonly cited as foundational agent workflows and are explicitly referenced as examples in discussions of agentic patterns and in reviews of the book. ([Medium][3])

### 2) Tool use and action loops

Patterns that allow the agent to go beyond “text generation”:

* **Tool Use / Function Calling**: call external tools/APIs deterministically.
* **ReAct-like loops**: interleave reasoning with actions and observations.

Tool use is repeatedly highlighted as a core agentic pattern because it changes the system from “model-only” to “model + capabilities.” ([LinkedIn][4])

### 3) Planning and task management

Patterns that create *intent* and prevent wandering:

* **Planning**: create an explicit plan (steps/goals) before execution.
* **Task decomposition with checkpoints**: enforce incremental progress and re-planning.

Planning is also recognized as one of the key “agentic design patterns” in system-theoretic framings of agentic systems. ([openreview.net][5])

### 4) Quality control and self-correction

Patterns that improve reliability:

* **Reflection / Self-checking**: critique and refine outputs.
* **Self-correction loops**: detect failure and repair.
* **Validation gates**: verify constraints before producing final output.

Reflection and self-correction show up repeatedly as central patterns for robustness. ([Medium][3])

### 5) Collaboration and coordination

Patterns for multiple roles/agents:

* **Multi-agent collaboration**: specialized agents with handoffs.
* **Human-in-the-loop**: explicit approval steps for high-impact actions.

Modern agentic guidance frequently emphasizes that multi-agent setups increase capability but require stronger coordination and contracts. ([philschmid.de][2])

---

## Relevance to YODA Framework

YODA is fundamentally about turning “agent work” into a **repeatable, auditable workflow**. Agentic design patterns provide a vocabulary and set of defaults for how YODA should behave when agents:

* **Plan work** (what to do next, what’s blocked, what requires spec updates),
* **Route work** (choose which issue/step to execute),
* **Use tools** (YODA scripts as tools),
* **Reflect/evaluate** (quality gates, logs, validation, status updates),
* **Coordinate** (multi-agent or role-based execution).

The book positioning as a “catalog of patterns for building robust agentic systems” maps directly onto YODA’s goal: constrain agent behavior using explicit artifacts + scripts. ([Springer Nature][1])

---

## Suggested use in YODA (practical mapping)

Below is a **high-leverage** mapping between common agentic pattern intents and YODA artifacts:

* **Planning →** Issue Markdown (acceptance criteria) + TODO metadata (priority, depends_on, status)
* **Routing →** `todo_next.py` + deterministic selection rules
* **Prompt Chaining →** YODA Flow phases (Study → Document → Implement → Evaluate)
* **Tool Use →** YODA scripts (validated, deterministic IO; JSON outputs; exit codes)
* **Reflection/Self-correction →** Evaluate phase + logs + `validate` checks
* **Parallelization →** multiple issues/subtasks in TODO (or multi-agent workers) with merge rules
* **Human-in-the-loop →** explicit “approval required” fields / states before high-impact actions

This aligns with the general principle that patterns are most useful when they map to **concrete interfaces and state**—exactly what YODA is formalizing. ([philschmid.de][2])

---

## Spec implications for YODA (normative hints)

These are guidance-level norms to shape YODA Framework specs and agent behavior.

### MUST

* **MUST** encode a **planning step** before execution for non-trivial work (the plan can be small, but must exist). ([openreview.net][5])
* **MUST** treat YODA scripts as **tools** with deterministic contracts (inputs/outputs/exit codes; machine-readable output like JSON). ([DEV Community][6])
* **MUST** implement a **reflection/quality gate** in the flow (Evaluate) that validates the output against acceptance criteria and records results in logs. ([Medium][3])
* **MUST** keep routing deterministic (given the same TODO state, the same “next issue” decision occurs). This is the equivalent of “routing pattern with stable rules.”

### SHOULD

* **SHOULD** separate responsibilities into clear roles (planner / executor / verifier), even if all roles run in one agent at v1. This mirrors multi-agent thinking without forcing multi-agent complexity. ([philschmid.de][2])
* **SHOULD** provide “safe action” controls for tools (e.g., `--dry-run`, validation-first, and explicit confirmation boundaries where needed).
* **SHOULD** allow “parallelizable” work to be represented explicitly (subtasks, separate issues) and define merge/evaluation rules. ([philschmid.de][2])

### MAY

* **MAY** introduce multi-agent collaboration patterns later (specialized agents per domain), but only after contracts and evaluation gates are strong enough to prevent drift. ([philschmid.de][2])
* **MAY** adopt contract-testing-like checks for agent expectations (tests that verify scripts and artifact behaviors remain stable as the framework evolves). ([openreview.net][5])

---

## References

* SpringerLink (book page) — **Agentic Design Patterns** (Antonio Gullí), highlights “21 essential agentic patterns” and hands-on examples. ([Springer Nature][1])
* Amazon (book details) — publication date and ISBN metadata for the same title. ([Amazon][7])
* Phil Schmid — overview of common agentic patterns and when to use agents. ([philschmid.de][2])
* OpenReview paper — system-theoretic framing of agentic design patterns (reflection, tool use, planning, etc.). ([openreview.net][5])
* Review/summary discussion (non-authoritative but useful) — mentions foundational patterns like prompt chaining and tool use. ([Medium][3])

---

[1]: https://link.springer.com/book/10.1007/978-3-032-01402-3?utm_source=chatgpt.com "Agentic Design Patterns - Springer Link"
[2]: https://www.philschmid.de/agentic-pattern?utm_source=chatgpt.com "Zero to One: Learning Agentic Patterns"
[3]: https://medium.com/%40adnanmasood/review-agentic-design-patterns-a-hands-on-guide-to-building-intelligent-systems-f65200a9eb0c?utm_source=chatgpt.com "Review: Agentic Design Patterns: A Hands-On Guide to ..."
[4]: https://www.linkedin.com/pulse/agentic-ai-design-patterns-5-tool-use-function-calling-tanmay-patra-gduuc?utm_source=chatgpt.com "Agentic AI Design Patterns #5: Tool Use (Function Calling)"
[5]: https://openreview.net/pdf/066e3d13cbc5a82a8c97b1861bb97c4b3cbbb053.pdf?utm_source=chatgpt.com "Agentic Design Patterns: A System-Theoretic Framework"
[6]: https://dev.to/knitex/common-agentic-ai-architecture-patterns-522d?utm_source=chatgpt.com "Common Agentic AI Architecture patterns"
[7]: https://www.amazon.com/Agentic-Design-Patterns-Hands-Intelligent-ebook/dp/B0FH1RQSWP?utm_source=chatgpt.com "Agentic Design Patterns: A Hands-On Guide to Building ..."
