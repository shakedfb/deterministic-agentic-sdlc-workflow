---
description: Safe parallel execution of tasks in a multi-agent SDLC pipeline requires the orchestrator to perform dependency graph analysis to confirm task independence before spawning concurrent workers — without this analysis, parallel fanout risks racing conditions and corrupted handoff context, making it a v2 architectural concern after the sequential baseline is validated.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[orchestrator-agent]]"
classification: open
---

# parallel task execution requires dependency graph analysis and is a v2 concern for SDLC pipelines

Parallel execution in a multi-agent pipeline is not simply "run multiple tasks at the same time." It requires the orchestrator to first determine which tasks are genuinely independent — tasks whose outputs do not depend on each other and which do not write to shared state that the other reads. This determination requires dependency graph analysis: building a model of task dependencies and confirming that the candidate parallel set forms a disconnected subgraph before spawning concurrent workers.

Without dependency analysis, parallel execution introduces two failure modes. Racing conditions occur when two tasks both read and write shared state in an uncoordinated sequence — the last writer wins, and context from the first write is lost. Context corruption occurs when a downstream task begins executing before an upstream task it depends on has completed — the downstream task receives incomplete or stale context that it cannot detect as incomplete, producing plausible but incorrect outputs.

Neither failure mode is easy to debug. They are non-deterministic (the failure depends on execution timing), they produce outputs that are syntactically correct but semantically wrong, and they are invisible in single-run testing. This is why parallel execution is explicitly deferred to v2: the debugging and validation cost of parallel coordination failures is too high to absorb before the sequential baseline is proven.

The v2 dependency analysis requirement places a new design burden on the orchestrator. In addition to routing, validation, context assembly, and escalation, the v2 orchestrator must maintain a task dependency model, evaluate which pending tasks form independent subsets, and coordinate parallel worker lifecycles including partial failures. This is a substantial increase in orchestrator complexity that would undermine the debuggability benefits of the v1 sequential design.

The open question this claim tracks is whether the dependency graph analysis can be made lightweight enough for the orchestrator to perform at runtime — or whether it requires a pre-compiled task graph built at crew initialization time. CrewAI Flows (an experimental feature) represents one implementation direction; LangGraph's explicit graph model is another. The resolution is empirical and depends on the SDLC workflow's actual task dependency structure.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[phased rollout prevents coordination chaos when building multi-agent systems]] — parallel execution is a v2 concern in the same way that deployment and operations agents are later-phase concerns; the phased rollout principle applies at the architecture level, not just the agent level
- [[sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops]] — the sequential v1 choice defers parallel complexity; this note explains the specific reason dependency analysis is required before that deferral can be lifted
- [[sequential pipeline predictability and parallel execution efficiency are in direct tension for SDLC build loops]] — parallel execution is the efficiency gain side of the tension; dependency graph analysis is the cost of accessing that gain safely
- [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — parallel execution with complex dependency relationships is one of the scenarios where LangGraph's explicit graph model may be necessary; CrewAI's parallel task support is less expressive for conditional dependencies

**Topics:**
- [[agent-registry]]
- [[design-phase]]
