---
description: Limiting a code generation agent to exactly one task per invocation produces more reliable output than multi-task batch generation because it keeps implementation scope narrow, makes failures diagnosable at the task level, and enables fast iteration without re-running the full batch.
topics: ["[[agent-registry]]", "[[development-phase]]"]
source: "[[code-generator-agent]]"
classification: closed
---

# single-task-per-invocation is the correct scope discipline for reliable code generation agents

Limiting a code generation agent to exactly one task per invocation is a deliberate architectural choice, not a performance constraint. Multi-task batch generation compounds failure modes: when a batch of three tasks partially fails, it is unclear whether task 2's failure caused task 3's failure, whether both failed independently, or whether the context window was degraded by the time the agent reached task 3. Diagnosing this requires re-running combinations of tasks, which is more expensive than running tasks individually in the first place.

Single-task invocation eliminates this diagnostic ambiguity. Each invocation has one scope, one output, and one failure mode. If the task fails self-check, the failure is attributed to that task — not to an interaction between tasks. The Orchestrator can retry the specific failing task without re-running the tasks that succeeded. Iteration is fast because the unit of work is minimal.

The orchestrator manages sequencing. The code generator manages focused execution. This division of responsibility is the specialist-side complement of sequential pipeline architecture: the pipeline is sequential precisely so that each specialist operates on a well-defined, bounded scope. Single-task invocation enforces that bound at the code generator level, making the pipeline's sequential invariant enforceable in practice.

The constraint also enables per-task hard iteration limits, which are required to prevent runaway autonomous loops in multi-agent pipelines. A limit of "3 attempts per task" is only meaningful when a task is a single unit of work. If tasks are batched, "3 attempts" could mean 3 attempts at 10 different tasks, which is operationally indistinguishable from unlimited iteration.

---

**Source:** [[code-generator-agent]]

**Relevant Notes:**
- [[sequential-pipeline-with-backward-iteration-loops-is-the-lower-risk-v1-architecture-for-multi-agent-build-loops]] — single-task invocation is the specialist-side complement of sequential pipeline architecture; the pipeline is sequential so each specialist operates on a well-defined scope, and single-task invocation enforces that scope at the code generator level
- [[hard-iteration-limits-per-task-are-required-to-prevent-runaway-loops-in-multi-agent-pipelines]] — single-task scope makes per-task iteration limits enforceable; without single-task invocation, per-task limits cannot be meaningfully applied
- [[the-orchestrator-agents-role-is-routing-and-validation-not-content-generation]] — task sequencing is the orchestrator's responsibility; single-task invocation at the code generator level is only viable because the orchestrator manages the full sequence and can target retries at specific failing tasks
- [[the-implementation-report-is-the-structured-handoff-artifact-that-enables-orchestrator-routing-decisions-after-code-generation]] — single-task invocation produces one IMPLEMENTATION REPORT per task, giving the orchestrator a clean per-task signal for routing decisions; batched invocation would produce a combined report that is harder to parse for individual task routing
- [[spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems]] — single-task invocation works because the spec provides the ground truth; the agent needs only the task assignment and the spec to produce its output, so there is no context accumulation benefit from batching tasks together

**Topics:**
- [[agent-registry]]
- [[development-phase]]
