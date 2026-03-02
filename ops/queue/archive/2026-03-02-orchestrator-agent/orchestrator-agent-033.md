---
id: claim-033
type: enrichment
batch: orchestrator-agent
target: "specific-escalation-patterns-in-production-agentic-sdlc-systems"
file: orchestrator-agent-033.md
created: 2026-03-02T00:00:00Z
current_phase: enrich
completed_phases: []
---

# Enrichment 033: specific-escalation-patterns-in-production-agentic-sdlc-systems (HOTL/HITL mapping)

## Source
ops/queue/archive/2026-03-02-orchestrator-agent/orchestrator-agent.md

## Target Note
agents/specific-escalation-patterns-in-production-agentic-sdlc-systems.md

## What to Add
Explicit HOTL/HITL governance tier mapping for the four escalation categories:
- confidence_threshold → HOTL (monitored, non-blocking): plausible but unvalidatable output
- ambiguity_detection → HITL (blocking): undecomposable intent or conflicting outputs
- irreversibility_gate → HITL (blocking): production modifications, elevated permissions, security changes
- loop_termination → HITL (blocking): exceeded retry limits

HOTL = Human on the Loop (monitoring without blocking)
HITL = Human in the Loop (blocks pipeline until human acts)

Source location: orchestrator-agent.md lines ~82-101 (prompt escalation section) and lines ~141-152 (YAML escalation_conditions field)

## Enrich
Added HOTL/HITL governance tier mapping table to agents/specific-escalation-patterns-in-production-agentic-sdlc-systems.md:
- confidence_threshold → HOTL (non-blocking)
- ambiguity_detection → HITL (blocking)
- irreversibility_gate → HITL (blocking)
- loop_termination → HITL (blocking)
Also added concrete iteration limit numbers in the same section.

## Reflect
Phase map interaction complete (2026-03-02). Discovery: design-phase + operations-phase MOC exploration + grep-only search. Sibling batch awareness applied.

Target note (specific-escalation-patterns) is the same as 032 — same target file, second enrichment adding HOTL/HITL governance tier mapping. Both enrichments are now reflected in the same note. Connections verified same as 032.

MOC updates: covered in 032 reflect pass.

Articulation test: PASS

## Reweave
(filled by reweave phase)

## Verify
**Verified:** 2026-03-02T00:00:00Z

Target note: agents/specific-escalation-patterns-in-production-agentic-sdlc-systems.md (same as 032)

Enrichment verification:
- HOTL/HITL governance mapping table present: confidence_threshold→HOTL, others→HITL — PASS
- Concrete iteration limit numbers present in "Concrete Iteration Limits for Loop Termination" section — PASS
- Both enrichments (032 + 033) are reflected in the same note — PASS

Note status (same as 032 verify): Overall PASS — see 032 for full verify details.
NOTE: Reweave section shows "(filled by reweave phase)" but queue claims reweave completed — task file not updated; reweave work is in the agent profile.

Overall: PASS
