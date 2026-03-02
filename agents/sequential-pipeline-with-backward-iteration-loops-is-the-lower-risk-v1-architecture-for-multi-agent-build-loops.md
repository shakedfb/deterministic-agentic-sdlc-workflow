---
description: A sequential pipeline that processes SDLC phases in fixed order, combined with explicit backward iteration loops within each phase, is the lower-risk first architecture for multi-agent build loops — it delivers predictability and debuggability before parallel execution or hierarchical delegation are introduced.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[orchestrator-agent]]"
classification: closed
---

# sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops

The simplest architecture that works is the right starting point for multi-agent build loops. A sequential pipeline processes SDLC phases in a fixed order — requirements first, then code generation, then test generation, then code review — with each phase receiving the output of the previous one. This is not an oversimplification: for v1 systems where the interaction contracts between agents are still being validated, sequentialism's primary benefit is that failures are attributable. When something goes wrong, there is exactly one candidate: the phase that just ran.

The "backward iteration loop" qualifier is critical. Sequential does not mean no retries. Within each phase, the orchestrator may loop backward — returning failed output to the specialist for a second or third attempt before proceeding downstream. A code generation agent that produces output failing the orchestrator's validation check gets the task back with the failure context attached. This loop is bounded (see [[hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines]]), but it is a deliberate part of the sequential architecture rather than a violation of it.

The risk calculus that makes sequential the v1 choice involves two comparisons. Against hierarchical-only: pure hierarchical delegation requires the manager agent to reason dynamically about task assignment, capability matching, and load balancing — adding orchestrator complexity before the specialist interactions are validated. Against parallel execution: running independent tasks concurrently requires dependency graph analysis to confirm independence before the fanout (see [[parallel task execution requires dependency graph analysis and is a v2 concern for SDLC pipelines]]); doing this incorrectly produces racing conditions and corrupted handoff context. Sequential avoids both problems by deferring them.

The tradeoff is explicit: sequential processing serializes work that could theoretically run in parallel, increasing wall-clock time. This is the [[sequential pipeline predictability and parallel execution efficiency are in direct tension for SDLC build loops]] tension, and for v1 it resolves toward predictability. The time cost of serialism is lower than the debugging cost of parallel coordination failures before the system is proven.

CrewAI's `Process.sequential` mode implements this pattern natively. The recommended path is to validate the entire phase sequence in sequential mode before introducing `Process.hierarchical` for dynamic routing.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[how does CrewAI handle agent-to-agent handoff and what does its interaction API look like]] — sequential pipeline maps to `Process.sequential` with explicit context dependencies; this is the specific CrewAI configuration for v1 SDLC pipelines
- [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — when backward iteration loops become conditional branching at runtime, LangGraph's conditional edge model becomes necessary; sequential CrewAI is the precursor that reveals whether that complexity is required
- [[phased rollout prevents coordination chaos when building multi-agent systems]] — phased rollout follows a sequential logic analogous to the sequential pipeline: each phase is validated before the next is introduced
- [[parallel task execution requires dependency graph analysis and is a v2 concern for SDLC pipelines]] — the parallel execution upgrade path that sequential v1 defers
- [[sequential pipeline predictability and parallel execution efficiency are in direct tension for SDLC build loops]] — the explicit tension this architecture embodies and resolves toward predictability

**Topics:**
- [[agent-registry]]
- [[design-phase]]
