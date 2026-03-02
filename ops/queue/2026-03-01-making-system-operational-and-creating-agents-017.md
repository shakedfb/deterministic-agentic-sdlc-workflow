---
claim: "what metrics distinguish a well-functioning orchestrator from a coordination bottleneck"
classification: open
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 017: what metrics distinguish a well-functioning orchestrator from a coordination bottleneck

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (line 97)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is an OPEN claim (open question / research direction).

Rationale: Claim 001 establishes the orchestrator as the first agent to build. Claim 002 establishes that team size affects coordination overhead. But neither provides metrics for detecting when the orchestrator itself becomes a bottleneck. This is a gap in the "metrics that matter" extraction category — it identifies measurable success criteria needed for the Orchestrator Agent profile's `metrics` field.

Semantic neighbor: null — connects to claims 001 and 002.

---

## Create

Created: `agents/what-metrics-distinguish-a-well-functioning-orchestrator-from-a-coordination-bottleneck.md`

Note title: what metrics distinguish a well-functioning orchestrator from a coordination bottleneck
Path: agents/what-metrics-distinguish-a-well-functioning-orchestrator-from-a-coordination-bottleneck.md
Status: complete (recovered from misplaced file in agents/ directory)

## /map

Completed: 2026-03-02

**Phase overview MOCs updated:**
- Added to [[design-phase]] and [[operations-phase]] Core Ideas sections

**Connections reviewed:**
- Already linked to [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], [[optimal multi-agent team size is 3 to 7 specialized agents]], [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]], [[what are the specific escalation patterns used in production agentic SDLC systems]]
- Coverage is comprehensive; this is the metrics complement to orchestrator-first

**Articulation test:** PASS

**Discovery trace:**
- Phase overviews read: [[design-phase]], [[operations-phase]]
- This note's four signal categories (delegation success, utilization balance, coordination overhead, error containment) are now referenced by [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] and [[optimal multi-agent team size is 3 to 7 specialized agents]] as the quantified mechanisms behind their claims

## /refine

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[phased-rollout-prevents-coordination-chaos-when-building-multi-agent-systems]] — added backward link: orchestrator health metrics as criteria for declaring phase stability
- [[specific-escalation-patterns-in-production-agentic-sdlc-systems]] — added backward link: escalation rate as a metric observable for calibration verification
- [[when-should-langgraph-be-chosen-over-crewai-for-an-sdlc-agent-team]] — added backward link: LangGraph tracing provides instrumentation surface for the four signal categories

**Gap check:**
- phased-rollout discussed phase readiness without linking the orchestrator metrics definition; gap closed
- specific-escalation-patterns mentioned escalation rate without linking what-metrics; gap closed
- when-langgraph discussed observability without linking metrics note; gap closed

**Sibling cross-check:**
- orchestrator-first, optimal-team-size already reference what-metrics via reflect phase

## /validate

**Verified:** 2026-03-02T12:35:07Z

Recite:
- Prediction: 4/5 — description adds mechanism/context beyond title
- Retrieval: deferred (semantic search disabled in config)
- Description: kept (passes minimum threshold, length exceeds 200-char guideline)

Validate:
- Required fields: PASS (description and topics present)
- Description constraints: WARN (506 chars, exceeds 200-char guideline; trailing period; adds mechanism)
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

