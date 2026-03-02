---
claim: "base model quality matters more than framework choice for agent capability"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 009: base model quality matters more than framework choice for agent capability

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 72-76)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim.

Rationale: The source argues that a reliable foundation model (GPT-4o, Claude Opus, or capable reasoning model) is the primary determinant of agent capability — agents on weak base models fail at planning and context retention regardless of framework sophistication. This is a priority-ordering claim (model > framework) with clear implications for the vault's `framework` field design. Fits extraction category "metrics that matter."

Semantic neighbor: null — no base model selection note exists.

---

## Create

Created: [[base-model-quality-matters-more-than-framework-choice-for-agent-capability]]

**Core argument:** A capable foundation model (GPT-4o, Claude Opus, or equivalent reasoning tier) is the primary determinant of agent capability. Agents on weak base models fail at planning and context retention regardless of framework sophistication — the framework is scaffolding; the model is the load-bearing element.

**Key design implication:** Model selection is a first-order design decision of equal weight to framework selection. The `framework` field in agent profiles must capture both the orchestration framework and the target base model. An agent profile missing the base model spec is missing a critical implementation parameter.

**Relevant Notes:**
- [[agent profile framework field should capture both orchestration framework and base model]] — direct schema consequence
- [[CrewAI aligns best with catalog-driven SDLC agent architectures]] — framework decision is downstream of model selection
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — orchestrator carries the highest reasoning load; its model selection is the most consequential
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — requirements analysis and code review are most demanding for base model reasoning

**Topics assigned:** [[agent-registry]], [[design-phase]]

## /map

Completed: 2026-03-02

**Phase overview MOC updated:**
- Added to [[design-phase]] Core Ideas section

**Connections reviewed:**
- Already linked to [[agent profile framework field should capture both orchestration framework and base model]], [[CrewAI aligns best with catalog-driven SDLC agent architectures]], [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]]
- Coverage is comprehensive

**Articulation test:** PASS

**Discovery trace:**
- Phase overview read: [[design-phase]]
- This note is now referenced by both [[CrewAI aligns best with catalog-driven SDLC agent architectures]] and [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] as a shared constraint (both framework options require a capable base model)

## /refine

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[when-should-langgraph-be-chosen-over-crewai-for-an-sdlc-agent-team]] — added backward link to base-model-quality (already linked in reflect phase, confirmed present)

**Gap check:**
- base-model-quality note is now referenced FROM when-langgraph (added in reflect phase for that note)
- No additional gaps found; note already well-linked via reflect phase connections

**Sibling cross-check:**
- crewai-aligns-best, orchestrator-first, minimal-viable-set, agent-profile-framework-field all link this note via reflect phase

## /validate

**Verified:** 2026-03-02T12:35:07Z

Recite:
- Prediction: 4/5 — description adds mechanism/context beyond title
- Retrieval: deferred (semantic search disabled in config)
- Description: kept (passes minimum threshold, length exceeds 200-char guideline)

Validate:
- Required fields: PASS (description and topics present)
- Description constraints: WARN (394 chars, exceeds 200-char guideline; trailing period; adds mechanism)
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

