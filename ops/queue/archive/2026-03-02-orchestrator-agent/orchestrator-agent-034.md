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
Added "Operational Mechanism: The Spec Travels with Every Handoff" section to agents/spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems.md:
- Four-component handoff protocol: spec artifact + upstream outputs + specific task + iteration feedback
- Distinction between spec existing vs spec being transferred at each handoff
- Context window tension corollary with reference to intelligent windowing
Also added two new relevant notes links.

## Reflect
Phase map interaction complete (2026-03-02). Discovery: design-phase MOC exploration + grep-only search. Sibling batch awareness applied.

Target note (spec-centric-architecture) verified for sibling connections:
- Enrichment added lossless-context-transfer (021) link and intelligent-windowing (025) link
- Note already links to orchestrator-first-bootstrapping, requirements-agents-must-produce-spec, requirements-analyst-agent
- Connections comprehensive for the new content

MOC updates: design-phase MOC already includes spec-centric-architecture from prior batch. Handoff section enrichment is internal to the note.

Articulation test: PASS

## Reweave
(filled by reweave phase)

## Verify
**Verified:** 2026-03-02T00:00:00Z

Target note: agents/spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems.md

Recite:
- Prediction from description: 5/5 — description captured (structured spec at center, replaces improvisation with defined endpoint, prevents interpretive drift)
- Retrieval: deferred (semantic search disabled)
- Description: kept — 178 chars, adds mechanism and outcome

Validate:
- Required fields: PASS
- Topics: PASS (["[[agent-registry]]", "[[requirements-phase]]", "[[development-phase]]", "[[design-phase]]"])
- YAML: PASS
- Composability: PASS

Review:
- Frontmatter: PASS
- Description quality: PASS
- Phase overview connection: PASS (appears in design-phase.md, requirements-phase.md, development-phase.md)
- Wiki links: 9+ outgoing — PASS
- Link resolution: PASS — all resolve; [[the orchestrator agent's role is routing and validation not content generation]] resolves by heading
- Enrichment verification: "Operational Mechanism: The Spec Travels with Every Handoff" section present with four-component protocol — PASS
- NOTE: Reweave section shows "(filled by reweave phase)" but queue claims reweave completed — task file not updated; reweave work is in the agent profile.

Overall: PASS
