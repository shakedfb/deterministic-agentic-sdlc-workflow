---
description: Production agentic SDLC systems are human-supervised automation, not fully autonomous pipelines — agents handle detection, analysis, and planning, but high-stakes actions require explicit human sign-off, making escalation design a structural requirement in every agent profile.
topics: ["[[agent-registry]]", "[[design-phase]]", "[[operations-phase]]", "[[deployment-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: closed
---

# agentic SDLC systems require explicit human supervision at high-stakes handoff points

Agentic SDLC systems are not fully autonomous. This is not a limitation to be engineered away — it is a design constraint that reflects the current state of agent reliability and the consequences of failure in production systems. The correct mental model is human-supervised automation: agents perform the detection, analysis, and planning work that would otherwise require human time, but the authorization to take high-stakes actions remains with a human.

The failure mode of treating agents as fully autonomous is not hypothetical. When agents make deployment decisions, security changes, or architectural modifications without human oversight, errors compound silently until a failure occurs that is expensive to reverse. A requirements agent that misinterprets scope and a code generation agent that produces plausible but incorrect implementation can both operate confidently within their designed parameters — the error is in the handoff contract between their outputs and production consequences, not in any individual agent's behavior. Human supervision at the right points catches these compounding failures before they reach irreversible states.

The design implication is structural: every agent profile must specify its escalation conditions — the circumstances under which the agent stops, surfaces its work, and waits for human authorization before proceeding. These are not edge cases to handle later; they are first-class design requirements. An agent profile without explicit escalation conditions is an incomplete design, because it does not specify the boundaries of the agent's authority.

Escalation conditions vary by phase and action type. A requirements agent should escalate when scope is ambiguous beyond a defined threshold — the human who stated the requirement must resolve the ambiguity before code generation begins. A deployment agent should escalate before any action that modifies production state. A code review agent can operate autonomously for standard patterns but should escalate when it identifies changes to security boundaries, authentication logic, or data access controls. The specific thresholds depend on the system's risk tolerance, but the requirement to define them does not.

This also connects to the phased rollout pattern from [[phased rollout prevents coordination chaos when building multi-agent systems]]: Phase 1 deliberately uses manual code review rather than an automated agent. That is not a temporary shortcut — it is an intentional human supervision checkpoint while the upstream agents are stabilizing. Supervision is built into the rollout sequence, not added after the fact.

The catalog-level implication is that `escalation_conditions` should be treated as a required field in every agent profile, not an optional annotation. If an agent profile does not specify when it escalates, the design is missing a critical constraint. The absence of that field is not a sign that the agent operates without limits — it is a sign that the limits have not been thought through.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (lines 66-70)

**Relevant Notes:**
- [[phased rollout prevents coordination chaos when building multi-agent systems]] — the phased rollout deliberately uses human review checkpoints at each phase boundary; supervision is a structural feature of the rollout sequence, not an afterthought
- [[agent profiles must include escalation conditions as a required design field]] — the operational consequence of this constraint: escalation conditions must be a required schema field, not an optional one
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator is the natural escalation routing layer; it receives agent signals and determines whether to proceed autonomously or surface to a human
- [[workflows are preferable to agents for deterministic SDLC phases]] — the agent-vs-workflow distinction overlaps with the supervision question: deterministic workflow phases can be gated without human involvement; agent-mediated judgment phases are where supervision conditions matter most
- [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — LangGraph's conditional edge model enables encoding supervision gates as first-class graph nodes; the framework choice has direct implications for how human supervision checkpoints are implemented in the execution graph

**Topics:**
- [[agent-registry]]
- [[design-phase]]
- [[operations-phase]]
- [[deployment-phase]]
