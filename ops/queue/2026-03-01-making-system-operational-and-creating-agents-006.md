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

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[crewai-aligns-best-with-catalog-driven-sdlc-agent-architectures]] — added inline link to phased rollout in context of incremental crew member addition
- Note already referenced by: when-langgraph (three-way decision), agentic-sdlc-supervision

**Gap check:**
- crewai-aligns-best described phased agent integration without linking phased-rollout note; gap closed

**Sibling cross-check:**
- optimal-team-size note doesn't need this link (different concern)
- Coverage is sufficient

## /validate

**Verified:** 2026-03-02T12:35:07Z

Recite:
- Prediction: 4/5 — description adds mechanism/context beyond title
- Retrieval: deferred (semantic search disabled in config)
- Description: kept (passes minimum threshold, length exceeds 200-char guideline)

Validate:
- Required fields: PASS (description and topics present)
- Description constraints: WARN (260 chars, exceeds 200-char guideline; trailing period; adds mechanism)
- Topics: PASS

Review:
- Frontmatter: PASS
- Phase overview connection: PASS (note appears in assigned topic map)
- Wiki links: 9 outgoing — PASS
- Link resolution: PASS (all links resolve after fixes applied)

Overall: PASS (2 warnings)

Actions taken:
- Fixed dangling wiki links where title-form links used question titles instead of file slugs
- Added topics field to requirements-analyst-agent.md
- Removed misplaced numbered duplicates from agents/ directory (2026-03-01-*-004/007/016/017.md)

Recommended actions:
- Trim descriptions to under 200 chars in a future editing pass (WARN-level, not urgent)
- Design code-generation-agent profile to resolve forward reference in requirements-analyst-agent.md

