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
Created: agents/hard-iteration-limits-per-task-are-required-to-prevent-runaway-loops-in-multi-agent-pipelines.md
Note title: "hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines"

## Reflect
Phase map interaction complete (2026-03-02). Discovery: design-phase + operations-phase MOC exploration + grep-only search. Sibling batch awareness applied.

Connections verified — note has comprehensive links: escalation-patterns, agentic-sdlc-supervision, four-phase-calibration, sequential-pipeline. Sibling connections to routing-not-generating (019), hybrid-orchestration (023) added from those notes referencing this one bidirectionally.

MOC updates: design-phase MOC updated (Orchestrator Agent Design Claims section); operations-phase MOC updated with hard-iteration-limits as loop control operations concern.

Articulation test: PASS

## Reweave
(filled by reweave phase)

## Verify
**Verified:** 2026-03-02T00:00:00Z

Recite:
- Prediction: 5/5 — description fully captured argument (hard limits required, escalation mandatory when hit, LLM behavior under repeated failure)
- Retrieval: deferred (semantic search disabled)
- Description: kept — 180 chars, adds mechanism ("hard limits, not soft guidelines") and consequence

Validate:
- Required fields: PASS
- Description constraints: PASS
- Topics: PASS (["[[agent-registry]]", "[[design-phase]]", "[[operations-phase]]"])
- Composability: PASS

Review:
- Frontmatter: PASS
- Description quality: PASS
- Phase overview connection: PASS (design-phase.md Orchestrator Agent Design Claims + operations-phase.md loop control section)
- Wiki links: 9 outgoing — PASS
- Link resolution: PASS — all links resolve; [[what are the specific escalation patterns used in production agentic SDLC systems]] resolves by heading; [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] resolves by heading

NOTE: Reweave section not filled in task file but reweave work done on agent profile (per queue state). No action needed.

Overall: PASS
