---
description: CrewAI's role-based team structure maps naturally to agent profiles defined by responsibility, making it the best-fit orchestration framework for catalog-driven SDLC architectures where agents are designed by role first and implemented second.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: closed
---

# CrewAI aligns best with catalog-driven SDLC agent architectures

Among current production-ready multi-agent frameworks — CrewAI, LangGraph, and Google Agent Development Kit (ADK) — CrewAI is the strongest fit for a catalog-driven SDLC architecture. The reason is structural alignment: CrewAI's core primitive is the role-based team. Agents in CrewAI are defined by their role, goal, and backstory before any implementation detail is specified. This maps directly to the catalog-first design philosophy of this vault, where agent profiles document what an agent does and why it exists before implementation begins.

LangGraph's strength is graph-based state machines for complex conditional branching. It excels when the workflow itself is the hard problem — when execution paths depend on runtime conditions that must be modeled explicitly. For an SDLC team with clear phase boundaries and well-defined handoff contracts, this power is unnecessary overhead. LangGraph asks you to think in graphs; CrewAI asks you to think in roles. The SDLC model is a role model.

Google ADK is optimized for Google Cloud infrastructure. Its multi-agent patterns are well-documented and its tooling is mature, but the architectural decisions are coupled to the Google ecosystem. A framework-agnostic catalog does not benefit from that coupling.

The CrewAI alignment is not incidental. The vault's two-tier navigation (hub → phase MOCs → agents), the dense schema emphasizing role definition, and the explicit interaction mapping between agents all reflect the same mental model that CrewAI implements in code: agents as role-defined team members with defined inputs, outputs, and handoff relationships. When the catalog says `interactions: [[requirements-analyst-agent]], [[code-generator-agent]]`, that is the same dependency mapping that CrewAI encodes in its task delegation graph.

This framework choice has a downstream implication: agent profiles in this vault can double as CrewAI agent definitions. The `current_prompt` field maps to the agent's backstory and system instructions; `responsibilities` maps to the agent's goal; `interactions` maps to task dependencies. The catalog is not just documentation — it is a pre-implementation spec that CrewAI can directly instantiate. This aligns with [[phased rollout prevents coordination chaos when building multi-agent systems]]: each phase of the rollout introduces new CrewAI crew members into an already-operational orchestrator context rather than deploying a full crew simultaneously.

The comparison also clarifies when CrewAI is the wrong choice. If an SDLC workflow requires complex runtime branching — for example, a code review agent that must choose between three different remediation paths based on error classification — LangGraph's graph model is more appropriate for that subgraph. The recommendation is not that CrewAI handles everything; it is that CrewAI should be the team-level orchestration layer, with LangGraph reserved for agents whose internal workflow is fundamentally conditional.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (lines 43-50)

**Relevant Notes:**
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — CrewAI's crew and task delegation model requires an orchestrator-style coordinator; the framework choice reinforces the orchestrator-first bootstrapping sequence
- [[optimal multi-agent team size is 3 to 7 specialized agents]] — CrewAI's role-based team model operates most cleanly within the 3-7 agent range; beyond 7 agents, hierarchical crew structures must be introduced which changes the coordination model
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — the 4-agent specialist set maps directly to CrewAI crew members with defined roles, goals, and inter-agent task dependencies
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — in CrewAI, the structured spec artifact produced by the requirements agent becomes the shared context passed through task delegation to downstream agents
- [[crewai-agent-to-agent-handoff-and-interaction-api]] — the implementation mechanics of this recommendation: the context parameter, TaskOutput schema contracts, and Process modes translate the catalog's interaction links to running code
- [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — the complementary decision criterion; together the two notes form a complete framework selection tree: CrewAI as default, LangGraph for conditional/cyclic workflows
- [[base model quality matters more than framework choice for agent capability]] — the framework recommendation assumes a capable base model; CrewAI's role-based structure does not compensate for weak model quality

**Topics:**
- [[agent-registry]]
- [[design-phase]]
