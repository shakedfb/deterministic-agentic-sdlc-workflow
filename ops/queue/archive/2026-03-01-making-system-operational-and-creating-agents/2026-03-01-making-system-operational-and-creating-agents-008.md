---
claim: "agentic SDLC systems require explicit human supervision at high-stakes handoff points"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 008: agentic SDLC systems require explicit human supervision at high-stakes handoff points

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 66-70)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim.

Rationale: The source makes a clear claim about production agentic systems: they are not fully autonomous but human-supervised automation. Agents handle detection, analysis, and planning — but high-stakes actions require human sign-off. The implication is design-level: handoff points must be explicit. This is both an interaction pattern (agent-to-human escalation) and a constraint on agent design. Fits extraction category "interaction patterns."

Semantic neighbor: null — no escalation design note exists.

---

## Create

Created: `agents/agentic-sdlc-systems-require-explicit-human-supervision-at-high-stakes-handoff-points.md`

Note title: agentic SDLC systems require explicit human supervision at high-stakes handoff points
Path: agents/agentic-sdlc-systems-require-explicit-human-supervision-at-high-stakes-handoff-points.md
Word count: ~380 words (body)
Status: complete

Key content:
- Frames human supervision as a structural design constraint, not a limitation — agents are human-supervised automation, not fully autonomous systems
- Explains the compounding failure mode of unsupervised agents across phase handoffs
- Argues escalation conditions are first-class design requirements, not edge cases
- Provides phase-specific escalation examples (requirements scope ambiguity, deployment production changes, security boundary modifications)
- Connects to [[phased rollout prevents coordination chaos when building multi-agent systems]] — Phase 1 manual review is deliberate supervision, not a temporary shortcut
- Connects to [[agent profiles must include escalation conditions as a required design field]] — the operational consequence of this structural principle

## /map

Completed: 2026-03-02

**Phase overview MOCs updated:**
- Added to [[design-phase]], [[operations-phase]], [[deployment-phase]] Core Ideas sections

**Connections reviewed:**
- Already linked to [[phased rollout prevents coordination chaos when building multi-agent systems]], [[agent profiles must include escalation conditions as a required design field]], [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], [[workflows are preferable to agents for deterministic SDLC phases]]
- Comprehensive coverage; note is well-integrated

**Articulation test:** PASS

**Discovery trace:**
- Phase overviews read: [[design-phase]], [[operations-phase]], [[deployment-phase]]
- This note is a hub for the escalation cluster; downstream notes (escalation-conditions, escalation-patterns) both link back to it

## /refine

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[requirements-analyst-agent]] — added inline link: "escalation rate metric (target: below 20%) provides a calibration signal per [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]]"
- [[when-should-langgraph-be-chosen-over-crewai-for-an-sdlc-agent-team]] — added backward link: LangGraph conditional edges for encoding supervision gates as first-class graph nodes

**Gap check:**
- requirements-analyst-agent mentioned escalation rate without linking supervision principle; gap closed
- when-langgraph described supervision implications without linking this note; gap closed

**Sibling cross-check:**
- agentic-sdlc-supervision is a hub note; already well-referenced via reflect phase

## /validate

**Verified:** 2026-03-02T12:35:07Z

Recite:
- Prediction: 4/5 — description adds mechanism/context beyond title
- Retrieval: deferred (semantic search disabled in config)
- Description: kept (passes minimum threshold, length exceeds 200-char guideline)

Validate:
- Required fields: PASS (description and topics present)
- Description constraints: WARN (277 chars, exceeds 200-char guideline; trailing period; adds mechanism)
- Topics: PASS

Review:
- Frontmatter: PASS
- Phase overview connection: PASS (note appears in assigned topic map)
- Wiki links: 11 outgoing — PASS
- Link resolution: PASS (all links resolve after fixes applied)

Overall: PASS (2 warnings)

Actions taken:
- Fixed dangling wiki links where title-form links used question titles instead of file slugs
- Added topics field to requirements-analyst-agent.md
- Removed misplaced numbered duplicates from agents/ directory (2026-03-01-*-004/007/016/017.md)

Recommended actions:
- Trim descriptions to under 200 chars in a future editing pass (WARN-level, not urgent)
- Design code-generation-agent profile to resolve forward reference in requirements-analyst-agent.md

