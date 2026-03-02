---
description: At every handoff boundary, the orchestrator must transfer the complete context package — spec artifact, all upstream outputs, the specific task, and any iteration feedback — because incomplete context causes specialist failures that cost more in tokens, time, and iterations than the context overhead saved.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[orchestrator-agent]]"
classification: closed
---

# lossless context transfer at handoff boundaries is the orchestrator's most critical responsibility

Of all the things an orchestrator does — routing, validation, state tracking, escalation — lossless context transfer at handoff boundaries is the most critical. This is not an implementation detail. It is the mechanism by which specialists can do their work reliably rather than under conditions of interpretive drift.

The context package that travels with every task assignment has four mandatory components: the spec artifact (or relevant sections), all upstream outputs produced so far in the pipeline, the specific task being delegated, and any iteration feedback from prior failed attempts at this task. Together, these components give the receiving specialist everything it needs to produce output aligned with the original intent and consistent with the work already done. Remove any one component, and the specialist must infer what should have been provided — and inference at this point is where errors originate.

The economic argument for completeness is direct. When a specialist receives incomplete context and produces incorrect output, the cost is not just the specialist's execution: the orchestrator must re-validate, return the task with additional context, and the specialist must re-execute. In practice, context-stripping to save tokens on the handoff produces two or three execution rounds where one would have sufficed. The tokens spent on the retry cycles exceed the tokens saved by the initial stripping. This is why [[token cost of lossless context transfer is justified by the failure cost of context stripping]] — lossless transfer is not generosity; it is the economically optimal strategy when downstream failure costs are accounted for.

The "lossless" constraint creates a real tension with context window limits for large spec artifacts, which is captured in [[lossless context transfer and context window limits are in direct tension for large spec artifacts]]. For v1 systems with manageable spec sizes, this tension does not materialize — full context fits in the window. For v2 systems processing large specs, intelligent windowing (delta-passing after the first task, relevance-filtered sections rather than full documents) is the resolution, but it adds orchestrator complexity that should not be introduced before the baseline is validated.

The orchestrator's prompt design must make the context assembly protocol explicit: what gets included, in what format, and at what level of detail for each handoff type. This is not left to the orchestrator's runtime judgment — it is a designed behavior. This discipline has measurable consequences: incomplete context transfer is one of the three documented root causes of delegation success rate degradation in [[what metrics distinguish a well-functioning orchestrator from a coordination bottleneck]], where the healthy threshold is 95%+ first-attempt delegation success — and failure to hit that threshold is frequently traced back to specialists lacking prerequisite information from upstream phases.

The dependency runs in both directions. The sequential pipeline architecture described in [[sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops]] is specifically built around the assumption that the orchestrator assembles context packages at each handoff boundary; without lossless transfer, the sequential pipeline's primary benefit — failure attribution — breaks down, because a specialist producing incorrect output under incomplete context cannot be distinguished from a specialist failing with complete context.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[the-implementation-report-is-the-structured-handoff-artifact-that-enables-orchestrator-routing-decisions-after-code-generation]] — the IMPLEMENTATION REPORT is the specialist-side half of lossless context transfer at the development phase boundary: the code generator packages its outputs in structured, parseable form so the Orchestrator can assemble the next handoff package without interpretation
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — the spec artifact is the first component in the context package; lossless transfer operationalizes spec-centric architecture at the handoff level, not just the design level
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator-first principle exists in part because context assembly is a non-trivial function; the orchestrator must be designed before specialists can receive properly assembled context
- [[token cost of lossless context transfer is justified by the failure cost of context stripping]] — the economic argument that makes completeness the rational choice even when it increases per-handoff token cost
- [[lossless context transfer and context window limits are in direct tension for large spec artifacts]] — the tension that lossless transfer creates with context window limits, and why intelligent windowing is the v2 resolution
- [[what metrics distinguish a well-functioning orchestrator from a coordination bottleneck]] — delegation success rate, one of the four orchestrator health signals, directly traces degradation to incomplete context transfer; the 95% threshold quantifies what lossless transfer is worth in measurable terms
- [[sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops]] — the sequential pipeline's failure attribution property depends on lossless context at each handoff boundary; corrupted context makes specialist failures indistinguishable from orchestrator errors

**Topics:**
- [[agent-registry]]
- [[design-phase]]
