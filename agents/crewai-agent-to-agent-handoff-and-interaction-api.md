---
description: CrewAI provides two distinct handoff mechanisms — sequential task chaining via the context parameter and hierarchical delegation via a manager agent — and the choice between them determines whether agent interaction is data-driven (outputs flow as context) or role-driven (manager assigns work dynamically at runtime).
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[2026-03-01-making-system-operational-and-creating-agents]]"
classification: open
---

# how does CrewAI handle agent-to-agent handoff and what does its interaction API look like

CrewAI implements agent-to-agent handoff through two mechanisms that operate at different levels of the system. Understanding the distinction is a prerequisite for designing interaction patterns in this vault, because the mechanism choice determines how agent profiles translate to running code.

## Mechanism 1: Sequential Task Chaining (Data-Driven Handoff)

The primary handoff primitive is the `context` parameter on the `Task` object. When a task specifies `context=[task_a, task_b]`, it waits for those upstream tasks to complete and receives their outputs as input context before executing.

```python
from crewai import Task, Crew, Process

research_task = Task(
    description="Research CrewAI framework architecture",
    agent=researcher_agent,
    expected_output="A structured summary of CrewAI's core primitives"
)

design_task = Task(
    description="Design agent interaction patterns based on the research",
    agent=architect_agent,
    context=[research_task]  # receives research_task.output as context
)

crew = Crew(
    agents=[researcher_agent, architect_agent],
    tasks=[research_task, design_task],
    process=Process.sequential
)
```

In `Process.sequential` mode (the default), task outputs chain automatically — each task receives the previous task's output. The `context` parameter enables non-sequential dependencies: a downstream task can explicitly pull from any upstream task, not just the immediately preceding one.

Task outputs are structured via `TaskOutput`, which exposes three formats: `raw` (unprocessed string), `pydantic` (validated via a BaseModel), and `json_dict` (dictionary). For agents whose outputs must be parsed by downstream agents, specifying `output_pydantic=YourModel` on the Task enforces a schema contract at the handoff boundary. This schema enforcement is the CrewAI-native implementation of [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]]: the Pydantic contract guarantees that the receiving agent gets a complete, validly-structured context package, not a free-form string that may omit required fields.

Task guardrails provide a validation layer at the handoff point: they intercept output before it passes downstream, can reject it (causing the agent to retry), and can transform it into a normalized form that the receiving agent expects.

## Mechanism 2: Hierarchical Delegation (Role-Driven Handoff)

The second mechanism is the hierarchical process, where a manager agent dynamically assigns tasks to specialist agents at runtime based on their roles and capabilities.

```python
from crewai import Agent, Crew, Process

manager = Agent(
    role="Project Manager",
    goal="Assign tasks to the right specialist and validate their outputs",
    allow_delegation=True,   # required for the manager to delegate
    llm="claude-opus-4-6"
)

crew = Crew(
    agents=[researcher_agent, writer_agent, reviewer_agent],
    tasks=[complex_task],
    manager_agent=manager,
    process=Process.hierarchical
)
```

In hierarchical mode, the manager LLM decides which agent receives which task at runtime, considering agent roles, goals, and available tools. Delegation is disabled by default — it must be explicitly enabled on the manager via `allow_delegation=True`. The `allowed_agents` parameter (added in a recent release) constrains which agents the manager can delegate to, enabling controlled multi-level hierarchies where a sub-manager can only route to its own team members.

The manager evaluates completed outputs and can reject and reassign work, providing a validation loop that does not exist in sequential mode.

## A2A Protocol (Remote Agent Handoff)

CrewAI also implements the A2A (Agent-to-Agent) protocol for inter-process and remote delegation. An agent configured with `A2AClientConfig` can delegate to agents running as separate processes or remote services:

```python
from crewai.a2a import A2AClientConfig

coordinator = Agent(
    role="Research Coordinator",
    goal="Coordinate research across specialist agents",
    a2a=A2AClientConfig(
        endpoint="https://specialist-agent.example.com/.well-known/agent-card.json",
        timeout=120,
        max_turns=10
    )
)
```

A2A uses JSONRPC (default), gRPC, or HTTP+JSON as transport. The LLM on the client agent decides whether to handle a task locally or delegate to a remote A2A endpoint. Structured output from remote agents is optional via Pydantic models.

## Implications for This Vault's Agent Interaction Design

The interaction patterns documented via `interactions:` wiki links in agent profiles correspond directly to CrewAI's task context dependencies:

