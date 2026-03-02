---
description: Every orchestrator design must include fixed maximum retry counts per task — not soft guidelines — because without hard limits, specialist failure loops compound indefinitely, and when limits are reached the only correct response is escalation to a human, not additional retries.
topics: ["[[agent-registry]]", "[[design-phase]]", "[[operations-phase]]"]
source: "[[orchestrator-agent]]"
classification: closed
---

# hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines

Error loops in multi-agent pipelines do not self-terminate. When a specialist agent fails a task, the orchestrator returns the task with feedback, and the specialist attempts again. If the second attempt also fails, the orchestrator returns the task again. Without a hard limit, this cycle continues until the context window fills or the calling system times out — both failure modes that are expensive and opaque. Hard iteration limits convert an unbounded failure loop into a bounded failure with a defined escalation path.

The requirement for hard limits — not soft guidelines — is a design constraint rooted in the behavior of LLMs under repeated failure. A specialist that has failed twice at a task is not in a different cognitive state on the third attempt; it is working from the same model weights with a slightly different prompt. Additional retries beyond a small number are statistically unlikely to produce different outcomes without substantive intervention, which only a human can provide. Soft guidelines ("try a few times before escalating") create ambiguity about when to stop; hard limits remove that ambiguity entirely.

The consequence of reaching a hard limit is non-negotiable: escalation to human review. The escalation must include the full iteration history — all attempts, all feedback, all failure signatures — so that the human reviewer can diagnose the root cause rather than simply being told that the task failed. This is the loop termination escalation pattern documented in [[what are the specific escalation patterns used in production agentic SDLC systems]], which classifies it as a HITL (blocking) escalation: the pipeline halts until the human acts. The full-history requirement is the hard iteration limit version of the lossless context transfer principle — just as [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]] applies at normal handoffs, the same completeness requirement applies at escalation handoffs, where stripping iteration history from the escalation packet leaves the human unable to diagnose root cause.

Calibrating the limits is a hypothesis that requires empirical validation. The baseline calibration in the orchestrator design — 3 attempts for code generation, 2 review cycles before escalation — is a reasonable starting point for typical development tasks, but this is documented in [[the four-phase build loop calibration hypothesis for iteration limits]] as an open question requiring production data. The specific numbers matter less than the principle: the numbers must be explicit, finite, and enforced.

The interaction with parallel execution is worth noting: in a pipeline where multiple tasks run concurrently, a single task hitting its iteration limit should not block the entire pipeline if other independent tasks can proceed. Sequential v1 architectures sidestep this complexity by serializing tasks — a runaway loop pauses the pipeline, which is visible and correctable. Parallel v2 architectures must handle iteration limit failures per-task without cascading; this is one of the reasons [[parallel task execution requires dependency graph analysis and is a v2 concern for SDLC pipelines]] — correctly isolating task failures in a parallel fanout requires confirmed independence analysis before the fanout, so that a limit breach in one task does not corrupt shared state used by others.

The hard limit is also the precise mechanism that makes the orchestrator's "escalate not absorb" role enforceable. The [[the orchestrator agents role is routing and validation not content generation]] principle holds that an orchestrator reaching the iteration limit must escalate to humans — not generate a fix itself. Without a hard limit, a poorly scoped orchestrator can rationalize continued specialist retries or begin absorbing the task, blurring the coordination boundary that makes failure attribution possible. The [[hybrid sequential-hierarchical orchestration gives predictable flow with dynamic error handling]] pattern makes this explicit: the orchestrator's hierarchical override authority activates on the exception path, but the exception path terminates at the hard limit, not at the orchestrator's judgment about whether another retry might succeed.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[single-task-per-invocation-is-the-correct-scope-discipline-for-reliable-code-generation-agents]] — single-task invocation makes per-task iteration limits enforceable; without a single bounded scope per invocation, the "per task" in "per-task limits" has no meaningful unit
- [[what are the specific escalation patterns used in production agentic SDLC systems]] — loop termination is one of the four escalation trigger categories; hard limits are the mechanism that triggers it; the note classifies loop termination escalation as HITL (blocking), providing the governance model that the hard limit principle requires
- [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] — hard limits enforce the boundary of agent authority; when the limit is hit, human judgment replaces agent iteration
- [[the four-phase build loop calibration hypothesis for iteration limits]] — the specific calibration numbers (3 code generation attempts, 2 review cycles) are open hypotheses that the hard limit principle makes testable
- [[sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops]] — the backward iteration loops in the sequential pipeline are the bounded version of retries; hard limits define how many backward iterations are permitted before escalation
- [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]] — the same completeness principle applies at escalation handoffs: the full iteration history (all attempts, feedback, failure signatures) is the escalation packet, and stripping it is as costly as stripping context at a normal handoff
- [[the orchestrator agents role is routing and validation not content generation]] — hard limits are the mechanism that enforces the "escalate not absorb" constraint; without a hard cap, an orchestrator can rationalize indefinite retries instead of surfacing the failure to humans
- [[hybrid sequential-hierarchical orchestration gives predictable flow with dynamic error handling]] — in the hybrid pattern, the orchestrator's hierarchical override authority activates on the exception path; the hard limit is what converts the exception path from an open-ended retry loop into a bounded sequence that terminates in escalation
- [[parallel task execution requires dependency graph analysis and is a v2 concern for SDLC pipelines]] — in v2 parallel architectures, per-task iteration limit breaches must not cascade to independent tasks; dependency graph analysis is the prerequisite for knowing which tasks are truly independent when one hits its limit
- [[what metrics distinguish a well-functioning orchestrator from a coordination bottleneck]] — the error containment factor metric tracks whether the orchestrator catches failures before they propagate; hard iteration limits are the structural mechanism that enables containment at the task level, and the 5-15% escalation rate target is the observable signal that limits are calibrated correctly

**Topics:**
- [[agent-registry]]
- [[design-phase]]
- [[operations-phase]]
