---
claim: "optimal multi-agent team size is 3 to 7 specialized agents"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 002: optimal multi-agent team size is 3 to 7 specialized agents

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 21-25)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim.

Rationale: Research-backed sizing threshold with clear upper and lower bounds and explanations for each boundary. Below 3: unnecessary complexity (single agent suffices). Above 7: coordination overhead outweighs benefit unless hierarchical structures are introduced. Fits extraction category "metrics that matter" — this is a measurable, actionable design constraint for catalog scoping.

Semantic neighbor: null — no existing agent profile captures team sizing principles.

---

## Create

Created: `agents/optimal-multi-agent-team-size-is-3-to-7-specialized-agents.md`

Note title: optimal multi-agent team size is 3 to 7 specialized agents
Path: agents/optimal-multi-agent-team-size-is-3-to-7-specialized-agents.md
Word count: ~280 words (body)
Status: complete

Key content:
- Explains the two distinct failure modes at each boundary (below 3: single agent suffices; above 7: coordination overhead dominates)
- Connects the sizing constraint to the orchestrator slot: effective specialist range is 2–6 within a 3–7 team
- Concrete vault implication: initial catalog scopes to 3–5 agents covering the core build loop
- Links to sibling claims: [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]]

## /map

Completed: 2026-03-02

**Phase overview MOC updated:**
- Added to [[design-phase]] Core Ideas section

**Connections added:**
- -> [[phased rollout prevents coordination chaos when building multi-agent systems]] — grounds: the 4-phase rollout produces 5-6 agents by Phase 4, staying within the 3-7 range
- -> [[what metrics distinguish a well-functioning orchestrator from a coordination bottleneck]] — grounds: the coordination overhead scaling research (super-linear at ~1.724) quantifies the mechanism behind the 7-agent upper boundary

**Articulation test:** PASS

**Discovery trace:**
- Phase overview read: [[design-phase]]
- Sibling claims: added phased-rollout (already listed in others but missing here) and metrics-orchestrator (which quantifies the scaling math behind the 3-7 boundary)

## /refine
(to be filled by /refine phase)

## /validate
(to be filled by /validate phase)