- `[[requirements-analyst-agent]] → [[code-generator-agent]]` maps to `code_task = Task(context=[requirements_task])`
- A hierarchical crew with a manager orchestrating requirements, code, and review agents maps to `Process.hierarchical` with an orchestrator agent holding `allow_delegation=True`

The choice between sequential and hierarchical mode is a design decision that should be recorded per crew, not per agent. Sequential mode is more predictable and easier to debug; hierarchical mode provides dynamic task routing that suits open-ended workflows where task assignment cannot be predetermined. For SDLC pipelines with known phase boundaries, sequential mode with explicit context dependencies is the lower-risk starting point. For [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]], the sequential mode with explicit context dependencies (requirements_task → code_task → test_task → review_task) is the appropriate starting architecture before introducing hierarchical delegation.

## Recommended CrewAI Configuration for Orchestrator Agents in SDLC Pipelines

The recommended CrewAI configuration for implementing an orchestrator agent in an SDLC pipeline uses `manager_agent` designation combined with `Process.sequential`:

```python
from crewai import Agent, Crew, Process

orchestrator = Agent(
    role="Orchestrator Agent",
    goal="Route work to specialists and validate outputs at handoff boundaries",
    allow_delegation=True,   # enables hierarchical override authority at runtime
    llm="claude-opus-4-6"
)

crew = Crew(
    agents=[requirements_agent, code_agent, test_agent, review_agent],
    tasks=[pipeline_task],
    manager_agent=orchestrator,
    process=Process.sequential  # pipeline-level sequential flow control
)
```

This configuration implements the [[hybrid sequential-hierarchical orchestration gives predictable flow with dynamic error handling]] pattern:

- `manager_agent=orchestrator` gives the orchestrator manager authority for the crew
- `allow_delegation=True` enables runtime routing decisions — the orchestrator can reassign tasks, initiate retries, and escalate exceptions dynamically
- `Process.sequential` maintains pipeline-level sequential flow — phases execute in the designed order under normal conditions

The result: hierarchical override authority (for exceptions and error handling) within a sequential pipeline structure (for predictable happy-path flow). Without `Process.sequential`, the orchestrator becomes a fully hierarchical manager with no built-in phase ordering — less predictable for SDLC pipelines where phase order is architecturally significant.

---

**Source:** [[2026-03-01-making-system-operational-and-creating-agents]] (line 94); enriched from [[orchestrator-agent]]

**Relevant Notes:**
- [[CrewAI aligns best with catalog-driven SDLC agent architectures]] — the framework recommendation that made this question necessary; understanding the handoff API validates whether CrewAI's interaction model matches the vault's wiki-link interaction graph
- [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] — task guardrails and the manager agent's validation loop are the CrewAI-native implementation of human-in-the-loop at handoff boundaries
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — the structured spec artifact produced by requirements agents becomes `TaskOutput` with a Pydantic schema, making the spec machine-parseable at the handoff boundary
- [[specific-escalation-patterns-in-production-agentic-sdlc-systems]] — task guardrails map to confidence threshold escalation; the hierarchical manager agent is the CrewAI implementation surface for inter-agent conflict escalation; the escalation taxonomy from that note maps to specific CrewAI API primitives
- [[hybrid sequential-hierarchical orchestration gives predictable flow with dynamic error handling]] — the architectural pattern that this CrewAI configuration implements; `manager_agent` + `Process.sequential` + `allow_delegation=True` is the concrete implementation
- [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]] — `TaskOutput` with Pydantic schema enforcement is the CrewAI API implementation of lossless transfer; the `context` parameter is how the orchestrator assembles and passes the complete context package to receiving agents
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — the `manager_agent=orchestrator` configuration directly instantiates the orchestrator-first principle in code; the manager agent is the coordination layer that must exist before specialists can form a functional crew
- [[when should LangGraph be chosen over CrewAI for an SDLC agent team]] — when sequential and hierarchical modes are insufficient (complex conditional routing at runtime), LangGraph wraps CrewAI agents; the handoff patterns documented here — context parameter, TaskOutput schema — must migrate to LangGraph's state management when that transition occurs
- [[can GitHub Spec Kit format be adopted as the canonical spec artifact format for this vault]] — the spec artifact (requirements.md with EARS syntax) becomes a Pydantic-validated `TaskOutput` at the requirements → code generation handoff boundary; the spec format decision and the handoff schema contract are coupled

**Topics:**
- [[agent-registry]]
- [[design-phase]]
