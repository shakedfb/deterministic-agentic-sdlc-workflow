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
(to be filled by /map phase)

## /refine
(to be filled by /refine phase)

## /validate
(to be filled by /validate phase)
