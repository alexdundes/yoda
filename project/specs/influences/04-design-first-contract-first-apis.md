# Design-First / Contract-First APIs

## What it is

**Design-first** (also called **contract-first** or **schema-first**) is an API development approach where the team **defines the API contract before writing implementation code**. The “contract” is typically a machine-readable specification (most commonly **OpenAPI**) that describes endpoints, request/response shapes, status codes, and constraints. ([APIs You Won't Hate][1])

In design-first, the contract becomes the shared source of truth that enables:

* early feedback on interface design,
* parallel work (clients, mocks, server stubs),
* automation (code generation, tests, docs, linting). ([Swagger][2])

---

## Why “contract-first” matters

### 1) It forces an outside-in interface design

Design-first makes you decide **what the API looks like to consumers** (names, shapes, errors) before implementation details bias the interface.

A key motivation is reducing “implementation-driven APIs” that leak internal data models or accidental complexity.

### 2) Fast feedback, cheap iteration

Changing a contract document is usually cheaper than refactoring code. Teams can review and iterate the API shape quickly before committing to implementation. ([VMware Blogs][3])

### 3) The contract becomes tooling leverage

When the contract is machine-readable, you can generate:

* server stubs,
* SDKs,
* documentation,
* test scaffolding,
* mock servers,
* conformance checks. ([OpenAPI Initiative][4])

---

## What qualifies as a “contract”

A good contract is **precise enough that humans and tools can rely on it**.

### Common contract artifacts

* **OpenAPI Specification (OAS)** for HTTP APIs (endpoints, parameters, request/response bodies, auth, errors). OAS is defined as a language-agnostic interface description for HTTP APIs that both humans and computers can understand. ([Swagger][5])
* **JSON Schema** for payload validation (often embedded in OpenAPI 3.1, or used alongside it). (OpenAPI 3.1 aligns closely with JSON Schema concepts; treat schema rigor as a key goal.) ([Swagger][5])
* **Contract tests** (see CDC below): executable expectations that verify provider behavior against consumer expectations. ([Pactflow Contract Testing Platform][6])

---

## Design-first vs code-first

### Code-first (implementation-first)

* Implement endpoints in code,
* Generate spec/docs afterward (if at all),
* Often leads to API shape reflecting internal structure.

### Design-first (contract-first)

* Define the API spec/contract first,
* Review and iterate contract,
* Implement to satisfy the contract.

Swagger’s design-first framing highlights defining an API specification (like OpenAPI) before coding to improve consistency and enable generation workflows. ([Swagger][7])
Azure’s API design guidance also explicitly notes OpenAPI promoting a contract-first approach (design contract first, then implement). ([Microsoft Learn][8])

---

## Typical workflow (thin slice)

A practical contract-first cycle for a feature slice:

1. **Draft contract**

   * resource names, endpoints, request/response schemas
   * auth, pagination, filtering conventions
   * error model (status codes + error payload schema)

2. **Review contract**

   * consumer review (frontend, integrators, other services)
   * naming/consistency review (lint rules, guidelines)

3. **Mock / stub**

   * mock server from OpenAPI (or stub implementation)
   * client development can proceed in parallel

4. **Implement provider**

   * implement endpoints to match contract
   * request/response validation against schema

5. **Conformance + regression**

   * contract conformance checks
   * automated tests (including CDC where applicable)

6. **Publish + version**

   * contract/spec published and versioned with release

This “contract as first deliverable” concept is central to API-first design thinking. ([Swagger][2])

---

## Consumer-Driven Contracts (CDC) and Pact

A common complement to design-first is **consumer-driven contract testing (CDC)**:

* Consumers define expectations for interactions (requests/responses),
* Providers verify they satisfy those expectations.

**Pact** is a widely used tool in this space; its docs describe it as a consumer-driven contract testing tool where contracts are produced from consumer tests, focusing verification on what consumers actually use. ([Pact Docs][9])

**Why CDC matters:** it reduces reliance on brittle end-to-end tests and helps detect breaking changes early, especially in microservices and integration-heavy environments. ([Pactflow Contract Testing Platform][6])

---

## Backward compatibility and versioning as part of the contract

A “contract-first” mindset usually forces explicit decisions about compatibility and change management.

### Example: Stripe’s approach to versioning and backward compatibility

Stripe documents a system where accounts/requests are tied to API versions and distinguishes between backward-compatible changes and major releases that can include breaking changes. ([Documentação Stripe][10])

**The key lesson:** versioning and compatibility rules should be part of the contract discipline, not an afterthought.

---

## Common pitfalls (and mitigations)

### Pitfall: “The contract becomes aspirational instead of enforced”

If the team writes a spec but doesn’t validate it, it becomes decorative.

**Mitigation:**

* schema validation at runtime or tests,
* CI conformance checks,
* breaking-change detection in reviews.

### Pitfall: “Over-specifying too early”

Trying to design the entire API up front can drift into waterfall.

**Mitigation:** design in **thin slices** (only what you will ship next), iterate contract frequently. ([VMware Blogs][3])

### Pitfall: “Contract ignores consumer reality”

A spec created without consumer input can be technically clean but impractical.

**Mitigation:** require consumer review, and/or adopt CDC to keep provider aligned with real usage. ([Pactflow Contract Testing Platform][6])

---

## How it inspires YODA Framework

YODA is not “an HTTP API framework”, but it *does* define **interfaces** that behave like APIs:

* CLI commands are an API (inputs, outputs, exit codes).
* YAML schemas are contracts (TODO schema, Issue metadata schema, logs schema).
* Agent entrypoints and file structures are “interfaces” that tools rely on.

So Design-first / Contract-first thinking suggests:

* Define the **machine-readable contract** for YODA artifacts first (schemas).
* Define the **CLI contract** first (flags, output formats, exit codes).
* Enforce contracts via automated validation in CI.
* Treat “agents” as consumers: contracts reduce hallucination and drift.

This mirrors the broader API-first idea: use an API description language to establish a contract for expected behavior. ([Swagger][2])

---

## Spec implications for YODA (normative hints)

These are guidance-level norms to shape YODA’s design and agent behavior.

### MUST

* **MUST** define machine-readable contracts for core artifacts (e.g., `TODO.<dev>.yaml`, Issue front matter, log schema) and treat them as the source of truth.
* **MUST** define the CLI as a contract: stable flags, exit codes, and machine-readable output formats (e.g., JSON), so tools/agents can rely on it.
* **MUST** validate artifacts against schemas in CI (schema validation + reference integrity), so “spec drift” becomes a failing build, not a surprise, **v2+ / when CI exists**.
* **MUST** treat “contract changes” (schemas/CLI outputs) as high-impact and require explicit review (breaking changes policy).

### SHOULD

* **SHOULD** adopt a design-first workflow for scripts: write the CLI contract/spec and JSON outputs first, then implement.
* **SHOULD** provide “mockable” behavior for agent/tooling development (e.g., `--dry-run`, predictable JSON outputs), similar to how API mocks enable parallel work. ([Swagger][7])
* **SHOULD** design contracts in thin slices (only what v1 needs), then iterate. ([APIs You Won't Hate][1])
* **SHOULD** encode backward-compatibility rules for contracts (what changes are allowed without bumping `schema_version`). (Stripe’s compatibility framing is a good model conceptually.) ([Documentação Stripe][11])

### MAY

* **MAY** generate code from contracts (e.g., validators, CLI help, docs sections) as long as human-readable docs remain clear and editable. ([Swagger][7])
* **MAY** add consumer-driven contract testing concepts for internal interfaces (e.g., “agent expectations” as tests) when YODA grows in complexity, inspired by CDC/Pact. ([Pactflow Contract Testing Platform][6])

---

## References

* Swagger — API-first approach and “contract as specification” framing. ([Swagger][2])
* OpenAPI Specification — standard interface description for HTTP APIs. ([Swagger][5])
* Swagger — design-first vs code-first discussion. ([Swagger][7])
* Azure Architecture Center — OpenAPI promotes contract-first design. ([Microsoft Learn][8])
* Pact documentation + PactFlow — consumer-driven contract testing overview. ([Pact Docs][9])
* Stripe docs/blog — versioning and backward-compatibility approach examples. ([Documentação Stripe][10])

---

[1]: https://apisyouwonthate.com/blog/a-developers-guide-to-api-design-first/?utm_source=chatgpt.com "A Developer's Guide to API Design-First"
[2]: https://swagger.io/resources/articles/adopting-an-api-first-approach/?utm_source=chatgpt.com "Understanding the API-First Approach to Building Products"
[3]: https://blogs.vmware.com/tanzu/understanding-api-first-development/?utm_source=chatgpt.com "Understanding API-First Development - Tanzu"
[4]: https://www.openapis.org/?utm_source=chatgpt.com "OpenAPI Initiative – The OpenAPI Initiative provides an open ..."
[5]: https://swagger.io/specification/?utm_source=chatgpt.com "OpenAPI Specification - Version 3.1.0"
[6]: https://pactflow.io/what-is-consumer-driven-contract-testing/?utm_source=chatgpt.com "What is Consumer-Driven Contract Testing (CDC)? - PactFlow"
[7]: https://swagger.io/blog/code-first-vs-design-first-api/?utm_source=chatgpt.com "Code-First vs. Design-First API Approaches"
[8]: https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design?utm_source=chatgpt.com "Web API Design Best Practices - Azure Architecture Center"
[9]: https://docs.pact.io/?utm_source=chatgpt.com "Pact Docs: Introduction"
[10]: https://docs.stripe.com/api/versioning?utm_source=chatgpt.com "Versioning | Stripe API Reference"
[11]: https://docs.stripe.com/upgrades?utm_source=chatgpt.com "API upgrades"
