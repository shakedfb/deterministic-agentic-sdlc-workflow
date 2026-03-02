---
id: claim-034
type: enrichment
batch: orchestrator-agent
target: "spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems"
file: orchestrator-agent-034.md
created: 2026-03-02T00:00:00Z
current_phase: enrich
completed_phases: []
---

# Enrichment 034: spec-centric-architecture (operational mechanism at handoffs)

## Source
ops/queue/archive/2026-03-02-orchestrator-agent/orchestrator-agent.md

## Target Note
agents/spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems.md

## What to Add
The operational mechanism for spec-centric architecture at runtime: the spec artifact (or relevant sections) must travel with every task assignment at handoff. The orchestrator's context transfer protocol mandates this.

This operationalizes spec-centric architecture at the handoff level — not just "have a spec" but "carry the spec forward at every transition."

Specific protocol: include spec artifact + all upstream outputs + specific task + prior iteration feedback at every handoff boundary.

Source location: orchestrator-agent.md lines ~167-175 (context transfer protocol section)

## Enrich
(filled by enrich phase)

## Reflect
(filled by reflect phase)

## Reweave
(filled by reweave phase)

## Verify
(filled by verify phase)
