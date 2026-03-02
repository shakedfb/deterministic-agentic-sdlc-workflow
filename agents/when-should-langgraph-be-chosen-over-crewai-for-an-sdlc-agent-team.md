---
description: LangGraph should be chosen over CrewAI when an SDLC agent team's workflow requires conditional branching, cycles, or complex runtime-dependent execution paths that cannot be predetermined — specifically when code review agents must route between multiple remediation paths, when iterative refinement loops are required, or when the workflow itself (not just the agents) is the primary engineering challenge; CrewAI remains the default for role-defined, phase-sequential SDLC pipelines where the execution path is predictable and the hard problem is agent role specification rather than control flow.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: open
---

# when should LangGraph be chosen over CrewAI for an SDLC agent team

The existing catalog note [[CrewAI aligns best with catalog-driven SDLC agent architectures]] establishes CrewAI as the default framework for role-defined SDLC agent teams. That recommendation holds — with a specific class of exceptions where LangGraph becomes the correct choice. The decision criterion is not team size, not agent count, and not production readiness; it is **whether the workflow's control flow is predetermined or runtime-conditional**.

## The Core Decision Criterion

CrewAI's sequential and hierarchical process modes model an SDLC team as a set of roles executing tasks with defined handoffs. The execution graph is set at design time: requirements agent produces spec, code generation agent consumes spec, test generation agent consumes generated code. When the phase sequence and handoff contracts are predictable, CrewAI's role-based model maps cleanly to the catalog's wiki-link interaction graph without friction.

LangGraph's core primitive is the conditional edge — a branch in execution that evaluates runtime state to determine the next node. When an SDLC workflow has branching that cannot be predetermined (e.g., a code review agent that must route to a security review path, a refactor path, or a rejection path based on error classification observed at runtime), LangGraph's explicit graph model is necessary. Trying to implement conditional routing in CrewAI produces what practitioners describe as "hacked-together loops" — the framework was not designed for it.

The decision gate: **if the workflow execution path depends on agent output content at runtime, use LangGraph for that subgraph.**

## Specific SDLC Scenarios That Tip to LangGraph

**1. Multi-path code review routing.** A code review agent that must choose between three downstream paths (security escalation, standard refactor request, or approval) based on error classification cannot express this cleanly in CrewAI's sequential model. LangGraph's conditional edges make the branching explicit and inspectable.

**2. Iterative refinement loops.** Code generation → test → fail → revise loops require cycles in the execution graph. LangGraph was designed around cycles (the "Graph" in LangGraph explicitly supports directed cycles, unlike simple DAG frameworks). CrewAI can simulate iteration but it is an awkward fit.

**3. Complex state-dependent orchestration.** When the orchestrator must track rich intermediate state across many agents and make routing decisions based on that accumulated state, LangGraph's explicit typed state management (via `TypedDict` state schemas) provides first-class support. CrewAI's context passing is per-task rather than per-session-state.

**4. Recovery and retry workflows.** LangGraph's built-in checkpointing (SqliteSaver, per-node timeouts, pause/resume) makes it production-appropriate for workflows that must survive failures mid-execution. For long-running SDLC pipelines that cannot restart from the beginning on failure, LangGraph's fault tolerance model is superior.

## The Recommended Hybrid Architecture

LangGraph and CrewAI are not mutually exclusive. LangGraph documentation includes official integration guides for wrapping CrewAI agents within LangGraph nodes. The emerging production pattern — increasingly common by late 2025 — uses CrewAI for team-level role definitions and inter-agent handoff contracts, with LangGraph as the outer execution graph that manages control flow, branching, and state persistence.

In this architecture: the vault's agent profiles (role definitions, prompt specifications, interaction links) remain CrewAI-native concepts. The workflow execution shell that decides which agent runs next, when a loop should terminate, and how to route based on output classification is implemented in LangGraph. This preserves the catalog's role-centric design while gaining LangGraph's control flow precision where the SDLC workflow requires it.

## What This Means for Profile Design

Agent profiles in this vault do not need to choose one framework or the other at the profile level. The `framework` field should specify the agent's implementation model (CrewAI for role definition and prompt management) separately from the workflow-level execution model (LangGraph for conditional routing when required). The two layers are orthogonal: an agent can be defined as a CrewAI role and executed within a LangGraph node.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (line 98)

**Relevant Notes:**
- [[CrewAI aligns best with catalog-driven SDLC agent architectures]] — this note establishes the default choice; the present note specifies the decision criterion that tips to LangGraph, making the two notes together a complete framework selection decision tree
- [[workflows-are-preferable-to-agents-for-deterministic-sdlc-phases]] — the same determinism principle that distinguishes agents from workflows also distinguishes CrewAI (predetermined execution path) from LangGraph (runtime-conditional execution); the three-way decision is: deterministic → workflow, role-sequential → CrewAI, branching/cyclic → LangGraph
- [[orchestrator-first bootstrapping reduces-multi-agent-coordination-failures]] — the orchestrator is the natural layer where LangGraph's conditional routing applies; specialist agents remain role-defined in CrewAI while the orchestrator's routing logic benefits from LangGraph's graph model

**Topics:**
- [[agent-registry]]
- [[design-phase]]
