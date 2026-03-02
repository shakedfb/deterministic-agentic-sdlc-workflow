---
description: When spec artifacts grow large enough to exceed context window limits, lossless full-spec transfer at every handoff becomes physically impossible, requiring a v2 solution of intelligent windowing — full spec on first task, then only deltas and relevant sections for subsequent tasks — though this adds orchestrator complexity that is deferred until the baseline is validated.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[orchestrator-agent]]"
classification: open
---

# intelligent context windowing is needed when spec artifacts exceed the context window

Lossless context transfer is the orchestrator's most critical responsibility at handoff boundaries. But context windows are finite, and spec artifacts for non-trivial software projects can grow large enough that passing the complete spec at every handoff exceeds what fits in a single context window. When this happens, the lossless transfer principle cannot be honored — not as a design choice but as a physical constraint.

The hypothesis tracked by this note is that intelligent windowing is the correct resolution. Rather than degrading to arbitrary context stripping (which produces the specialist failures that make stripping irrational), intelligent windowing takes a structured approach: the full spec travels with the first task assignment in the pipeline, giving the first specialist (the requirements analyst) full context. For subsequent handoffs, the orchestrator passes only the delta since the last handoff and the sections of the spec directly relevant to the current task. This preserves the essential content while managing the token budget.

The design challenge is that "relevant sections" requires the orchestrator to perform semantic relevance judgment — determining which parts of a large spec are germane to a code generation task versus a test generation task. This is non-trivial and introduces a new failure mode: incorrect section selection causes specialists to miss constraints that are present in the spec but absent from the window they received. The orchestrator's relevance judgment must be conservative (err toward inclusion) and must be explicit about what was omitted, so specialists can request additional context if needed.

This remains an open hypothesis because it has not been validated in production. V1 systems with manageable spec sizes sidestep the problem entirely — the tension between [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]] and [[lossless context transfer and context window limits are in direct tension for large spec artifacts]] does not materialize until spec size exceeds the window. The right time to implement intelligent windowing is when spec size first causes handoff failures, not before.

The alternative to windowing — splitting large specs into sub-specs per phase — is simpler to implement but changes the spec structure to accommodate an infrastructure limitation, which is an inversion of concerns. The spec should be authoritative; the orchestrator should adapt to it.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]] — the principle that intelligent windowing must preserve as closely as possible; windowing is the strategy for honoring lossless transfer when full transfer is infeasible
- [[lossless context transfer and context window limits are in direct tension for large spec artifacts]] — the tension that this hypothesis addresses; the tension is documented as unresolvable in v1
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — spec-centric architecture creates the large spec artifact that necessitates windowing; the two are architecturally coupled

**Topics:**
- [[agent-registry]]
- [[design-phase]]
