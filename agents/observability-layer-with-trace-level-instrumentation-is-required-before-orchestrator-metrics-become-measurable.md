---
description: The orchestrator's four health metrics — delegation success rate, specialist utilization balance, coordination overhead ratio, and error containment factor — are aspirational rather than operational until a dedicated observability layer captures per-delegation timing, per-handoff validation results, and per-workflow state transitions at trace level.
topics: ["[[agent-registry]]", "[[design-phase]]", "[[operations-phase]]"]
source: "[[orchestrator-agent]]"
classification: open
---

# observability layer with trace-level instrumentation is required before orchestrator metrics become measurable

An orchestrator prompt can be written to report pipeline state at the end of each run. It can log which tasks it delegated, which succeeded, and which failed. But logging is not measurement. The difference is the granularity and the persistence: a prompt-level state report tells you what happened in one run; an observability layer tells you what is happening across all runs, with enough detail to detect trends, identify outliers, and calibrate thresholds based on actual data.

The four orchestrator health metrics defined in [[what metrics distinguish a well-functioning orchestrator from a coordination bottleneck]] — delegation success rate, specialist utilization balance, coordination overhead ratio, and error containment factor — require trace-level data to be computed. Delegation success rate needs a count of all delegations and their outcomes per time window, not per-run summaries. Utilization balance requires timing data across all specialist invocations to detect skew. Coordination overhead requires per-task timing that separates the orchestrator's processing time from specialist execution time. Error containment requires tracking which errors were handled by the orchestrator versus which escalated to humans, across a meaningful sample.

None of this can be inferred from prompt-level reports. The orchestrator's self-reported output is too coarse and too ephemeral — it exists within a conversation context and is not persisted to a queryable store.

The observability layer design requires three components: instrumentation hooks in the orchestrator's execution (capturing timing and outcome at every delegation and handoff boundary), a persistent store (capturing across runs and accessible to analysis queries), and a query layer (allowing the four metrics to be computed on demand). OpenTelemetry-standard structured tracing across all LLM calls, tool invocations, and agent steps is the data layer implementation — the minimum instrumentation surface covers per-delegation timing, per-handoff validation results, per-workflow breakdowns, and per-error handling decisions, exactly the events that [[the orchestrator agents role is routing and validation not content generation]] isolates by enforcing strict role separation between the coordinator and its specialists. Building this layer is a prerequisite for the metric assertions in the Orchestrator Agent profile to be validated rather than aspirational.

The observability layer is also the gate for two specific v2 enhancements. [[specialist capability matching and load balancing is a v2 orchestrator routing enhancement]] requires real-time specialist load data the layer provides. More subtly, [[phased rollout prevents coordination chaos when building multi-agent systems]] uses phase readiness criteria — delegation success rate ≥ 95%, coordination overhead < 20% — that can only be evaluated if those metrics are being measured across runs. Without the observability layer, phase advancement decisions are judgment calls rather than data-driven assessments.

The practical implication for v1: implement the orchestrator without the observability layer, run it on test cases, and instrument it manually as needed for specific investigations. The observability layer is the v1.5 enhancement that makes continuous monitoring viable. Without it, the metrics are design targets and calibration hypotheses like those in [[the four-phase build loop calibration hypothesis for iteration limits]] — which requires execution trace data to validate whether 3 code generation attempts and 2 review cycles are correctly scoped — remain unverifiable. With the observability layer, they become operational signals.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[what metrics distinguish a well-functioning orchestrator from a coordination bottleneck]] — the four metric categories that the observability layer must be built to compute; without instrumentation, these metrics are defined but not computable
- [[the four-phase build loop calibration hypothesis for iteration limits]] — one of the open hypotheses that requires production trace data to validate; the calibration numbers for iteration limits cannot be empirically confirmed without execution trace data
- [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] — escalation events are the high-value signals that the observability layer must capture; the rate of human escalations is itself a metric that reveals orchestrator health
- [[specialist capability matching and load balancing is a v2 orchestrator routing enhancement]] — load balancing requires real-time specialist load data that only the observability layer can provide; the v2 routing enhancement is blocked until the observability layer is operational
- [[the orchestrator agents role is routing and validation not content generation]] — strict role separation between routing and generation is the architectural precondition that makes the orchestrator's functions independently instrumentable; the observability layer instruments precisely those isolated functions, and without role separation the instrumentation surface would be ambiguous
- [[phased rollout prevents coordination chaos when building multi-agent systems]] — phase readiness criteria (delegation success rate ≥ 95%, coordination overhead < 20%) are the decision gates for advancing between rollout phases; these gates require the observability layer to produce measurable signals rather than subjective assessments
- [[hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines]] — iteration limit calibration (3 code generation attempts, 2 review cycles) cannot be empirically validated without execution trace data; the observability layer is the measurement prerequisite that converts the hard limit principle into a tunable operational parameter

**Topics:**
- [[agent-registry]]
- [[design-phase]]
- [[operations-phase]]
