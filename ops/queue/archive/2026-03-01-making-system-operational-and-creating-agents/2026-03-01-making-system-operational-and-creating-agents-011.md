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

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[requirements-analyst-agent]] — added inline link: escalation conditions section implements [[agent profiles must include escalation conditions as a required design field]]
- [[agent-profiles-must-include-escalation-conditions]] — added backward link to [[what does a minimum viable Requirements Analyst Agent prompt look like]] as the first concrete implementation

**Gap check:**
- requirements-analyst-agent implemented escalation conditions without linking the schema requirement; gap closed
- escalation-conditions note didn't reference its first concrete implementation; gap closed

**Sibling cross-check:**
- specific-escalation-patterns already references escalation-conditions as the schema requirement note

## /validate

**Verified:** 2026-03-02T12:35:07Z

Recite:
- Prediction: 4/5 — description adds mechanism/context beyond title
- Retrieval: deferred (semantic search disabled in config)
- Description: kept (passes minimum threshold, length exceeds 200-char guideline)

Validate:
- Required fields: PASS (description and topics present)
- Description constraints: WARN (336 chars, exceeds 200-char guideline; trailing period; adds mechanism)
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

