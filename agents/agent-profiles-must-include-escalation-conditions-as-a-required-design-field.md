---
description: Every agent profile must explicitly define its escalation conditions — the circumstances under which it stops, surfaces its work, and waits for human authorization — making `escalation_conditions` a required schema field because an agent profile without it is an incomplete design that leaves the agent's authority boundaries undefined.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: closed
---

# agent profiles must include escalation conditions as a required design field

The current agent profile schema has a structural gap: it documents what agents do, but not when they stop. Without explicit escalation conditions, an agent profile specifies the agent's capabilities and interactions while leaving its authority boundaries undefined. That is an incomplete design.

The gap matters in practice. An agent that knows how to perform its task but does not know when to escalate is an agent that will either fail silently — continuing to operate past the point where human judgment is required — or fail noisily by halting without a defined protocol. Both failure modes are worse than the alternative: explicitly specifying, at design time, the conditions under which the agent surfaces its work and waits for human authorization before proceeding.

Escalation conditions are not edge cases to be added after the core design is stable. They are a core design requirement with the same standing as the agent's responsibilities, inputs, and outputs. The reason is structural: the SDLC workflow depends on agents operating within their intended scope. When an agent's scope ends — when it reaches ambiguity it cannot resolve, a risk threshold it should not cross autonomously, or a decision it lacks authority to make — it must have a defined path to human oversight. The absence of that path is not neutral; it means the agent either invents its own boundaries (unreliable) or defers to implicit conventions (invisible and unenforced).

The schema amendment is therefore not an optional enhancement but a completeness requirement. Every agent profile should include an `escalation_conditions` field as a required entry, alongside the existing required fields. The format should document at minimum:

- **Ambiguity thresholds**: at what point does the agent stop trying to resolve uncertainty and escalate for clarification (e.g., scope ambiguity beyond a defined threshold for a requirements agent)
- **Risk thresholds**: what actions or outputs trigger mandatory human review before proceeding (e.g., any modification to production state for a deployment agent)
- **Confidence thresholds**: when the agent's own output confidence drops below an acceptable level for its role (e.g., a code review agent flagging security boundary changes it cannot fully evaluate)

The escalation conditions field also has a validation consequence. Schema validation that checks for completeness of required fields already catches missing descriptions, missing metrics, or missing interaction links. Adding `escalation_conditions` to the required set means that incomplete escalation design is surfaced at the same time as other schema gaps — before the agent reaches testing, not after it fails in deployment.

This is the operational counterpart to the structural claim in [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]]. That note establishes why supervision is a design requirement. This note establishes where in the schema that requirement must be enforced.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (lines 68-70)

**Relevant Notes:**
- [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] — the structural argument for why supervision is a first-class design constraint, of which this schema amendment is the direct operational consequence
- [[phased rollout prevents coordination chaos when building multi-agent systems]] — the phased rollout builds human review checkpoints into each phase boundary; those checkpoints are the escalation conditions at the system level, and per-agent escalation conditions are their granular implementation
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the orchestrator is the natural routing layer for escalation signals from specialist agents; escalation conditions at the specialist level feed into the orchestrator's supervision protocol
- [[agent profile framework field should capture both orchestration framework and base model]] — a parallel schema completeness argument: just as model selection is a required undocumented design decision, escalation conditions are a required undocumented operational boundary
- [[specific-escalation-patterns-in-production-agentic-sdlc-systems]] — provides the specific taxonomy (confidence threshold, ambiguity detection, irreversibility gate, loop termination) and governance models (HITL/HOTL) that populate the `escalation_conditions` field with actionable content rather than placeholders
- [[requirements-analyst-agent]] — the Requirements Analyst Agent is the first concrete implementation of escalation conditions in the vault; its four explicit escalation triggers (scope ambiguity, implied security constraints, system overlap, irreversible data model decisions) demonstrate how `escalation_conditions` translates from schema requirement to prompt design

**Topics:**
- [[agent-registry]]
- [[design-phase]]
