---
id: claim-042
type: enrichment
batch: code-generator-agent
target: "intelligent-context-windowing-is-needed-when-spec-artifacts-exceed-the-context-window"
file: code-generator-agent-042.md
created: 2026-03-02T00:00:00Z
current_phase: enrich
completed_phases: []
---

# Enrichment 042: intelligent-context-windowing-is-needed-when-spec-artifacts-exceed-the-context-window

## Source
ops/queue/archive/2026-03-02-code-generator-agent/code-generator-agent.md

## Enrichment
The Code Generator Agent source explicitly identifies the specialist-level analog of the orchestrator-level windowing problem. As tasks accumulate, the "prior code" input grows with each task completion. On larger projects, passing all prior code exceeds the context window. The v2 resolution proposed is to pass only the files relevant to the current task's component dependencies, determined from design.md's component graph.

This confirms that intelligent context windowing is a pipeline-wide pattern, not an orchestrator-only concern. Both the orchestrator-level (spec transfer) and specialist-level (prior code accumulation) instances share the same mechanism: dependency graph → relevant sections → filtered delivery. The source document names this explicitly as "the specialist-level instance of the pipeline-wide pattern."

New content to add to agents/intelligent-context-windowing-is-needed-when-spec-artifacts-exceed-the-context-window.md:
- The specialist-level accumulation problem is confirmed by the Code Generator Agent design
- The resolution mechanism (design.md component graph as relevance filter) is a concrete implementation of the windowing principle at the specialist level
- Both the orchestrator and code generator apply the same semantic relevance judgment mechanism (dependency graph → relevant sections), revealing windowing as a cross-cutting architectural pattern

## Connections to add
- [[code-generator-agent]] — the Code Generator's v2 context selection problem is the specialist-level analog; should be added to Relevant Notes

## Enrich
(filled by enrich phase)

## Reflect
(filled by reflect phase)

## Reweave
(filled by reweave phase)

## Verify
(filled by verify phase)
