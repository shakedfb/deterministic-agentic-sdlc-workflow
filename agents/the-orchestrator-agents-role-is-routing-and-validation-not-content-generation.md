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

The distinction between routing and generating is the clearest test of whether a system has an orchestrator or a super-agent. A super-agent absorbs tasks when specialists struggle; an orchestrator escalates when specialists reach their limits. For SDLC pipelines, this translates directly: the Orchestrator Agent routes requirements analysis work to the [[requirements-analyst-agent]], code generation to the Code Generator Agent, and test creation to the Test Generator Agent. None of that work is absorbed into the orchestrator's own output.

This constraint also simplifies the orchestrator's prompt design. Because it never generates domain content, its system instructions focus entirely on routing logic, validation criteria, context assembly, and escalation conditions — without the complexity of domain-specific generation.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator-first principle applies to an agent defined strictly as coordinator; adding generation duties would change its role and undermine the bootstrapping rationale
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — the four specialists in the minimal set exist precisely because the orchestrator does not perform their functions; role separation is the precondition for specialist specialization
- [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]] — the orchestrator's validation role at handoffs is the mechanism by which lossless transfer is enforced
- [[hybrid sequential-hierarchical orchestration gives predictable flow with dynamic error handling]] — the hybrid architecture pattern assumes an orchestrator whose role is routing; generation duties would collapse the distinction between the manager and specialist layers

**Topics:**
- [[agent-registry]]
- [[design-phase]]
