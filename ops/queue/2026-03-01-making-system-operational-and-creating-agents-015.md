---
claim: "what are the specific escalation patterns used in production agentic SDLC systems"
classification: open
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 015: what are the specific escalation patterns used in production agentic SDLC systems

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (line 95)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is an OPEN claim (open question / research direction).

Rationale: Claim 008 establishes that escalation conditions must be designed into agent profiles, but does not specify what those patterns look like in practice. This open question is the necessary follow-up — what triggers escalation, how is it communicated, who handles it? Answering this fills the gap that claim 011 identifies (escalation as a required schema field). Fits extraction category "interaction patterns."

Semantic neighbor: null — connects to claim 008 (human supervision) and claim 011 (escalation conditions as schema field).

---

## Create

Created: `agents/specific-escalation-patterns-in-production-agentic-sdlc-systems.md`

Note title: what are the specific escalation patterns used in production agentic SDLC systems
Path: agents/specific-escalation-patterns-in-production-agentic-sdlc-systems.md
Word count: ~850 words (body)
Status: complete

Key content:
- Documents four escalation trigger categories: confidence threshold, ambiguity detection, irreversibility gate, and iteration/loop termination
- Defines three governance models (HITL blocking, HOTL monitored, advisory) and maps trigger types to appropriate governance levels
- Documents five communication mechanisms (inline interrupt, issue creation, PR comment, daily digest, audit trail) keyed to governance model
- Specifies what the `escalation_conditions` field in agent profiles must contain: confidence threshold (numeric), ambiguity classes, irreversibility action classes, and governance model per condition
- Introduces 5–15% escalation rate and escalation quality as the primary behavioral metrics for evaluating calibration
- Connects to: [[agent profiles must include escalation conditions as a required design field]], [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]], [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], [[how does CrewAI handle agent-to-agent handoff and what does its interaction API look like]]

## /map

Completed: 2026-03-02

**Phase overview MOCs updated:**
- Added to [[design-phase]] and [[operations-phase]] Core Ideas sections

**Connections reviewed:**
- Already linked to [[agent profiles must include escalation conditions as a required design field]], [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]], [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], [[how does CrewAI handle agent-to-agent handoff and what does its interaction API look like]]
- Coverage is comprehensive; this is a hub note for the escalation cluster

**Articulation test:** PASS — this note and escalation-conditions (011) form a clear pair: 011 establishes the schema requirement, 015 fills it with actionable vocabulary

**Discovery trace:**
- Phase overviews read: [[design-phase]], [[operations-phase]]
- The four trigger categories and governance models defined here provide the vocabulary for the `escalation_conditions` schema field in all agent profiles

## /refine

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[requirements-analyst-agent]] — added inline link: escalation taxonomy from [[what are the specific escalation patterns used in production agentic SDLC systems]]
- [[specific-escalation-patterns]] — added backward links to what-metrics (orchestrator escalation rate) and requirements-analyst-agent (first concrete application)

**Gap check:**
- requirements-analyst-agent described escalation conditions without linking the taxonomy source; gap closed
- specific-escalation-patterns didn't reference its metrics counterpart or first concrete implementation; gaps closed

**Sibling cross-check:**
- escalation-conditions and agentic-sdlc-supervision both link this note via reflect phase

## /validate
(to be filled by /validate phase)
