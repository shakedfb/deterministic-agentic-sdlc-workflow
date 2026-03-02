---
description: A reliable, high-capability foundation model (GPT-4o, Claude Opus, or equivalent reasoning model) is the primary determinant of agent capability — agents built on weak base models fail at planning and context retention regardless of the orchestration framework's sophistication, making model selection a higher-priority decision than framework selection when designing multi-agent SDLC systems.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: closed
---

# base model quality matters more than framework choice for agent capability

Framework choice dominates the conversation about multi-agent architecture — CrewAI vs. LangGraph vs. ADK is a well-debated decision with clear tradeoffs. But this framing inverts the priority order. The variable with the greatest impact on whether an agent actually works is not which orchestration framework routes its tasks; it is the quality of the foundation model generating its outputs.

The failure mode is specific and observable. Agents built on weak base models fail at planning and context retention. They produce plausible-sounding but incorrect outputs, lose thread across multi-step reasoning chains, and cannot reliably decompose complex tasks into executable subtasks. These failures occur regardless of framework sophistication. CrewAI's role-based delegation structure cannot compensate for a model that cannot maintain coherent intent across a 10-step requirements analysis. LangGraph's precise state machine cannot recover the reasoning that the base model failed to produce in the first place. The framework is scaffolding; the model is the load-bearing element.

This creates an asymmetry in the design decision space. A capable foundation model (GPT-4o, Claude Opus, or a capable reasoning model in the same tier) can produce useful outputs even with a minimal orchestration setup — a basic prompt chain or a simple CrewAI crew. A weak base model will underperform even with sophisticated orchestration. The ceiling is set by the model; the framework determines how close you get to that ceiling.

The practical implication is sequencing: when evaluating agents in this vault, model selection should be a first-order consideration, not a footnote. If an agent's prototype is failing, the first diagnostic question is whether the base model is capable of the task at all — not whether the framework configuration is optimal. Framework tuning is premature optimization if the model cannot handle the underlying task.

This also has a concrete consequence for the agent profile schema. The `framework` field as currently defined captures the orchestration framework. But model selection is an equally important design decision — one that should be captured explicitly, not assumed. An agent profile that specifies CrewAI but leaves the base model unspecified is missing a critical implementation parameter. The `framework` field should capture both the orchestration framework and the target base model as co-equal specifications.

This aligns with the insight from [[agent profile framework field should capture both orchestration framework and base model]]: the schema implication of this claim is not just organizational neatness — it reflects the fact that model choice is a design decision of equivalent weight to framework choice, and both must be tracked to evaluate whether an agent's design is implementable.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (lines 72-76)

**Relevant Notes:**
- [[agent profile framework field should capture both orchestration framework and base model]] — the direct schema consequence of this claim: the `framework` field must capture both orchestration layer and base model as co-equal design decisions
- [[CrewAI aligns best with catalog-driven SDLC agent architectures]] — framework selection is still a meaningful decision, but it is downstream of model selection; CrewAI's fit for catalog-driven architecture is evaluated assuming a capable base model is in place
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator carries the highest reasoning load in a multi-agent system (context tracking, task routing, escalation judgment); its base model selection is the most consequential single model decision in the catalog
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — each agent in the minimal set has different capability requirements; requirements analysis and code review are most demanding for base model reasoning, which should inform model tier selection per agent

**Topics:**
- [[agent-registry]]
- [[design-phase]]
