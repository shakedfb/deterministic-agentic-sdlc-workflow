---
claim: "when should LangGraph be chosen over CrewAI for an SDLC agent team"
classification: open
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 018: when should LangGraph be chosen over CrewAI for an SDLC agent team

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (line 98)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is an OPEN claim (open question / research direction).

Rationale: Claim 005 recommends CrewAI for catalog-driven architectures, but notes LangGraph is better for complex conditional workflows with branching. This open question asks for the specific decision criteria — when does branching complexity tip the balance toward LangGraph? Answering this produces a reusable decision framework. Fits extraction category "agent design patterns" (framework selection decision criteria).

Semantic neighbor: null — connects to claim 005 (CrewAI recommendation) with the alternative framing.

---

## Create

Created: `agents/when-should-langgraph-be-chosen-over-crewai-for-an-sdlc-agent-team.md`

The note answers the open question by establishing a concrete decision criterion: choose LangGraph when the workflow's control flow is runtime-conditional (branching edges, iteration cycles, complex state-dependent routing) rather than predetermined. CrewAI remains the default for role-sequential SDLC pipelines where the execution path is predictable.

Four specific SDLC scenarios that tip to LangGraph were documented: multi-path code review routing, iterative refinement loops, complex state-dependent orchestration, and recovery/retry workflows. The note also introduces the hybrid architecture pattern (CrewAI for agent role definition within LangGraph nodes for execution graph control) as the emerging production approach.

This connects to [[CrewAI aligns best with catalog-driven SDLC agent architectures]] (which establishes CrewAI as default) and [[workflows-are-preferable-to-agents-for-deterministic-sdlc-phases]] (which provides the parallel determinism logic for the three-way decision).

## /map

Completed: 2026-03-02

**Phase overview MOC updated:**
- Added to [[design-phase]] Core Ideas section

**New connection added:**
- -> [[base model quality matters more than framework choice for agent capability]] — extends: both LangGraph and CrewAI require a capable base model; the framework selection is downstream of model selection for either choice

**Existing connections reviewed:**
- [[CrewAI aligns best with catalog-driven SDLC agent architectures]] (default choice), [[workflows are preferable to agents for deterministic SDLC phases]] (three-way decision tree), [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] (orchestrator as LangGraph routing layer)
- Broken wiki link fixed: `[[orchestrator-first bootstrapping reduces-multi-agent-coordination-failures]]` corrected to `[[orchestrator-first bootstrapping reduces multi-agent coordination failures]]`

**Articulation test:** PASS

**Discovery trace:**
- Phase overview read: [[design-phase]]
- base-model-quality (009) is a constraint shared by both framework options; the parallel constraint makes it a natural extension of the when-langgraph decision criteria

## /refine
(to be filled by /refine phase)

## /validate
(to be filled by /validate phase)
