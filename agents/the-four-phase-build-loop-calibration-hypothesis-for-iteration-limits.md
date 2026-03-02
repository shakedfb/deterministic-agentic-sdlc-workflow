---
description: The specific iteration limits of 3 code generation attempts and 2 code review cycles before escalation are calibration hypotheses derived from typical development task complexity — reasonable starting points that require empirical validation against production data to determine whether they are too tight for complex tasks or too loose for simple ones.
topics: ["[[agent-registry]]", "[[design-phase]]", "[[operations-phase]]"]
source: "[[orchestrator-agent]]"
classification: open
---

# the four-phase build loop calibration hypothesis for iteration limits

The four-phase build loop — requirements, code generation, test generation, code review — requires iteration limits at each phase to prevent runaway loops. The question that design answers in principle (hard limits are required) leaves open in practice: what are the specific numbers?

The baseline calibration hypothesis is:
- Code generation: maximum 3 attempts before escalation
- Code review cycles: maximum 2 before escalation
- Workflow-level escalation threshold: 3 or more task-level escalations triggers a full human review of the entire workflow

These numbers are not arbitrary, but they are hypotheses. The reasoning behind them: code generation typically converges in 1-2 iterations when context is complete; a third attempt with fresh feedback and full context is warranted before concluding the task requires human intervention. Code review cycles are shorter because the review agent has less ambiguity about success criteria — if two rounds of review-feedback-revision have not resolved the issue, the issue is likely one that requires architectural judgment beyond the review agent's authority.

The "typical development task" assumption embedded in these numbers is the weakest point. Complex tasks — implementing a new authentication flow, refactoring a core module with multiple dependencies — may legitimately require more iterations before the output converges. Simple tasks — adding a utility function with clear specification — should converge in one attempt; allowing three is overhead. The calibration may need to be task-specific rather than uniform across all tasks in the pipeline.

The dependency on observability is critical: these numbers cannot be validated without [[observability layer with trace-level instrumentation is required before orchestrator metrics become measurable]]. Until execution traces capture per-task retry counts and outcomes, the hypothesis cannot be confirmed or refuted. The numbers will remain calibration guesses rather than validated thresholds until the observability layer exists.

The practical implication for v1 is to implement the baseline calibration, instrument the retry counts, and flag tasks that consistently hit their limits. Patterns in which tasks and which agents trigger frequent escalation are the empirical signal that recalibration is needed.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines]] — the principle that makes calibration necessary; this note provides the specific numbers being hypothesized
- [[what are the specific escalation patterns used in production agentic SDLC systems]] — loop termination is one of the four escalation categories; the calibration numbers determine when loop termination triggers
- [[observability layer with trace-level instrumentation is required before orchestrator metrics become measurable]] — the measurement prerequisite for validating these hypotheses; without execution trace data, the numbers cannot be empirically tested

**Topics:**
- [[agent-registry]]
- [[design-phase]]
- [[operations-phase]]
