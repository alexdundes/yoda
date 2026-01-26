# Literate Programming and Computational Notebooks

## What it is

### Literate Programming (Knuth)

**Literate Programming (LP)** is a programming paradigm introduced by Donald Knuth in the 1980s where a program is written primarily as **an explanatory narrative for humans**, with code embedded inside that narrative. The same source can be processed to produce:

* **“tangled”** machine-executable source code, and
* **“woven”** human-readable documentation. ([Wikipedia][1])

Knuth’s original tooling (WEB / CWEB) embodied the idea that we should write software in the **order of human reasoning**, not in the order imposed by a compiler. ([Wikipedia][1])

### Literate Computing (Notebooks as the modern expression)

Computational notebooks (like Jupyter) are often described as a modern “literate computing” environment: they combine **narrative text**, **executable code**, and **rendered outputs** (tables, figures, results) in a single document. ([docs.jupyter.org][2])

Millman & Pérez (2014) argue that a literate computing approach (interactive notebooks) is a better fit for the needs of reproducibility in computational research than traditional literate programming tools, using the IPython/Jupyter notebook as an example. ([jarrodmillman.com][3])

---

## The core concepts that matter

### 1) Narrative-first structure

In LP and notebook-style literate computing, the primary artifact is a **story of intent**:

* the “why” and “what”
* the assumptions and constraints
* the steps a reader should follow
* and only then the code fragments that realize it ([Wikipedia][1])

This idea maps strongly to agentic development: the narrative constrains the code, instead of the code being the only truth.

### 2) “Weave” and “tangle” as a general pattern

The classic LP framing is:

* **Weave:** produce formatted documentation from the literate source
* **Tangle:** extract/assemble executable code from the literate source ([Wikipedia][1])

Modern notebook/publishing systems implement similar patterns:

* Jupyter Books can **execute notebook content and include outputs** in generated docs ([jupyterbook.org][4])
* Quarto positions itself as a system for creating **reproducible, re-generatable** documents from executable sources ([Quarto][5])

### 3) Notebook documents are code + state + output

Jupyter notebooks (`.ipynb`) are **JSON documents** composed of ordered “cells” containing text/code/output plus metadata. ([docs.jupyter.org][2])
That makes notebooks powerful for exploration and explanation, but it also introduces reproducibility hazards (see below).

---

## Why notebooks are powerful (and why they can be dangerous)

### Strengths

* **Exploration + explanation in one artifact** (ideal for discovery and teaching) ([docs.jupyter.org][2])
* **Outputs are captured** next to the code that produced them (figures, tables, derived values) ([nbformat.readthedocs.io][6])
* Good fit for “build knowledge, then harden into software”

### Reproducibility pitfalls

Notebooks can easily become **non-reproducible** due to:

* **hidden state** in the running kernel (variables created earlier)
* **out-of-order execution** (cells run in a different order than they appear)
* reliance on external environment (packages, data paths, credentials)

A widely recommended discipline is to **restart the kernel and run all cells top-to-bottom** before committing or considering a notebook “done”, to catch missing dependencies and ordering bugs. ([Carpenter-Singh Lab][7])

---

## Techniques to make notebooks “production-grade”

### 1) Parameterization and repeatable execution

A common approach is to treat a notebook as a parameterized, repeatable job:

* **Papermill** parameterizes notebooks by tagging a “parameters” cell, then executes the notebook with a chosen parameter set ([papermill.readthedocs.io][8])
* This enables consistent re-runs and integration into pipelines

“Ten Simple Rules for Reproducible Research in Jupyter Notebooks” (Rule et al., 2018) explicitly discusses parameterizing notebooks with tools like papermill as a reproducibility technique. ([arXiv][9])

### 2) Publish notebooks as structured docs

* **Jupyter Book**: build books/sites from notebooks and MyST Markdown; supports execution and embedding outputs ([jupyterbook.org][10])
* **Quarto**: publish reproducible documents (HTML/PDF/Word/etc.) from executable sources ([Quarto][5])

### 3) Separate “exploration” from “library code”

A practical pattern:

* keep the notebook as narrative + orchestration
* move reusable logic into a package/module
* the notebook remembers *how to use it*, not *all of it*

---

## How this influences the YODA Framework

YODA is not “a notebook platform”, but it benefits from notebook/literate programming concepts in two high-leverage ways:

