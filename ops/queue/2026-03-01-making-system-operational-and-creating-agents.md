---
id: 2026-03-01-making-system-operational-and-creating-agents
type: extract
source: ops/queue/archive/2026-03-01-making-system-operational-and-creating-agents/2026-03-01-making-system-operational-and-creating-agents.md
original_path: design-ideas/2026-03-01-making-system-operational-and-creating-agents.md
archive_folder: ops/queue/archive/2026-03-01-making-system-operational-and-creating-agents
created: 2026-03-01T00:00:00Z
next_claim_start: 1
---

# Extract agent profiles from 2026-03-01-making-system-operational-and-creating-agents

## Source
Original: design-ideas/2026-03-01-making-system-operational-and-creating-agents.md
Archived: ops/queue/archive/2026-03-01-making-system-operational-and-creating-agents/2026-03-01-making-system-operational-and-creating-agents.md
Size: 98 lines
Content type: Research synthesis / web-search findings on bootstrapping a multi-agent SDLC development team

## Scope
Full document

## Acceptance Criteria
- Extract agent design patterns, interaction patterns, workflow bottlenecks, and metrics that matter
- Duplicate check against agents/ during extraction
- Near-duplicates create enrichment tasks (do not skip)
- Each output type gets appropriate handling

## Execution Notes

Processed 2026-03-01. Source: 98-line research synthesis on bootstrapping multi-agent SDLC teams (web-search, domain-relevant).

Extraction approach: comprehensive (domain-relevant source, moderate selectivity config). No existing agent profiles to check for duplicates — vault is fresh. Semantic search unavailable (no qmd/vector search configured). Used structural analysis and claim categorization.

Yield: 18 claims extracted (9 core domain claims, 3 implementation ideas, 6 open questions). 0 skipped. 0 enrichments (no existing notes to enrich). Skip rate: 0% — appropriate for a fresh domain-relevant source.

Queue format note: queue.yaml used (not queue.json as referenced in reduce skill). Updated queue.yaml directly.

Process note: Task tool not available in lead session — extraction executed inline rather than via subagent. Flagged in final ralph report.

## Outputs

Claims created (001-012, closed):
- 001: orchestrator-first bootstrapping reduces multi-agent coordination failures
- 002: optimal multi-agent team size is 3 to 7 specialized agents
- 003: the minimal viable agent set for software-building is requirements, code generation, test generation, and code review
- 004: spec-centric architecture is the most reliable pattern for agents building systems
- 005: CrewAI aligns best with catalog-driven SDLC agent architectures
- 006: workflows are preferable to agents for deterministic SDLC phases
- 007: phased rollout prevents coordination chaos when building multi-agent systems
- 008: agentic SDLC systems require explicit human supervision at high-stakes handoff points
- 009: base model quality matters more than framework choice for agent capability
- 010: agent profile framework field should capture both orchestration framework and base model
- 011: agent profiles must include escalation conditions as a required design field
- 012: requirements agents must produce a structured spec artifact not just prose notes

Open questions created (013-018, open):
- 013: what does a minimum viable Requirements Analyst Agent prompt look like and how does it produce a structured spec
- 014: how does CrewAI handle agent-to-agent handoff and what does its interaction API look like
- 015: what are the specific escalation patterns used in production agentic SDLC systems
- 016: can GitHub Spec Kit format be adopted as the canonical spec artifact format for this vault
- 017: what metrics distinguish a well-functioning orchestrator from a coordination bottleneck
- 018: when should LangGraph be chosen over CrewAI for an SDLC agent team

All task files created in ops/queue/. Queue updated (extract task marked done, 18 claim entries added at current_phase: create).
