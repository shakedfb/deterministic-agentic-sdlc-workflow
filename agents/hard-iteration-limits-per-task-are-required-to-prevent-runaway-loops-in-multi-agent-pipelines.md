---
description: Every orchestrator design must include fixed maximum retry counts per task — not soft guidelines — because without hard limits, specialist failure loops compound indefinitely, and when limits are reached the only correct response is escalation to a human, not additional retries.
topics: ["[[agent-registry]]", "[[design-phase]]", "[[operations-phase]]"]
source: "[[orchestrator-agent]]"
classification: closed
---

# hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines

Error loops in multi-agent pipelines do not self-terminate. When a specialist agent fails a task, the orchestrator returns the task with feedback, and the specialist attempts again. If the second attempt also fails, the orchestrator returns the task again. Without a hard limit, this cycle continues until the context window fills or the calling system times out — both failure modes that are expensive and opaque. Hard iteration limits convert an unbounded failure loop into a bounded failure with a defined escalation path.

The requirement for hard limits — not soft guidelines — is a design constraint rooted in the behavior of LLMs under repeated failure. A specialist that has failed twice at a task is not in a different cognitive state on the third attempt; it is working from the same model weights with a slightly different prompt. Additional retries beyond a small number are statistically unlikely to produce different outcomes without substantive intervention, which only a human can provide. Soft guidelines ("try a few times before escalating") create ambiguity about when to stop; hard limits remove that ambiguity entirely.

The consequence of reaching a hard limit is non-negotiable: escalation to human review. The escalation must include the full iteration history — all attempts, all feedback, all failure signatures — so that the human reviewer can diagnose the root cause rather than simply being told that the task failed. This is the loop termination escalation pattern documented in [[what are the specific escalation patterns used in production agentic SDLC systems]].

Calibrating the limits is a hypothesis that requires empirical validation. The baseline calibration in the orchestrator design — 3 attempts for code generation, 2 review cycles before escalation — is a reasonable starting point for typical development tasks, but this is documented in [[the four-phase build loop calibration hypothesis for iteration limits]] as an open question requiring production data. The specific numbers matter less than the principle: the numbers must be explicit, finite, and enforced.

The interaction with parallel execution is worth noting: in a pipeline where multiple tasks run concurrently, a single task hitting its iteration limit should not block the entire pipeline if other independent tasks can proceed. Sequential v1 architectures sidestep this complexity by serializing tasks — a runaway loop pauses the pipeline, which is visible and correctable. Parallel v2 architectures must handle iteration limit failures per-task without cascading.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[what are the specific escalation patterns used in production agentic SDLC systems]] — loop termination is one of the four escalation trigger categories; hard limits are the mechanism that triggers it
- [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] — hard limits enforce the boundary of agent authority; when the limit is hit, human judgment replaces agent iteration
- [[the four-phase build loop calibration hypothesis for iteration limits]] — the specific calibration numbers (3 code generation attempts, 2 review cycles) are open hypotheses that the hard limit principle makes testable
- [[sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops]] — the backward iteration loops in the sequential pipeline are the bounded version of retries; hard limits define how many backward iterations are permitted before escalation

**Topics:**
- [[agent-registry]]
- [[design-phase]]
- [[operations-phase]]
