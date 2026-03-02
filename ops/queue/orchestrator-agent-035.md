---
id: claim-035
type: enrichment
batch: orchestrator-agent
target: "crewai-agent-to-agent-handoff-and-interaction-api"
file: orchestrator-agent-035.md
created: 2026-03-02T00:00:00Z
current_phase: enrich
completed_phases: []
---

# Enrichment 035: crewai-agent-to-agent-handoff (orchestrator configuration)

## Source
ops/queue/archive/2026-03-02-orchestrator-agent/orchestrator-agent.md

## Target Note
agents/crewai-agent-to-agent-handoff-and-interaction-api.md

## What to Add
The recommended CrewAI configuration for orchestrator agents in SDLC pipelines:
- Use `manager_agent` designation in CrewAI
- Set `allow_delegation=True` for runtime routing decisions
- Combine with `Process.sequential` for pipeline-level flow control
- Result: hierarchical override authority within a sequential pipeline structure

This is the concrete configuration that implements the hybrid sequential-hierarchical pattern.

Source location: orchestrator-agent.md lines ~163-166 (current approach section)

## Enrich
(filled by enrich phase)

## Reflect
(filled by reflect phase)

## Reweave
(filled by reweave phase)

## Verify
(filled by verify phase)
