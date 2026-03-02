---
description: Spec-centric architecture places a structured specification at the center of the engineering process — the spec drives implementation, checklists, and task breakdowns, making it the most reliable pattern for agents building systems because it replaces improvisation with a defined endpoint.
topics: ["[[agent-registry]]", "[[requirements-phase]]", "[[development-phase]]", "[[design-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: closed
---

# spec-centric architecture is the most reliable pattern for agents building systems

Spec-centric architecture places a structured specification at the center of the engineering process. Rather than having an agent improvise toward a loosely stated goal, the agent works from — and toward — a defined endpoint: the spec. The spec drives implementation tasks, acceptance checklists, and subtask breakdowns. Every downstream agent in the pipeline receives the same ground truth, not an interpreted version of what a previous agent understood the goal to be.

This is why spec-centric architecture outperforms prompt-and-generate approaches for agentic systems. When agents operate without a shared spec, each handoff introduces interpretive drift. The requirements agent summarizes intent in one form, the code generation agent infers implementation from that summary, the test generation agent infers expected behavior from the generated code, and the code review agent evaluates the result against unstated criteria. Each step amplifies the ambiguity introduced by the last. A structured spec breaks this chain by giving every agent the same authoritative reference.

GitHub's open-source Spec Kit (2025) operationalizes this pattern. The spec is not a prose description — it is a structured artifact that defines requirements, acceptance criteria, and implementation checklists in a machine-readable format. Agents can reference specific sections, mark checklist items as complete, and verify their output against explicit criteria. The spec becomes the shared memory of the engineering process, readable by both agents and humans. Whether Spec Kit can be adopted as the canonical format for this vault is answered in [[can GitHub Spec Kit format be adopted as the canonical spec artifact format for this vault]].

The implication for this vault is non-negotiable: the Requirements Analyst Agent must produce a structured spec artifact as its primary output, not notes or prose summaries. If the requirements agent produces unstructured output, every downstream agent loses the alignment benefit that makes spec-centric architecture reliable. The spec format must be agreed upon before building any downstream agents, because the format determines what downstream agents can consume.

This also clarifies the architectural role of the Requirements Analyst Agent within the minimal viable agent set from [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]]. It is not simply "the first agent" — it is the agent that creates the shared ground truth. Its output quality determines the ceiling for every agent that follows.

## Operational Mechanism: The Spec Travels with Every Handoff

Spec-centric architecture has a specific operational mechanism at runtime. The spec artifact (or its relevant sections) must travel with every task assignment at handoff boundaries. The orchestrator's context transfer protocol mandates this behavior.

The specific protocol: at each handoff, the orchestrator packages four components — the spec artifact, all upstream outputs produced so far, the specific task being delegated, and any iteration feedback from prior failed attempts. The spec is always the first component, because without it, downstream agents lose the authoritative ground truth and begin interpreting from prior outputs rather than from original intent.

This operationalizes spec-centric architecture at the handoff level: not just "maintain a spec" but "carry the spec forward at every pipeline transition." A spec that exists but is not transferred becomes reference material that agents cannot access at execution time — architecturally present but operationally absent. The orchestrator's responsibility is to ensure the spec is present in every specialist's context window, not merely stored somewhere retrievable.

The orchestrator's validation function at each handoff boundary is specifically validation against the spec — checking whether the specialist's output satisfies the handoff contract as defined by the spec's acceptance criteria. This is why [[the orchestrator agent's role is routing and validation not content generation]] is the architectural complement to spec-centric design: an orchestrator that also generates content cannot perform objective spec-based validation, because it would be evaluating outputs it partially produced. Strict role separation preserves the spec as the neutral reference.

The corollary: large specs create a context window tension (see [[lossless context transfer and context window limits are in direct tension for large spec artifacts]]). For manageable spec sizes, the full spec transfers at every handoff. For large specs, intelligent windowing sends the full spec on the first task and relevant sections on subsequent tasks. In both cases, the principle is unchanged: the spec components the specialist needs must be in their context window, not referenced externally.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (lines 37-41); enriched from [[orchestrator-agent]]

**Relevant Notes:**
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — the requirements agent in the minimal set must produce a structured spec for downstream agents to consume; spec-centric architecture defines the output contract for that agent
- [[requirements agents must produce a structured spec artifact not just prose notes]] — the operational consequence of this architectural principle applied to the Requirements Analyst Agent profile
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator coordinates against the spec as shared state; without a spec, the orchestrator has no consistent ground truth to route work from
- [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]] — the handoff protocol that carries the spec forward at every pipeline transition; lossless transfer operationalizes spec-centric architecture at the execution level
- [[lossless context transfer and context window limits are in direct tension for large spec artifacts]] — the constraint that emerges when spec size grows; the spec-centric principle creates the artifact that creates the context window tension
- [[the orchestrator agent's role is routing and validation not content generation]] — the orchestrator's validation function at every handoff is spec-based validation; routing-not-generating preserves the spec as the neutral reference that neither the orchestrator nor any specialist can contaminate by generating against their own judgment
- [[token cost of lossless context transfer is justified by the failure cost of context stripping]] — the spec artifact is the largest component of the context package at each handoff; this note provides the economic argument that the token cost of carrying the spec forward is rational, making spec-centric architecture economically defensible
- [[sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops]] — the sequential pipeline is the primary architectural instantiation of spec-centric flow; each phase produces output that the next phase validates against the same spec, and backward iteration loops are the mechanism for converging on spec compliance within each phase
- [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] — the spec defines the acceptance criteria that determine when agent authority ends and human judgment begins; ambiguity in the spec that agents cannot resolve autonomously is the primary trigger for escalation, making spec quality the upstream determinant of supervision frequency

**Topics:**
- [[agent-registry]]
- [[requirements-phase]]
- [[development-phase]]
- [[design-phase]]
