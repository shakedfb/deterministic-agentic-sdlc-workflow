---
id: claim-025
type: claim
batch: orchestrator-agent
target: "intelligent context windowing is needed when spec artifacts exceed the context window"
classification: open
file: orchestrator-agent-025.md
created: 2026-03-02T00:00:00Z
current_phase: create
completed_phases: []
---

# Claim 025: intelligent context windowing is needed when spec artifacts exceed the context window

## Source
ops/queue/archive/2026-03-02-orchestrator-agent/orchestrator-agent.md

## Claim
For large specs, passing the full spec artifact at every handoff will exceed context windows. The v2 solution is intelligent windowing: full spec for the first task, then only deltas and relevant sections for subsequent tasks.

## Classification
OPEN — hypothesis, not yet validated

## Connections
- [[lossless context transfer (orchestrator-agent-021)]]
- [[spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems]]

## Create
(filled by create phase)

## Reflect
(filled by reflect phase)

## Reweave
(filled by reweave phase)

## Verify
(filled by verify phase)
