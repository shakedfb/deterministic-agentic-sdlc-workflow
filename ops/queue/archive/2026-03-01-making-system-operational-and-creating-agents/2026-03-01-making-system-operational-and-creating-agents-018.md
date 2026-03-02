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

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[agentic-sdlc-systems-require-explicit-human-supervision-at-high-stakes-handoff-points]] — added backward link: LangGraph conditional edges for encoding supervision gates as first-class graph nodes
- [[when-should-langgraph]] — added backward links to agentic-sdlc-supervision and what-metrics in Relevant Notes
- [[base-model-quality-matters-more-than-framework-choice-for-agent-capability]] — added backward link: both LangGraph and CrewAI share the base model prerequisite

**Gap check:**
- agentic-sdlc-supervision didn't reference LangGraph as the implementation mechanism for supervision gates; gap closed
- base-model-quality mentioned LangGraph inline without wiki-linking when-langgraph; gap closed (via when-langgraph's reflect)

**Sibling cross-check:**
- crewai-aligns-best, workflows-preferable, agent-profile-framework-field all reference when-langgraph via reflect phase

## /validate

**Verified:** 2026-03-02T12:35:07Z

Recite:
- Prediction: 3/5 — description adds mechanism/context beyond title
- Retrieval: deferred (semantic search disabled in config)
- Description: kept (passes minimum threshold, length exceeds 200-char guideline)

Validate:
- Required fields: PASS (description and topics present)
- Description constraints: WARN (599 chars, exceeds 200-char guideline; trailing period; adds mechanism)
- Topics: PASS

Review:
- Frontmatter: PASS
- Phase overview connection: PASS (note appears in assigned topic map)
- Wiki links: 10 outgoing — PASS
- Link resolution: PASS (all links resolve after fixes applied)

Overall: PASS (2 warnings)

Actions taken:
- Fixed dangling wiki links where title-form links used question titles instead of file slugs
- Added topics field to requirements-analyst-agent.md
- Removed misplaced numbered duplicates from agents/ directory (2026-03-01-*-004/007/016/017.md)

Recommended actions:
- Trim descriptions to under 200 chars in a future editing pass (WARN-level, not urgent)
- Design code-generation-agent profile to resolve forward reference in requirements-analyst-agent.md

