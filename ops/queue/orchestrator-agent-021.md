---
id: claim-021
type: claim
batch: orchestrator-agent
target: "lossless context transfer at handoff boundaries is the orchestrator's most critical responsibility"
classification: closed
file: orchestrator-agent-021.md
created: 2026-03-02T00:00:00Z
current_phase: create
completed_phases: []
---

# Claim 021: lossless context transfer at handoff boundaries is the orchestrator's most critical responsibility

## Source
ops/queue/archive/2026-03-02-orchestrator-agent/orchestrator-agent.md

## Claim
At every handoff, the orchestrator must include the spec artifact, all upstream outputs, the specific task, and any iteration feedback. Stripping context to save tokens causes specialist failures that cost more than the tokens saved.

## Classification
CLOSED — explicit design constraint with economic rationale

## Connections
- [[spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems]]
- [[orchestrator-first-bootstrapping-reduces-multi-agent-coordination-failures]]

## Create
(filled by create phase)

## Reflect
(filled by reflect phase)

## Reweave
(filled by reweave phase)

## Verify
(filled by verify phase)
