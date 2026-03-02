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
- [[how does CrewAI handle agent-to-agent handoff and what does its interaction API look like]] — the CrewAI interaction API documentation needed before designing handoff patterns
- [[can GitHub Spec Kit format be adopted as the canonical spec artifact format for this vault]] — the spec format decision resolving the prerequisite for downstream agent design
- [[what metrics distinguish a well-functioning orchestrator from a coordination bottleneck]] — the metric definitions needed for the Orchestrator Agent profile's `metrics` field
- [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — the framework decision criterion completing the CrewAI-vs-LangGraph selection tree

## Tensions

- [[CrewAI aligns best with catalog-driven SDLC agent architectures]] recommends CrewAI as default while [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] identifies scenarios where LangGraph is required — resolved via the hybrid architecture (CrewAI for role definitions, LangGraph for conditional routing)
- [[base model quality matters more than framework choice for agent capability]] inverts the typical framework-first design conversation — model selection is the higher-priority decision

## Gaps

- Orchestrator Agent profile not yet designed (first deliverable per orchestrator-first principle)
- Code Generation Agent, Test Generation Agent, Code Review Agent profiles pending
- Hybrid CrewAI + LangGraph architecture pattern not documented as a standalone note

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
