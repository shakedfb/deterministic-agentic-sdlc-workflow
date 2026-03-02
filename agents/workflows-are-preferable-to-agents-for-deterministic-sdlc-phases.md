---
description: Predefined workflow code paths outperform agents for SDLC phases where the task is well-defined and consistency matters more than judgment, making the agent-vs-workflow distinction a prerequisite design decision for every phase of an AI-assisted SDLC pipeline.
topics: ["[[agent-registry]]", "[[design-phase]]", "[[deployment-phase]]", "[[operations-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: closed
---

# workflows are preferable to agents for deterministic SDLC phases

Not every SDLC phase requires an agent. The distinction between a workflow and an agent is not a matter of implementation convenience — it is a design decision that determines correctness, predictability, and debuggability of the system.

An agent is appropriate when the task requires judgment: interpreting ambiguous requirements, evaluating code quality against unstated criteria, or deciding which of several remediation paths is most appropriate for a given error. Agents bring flexibility and contextual reasoning to problems where the right output cannot be fully specified in advance. That flexibility has a cost — agents can hallucinate, drift from intent, or produce inconsistent results across identical inputs.

A workflow is appropriate when the task is deterministic: linting, formatting checks, dependency version scanning, deployment pipeline triggers, or any process where the correct behavior is fully specifiable as a predefined code path. These tasks do not benefit from an agent's flexibility. They actively suffer from it. A linting step that reasons about whether to apply a rule is worse than a linter that applies it consistently. A deployment trigger that judges whether conditions are met is less reliable than a deployment gate with explicit pass/fail criteria.

The practical implication is that the catalog should distinguish between agent profiles and workflow definitions. The six SDLC phases are not uniformly agentic. Requirements analysis is fundamentally a judgment task — an agent is appropriate. Code linting is deterministic — a workflow is appropriate. Code review occupies a middle ground where automated pattern detection is a workflow and qualitative evaluation is an agent concern. Conflating these is a common source of over-engineering: building agents to do what shell scripts do, then wondering why the system is fragile.

This distinction also connects to testability. Workflows are deterministic and therefore straightforwardly testable. Given input X, the workflow must produce output Y. Agents are probabilistic and require evaluation frameworks, test sets, and success metrics rather than simple input/output assertions. The debugging cost of an agent failure is substantially higher than a workflow failure. Defaulting to agents when workflows suffice multiplies debugging surface without adding value.

The design question before building any component in this vault is explicit: is judgment required, or is this deterministic enough for a workflow? If the answer is workflow, do not build an agent. The catalog documents agents. Workflows are implementation details that support agents but are not themselves agents. This creates a three-way decision tree in practice: deterministic → workflow; role-sequential with predictable handoffs → [[CrewAI aligns best with catalog-driven SDLC agent architectures]]; branching or cyclic with runtime-conditional execution → LangGraph.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (lines 52-56)

**Relevant Notes:**
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — the four-agent set covers the judgment-intensive phases of the build loop; the surrounding mechanical tasks (linting, deployment triggers) are workflow territory
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — the spec itself enables deterministic validation workflows downstream; once a spec exists, checklist verification is a workflow, not an agent task
- [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] — high-stakes handoffs are agent-mediated judgment calls; lower-stakes transitions between phases can be workflow-gated without human or agent involvement

**Topics:**
- [[agent-registry]]
- [[design-phase]]
- [[deployment-phase]]
- [[operations-phase]]
