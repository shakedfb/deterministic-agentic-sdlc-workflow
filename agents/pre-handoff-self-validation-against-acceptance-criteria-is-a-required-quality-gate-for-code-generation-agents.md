---
description: Code generation agents must self-check their output against acceptance criteria from the spec before reporting completion — this pre-filter catches obvious failures before the more expensive test generation and review phases, reducing iteration cost, and requires explicit failure reporting rather than silent shipment of broken code.
topics: ["[[agent-registry]]", "[[development-phase]]"]
source: "[[code-generator-agent]]"
classification: closed
---

# pre-handoff self-validation against acceptance criteria is a required quality gate for code generation agents

Code generation agents must validate their output against applicable acceptance criteria from the spec before reporting completion to the Orchestrator. This is not an optional quality step — it is a required gate that determines what the Orchestrator receives and how it routes.

The rationale for the self-check is asymmetric cost. Test generation and code review are expensive phases that run downstream of code generation. If a code generation agent ships output with an obvious acceptance criterion failure — a missing required field, an endpoint that doesn't match the specified signature, an error case that isn't handled — that failure propagates through test generation (which writes tests that document the broken behavior) and code review (which either catches the issue late or misses it). Catching obvious failures at the code generation stage, before they enter the downstream pipeline, reduces the total iteration cost of the build loop.

The self-check is not a substitute for external testing. It is a pre-filter. The agent evaluates its output against the acceptance criteria it can reason about directly — checking whether the implementation matches the spec's stated requirements — without executing the code or running the test suite. A code generator that produces output passing self-check can still fail external tests (for edge cases, integration issues, or runtime behavior the self-check cannot evaluate). The self-check reduces the set of failures that reach testing; it does not eliminate them.

The one-attempt self-correction protocol matters. When self-check fails, the agent gets exactly one attempt to fix the issue before reporting. This limit prevents the self-correction from becoming its own retry loop. If the second attempt also fails, the agent must report the failure explicitly in the IMPLEMENTATION REPORT rather than shipping code it knows is broken. This implements the principle of transparent uncertainty over confident errors: an agent that knows its output fails an acceptance criterion but ships it anyway has substituted its own judgment for the spec's authority. Silent failures are worse than reported failures because they propagate uncorrected.

The governance model for self-check failures is HOTL (Human on the Loop), non-blocking. The Orchestrator receives the self-check failure report and decides whether to retry with more context, escalate to human review, or continue to downstream phases with the known failure flagged. This preserves the Orchestrator's routing authority — the code generator surfaces the quality signal; the Orchestrator acts on it.

---

**Source:** [[code-generator-agent]]

**Relevant Notes:**
- [[spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems]] — self-validation only works because acceptance criteria exist in the spec; spec-centric architecture is the prerequisite that makes pre-handoff self-validation possible; without a spec, there is no authoritative criterion to validate against
- [[specific-escalation-patterns-in-production-agentic-sdlc-systems]] — self-check failure maps to the confidence threshold escalation category (HOTL governance, non-blocking); the explicit reporting requirement implements "transparent uncertainty over confident errors," the key design principle of the confidence threshold pattern
- [[agentic-sdlc-systems-require-explicit-human-supervision-at-high-stakes-handoff-points]] — self-check failure reporting is the mechanism by which the code generator surfaces quality issues before they reach human-visible handoff points; the self-check is the agent's contribution to the supervision surface
- [[the-implementation-report-is-the-structured-handoff-artifact-that-enables-orchestrator-routing-decisions-after-code-generation]] — the self-check results are a required section of the IMPLEMENTATION REPORT; without the self-check, the report lacks the quality signal the Orchestrator needs for routing decisions
- [[hard-iteration-limits-per-task-are-required-to-prevent-runaway-loops-in-multi-agent-pipelines]] — the one-attempt self-correction limit is the micro-level application of hard iteration limits; the principle applies at the self-check level just as it applies at the orchestrator-level retry level
- [[the-orchestrator-agents-role-is-routing-and-validation-not-content-generation]] — the HOTL governance model for self-check failures preserves the Orchestrator's routing authority; the code generator reports the signal, the Orchestrator acts on it, maintaining the coordination boundary

**Topics:**
- [[agent-registry]]
- [[development-phase]]