1. **Literate artifacts for agents:**
   YODA’s Issues and Specs should read like “explain-first documents” with embedded, testable snippets (CLI commands, expected outputs, invariants). This mirrors LP’s “code embedded in narrative.” ([Wikipedia][1])

2. **Weave/tangle pattern for automation:**
   YODA scripts can behave like a literate toolchain:

   * **Weave:** render or compile human-friendly docs (e.g., templates → filled docs, indexes, digests)
   * **Tangle:** extract structured metadata and executable intents (TODO items, CLI contracts, validations) from docs

3. **Reproducibility discipline as a first-class rule:**
   “Restart and run all” translates to: “validate from a clean state”:

   * when a YODA document contains executable examples, a validator should simulate “clean environment” execution (as far as feasible) and ensure examples are consistent. ([Carpenter-Singh Lab][7])

---

## Spec implications for YODA (normative hints)

These are guidance-level norms to shape YODA specs and agent behavior.

### MUST

* **MUST** keep YODA’s primary artifacts (specs/issues/logs) **human-first**: narrative explanations with embedded structured elements, instead of “raw code dumps.” ([Wikipedia][1])
* **MUST** provide a “weave/tangle” equivalent in the workflow: (a) generate/read human docs and (b) derive machine-usable structure from them (schemas, indexes, CLI outputs). ([Wikipedia][1])
* **MUST** treat any executable example in docs (commands, expected outputs) as part of the contract: if it’s present, it must remain true or be updated.

### SHOULD

* **SHOULD** include a “reproducibility check” discipline similar to notebooks: validation should assume a clean state and detect order-dependent/hard-coded assumptions. ([Carpenter-Singh Lab][7])
* **SHOULD** support parameterized, repeatable execution patterns (notebook-inspired), where the same “documented flow” can run with different inputs (similar to notebook parameterization). ([papermill.readthedocs.io][8])
* **SHOULD** separate “exploration” from “stable logic”: exploratory notes can exist, but must be distilled into stable specs/contracts before implementation is considered complete.

### MAY

* **MAY** adopt publishing tooling patterns (Quarto/Jupyter Book style) for generating richer rendered documentation (sites/books) from YODA’s Markdown/YAML sources. ([Quarto][5])
* **MAY** support notebook artifacts as *temporary research inputs* (Study phase) as long as outcomes are captured into stable YODA docs (Document phase). ([jarrodmillman.com][3])

---

## References

* Knuth / Literate Programming: concept + weave/tangle model + WEB/CWEB ([literateprogramming.com][11])
* Project Jupyter: what notebooks are; `.ipynb` concept ([docs.jupyter.org][2])
* Millman & Pérez (2014): literate computing and reproducibility framing ([jarrodmillman.com][3])
* “Restart + run all” reproducibility discipline (practical best practice) ([Carpenter-Singh Lab][7])
* Papermill: parameterization and execution of notebooks ([papermill.readthedocs.io][8])
* Jupyter Book and Quarto: executable publishing systems ([jupyterbook.org][4])

[1]: https://en.wikipedia.org/wiki/Literate_programming?utm_source=chatgpt.com "Literate programming"
[2]: https://docs.jupyter.org/en/latest/what_is_jupyter.html?utm_source=chatgpt.com "What is Jupyter?"
[3]: https://jarrodmillman.com/publications/millman2014developing.pdf?utm_source=chatgpt.com "Developing open source scientific practice"
[4]: https://jupyterbook.org/v1/intro.html?utm_source=chatgpt.com "Built with Jupyter Book"
[5]: https://quarto.org/?utm_source=chatgpt.com "Quarto"
[6]: https://nbformat.readthedocs.io/?utm_source=chatgpt.com "The Jupyter Notebook Format — nbformat 5.10 documentation"
[7]: https://carpenter-singh-lab.broadinstitute.org/blog/best-practices-jupyter-notebook?utm_source=chatgpt.com "Best Practices for Jupyter Notebook | Carpenter-Singh Lab"
[8]: https://papermill.readthedocs.io/en/latest/usage-parameterize.html?utm_source=chatgpt.com "Parameterize - papermill 2.6.0 documentation"
[9]: https://arxiv.org/pdf/1810.08055?utm_source=chatgpt.com "Ten Simple Rules for Reproducible Research in Jupyter ..."
[10]: https://jupyterbook.org/?utm_source=chatgpt.com "Jupyter Book - Jupyter Book"
[11]: https://www.literateprogramming.com/knuthweb.pdf?utm_source=chatgpt.com "Literate Programming"
