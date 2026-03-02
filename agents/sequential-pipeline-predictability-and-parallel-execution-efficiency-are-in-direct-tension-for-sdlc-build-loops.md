---
description: Sequential processing is predictable and debuggable but serializes independent tasks that could run concurrently; parallel execution reduces wall-clock time but requires dependency graph analysis to be safe — this tension cannot be dissolved in v1, where sequentialism is the deliberate trade-off accepting higher wall-clock time in exchange for lower coordination risk.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[orchestrator-agent]]"
classification: closed
---

# sequential pipeline predictability and parallel execution efficiency are in direct tension for SDLC build loops

Sequential pipelines and parallel execution represent a genuine trade-off, not a problem with a clean solution. Sequential processing has a property that parallel execution cannot: every failure is attributable to exactly one phase, the pipeline state is fully known at every point, and debugging proceeds backward through a linear trace. These properties are valuable when a system is being validated for the first time — they make the learning loop fast. But they come at a cost: tasks that could run concurrently are serialized, and wall-clock time increases proportionally to the number of phases.

Parallel execution recovers this wall-clock time by running independent tasks simultaneously. If test generation does not depend on code review results, there is no reason to wait for code review before starting test generation — both can proceed from the code generation output. This is genuinely more efficient. But it is only safe when the orchestrator has performed dependency graph analysis to confirm that the tasks are truly independent: they do not read shared mutable state, their outputs do not conflict, and completing one does not change the context that the other requires (see [[parallel task execution requires dependency graph analysis and is a v2 concern for SDLC pipelines]]).

The tension is inescapable. Sequentialism trades time for certainty; parallelism trades certainty for time. For SDLC pipelines where the task graph is not well-understood until the first few runs have been analyzed, certainty is more valuable — hence the v1 default to sequential. For pipelines that have been validated and where the dependency structure is known, parallelism becomes accessible.

The v1 resolution is deliberate: accept the time cost of sequentialism and use the first runs to map the actual dependency structure. The v2 unlock is dependency graph analysis that converts the known structure into safe parallel subgraphs. This is not a failure of the v1 design; it is the v1 design doing its job by generating the data that makes v2 improvements safe to implement.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops]] — the v1 choice that accepts this tension in favor of predictability; this tension note explains why sequentialism was chosen
- [[parallel task execution requires dependency graph analysis and is a v2 concern for SDLC pipelines]] — the v2 path that resolves the efficiency side of the tension; dependency analysis is the gate that makes parallel execution safe
- [[phased rollout prevents coordination chaos when building multi-agent systems]] — the phased rollout principle embodies the same tension at the agent-introduction level: sequential agent introduction trades time for control

**Topics:**
- [[agent-registry]]
- [[design-phase]]
