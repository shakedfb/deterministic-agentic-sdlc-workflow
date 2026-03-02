---
batch: 2026-03-01-making-system-operational-and-creating-agents
source: design-ideas/2026-03-01-making-system-operational-and-creating-agents.md
archived: 2026-03-01
agent_profiles_created: 18
enrichments: 0
status: complete
---

# Batch Summary: Making the System Operational and Creating Agents

## Source

- **File:** `design-ideas/2026-03-01-making-system-operational-and-creating-agents.md`
- **Type:** Web-search research synthesis
- **Size:** 98 lines
- **Content:** 9 key findings covering bootstrapping a multi-agent SDLC team — architecture patterns, framework choices, team sizing, phased rollout strategies, and 6 open research questions

## Extraction Results

- **Agent profiles extracted:** 18
- **Closed claims (established findings):** 12
- **Open questions (research directions):** 6
- **Enrichments:** 0 (vault was empty at processing time — no existing notes to enrich)

## Agent Profiles Created

### Closed Claims (Established Findings)

1. [[orchestrator-first-bootstrapping-reduces-multi-agent-coordination-failures]]
2. [[optimal-multi-agent-team-size-is-3-to-7-specialized-agents]]
3. [[the-minimal-viable-agent-set-for-software-building-is-requirements-code-generation-test-generation-and-code-review]]
4. [[spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems]]
5. [[crewai-aligns-best-with-catalog-driven-sdlc-agent-architectures]]
6. [[workflows-are-preferable-to-agents-for-deterministic-sdlc-phases]]
7. [[phased-rollout-prevents-coordination-chaos-when-building-multi-agent-systems]]
8. [[agentic-sdlc-systems-require-explicit-human-supervision-at-high-stakes-handoff-points]]
9. [[base-model-quality-matters-more-than-framework-choice-for-agent-capability]]
10. [[agent-profile-framework-field-should-capture-both-orchestration-framework-and-base-model]]
11. [[agent-profiles-must-include-escalation-conditions-as-a-required-design-field]]
12. [[requirements-agents-must-produce-a-structured-spec-artifact-not-just-prose-notes]]

### Open Questions (Research Directions)

13. [[requirements-analyst-agent]] — minimum viable prompt + full agent profile
14. [[crewai-agent-to-agent-handoff-and-interaction-api]]
15. [[specific-escalation-patterns-in-production-agentic-sdlc-systems]]
16. [[can-github-spec-kit-format-be-adopted-as-the-canonical-spec-artifact-format-for-this-vault]]
17. [[what-metrics-distinguish-a-well-functioning-orchestrator-from-a-coordination-bottleneck]]
18. [[when-should-langgraph-be-chosen-over-crewai-for-an-sdlc-agent-team]]

## Processing Metrics

- **Connections added (reflect phase):** 13 new cross-links between agent profile notes
- **Phase MOCs updated:** 6 (design-phase, requirements-phase, development-phase, testing-phase, deployment-phase, operations-phase)
- **Backward links added (reweave phase):** 14 agent profiles updated
- **Dangling links fixed (verify phase):** 9
- **Misplaced files cleaned up:** 4 numbered duplicate files deleted from agents/
- **All verify checks:** PASS (18/18)

## Notable Learnings

- **[Surprise]:** The open-questions cluster (claims 013-018) produced implementation-ready content richer than the closed claims — the requirements-analyst-agent.md is a full agent profile with a minimum viable system prompt
- **[Methodology]:** The escalation cluster (claims 008, 011, 015) was internally well-connected but isolated from the concrete agent profile implementations; the reweave pass bridged theory to practice
- **[Friction]:** 4 task files used batch-file naming rather than semantic filenames during the create phase — a quality gate should enforce semantic naming
- **[Process gap]:** Wiki links using full question-form titles vs. short slugs caused systematic dangling links requiring cleanup during verify; link format should be standardized at create time

## Archive Location

`ops/queue/archive/2026-03-01-making-system-operational-and-creating-agents/`

Contains: extract task file, 18 claim task files (001-018), this summary.
