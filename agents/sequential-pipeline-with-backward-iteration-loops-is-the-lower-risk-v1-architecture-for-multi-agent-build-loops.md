---
description: A sequential pipeline that processes SDLC phases in fixed order, combined with explicit backward iteration loops within each phase, is the lower-risk first architecture for multi-agent build loops — it delivers predictability and debuggability before parallel execution or hierarchical delegation are introduced.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[orchestrator-agent]]"
classification: closed
---

# sequential pipeline with backward iteration loops is the lower-risk v1 architecture for multi-agent build loops

The simplest architecture that works is the right starting point for multi-agent build loops. A sequential pipeline processes SDLC phases in a fixed order — requirements first, then code generation, then test generation, then code review — with each phase receiving the output of the previous one. This is not an oversimplification: for v1 systems where the interaction contracts between agents are still being validated, sequentialism's primary benefit is that failures are attributable. When something goes wrong, there is exactly one candidate: the phase that just ran. This attributability depends on [[the orchestrator agents role is routing and validation not content generation]] being honored: when the orchestrator routes rather than generates, a failure at any phase belongs to the specialist, not to a hybrid of orchestrator + specialist actions that cannot be disentangled.

The "backward iteration loop" qualifier is critical. Sequential does not mean no retries. Within each phase, the orchestrator may loop backward — returning failed output to the specialist for a second or third attempt before proceeding downstream. A code generation agent that produces output failing the orchestrator's validation check gets the task back with the failure context attached. This loop is bounded (see [[hard iteration limits per task are required to prevent runaway loops in multi-agent pipelines]]), but it is a deliberate part of the sequential architecture rather than a violation of it. Each backward loop that exhausts its retry count triggers a loop termination escalation (see [[what are the specific escalation patterns used in production agentic SDLC systems]]) — the backward iteration mechanism and the escalation taxonomy are operationally coupled.

The risk calculus that makes sequential the v1 choice involves two comparisons. Against hierarchical-only: pure hierarchical delegation requires the manager agent to reason dynamically about task assignment, capability matching, and load balancing — adding orchestrator complexity before the specialist interactions are validated. Against parallel execution: running independent tasks concurrently requires dependency graph analysis to confirm independence before the fanout (see [[parallel task execution requires dependency graph analysis and is a v2 concern for SDLC pipelines]]); doing this incorrectly produces racing conditions and corrupted handoff context. Sequential avoids both problems by deferring them.

The tradeoff is explicit: sequential processing serializes work that could theoretically run in parallel, increasing wall-clock time. This is the [[sequential pipeline predictability and parallel execution efficiency are in direct tension for SDLC build loops]] tension, and for v1 it resolves toward predictability. The time cost of serialism is lower than the debugging cost of parallel coordination failures before the system is proven.

The sequential pipeline is the architecture that [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] prepares the orchestrator to run. Building the orchestrator before any specialist is necessary precisely because the sequential pipeline requires a coordination layer to sequence phases, assemble context packages at each handoff, and enforce the iteration limits that keep backward loops bounded. Without the orchestrator in place first, there is no executor for the sequential flow.

CrewAI's `Process.sequential` mode implements this pattern natively. The recommended path is to validate the entire phase sequence in sequential mode before introducing `Process.hierarchical` for dynamic routing — the combination of both is what [[hybrid sequential-hierarchical orchestration gives predictable flow with dynamic error handling]] describes as the next-phase architecture upgrade.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[single-task-per-invocation-is-the-correct-scope-discipline-for-reliable-code-generation-agents]] — single-task invocation at the specialist level is the implementation complement of the sequential pipeline at the orchestrator level; both enforce narrow, bounded scopes that make failure attribution possible
- [[how does CrewAI handle agent-to-agent handoff and what does its interaction API look like]] — sequential pipeline maps to `Process.sequential` with explicit context dependencies; this is the specific CrewAI configuration for v1 SDLC pipelines
- [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — when backward iteration loops become conditional branching at runtime, LangGraph's conditional edge model becomes necessary; sequential CrewAI is the precursor that reveals whether that complexity is required
- [[phased rollout prevents coordination chaos when building multi-agent systems]] — phased rollout follows a sequential logic analogous to the sequential pipeline: each phase is validated before the next is introduced
- [[parallel task execution requires dependency graph analysis and is a v2 concern for SDLC pipelines]] — the parallel execution upgrade path that sequential v1 defers
- [[sequential pipeline predictability and parallel execution efficiency are in direct tension for SDLC build loops]] — the explicit tension this architecture embodies and resolves toward predictability
- [[hybrid sequential-hierarchical orchestration gives predictable flow with dynamic error handling]] — the v1.5 architecture that extends the sequential baseline with hierarchical override authority; the sequential pipeline is the substrate on which the hybrid pattern builds
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator must exist before the sequential pipeline can run; bootstrapping first is the prerequisite for sequential sequencing, context assembly, and iteration limit enforcement
- [[the orchestrator agents role is routing and validation not content generation]] — the routing-not-generating constraint is what makes the sequential pipeline's failure attribution work: a pure coordinator cannot corrupt phase output, so failures remain attributable to the specialist that ran
- [[what are the specific escalation patterns used in production agentic SDLC systems]] — the backward iteration loops in the sequential pipeline are the operational mechanism that generates loop termination escalations; the two notes are mechanistically coupled at the phase-retry boundary

**Topics:**
- [[agent-registry]]
- [[design-phase]]
