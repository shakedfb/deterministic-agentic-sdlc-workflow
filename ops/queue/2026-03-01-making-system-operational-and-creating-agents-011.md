---
claim: "agent profiles must include escalation conditions as a required design field"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 011: agent profiles must include escalation conditions as a required design field

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 68-70)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim (implementation idea / schema design decision).

Rationale: The source's implication is direct: "Every agent profile should specify its escalation conditions — when it stops and asks a human." This is a schema completeness requirement derived from the human supervision constraint. The existing template does not explicitly include escalation conditions as a field. This is an actionable gap. Fits extraction category "agent design patterns" — schema gap identification.

Semantic neighbor: null — no escalation conditions schema note exists.

---

## Create

Created: `agents/agent-profiles-must-include-escalation-conditions-as-a-required-design-field.md`

Note title: agent profiles must include escalation conditions as a required design field
Path: agents/agent-profiles-must-include-escalation-conditions-as-a-required-design-field.md
Word count: ~430 words (body)
Status: complete

Key content:
- Frames the gap in the current schema: agent profiles document what agents do but not when they stop, leaving authority boundaries undefined
- Argues escalation conditions are a first-class design requirement (same standing as responsibilities, inputs, outputs) not an edge case to add later
- Specifies three categories of escalation conditions every profile should document: ambiguity thresholds, risk thresholds, confidence thresholds
- Notes the validation consequence: adding `escalation_conditions` to required fields surfaces incomplete escalation design at schema validation time, before testing
- Positions this as the operational counterpart to [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] — that note argues why supervision is required; this note specifies where in the schema it must be enforced
- Links to [[phased rollout prevents coordination chaos when building multi-agent systems]], [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], and [[agent profile framework field should capture both orchestration framework and base model]] as parallel schema completeness and escalation routing context

## /map

Completed: 2026-03-02

**Phase overview MOC updated:**
- Added to [[design-phase]] Core Ideas section

**New connection added:**
- -> [[what are the specific escalation patterns used in production agentic SDLC systems]] — extends: provides the specific trigger taxonomy and governance models (HITL/HOTL) that populate the `escalation_conditions` field with actionable content

**Existing connections reviewed:**
- [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]], [[phased rollout prevents coordination chaos when building multi-agent systems]], [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], [[agent profile framework field should capture both orchestration framework and base model]] — all well-articulated

**Articulation test:** PASS

**Discovery trace:**
- Phase overview read: [[design-phase]]
- specific-escalation-patterns (015) was the natural follow-on that fills the schema field with concrete vocabulary

## /refine
(to be filled by /refine phase)

## /validate
(to be filled by /validate phase)
