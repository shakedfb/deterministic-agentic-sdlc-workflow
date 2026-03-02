---
claim: "base model quality matters more than framework choice for agent capability"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 009: base model quality matters more than framework choice for agent capability

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 72-76)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim.

Rationale: The source argues that a reliable foundation model (GPT-4o, Claude Opus, or capable reasoning model) is the primary determinant of agent capability — agents on weak base models fail at planning and context retention regardless of framework sophistication. This is a priority-ordering claim (model > framework) with clear implications for the vault's `framework` field design. Fits extraction category "metrics that matter."

Semantic neighbor: null — no base model selection note exists.

---

## Create

Created: [[base-model-quality-matters-more-than-framework-choice-for-agent-capability]]

**Core argument:** A capable foundation model (GPT-4o, Claude Opus, or equivalent reasoning tier) is the primary determinant of agent capability. Agents on weak base models fail at planning and context retention regardless of framework sophistication — the framework is scaffolding; the model is the load-bearing element.

**Key design implication:** Model selection is a first-order design decision of equal weight to framework selection. The `framework` field in agent profiles must capture both the orchestration framework and the target base model. An agent profile missing the base model spec is missing a critical implementation parameter.

**Relevant Notes:**
- [[agent profile framework field should capture both orchestration framework and base model]] — direct schema consequence
- [[CrewAI aligns best with catalog-driven SDLC agent architectures]] — framework decision is downstream of model selection
- [[orchestrator-first bootstrapping reduces multi-agent coordination failures]] — orchestrator carries the highest reasoning load; its model selection is the most consequential
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — requirements analysis and code review are most demanding for base model reasoning

**Topics assigned:** [[agent-registry]], [[design-phase]]

## /map
(to be filled by /map phase)

## /refine
(to be filled by /refine phase)

## /validate
(to be filled by /validate phase)
