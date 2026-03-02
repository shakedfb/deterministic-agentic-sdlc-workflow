---
claim: "how does CrewAI handle agent-to-agent handoff and what does its interaction API look like"
classification: open
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 014: how does CrewAI handle agent-to-agent handoff and what does its interaction API look like

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (line 94)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is an OPEN claim (open question / research direction).

Rationale: Given that claim 005 recommends CrewAI for this vault's architecture, understanding its handoff API is a prerequisite for designing the interaction patterns between agents. This is a practical implementation question needed before building any multi-agent interaction in CrewAI. Fits extraction category "interaction patterns" (open question variant).

Semantic neighbor: null — connects to claim 005 (CrewAI recommendation) and claim 008 (human supervision at handoff points).

---

## Create

Created: `agents/crewai-agent-to-agent-handoff-and-interaction-api.md`

Note title: how does CrewAI handle agent-to-agent handoff and what does its interaction API look like
Path: agents/crewai-agent-to-agent-handoff-and-interaction-api.md
Word count: ~750 words (body)
Status: complete

Key content:
- Documents two primary handoff mechanisms: sequential task chaining via the `context` parameter (data-driven) and hierarchical delegation via a manager agent (role-driven)
- Explains TaskOutput structure (raw, pydantic, json_dict) and how output_pydantic enforces schema contracts at handoff boundaries
- Documents task guardrails as a validation/transformation layer at handoff points
- Covers hierarchical process API: allow_delegation flag, manager_agent parameter, allowed_agents for controlled delegation, Process.hierarchical vs Process.sequential
- Documents A2A protocol for remote agent delegation with A2AClientConfig
- Maps vault wiki-link interaction patterns to CrewAI task context dependencies
- Recommends sequential mode with explicit context dependencies as the lower-risk starting point for SDLC pipelines with known phase boundaries
- Connects to: [[CrewAI aligns best with catalog-driven SDLC agent architectures]], [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]], [[spec-centric architecture is the most reliable pattern for agents building systems]]

## /map

Completed: 2026-03-02

**Phase overview MOC updated:**
- Added to [[design-phase]] Core Ideas section

**New connection added:**
- -> [[what are the specific escalation patterns used in production agentic SDLC systems]] — extends: task guardrails map to confidence threshold escalation; hierarchical manager maps to inter-agent conflict escalation; the escalation taxonomy maps to specific CrewAI API primitives

**Existing connections reviewed:**
- [[CrewAI aligns best with catalog-driven SDLC agent architectures]], [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]], [[spec-centric architecture is the most reliable pattern for agents building systems]] — all well-articulated

**Articulation test:** PASS

**Discovery trace:**
- Phase overview read: [[design-phase]]
- specific-escalation-patterns (015) is the natural extension: the two notes together provide both the escalation taxonomy and the CrewAI API surface where each trigger type is implemented

## /refine
(to be filled by /refine phase)

## /validate
(to be filled by /validate phase)
