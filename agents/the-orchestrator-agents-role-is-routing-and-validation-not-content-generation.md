---
description: The orchestrator agent coordinates work by routing tasks to specialist agents and validating outputs at handoff boundaries — it never generates code, writes tests, or analyzes requirements itself, making role separation the architectural definition of the coordination layer.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[orchestrator-agent]]"
classification: closed
---

# the orchestrator agent's role is routing and validation not content generation

The orchestrator agent's job is coordination, not creation. This distinction is architectural, not cosmetic. When the orchestrator receives a task, it does not write code, produce test cases, or interpret requirements — it determines which specialist agent should handle the task, packages the context those specialists need to succeed, and validates their outputs before the work proceeds downstream. The separation is total: the orchestrator touches every part of the pipeline, but it generates nothing in that pipeline.

This role separation explains why the orchestrator is the prerequisite anchor for a multi-agent system, as established in [[orchestrator-first bootstrapping reduces multi-agent coordination failures]]. An orchestrator that also generates content would blur the boundary between coordination and execution, making the system harder to reason about and debug. If the orchestrator can "help" the code generator by writing a few lines of code directly, then failures at the code generation stage become ambiguous — was it the specialist or the orchestrator that produced the defective output? Strict role separation eliminates this ambiguity.

The validator function is equally important. At every handoff boundary, the orchestrator applies a qualification check before passing outputs downstream. This is not quality review in the specialist's domain — the orchestrator does not judge whether the code is well-architected or whether the tests are comprehensive. It checks whether the output satisfies the handoff contract: is the format correct, are required fields present, does the output address the task that was assigned? When the output fails this check, the orchestrator routes it back to the specialist for iteration, not to itself for repair.

The distinction between routing and generating is the clearest test of whether a system has an orchestrator or a super-agent. A super-agent absorbs tasks when specialists struggle; an orchestrator escalates when specialists reach their limits, as defined by [[hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines]]. For SDLC pipelines, this translates directly: the Orchestrator Agent routes requirements analysis work to the [[requirements-analyst-agent]], code generation to the Code Generator Agent, and test creation to the Test Generator Agent. None of that work is absorbed into the orchestrator's own output.

This constraint also simplifies the orchestrator's prompt design. Because it never generates domain content, its system instructions focus entirely on routing logic, validation criteria, context assembly, and [[what are the specific escalation patterns used in production agentic SDLC systems|escalation conditions]] — without the complexity of domain-specific generation. This focused instruction set is also what makes the orchestrator's behavior measurable: when routing and validation are the only functions, each function can be instrumented and traced independently, which is the prerequisite for the delegation success rate, coordination overhead ratio, and error containment metrics defined in [[what metrics distinguish a well-functioning orchestrator from a coordination bottleneck]].

The routing role also has an architectural ceiling. When routing decisions become conditional on runtime agent output — not just fixed role assignments but branching paths based on what a specialist produced — the orchestrator's routing logic may outgrow what can be expressed in prompt instructions alone. This is the point at which [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] becomes relevant: LangGraph's conditional edges provide a first-class implementation surface for complex routing logic that CrewAI's sequential model cannot cleanly express. The routing-not-generating constraint remains in force at that transition; what changes is the implementation substrate for expressing routing decisions. The v2 extension of the routing function — routing across multiple specialist instances by capability profile and current load rather than by role alone — is the design concern addressed in [[specialist capability matching and load balancing is a v2 orchestrator routing enhancement]]; the "routing not generating" constraint holds through that upgrade.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator-first principle applies to an agent defined strictly as coordinator; adding generation duties would change its role and undermine the bootstrapping rationale
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — the four specialists in the minimal set exist precisely because the orchestrator does not perform their functions; role separation is the precondition for specialist specialization
- [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]] — the orchestrator's validation role at handoffs is the mechanism by which lossless transfer is enforced
- [[hybrid sequential-hierarchical orchestration gives predictable flow with dynamic error handling]] — the hybrid architecture pattern assumes an orchestrator whose role is routing; generation duties would collapse the distinction between the manager and specialist layers
- [[hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines]] — the iteration limit is the point at which the orchestrator's "escalate not absorb" behavior triggers; hard limits define when the routing-not-generating role calls for human review rather than continued specialist retries
- [[what are the specific escalation patterns used in production agentic SDLC systems]] — the four trigger categories (confidence threshold, ambiguity detection, irreversibility gate, loop termination) are the specific escalation conditions that form the orchestrator's non-generation instruction set
- [[what metrics distinguish a well-functioning orchestrator from a coordination bottleneck]] — strict role separation (routing and validation only) is the architectural precondition for those four metrics to be unambiguous; an orchestrator that also generates content makes delegation success rate and coordination overhead ratio difficult to isolate and measure
- [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — when routing logic grows complex enough to require runtime-conditional branching, LangGraph's conditional edges are the implementation upgrade for the routing function; the role constraint (no generation) transfers directly across the framework boundary
- [[workflows are preferable to agents for deterministic SDLC phases]] — the orchestrator's routing function is the coordination-layer analog of this principle: deterministic handoff sequencing belongs to the orchestrator, just as deterministic task execution belongs to workflows rather than agents; both patterns enforce the same separation between fixed-path coordination and judgment-intensive work

**Topics:**
- [[agent-registry]]
- [[design-phase]]
