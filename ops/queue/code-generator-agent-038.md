---
id: claim-038
type: claim
batch: code-generator-agent
target: "pre-handoff self-validation against acceptance criteria is a required quality gate for code generation agents"
classification: closed
file: code-generator-agent-038.md
created: 2026-03-02T00:00:00Z
current_phase: create
completed_phases: []
---

# Claim 038: pre-handoff self-validation against acceptance criteria is a required quality gate for code generation agents

## Source
ops/queue/archive/2026-03-02-code-generator-agent/code-generator-agent.md

## Claim
Code generation agents must self-validate their output against applicable acceptance criteria from the spec before reporting completion. This pre-filter catches obvious failures before the more expensive test generation and review phases, reducing iteration cost in the outer loop. The self-check is not a substitute for external testing — it is a quality gate that prevents known-broken code from advancing. When self-check fails after one self-correction attempt, the agent must report the failure explicitly rather than shipping broken output (transparent uncertainty over confident errors).

## Classification
CLOSED — asserted as required design constraint in Code Generator Agent v1; connected to escalation taxonomy

## Connections
- [[specific-escalation-patterns-in-production-agentic-sdlc-systems]] (applies: self-check failure maps to HOTL governance — monitored but non-blocking, Orchestrator routes based on result)
- [[agentic-sdlc-systems-require-explicit-human-supervision-at-high-stakes-handoff-points]] (implements: self-check failure reporting is the mechanism by which the code generator surfaces quality issues for human awareness)
- [[spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems]] (requires: self-validation only works because acceptance criteria live in the spec; without spec, no criteria to validate against)

## Create
(filled by create phase)

## Reflect
(filled by reflect phase)

## Reweave
(filled by reweave phase)

## Verify
(filled by verify phase)
