---
description: Combining a sequential pipeline structure for predictable phase ordering with hierarchical override authority in the orchestrator for runtime routing decisions delivers both deterministic happy-path flow and dynamic exception handling — the two properties that SDLC pipelines require but that neither pure architecture provides alone.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[orchestrator-agent]]"
classification: closed
---

# hybrid sequential-hierarchical orchestration gives predictable flow with dynamic error handling

Pure sequential and pure hierarchical orchestration each solve half the problem for SDLC pipelines. Sequential processing gives deterministic phase ordering — requirements before code generation, code before tests, tests before review — which makes the happy path predictable and debuggable. But sequential processing cannot handle runtime exceptions elegantly: a failed task blocks the pipeline, and the sequential structure has no mechanism for the orchestrator to reroute, reframe, or escalate dynamically.

Hierarchical processing gives the orchestrator authority to assign and reassign tasks at runtime based on agent capability, current load, or escalation state. But pure hierarchical mode makes the execution path opaque — when the manager agent decides dynamically which specialist gets which task, the phase order becomes runtime-variable, which complicates debugging and makes the happy-path sequence harder to validate.

The hybrid pattern resolves this by assigning sequential structure to the pipeline level and hierarchical authority to the exception path. In CrewAI terms, this is `Process.sequential` for the crew combined with `allow_delegation=True` on the manager agent. The sequential process ensures that phases execute in the designed order under normal conditions. The hierarchical authority activates when exceptions occur: the orchestrator can override the sequential flow to re-delegate a task to a different specialist, initiate a retry loop, or escalate to human review, without disrupting the overall pipeline structure.

This architecture pattern is an explicit design choice, not a default. It requires the orchestrator to be configured as both a pipeline sequencer and a runtime authority — two responsibilities that must be reflected in its system prompt and escalation conditions. The sequential structure handles predictability; the hierarchical authority handles adaptation.

The pattern also clarifies the relationship between [[sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops]] and hierarchical delegation. The sequential pipeline is not incompatible with the orchestrator having override authority — the sequential structure defines the default execution path, and the hierarchical authority defines the exception handling overlay. V1 exercises the sequential path; adding hierarchical override capability is the v1.5 enhancement before parallel execution is introduced in v2.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[how does CrewAI handle agent-to-agent handoff and what does its interaction API look like]] — `Process.sequential` + `allow_delegation=True` is the CrewAI configuration that implements this hybrid pattern; the note documents the specific API primitives
- [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — when the exception handling paths become complex enough to require conditional edges at the graph level, LangGraph may replace the hierarchical override layer; the hybrid pattern is the CrewAI ceiling before LangGraph becomes necessary
- [[workflows are preferable to agents for deterministic SDLC phases]] — the sequential layer of the hybrid maps to workflow-style determinism; the hierarchical layer covers the judgment-intensive exception cases that require agent reasoning
- [[the orchestrator agents role is routing and validation not content generation]] — the orchestrator's hierarchical authority is exercised strictly for routing decisions (which specialist, retry, escalate) — never for generating content directly

**Topics:**
- [[agent-registry]]
- [[design-phase]]
