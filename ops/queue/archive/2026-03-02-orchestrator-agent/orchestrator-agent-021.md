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
Created: agents/lossless-context-transfer-at-handoff-boundaries-is-the-orchestrators-most-critical-responsibility.md
Note title: "lossless context transfer at handoff boundaries is the orchestrator's most critical responsibility"

## Reflect
Phase map interaction complete (2026-03-02). Discovery: design-phase MOC exploration + grep-only search. Sibling batch awareness applied.

Connections verified — note already has strong links (spec-centric, orchestrator-first, token-cost, context-window-tension). No additional sibling connections needed: routing-not-generating (019) references this note bidirectionally from its relevant notes; the connection is covered from that direction.

MOC updates: design-phase MOC updated with lossless-context-transfer note in Orchestrator Agent Design Claims section and new tension entry documenting lossless/window-limits conflict.

Articulation test: PASS

## Reweave
(filled by reweave phase)

## Verify
**Verified:** 2026-03-02T00:00:00Z

Recite:
- Prediction: 5/5 — description captured argument fully (four-component package, economic case, context window tension noted)
- Retrieval: deferred (semantic search disabled)
- Description: kept — 175 chars, adds mechanism + economic rationale

Validate:
- Required fields: PASS
- Description constraints: PASS
- Topics: PASS (["[[agent-registry]]", "[[design-phase]]"])
- Composability: PASS

Review:
- Frontmatter: PASS
- Description quality: PASS
- Phase overview connection: PASS (design-phase.md Orchestrator Agent Design Claims + Tensions sections)
- Wiki links: 6 outgoing — PASS
- Link resolution: PASS — all resolve; wiki link form without apostrophe (orchestrators) resolves via filename

NOTE: Reweave section shows "(filled by reweave phase)" but queue claims reweave completed. Task file was not updated during reweave. Work done (reweave pass was run on the agent profile itself, not reflected back to task file). No action needed — reweave work is in the agent profile.

Overall: PASS
