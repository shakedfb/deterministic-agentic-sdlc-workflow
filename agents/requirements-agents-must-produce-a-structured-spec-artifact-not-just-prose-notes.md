---
description: Requirements agents must produce a structured spec artifact — not unstructured prose notes — because a spec is the shared contract that downstream agents (code generation, test generation, review) depend on; without a defined output format agreed upon before any downstream agent is built, the entire spec-centric pipeline is structurally undefined.
topics: ["[[agent-registry]]", "[[requirements-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: closed
---

# requirements agents must produce a structured spec artifact not just prose notes

A requirements agent that produces prose notes has not completed its job. Prose captures intent but does not define a contract. Downstream agents — code generation, test generation, code review — cannot reliably consume unstructured notes as their input. They need a spec: a document with a defined format, defined sections, and a defined level of specificity that makes implementation deterministic rather than interpretive.

The distinction matters because of how errors propagate. If a requirements agent emits ambiguous notes, every downstream agent must make interpretive decisions to resolve the ambiguity. Those decisions will not be coordinated. The code generation agent and the test generation agent will resolve the same ambiguity differently, producing code that does not match its tests. The code review agent will have no authoritative reference against which to evaluate the implementation. The result is coordinated failure traced back to the output format of the first agent in the pipeline.

A structured spec artifact solves this by establishing a shared contract at the start of the pipeline. The spec is the source of truth: implementation flows from it, tests validate against it, and review checks the implementation against it. When downstream agents operate from the same artifact, their outputs are coherently related even without direct coordination between those agents.

The GitHub Spec Kit pattern (2025) operationalizes this approach. It places a specification at the center of the engineering process, with the spec driving implementation checklists, task breakdowns, and acceptance criteria. The agent works toward a defined endpoint rather than improvising from vague guidance. This is the most reliable pattern currently in production for agents building software.

The sequencing implication is strict: **the spec format must be agreed upon before any downstream agent is designed.** Designing a code generation agent before the spec format is defined means designing an agent whose input format is unknown. That agent will need to be redesigned once the spec format is settled. The spec format is therefore a prerequisite for the entire downstream agent catalog, not a detail to be refined after agents are built.

For this vault, this means the Requirements Analyst Agent profile must specify both the output format (what sections, what fields, what level of detail) and the validation criteria for a well-formed spec. The `outputs` field in the agent profile is not satisfied by "a specification document" — it must describe the spec format precisely enough that a downstream agent designer can read it and know exactly what input their agent will receive.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (lines 39-41)

**Relevant Notes:**
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — the architectural claim that this note operationalizes at the requirements phase: the spec is not just good practice, it is the structural anchor for spec-centric pipelines
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — the 4-agent set that depends on requirements output being a structured artifact; code generation, test generation, and review are all downstream consumers of the spec
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator-first principle parallels the spec-format-first principle: both are prerequisite infrastructure that must exist before downstream components can be validly designed
- [[agent profiles must include escalation conditions as a required design field]] — a parallel completeness argument for agent schema: just as escalation conditions are a required undocumented field, the spec output format is a required undocumented design decision in the requirements agent profile
- [[can GitHub Spec Kit format be adopted as the canonical spec artifact format for this vault]] — resolves the open question of what format the structured spec takes: Spec Kit's section taxonomy for requirements.md with EARS syntax and interface contracts as extensions; the spec format question raised here is now answered

**Topics:**
- [[agent-registry]]
- [[requirements-phase]]
