---
description: The four-agent specialist set of requirements analyst, code generator, test generator, and code reviewer covers the entire core build loop and delivers the most value before any deployment or operations agents are added.
topics: ["[[agent-registry]]", "[[development-phase]]", "[[requirements-phase]]", "[[testing-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: closed
---

# the minimal viable agent set for software-building is requirements, code generation, test generation, and code review

The core build loop for software development involves four repeating activities: translating intent into structured specifications, generating implementation from those specifications, creating tests that verify the implementation, and reviewing the generated code before it is committed. These four activities are not arbitrary — they represent the irreducible sequence that takes a human requirement to a tested, reviewable artifact. Any agent system that covers all four can produce working software. Any system that omits one has a gap in its build loop.

Industry adoption patterns confirm this prioritization. When organizations deploy agentic SDLC systems, these four roles appear first because they deliver compounding value: a structured spec makes code generation more accurate, accurate code generation makes test generation more relevant, and automated test generation gives code review something concrete to evaluate. The four agents form a dependency chain where each makes the next more effective.

Deployment and monitoring agents, while valuable, operate on the output of the build loop rather than within it. They can be added in a second iteration once the core loop is validated. Adding them before the build loop is stable introduces operational complexity without addressing the foundational gaps — the system can deploy broken software or monitor processes that were never reliable. The build loop is the prerequisite.

For this vault, this prioritization is the founding scope of the agent catalog. The four specialist profiles — Requirements Analyst Agent, Code Generation Agent, Test Generation Agent, and Code Review Agent — are the first four agents to design after the Orchestrator Agent. Together with the orchestrator, this produces a 5-agent team that sits at the midpoint of the [[optimal multi-agent team size is 3 to 7 specialized agents]] range, confirming that the scope is neither too minimal nor over-engineered.

The constraint also clarifies what to defer. Deployment Orchestrator Agent, Operations Monitoring Agent, and Incident Response Agent are all legitimate candidates for iteration 2, but designing them before the build loop agents is scope creep. The minimal viable set earns the word "viable" precisely because software can be built, tested, and reviewed with just these four specialists — not merely sketched or partially automated.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (lines 27-35)

**Relevant Notes:**
- [[optimal multi-agent team size is 3 to 7 specialized agents]] — a 4-agent specialist set plus orchestrator lands at 5 agents, within the optimal 3–7 range
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator is the prerequisite anchor; the minimal viable specialist set is built on top of it
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — the requirements agent in this set must produce a structured spec artifact to enable the downstream code generation agent
- [[phased rollout prevents coordination chaos when building multi-agent systems]] — this 4-agent set maps directly to Phase 1 and Phase 2 of the recommended phased rollout

**Topics:**
- [[agent-registry]]
- [[development-phase]]
- [[requirements-phase]]
- [[testing-phase]]
