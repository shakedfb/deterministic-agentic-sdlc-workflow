---
id: claim-033
type: enrichment
batch: orchestrator-agent
target: "specific-escalation-patterns-in-production-agentic-sdlc-systems"
file: orchestrator-agent-033.md
created: 2026-03-02T00:00:00Z
current_phase: enrich
completed_phases: []
---

# Enrichment 033: specific-escalation-patterns-in-production-agentic-sdlc-systems (HOTL/HITL mapping)

## Source
ops/queue/archive/2026-03-02-orchestrator-agent/orchestrator-agent.md

## Target Note
agents/specific-escalation-patterns-in-production-agentic-sdlc-systems.md

## What to Add
Explicit HOTL/HITL governance tier mapping for the four escalation categories:
- confidence_threshold → HOTL (monitored, non-blocking): plausible but unvalidatable output
- ambiguity_detection → HITL (blocking): undecomposable intent or conflicting outputs
- irreversibility_gate → HITL (blocking): production modifications, elevated permissions, security changes
- loop_termination → HITL (blocking): exceeded retry limits

HOTL = Human on the Loop (monitoring without blocking)
HITL = Human in the Loop (blocks pipeline until human acts)

Source location: orchestrator-agent.md lines ~82-101 (prompt escalation section) and lines ~141-152 (YAML escalation_conditions field)

## Enrich
(filled by enrich phase)

## Reflect
(filled by reflect phase)

## Reweave
(filled by reweave phase)

## Verify
(filled by verify phase)
