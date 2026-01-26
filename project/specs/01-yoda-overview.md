# YODA Framework Overview

## Definition

 The YODA Framework is a document-first approach to AI-assisted development. It organizes collaboration between humans and agents using structured documentation and automation, focused on consistency, repeatability, and traceability.

## Acronym

YODA = YAML-Oriented Documentation & Agents

## Core principles

- Documentation as source of truth: the project is described before implementation.
- YAML as the gravity center: metadata and structure live in YAML.
- Markdown as the narrative layer: context, criteria, and details live in free text.
- Agents and scripts execute what is documented.
- Agents can start with zero context by reading the right files.
- Human entrypoint: repo `README.md`. Agent entrypoint: [`yoda/yoda.md`](/yoda/yoda.md).

## Goal

Create an environment where humans and AI follow a shared flow, with clear patterns for artifacts, scripts, and process.

## Stack profiles

YODA v1 is stack-agnostic. Stack profiles are not part of the core and are deferred as optional extensions for future versions.

## Tooling policy

Tooling is mandatory when scripts are available. During bootstrap, tooling is optional.

## Audience and positioning

Primary audience: solo developers using one human + one agent with YODA Flow.

Positioning: a framework to support AI-assisted development, grounded in issue documentation versioned with the project source.

Scope: a general-purpose process framework for developers who want tighter control over agent-assisted development.
