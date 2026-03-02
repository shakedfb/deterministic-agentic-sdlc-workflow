---
description: The agent profile schema's `framework` field should record both the orchestration framework (e.g., CrewAI, LangGraph) and the target base model (e.g., GPT-4o, Claude Opus) as co-equal design parameters, because model selection is as consequential as framework selection and omitting it leaves a critical implementation decision undocumented.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: closed
---

# agent profile framework field should capture both orchestration framework and base model

The `framework` field in the current agent profile schema captures one dimension of a two-dimensional design decision. It records which orchestration framework routes the agent's tasks — CrewAI, LangGraph, or Google ADK — but says nothing about the base model that actually generates the agent's outputs. This is an incomplete specification.

The omission matters because model selection and framework selection are not equivalent in consequence. Framework choice determines how tasks are routed, how agents coordinate, and how state is managed across phases. These are structural concerns. Model choice determines whether the agent can actually perform the reasoning its role requires — whether it can maintain context across a multi-step requirements analysis, decompose complex tasks into executable subtasks, or produce reliable code review judgments. An agent's ceiling is set by the model; the framework determines how close you get to that ceiling. Specifying one without the other is like specifying a team's org chart without specifying whether the team has senior or junior staff.

This creates a concrete gap in the catalog's utility. An agent profile that specifies CrewAI but leaves the base model unspecified is not implementable without additional information. A future session reading that profile cannot know whether the agent was designed for Claude Opus's reasoning tier or a faster, less capable model. The design decision has been made but not recorded, which defeats the catalog's purpose as a blueprint.

The fix is a schema amendment: the `framework` field should be treated as a compound field capturing both dimensions. For example, `framework: "CrewAI / Claude Opus 4.6"` or structured as separate sub-fields `orchestration_framework` and `base_model`. Either approach ensures that the two co-equal design decisions are explicitly documented together. The specific format matters less than the principle: both parameters belong in the profile, and neither is optional.

This amendment also has an ordering implication for the design process. When drafting a new agent profile, base model selection should be considered alongside framework selection — not deferred as an implementation detail. The catalog is the blueprint; model selection is a blueprint-level decision.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (lines 74-76)

**Relevant Notes:**
- [[base model quality matters more than framework choice for agent capability]] — the foundational claim that motivates this schema change: model selection is the higher-priority design decision, so the schema must capture it
- [[CrewAI aligns best with catalog-driven SDLC agent architectures]] — framework selection is still a meaningful decision documented here; the schema amendment ensures both framework and model are co-documented
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator carries the highest reasoning load and has the most consequential base model requirement; this schema amendment ensures that requirement is explicitly captured in its profile
- [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — when the framework choice is LangGraph rather than CrewAI for a specific agent, the compound `framework` field must capture that distinction; the schema amendment applies to both framework options

**Topics:**
- [[agent-registry]]
- [[design-phase]]
