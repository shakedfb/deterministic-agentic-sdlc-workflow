---
description: V1 orchestrator routing assigns tasks to specialist agents by role definition — requirements work goes to the Requirements Analyst, code generation to the Code Generator; v2 routing should extend this to capability matching and current load balancing when multiple specialist instances exist, which is the prerequisite for scaling beyond single-instance specialists.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[orchestrator-agent]]"
classification: open
---

# specialist capability matching and load balancing is a v2 orchestrator routing enhancement

V1 orchestrator routing is role-based: each specialist type handles the corresponding task type. The Requirements Analyst Agent receives requirements tasks; the Code Generator Agent receives code generation tasks. This is simple to implement, simple to debug, and sufficient for single-instance specialist teams within the [[optimal multi-agent team size is 3 to 7 specialized agents]] range.

The limitation of role-based routing appears when the system scales. If a code generation task is large enough to benefit from multiple Code Generator Agent instances working on independent sub-tasks, the v1 orchestrator has no mechanism to route across instances — it knows the role but not which instance is available, capable, or appropriate for the specific task. The same limitation applies when specialist agents have differentiated capabilities: if one Code Generator Agent instance has been fine-tuned for frontend tasks and another for backend tasks, role-based routing cannot exploit this differentiation.

V2 routing addresses this with two enhancements. Capability matching routes tasks based on task characteristics matched against specialist capability profiles: does the task require frontend expertise? Route to the frontend-capable specialist. Does it require security-sensitive code? Route to the agent with the strongest security track record. Load balancing adds a second dimension: among equally capable specialists, route to the one with the shortest current task queue.

Both enhancements require infrastructure that does not exist in v1. Capability matching requires a capability registry that maps specialist instances to their strength profiles, updated as operational data accumulates. Load balancing requires real-time state tracking of each specialist's current task load — which in turn requires the [[observability layer with trace-level instrumentation is required before orchestrator metrics become measurable]] to be operational.

The deferral to v2 is appropriate because single-instance specialist teams — which cover the entire [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — do not require load balancing or capability differentiation. The enhancement becomes necessary only when specialists scale to multiple instances, which should not happen until the single-instance baseline is validated.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[optimal multi-agent team size is 3 to 7 specialized agents]] — multiple instances of the same specialist type push the team above the 7-agent ceiling unless hierarchical structures are introduced; capability matching is one way to maintain the benefits of specialization while managing scale
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — the minimal set uses single instances of each specialist role; v2 capability routing becomes relevant when any specialist role is expanded to multiple instances
- [[observability layer with trace-level instrumentation is required before orchestrator metrics become measurable]] — load balancing requires real-time specialist load data, which only the observability layer can provide; without instrumentation, load balancing cannot be implemented correctly

**Topics:**
- [[agent-registry]]
- [[design-phase]]
