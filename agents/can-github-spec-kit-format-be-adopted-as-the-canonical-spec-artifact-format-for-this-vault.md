---
description: GitHub Spec Kit format can be adopted as the canonical spec artifact for this vault in its spirit but not verbatim — the vault's three-file structure (requirements.md, design.md, tasks.md) is a Spec Kit-compatible derivative that extends the format with machine-parseable EARS syntax and explicit interface contracts, and adopting Spec Kit's section taxonomy directly into requirements.md produces a compatible, interoperable spec without abandoning the extensions that make the artifact consumable by downstream code generation and test agents.
topics: ["[[agent-registry]]", "[[requirements-phase]]", "[[design-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: open
---

# can GitHub Spec Kit format be adopted as the canonical spec artifact format for this vault

The answer is: yes, with a specific adaptation. GitHub Spec Kit's `spec.md` section taxonomy can be adopted directly into the vault's `requirements.md` artifact, making the vault's three-file structure a Spec Kit-compatible derivative rather than a competing format. This preserves interoperability with the broader Spec Kit ecosystem while retaining the vault-specific extensions that make the spec machine-consumable by downstream agents.

## What GitHub Spec Kit Actually Specifies

GitHub Spec Kit (released September 2025, MIT-licensed, ~50k GitHub stars by late 2025) is a toolkit for spec-driven development organized around a `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement` pipeline. The core artifact chain is:

- **spec.md** — functional specification (the "what" and "why")
- **plan.md** — technical architecture and implementation approach (the "how")
- **tasks.md** — discrete, checkboxed implementation work units derived from the plan

The `spec.md` template enforces seven mandatory sections:

1. **Overview** — high-level feature description and goals
2. **User Stories** — structured as "As a [role], I want [capability] so that [benefit]"
3. **Functional Requirements** — specific, testable requirements organized by category
4. **Non-Functional Requirements** — performance, security, scalability constraints
5. **Acceptance Criteria** — measurable validation conditions
6. **Out of Scope** — explicit exclusions to prevent scope creep
7. **Review & Acceptance Checklist** — quality validation gates

The `[NEEDS CLARIFICATION]` marker system allows underspecified areas to be flagged for structured refinement via `/speckit.clarify` before technical planning begins.

## The Vault's Current Spec Structure

The [[requirements-analyst-agent]] already produces a three-file structure that is structurally homologous with Spec Kit's artifact chain:

| GitHub Spec Kit | This Vault |
|-----------------|------------|
| spec.md | requirements.md |
| plan.md | design.md |
| tasks.md | tasks.md |

The `requirements.md` sections already mirror Spec Kit's spec.md taxonomy (Overview, User Stories, Functional Requirements, Non-Functional Requirements, Acceptance Criteria, Out of Scope). This convergence is not accidental — both patterns independently arrived at the same functional decomposition because it is load-bearing for agent consumption.

The vault's structure makes three extensions beyond Spec Kit's spec.md:

1. **EARS syntax for requirements** — requirements are formatted as `WHEN [trigger] THE SYSTEM SHALL [behavior]` rather than natural-language prose, making them machine-parseable and unambiguous
2. **Explicit interface contracts in design.md** — API endpoints, event schemas, and function signatures that a code generation agent needs to begin implementation without asking clarifying questions; Spec Kit's plan.md is less prescriptive about this
3. **Mandatory three-file single-pass delivery** — the vault enforces that all three files must be produced together before `SPEC COMPLETE` is emitted; Spec Kit treats the phases as sequentially distinct commands

## Can the Spec Kit Format Be Adopted Verbatim?

Not without trade-offs. The specific incompatibilities:

**EARS vs. prose requirements.** Spec Kit's Functional Requirements section uses natural-language prose organized by category. The vault's use of EARS syntax (a formal requirements notation) is machine-parseable in ways that prose is not — downstream code generation agents can extract individual requirements as discrete units rather than parsing narrative text. Adopting Spec Kit verbatim would mean dropping EARS, which degrades machine-consumability.

**Spec.md has no interface contracts.** Spec Kit intentionally keeps spec.md free of implementation specifics ("no tech stack, APIs, or code structure" — written for business stakeholders). The vault's design.md fills this gap with an architecture-level layer (component breakdown, data models, interface contracts). A code generation agent that only has Spec Kit's spec.md would be missing the structural information it needs; it would need to derive architecture from functional requirements, which introduces interpretive variance.

**Spec Kit's experimental status.** As of early 2026, Spec Kit is at v0.1.4 and explicitly experimental. Practitioners have noted a 10x speed disadvantage compared to iterative prompting, 2,000+ lines of markdown per feature, and implementation bugs despite detailed specs. The template structure is sound; the full toolkit overhead may not be appropriate for the vault's agent-catalog use case.

**Section names differ.** Spec Kit uses "Review & Acceptance Checklist" as the validation gate section; the vault's structure does not have an equivalent formal checklist section. This is a minor incompatibility — additive rather than conflicting.

## The Correct Adoption Decision

**Adopt Spec Kit's section taxonomy into requirements.md; treat design.md as a vault-specific extension of Spec Kit's plan.md.**

Specifically:
- `requirements.md` section headers match Spec Kit's spec.md headers exactly (Overview, User Stories, Functional Requirements, Non-Functional Requirements, Acceptance Criteria, Out of Scope) — making the artifact directly recognizable to any Spec Kit consumer
- Functional Requirements content uses EARS syntax within that section — a vault-internal convention that is additive, not conflicting
- `design.md` extends where Spec Kit's plan.md is intentionally underspecified for code generation agent consumption — adding Interface Contracts as a required section
- `tasks.md` is structurally identical to Spec Kit's tasks artifact

This makes the vault's spec format a **strict superset of Spec Kit's spec.md** — any tool that can consume Spec Kit output can consume the vault's requirements.md (because the section taxonomy matches), and the vault's additional content provides more machine-consumable precision than Spec Kit's baseline.

The `[NEEDS CLARIFICATION]` marker system from Spec Kit should be adopted directly. It maps cleanly to the vault's escalation design: a requirements agent that encounters an input it cannot resolve without guessing inserts `[NEEDS CLARIFICATION: X]` and emits the partial spec for human review, rather than silently assuming. This is operationally equivalent to the escalation trigger defined in [[agent profiles must include escalation conditions as a required design field]].

## What This Resolves

This question was raised because [[requirements agents must produce a structured spec artifact not just prose notes]] established that the spec format must be agreed upon before downstream agents are designed, but did not specify whether to adopt Spec Kit verbatim, derive a custom format, or adapt. The answer removes that ambiguity:

**Use Spec Kit's section taxonomy as the canonical section structure for requirements.md.** Downstream agents — code generation, test generation, code review — can be designed against a well-defined requirements.md format that is also interoperable with the broader Spec Kit ecosystem. The format decision is now made; downstream agent design can proceed.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (line 96)

**Relevant Notes:**
- [[requirements agents must produce a structured spec artifact not just prose notes]] — this note resolves the open question that note left open: the spec format is Spec Kit-compatible requirements.md with EARS syntax and vault-specific extensions
- [[requirements-analyst-agent]] — the agent profile that implements this decision; its output format (three-file artifact) is now confirmed as canonical and Spec Kit-compatible
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — the architectural claim this note operationalizes: Spec Kit IS the industry-validated spec-centric pattern, and the vault's adoption decision connects the abstract principle to a specific format
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — the four-agent set whose input/output contracts depend on the spec format being agreed upon; this note closes the prerequisite
- [[crewai-agent-to-agent-handoff-and-interaction-api]] — the spec artifact (as TaskOutput with Pydantic schema) is the data structure that passes between agents at the requirements → code generation handoff

**Topics:**
- [[agent-registry]]
- [[requirements-phase]]
- [[design-phase]]
