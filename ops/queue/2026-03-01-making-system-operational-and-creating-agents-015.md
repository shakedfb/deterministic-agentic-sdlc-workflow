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
(to be filled by /map phase)

## /refine
(to be filled by /refine phase)

## /validate
(to be filled by /validate phase)
