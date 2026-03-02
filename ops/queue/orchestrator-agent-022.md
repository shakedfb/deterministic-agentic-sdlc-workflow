---
id: claim-022
type: claim
batch: orchestrator-agent
target: "hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines"
classification: closed
file: orchestrator-agent-022.md
created: 2026-03-02T00:00:00Z
current_phase: create
completed_phases: []
---

# Claim 022: hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines

## Source
ops/queue/archive/2026-03-02-orchestrator-agent/orchestrator-agent.md

## Claim
Fixed maximum retry counts per task (not soft guidelines) must be part of every orchestrator design. When limits are reached, escalation to human is mandatory. Without hard limits, error loops compound indefinitely.

## Classification
CLOSED — design constraint with explicit rationale

## Connections
- [[specific-escalation-patterns-in-production-agentic-sdlc-systems]]
- [[agentic-sdlc-systems-require-explicit-human-supervision-at-high-stakes-handoff-points]]

## Create
(filled by create phase)

## Reflect
(filled by reflect phase)

## Reweave
(filled by reweave phase)

## Verify
(filled by verify phase)
