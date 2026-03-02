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
Created: agents/intelligent-context-windowing-is-needed-when-spec-artifacts-exceed-the-context-window.md
Note title: "intelligent context windowing is needed when spec artifacts exceed the context window"

## Reflect
Phase map interaction complete (2026-03-02). Discovery: design-phase MOC exploration + grep-only search. Sibling batch awareness applied.

Connections added to agents/intelligent-context-windowing-is-needed-when-spec-artifacts-exceed-the-context-window.md:
- Inline: [[token cost of lossless context transfer is justified by the failure cost of context stripping]] in the sentence about arbitrary context stripping being irrational
- Relevant Notes: added token-cost (economic argument applies to both stripping and windowing)

MOC updates: design-phase MOC updated (Orchestrator Agent Design Claims section).

Articulation test: PASS

## Reweave
(filled by reweave phase)

## Verify
**Verified:** 2026-03-02T00:00:00Z

Recite:
- Prediction: 5/5 — description captured the argument (physical constraint when spec exceeds window, full-spec-first + delta-passing approach, v2 deferral)
- Retrieval: deferred (semantic search disabled)
- Description: kept — adds mechanism (windowing strategy) and scope (v2, deferred until baseline validated)

Validate:
- Required fields: PASS
- Description constraints: PASS (250 chars — slightly long; adds mechanism and timing)
- Topics: PASS (["[[agent-registry]]", "[[design-phase]]"])
- Composability: PASS

Review:
- Frontmatter: PASS
- Description quality: PASS
- Phase overview connection: PASS (design-phase.md Orchestrator Agent Design Claims section)
- Wiki links: 6 outgoing — PASS
- Link resolution: PASS — all resolve; [[code-generator-agent]] resolves to design-ideas/code-generator-agent.md
- NOTE: Reweave section shows "(filled by reweave phase)" but queue claims reweave completed — task file not updated during reweave pass; reweave work is in the agent profile.

Overall: PASS
