---
claim: "agent profile framework field should capture both orchestration framework and base model"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 010: agent profile framework field should capture both orchestration framework and base model

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 74-76)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim (implementation idea / schema design decision).

Rationale: The source explicitly calls out an implication for the vault's `framework` field — it should record both the orchestration framework (CrewAI, LangGraph) AND the target base model (GPT-4o, Claude Opus). This is an actionable schema enhancement that prevents losing model selection context. Fits extraction category "agent design patterns" (schema design). Implementation idea that changes the agent profile template.

Semantic neighbor: null — no schema design note exists yet.

---

## Create
Created: agents/agent-profile-framework-field-should-capture-both-orchestration-framework-and-base-model.md
Title: agent profile framework field should capture both orchestration framework and base model
Status: complete

## /map

Completed: 2026-03-02

**Phase overview MOC updated:**
- Added to [[design-phase]] Core Ideas section

**New connection added:**
- -> [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — extends: when the framework choice is LangGraph rather than CrewAI, the compound `framework` field must capture both the LangGraph execution model and the base model

**Existing connections reviewed:**
- [[base model quality matters more than framework choice for agent capability]], [[CrewAI aligns best with catalog-driven SDLC agent architectures]], [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — all well-articulated

**Articulation test:** PASS

**Discovery trace:**
- Phase overview read: [[design-phase]]
- when-langgraph (018) references the framework field amendment in its profile design section, making it a natural bidirectional connection

## /refine

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[base-model-quality-matters-more-than-framework-choice-for-agent-capability]] — added [[when-should-langgraph]] as a backward link to base-model-quality (both frameworks share the base model prerequisite); this note also links base-model-quality as its foundational claim
- Note already referenced by: base-model-quality, crewai-aligns-best, orchestrator-first, when-langgraph via reflect phase

**Gap check:**
- No additional backward link gaps found; agent-profile-framework-field is well-referenced

**Sibling cross-check:**
- Coverage sufficient; the schema amendment note is properly positioned

## /validate
(to be filled by /validate phase)
