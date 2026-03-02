---
claim: "workflows are preferable to agents for deterministic SDLC phases"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 006: workflows are preferable to agents for deterministic SDLC phases

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 52-56)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim.

Rationale: This is a tension/decision heuristic: agent vs. workflow is a design choice, not an assumption. The source provides the deciding criterion — judgment required vs. deterministic. Examples given: agents for requirements analysis and code review (judgment-heavy); workflows for linting and deployment triggers (mechanical). This prevents over-engineering by building agents where workflows suffice. Fits extraction category "workflow bottlenecks" (clarifying when agents are the wrong tool) and "agent design patterns."

Semantic neighbor: null — no note on agent vs. workflow decision criteria exists.

---

## Create

Created: `agents/workflows-are-preferable-to-agents-for-deterministic-sdlc-phases.md`

Note title: workflows are preferable to agents for deterministic SDLC phases
Path: agents/workflows-are-preferable-to-agents-for-deterministic-sdlc-phases.md
Status: complete

## /map

Completed: 2026-03-02

**Phase overview MOCs updated:**
- Added to [[design-phase]], [[development-phase]], [[deployment-phase]], [[operations-phase]] Core Ideas sections

**Connections reviewed:**
- Already linked to [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]], [[spec-centric architecture is the most reliable pattern for agents building systems]], [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]]
- Existing connections are comprehensive for this note

**Articulation test:** PASS

**Discovery trace:**
- Phase overviews read: [[design-phase]], [[deployment-phase]], [[operations-phase]]
- This note's three-way decision (deterministic→workflow, role-sequential→CrewAI, branching/cyclic→LangGraph) is now explicitly referenced in [[when should LangGraph be chosen over CrewAI for an SDLC agent team]]

## /refine
(to be filled by /refine phase)

## /validate
(to be filled by /validate phase)
