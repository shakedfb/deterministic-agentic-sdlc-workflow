---
id: claim-030
type: claim
batch: orchestrator-agent
target: "lossless context transfer and context window limits are in direct tension for large spec artifacts"
classification: closed
file: orchestrator-agent-030.md
created: 2026-03-02T00:00:00Z
current_phase: create
completed_phases: []
---

# Claim 030: lossless context transfer and context window limits are in direct tension for large spec artifacts

## Source
ops/queue/archive/2026-03-02-orchestrator-agent/orchestrator-agent.md

## Claim
Full context at every handoff prevents specialist failures from interpretive drift. But large specs may exceed context windows, making lossless transfer physically impossible. The correct resolution is intelligent windowing (delta-passing after the first task), but this adds orchestrator complexity. This tension cannot be dissolved in v1.

## Classification
CLOSED — explicit tension in source

## Connections
- [[lossless context transfer (orchestrator-agent-021)]]
- [[intelligent context windowing (orchestrator-agent-025)]]
- [[spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems]]

## Create
Created: agents/lossless-context-transfer-and-context-window-limits-are-in-direct-tension-for-large-spec-artifacts.md
Note title: "lossless context transfer and context window limits are in direct tension for large spec artifacts"

## Reflect
(filled by reflect phase)

## Reweave
(filled by reweave phase)

## Verify
(filled by verify phase)
