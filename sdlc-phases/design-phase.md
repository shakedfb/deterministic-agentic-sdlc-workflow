---
description: Architecture and design phase -- agents that create system and component designs
type: moc
phase_purpose: "Transform requirements into architectural and detailed designs"
agents: []
---

# design phase

## Purpose

Agents in this phase translate requirements into architectural decisions, system designs, and component specifications.

## Agents in This Phase

Research claims that establish how agents in this vault should be designed:

- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator must be the first agent designed; all specialist profiles are downstream decisions
- [[optimal multi-agent team size is 3 to 7 specialized agents]] — the design constraint that scopes the catalog; team sizing is a prerequisite
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — the architectural pattern that the requirements phase must implement
- [[CrewAI aligns best with catalog-driven SDLC agent architectures]] — the framework selection recommendation for role-defined SDLC agents
- [[workflows are preferable to agents for deterministic SDLC phases]] — the design decision gate reserving agents for judgment tasks only
- [[phased rollout prevents coordination chaos when building multi-agent systems]] — the implementation sequence that prevents coordination failures
- [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] — the supervision constraint that shapes escalation design across all phases
- [[base model quality matters more than framework choice for agent capability]] — the priority ordering for model vs. framework selection
- [[agent profile framework field should capture both orchestration framework and base model]] — the schema amendment making model selection an explicit design decision
- [[agent profiles must include escalation conditions as a required design field]] — the schema completeness requirement ensuring authority boundaries are designed explicitly
- [[what are the specific escalation patterns used in production agentic SDLC systems]] — the escalation trigger taxonomy (confidence threshold, ambiguity detection, irreversibility gate, loop termination) and governance models (HITL/HOTL) that operationalize the `escalation_conditions` field in every agent profile
- [[how does CrewAI handle agent-to-agent handoff and what does its interaction API look like]] — the CrewAI interaction API documentation needed before designing handoff patterns
- [[can GitHub Spec Kit format be adopted as the canonical spec artifact format for this vault]] — the spec format decision resolving the prerequisite for downstream agent design
- [[what metrics distinguish a well-functioning orchestrator from a coordination bottleneck]] — the metric definitions needed for the Orchestrator Agent profile's `metrics` field
- [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — the framework decision criterion completing the CrewAI-vs-LangGraph selection tree

### Orchestrator Agent Design Claims (batch: orchestrator-agent)

The following claims define the Orchestrator Agent's architecture, responsibilities, and v1/v2 design boundaries:

- [[the orchestrator agent's role is routing and validation not content generation]] — the architectural definition of the coordination layer: role separation between orchestrator and specialists
- [[sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops]] — the risk-adjusted v1 architecture choice: sequential with bounded retries before parallel complexity
- [[lossless context transfer at handoff boundaries is the orchestrator's most critical responsibility]] — the critical operational constraint: complete context package at every handoff boundary
- [[hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines]] — the loop control design requirement: fixed maximum retries with mandatory escalation
- [[hybrid sequential-hierarchical orchestration gives predictable flow with dynamic error handling]] — the architectural pattern: sequential pipeline structure + hierarchical override authority for exceptions
- [[parallel task execution requires dependency graph analysis and is a v2 concern for SDLC pipelines]] — the v2 deferral: dependency graph analysis required before parallel execution is safe
- [[intelligent context windowing is needed when spec artifacts exceed the context window]] — the v2 hypothesis: structured windowing when full transfer is physically impossible
- [[token cost of lossless context transfer is justified by the failure cost of context stripping]] — the economic argument: retry costs from stripping exceed transfer overhead of completeness
- [[the four-phase build loop calibration hypothesis for iteration limits]] — the open hypothesis: baseline calibration numbers (3 code gen, 2 review cycles) requiring empirical validation
- [[observability layer with trace-level instrumentation is required before orchestrator metrics become measurable]] — the measurement prerequisite: trace-level instrumentation is required before metrics become operational
- [[specialist capability matching and load balancing is a v2 orchestrator routing enhancement]] — the v2 routing enhancement: capability matching and load balancing for multi-instance specialist teams
- [[lossless context transfer and context window limits are in direct tension for large spec artifacts]] — the unresolvable v1 tension: two correct principles conflict at scale, resolved only by v2 windowing
- [[sequential pipeline predictability and parallel execution efficiency are in direct tension for SDLC build loops]] — the deliberate v1 trade-off: sequentialism accepts higher wall-clock time for lower coordination risk

## Tensions

- [[CrewAI aligns best with catalog-driven SDLC agent architectures]] recommends CrewAI as default while [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] identifies scenarios where LangGraph is required — resolved via the hybrid architecture (CrewAI for role definitions, LangGraph for conditional routing)
- [[base model quality matters more than framework choice for agent capability]] inverts the typical framework-first design conversation — model selection is the higher-priority decision
- [[lossless context transfer at handoff boundaries is the orchestrator's most critical responsibility]] requires full context at every handoff while [[lossless context transfer and context window limits are in direct tension for large spec artifacts]] documents that this is physically impossible for large specs — the tension is deliberate and cannot be dissolved in v1; [[intelligent context windowing is needed when spec artifacts exceed the context window]] is the v2 resolution
- [[sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops]] favors predictability over efficiency while [[sequential pipeline predictability and parallel execution efficiency are in direct tension for SDLC build loops]] documents the wall-clock time cost of sequentialism — resolved deliberately in favor of v1 predictability
- [[hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines]] establishes the principle while [[the four-phase build loop calibration hypothesis for iteration limits]] documents that the specific numbers (3 code gen, 2 review cycles) are open hypotheses requiring empirical validation

## Gaps

- Orchestrator Agent profile design (the 13 research claims above are the design substrate; the formal agent profile is the next deliverable)
- Code Generation Agent, Test Generation Agent, Code Review Agent profiles pending
- Observability layer design not yet documented as a standalone agent profile or implementation note
- Dependency graph analysis mechanism for v2 parallel execution not documented

## Inputs

From [[requirements-phase]]:
- Structured requirements
- User stories
- Constraints

## Outputs

To [[development-phase]]:
- System architecture
- Component designs
- Interface specifications
- Design patterns and guidelines

---

Topics:
- [[agent-registry]]

Agent Notes:
- 2026-03-02: Design phase is heavily loaded with foundational research claims from batch 2026-03-01. The phase has no agent profiles yet — only research claims about how to design agents. The Orchestrator Agent profile is the clear first deliverable based on orchestrator-first bootstrapping. Claims 001+002+003+007 form a coherent team design blueprint: build orchestrator first, scope to 5 agents (3-7 range), cover the core build loop, roll out in phases.
- 2026-03-02: Batch orchestrator-agent added 13 new research claims (019-031) establishing the Orchestrator Agent's v1/v2 architecture. The batch forms two clusters: (1) v1 design constraints — routing role, sequential pipeline, lossless context transfer, hard iteration limits, hybrid orchestration; (2) v2 roadmap — parallel execution, intelligent windowing, capability routing, observability. The two tension notes (030, 031) are the explicit acknowledgments of trade-offs accepted in v1. The calibration hypothesis (027) and observability prerequisite (028) are the open questions blocking metric validation.
