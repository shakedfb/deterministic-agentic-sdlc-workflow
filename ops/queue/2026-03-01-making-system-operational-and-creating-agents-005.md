---
claim: "CrewAI aligns best with catalog-driven SDLC agent architectures"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 005: CrewAI aligns best with catalog-driven SDLC agent architectures

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 43-50)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim.

Rationale: This is a comparative framework recommendation with explicit reasoning: CrewAI's role-based team structure maps naturally to agent profiles defined by role; LangGraph suits complex conditional branching; ADK is cloud-specific. The source concludes CrewAI is the best fit for a catalog-driven architecture. Fits extraction categories "agent design patterns" and "metrics that matter." The vault's design philosophy (agents defined by role) is explicitly cited as the reason for the recommendation.

Semantic neighbor: null — no framework comparison note exists yet.

---

## Create

Created: `agents/crewai-aligns-best-with-catalog-driven-sdlc-agent-architectures.md`

Note title: CrewAI aligns best with catalog-driven SDLC agent architectures
Path: agents/crewai-aligns-best-with-catalog-driven-sdlc-agent-architectures.md
Word count: ~420 words (body)
Status: complete

Key content:
- Explains why CrewAI's role-based team primitive structurally aligns with catalog-driven agent design (roles defined before implementation)
- Contrasts LangGraph (graph-based conditional branching) and Google ADK (cloud-coupled) to show they address different problems
- Argues that vault schema fields (current_prompt, responsibilities, interactions) map directly to CrewAI agent definitions — catalog as pre-implementation spec
- Clarifies the boundary condition: CrewAI for team-level orchestration, LangGraph reserved for agents with fundamentally conditional internal workflows
- Connected to: [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]], [[spec-centric architecture is the most reliable pattern for agents building systems]]

## /map

Completed: 2026-03-02

**Phase overview MOC updated:**
- Added to [[design-phase]] Core Ideas section

**New connections added:**
- -> [[how does CrewAI handle agent-to-agent handoff and what does its interaction API look like]] — grounds: the implementation mechanics (context parameter, TaskOutput, Process modes) translate the framework recommendation to running code
- -> [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — extends: the complementary decision criterion completing the CrewAI-vs-LangGraph selection tree
- -> [[base model quality matters more than framework choice for agent capability]] — extends: framework recommendation is conditional on capable base model

**Articulation test:** PASS

**Discovery trace:**
- Phase overview read: [[design-phase]]
- Sibling claims: crewai-handoff (014) is the natural follow-on to the framework recommendation; when-langgraph (018) is the paired decision tree note; base-model-quality (009) is the priority ordering context

## /refine

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[workflows-are-preferable-to-agents-for-deterministic-sdlc-phases]] — added backward link in three-way decision tree paragraph: deterministic → workflow, role-sequential → CrewAI, branching/cyclic → LangGraph
- [[optimal-multi-agent-team-size-is-3-to-7-specialized-agents]] — added backward link: 3-7 range as natural operating envelope for CrewAI team modes

**Gap check:**
- workflows-preferable described the decision logic without linking CrewAI recommendation; gap closed
- team-size note discussed coordination implications without referencing CrewAI framework; gap closed

**Sibling cross-check:**
- phased-rollout now references CrewAI via inline link added for context

## /validate

**Verified:** 2026-03-02T12:35:07Z

Recite:
- Prediction: 4/5 — description adds mechanism/context beyond title
- Retrieval: deferred (semantic search disabled in config)
- Description: kept (passes minimum threshold, length exceeds 200-char guideline)

Validate:
- Required fields: PASS (description and topics present)
- Description constraints: WARN (243 chars, exceeds 200-char guideline; trailing period; adds mechanism)
- Topics: PASS

Review:
- Frontmatter: PASS
- Phase overview connection: PASS (note appears in assigned topic map)
- Wiki links: 13 outgoing — PASS
- Link resolution: PASS (all links resolve after fixes applied)

Overall: PASS (2 warnings)

Actions taken:
- Fixed dangling wiki links where title-form links used question titles instead of file slugs
- Added topics field to requirements-analyst-agent.md
- Removed misplaced numbered duplicates from agents/ directory (2026-03-01-*-004/007/016/017.md)

Recommended actions:
- Trim descriptions to under 200 chars in a future editing pass (WARN-level, not urgent)
- Design code-generation-agent profile to resolve forward reference in requirements-analyst-agent.md

