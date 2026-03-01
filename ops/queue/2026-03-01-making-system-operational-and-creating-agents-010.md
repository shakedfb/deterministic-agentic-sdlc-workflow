---
claim: "agent profile framework field should capture both orchestration framework and base model"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 010: agent profile framework field should capture both orchestration framework and base model

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 74-76)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim (implementation idea / schema design decision).

Rationale: The source explicitly calls out an implication for the vault's `framework` field — it should record both the orchestration framework (CrewAI, LangGraph) AND the target base model (GPT-4o, Claude Opus). This is an actionable schema enhancement that prevents losing model selection context. Fits extraction category "agent design patterns" (schema design). Implementation idea that changes the agent profile template.

Semantic neighbor: null — no schema design note exists yet.

---

## Create
(to be filled by create phase)

## /map
(to be filled by /map phase)

## /refine
(to be filled by /refine phase)

## /validate
(to be filled by /validate phase)
