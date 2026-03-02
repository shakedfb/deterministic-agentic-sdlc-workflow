---
id: claim-037
type: claim
batch: code-generator-agent
target: "single-task-per-invocation is the correct scope discipline for reliable code generation agents"
classification: closed
file: code-generator-agent-037.md
created: 2026-03-02T00:00:00Z
current_phase: create
completed_phases: []
---

# Claim 037: single-task-per-invocation is the correct scope discipline for reliable code generation agents

## Source
ops/queue/archive/2026-03-02-code-generator-agent/code-generator-agent.md

## Claim
Limiting a code generation agent to exactly one task per invocation produces more reliable output than multi-task batch generation because it keeps the implementation scope narrow, makes failures diagnosable at the task level, and enables fast iteration on individual task failures without re-running the full batch. The orchestrator manages task sequencing; the code generator's job is focused execution within a single bounded scope.

## Classification
CLOSED — asserted as settled design principle in the Code Generator Agent v1 design

## Connections
- [[sequential-pipeline-with-backward-iteration-loops-is-the-lower-risk-v1-architecture-for-multi-agent-build-loops]] (instantiates: single-task invocation is the specialist-side complement of sequential pipeline architecture)
- [[hard-iteration-limits-per-task-are-required-to-prevent-runaway-loops-in-multi-agent-pipelines]] (enables: single-task scope makes per-task iteration limits meaningful and enforceable)
- [[the-orchestrator-agents-role-is-routing-and-validation-not-content-generation]] (depends on: task sequencing is the orchestrator's responsibility, freeing code generator for focused execution)

## Create
Created: agents/single-task-per-invocation-is-the-correct-scope-discipline-for-reliable-code-generation-agents.md
Note title: "single-task-per-invocation is the correct scope discipline for reliable code generation agents"

## Reflect
Phase map interaction complete (2026-03-02). Connections mapped:
- hard-iteration-limits-per-task-are-required-to-prevent-runaway-loops-in-multi-agent-pipelines (enables enforcement)
- sequential-pipeline-with-backward-iteration-loops-is-the-lower-risk-v1-architecture-for-multi-agent-build-loops (specialist complement)
- the-orchestrator-agents-role-is-routing-and-validation-not-content-generation (depends on: orchestrator owns sequencing)
- the-implementation-report-is-the-structured-handoff-artifact (per-task scope → per-task report → clean routing signal)
- spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems (enables: spec removes need for batch context)

Backlinks added to:
- hard-iteration-limits: added single-task note as prerequisite for enforceable per-task limits
- sequential-pipeline: added single-task note as specialist-level complement

Articulation test: PASS

## Reweave
Updated agents/hard-iteration-limits-per-task-are-required-to-prevent-runaway-loops-in-multi-agent-pipelines.md — added [[single-task-per-invocation]] to Relevant Notes
Updated agents/sequential-pipeline-with-backward-iteration-loops-is-the-lower-risk-v1-architecture-for-multi-agent-build-loops.md — added [[single-task-per-invocation]] to Relevant Notes

## Verify
**Verified:** 2026-03-02T00:00:00Z

Recite:
- Prediction: 5/5 — description fully captured the argument (single-task = narrow scope, diagnosable failures, fast iteration, enforceable limits)
- Description: kept — 168 chars, adds mechanism
- Required fields: PASS
- Topics: PASS
- Composability: PASS
- Phase overview connection: development-phase
- Wiki links: 5 outgoing — PASS

Overall: PASS
