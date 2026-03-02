---
claim: "the minimal viable agent set for software-building is requirements, code generation, test generation, and code review"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 003: the minimal viable agent set for software-building is requirements, code generation, test generation, and code review

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 27-35)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim.

Rationale: This is a prioritization claim based on industry adoption patterns — it tells us which 4 agents deliver the most value in the core build loop. The source is explicit that deployment/monitoring can wait for iteration 2. Fits extraction category "agent design patterns" — this is the minimal catalog scope recommendation. Also serves as the founding set for this vault's agent catalog.

Semantic neighbor: null — vault has no agent profiles yet.

---

## Create

Created agent profile at: `agents/the-minimal-viable-agent-set-for-software-building-is-requirements-code-generation-test-generation-and-code-review.md`

The note argues that the four-agent specialist set (requirements analyst, code generator, test generator, code reviewer) covers the irreducible core build loop. Each agent in the set makes the next more effective — structured specs improve code generation accuracy, accurate code generation makes test generation more relevant, and automated tests give code review something concrete to evaluate. Deployment and operations agents are explicitly deferred to iteration 2 as they operate on build loop output, not within it.

The note links to four related claims already in the vault: optimal team size (5 agents total lands within 3–7 range), orchestrator-first bootstrapping (specialist set is built on top of the orchestrator anchor), spec-centric architecture (requirements agent must produce a structured spec), and phased rollout (this set maps to phases 1 and 2 of the rollout sequence).

## /map

Completed: 2026-03-02

**Phase overview MOCs updated:**
- Added to [[development-phase]] Core Ideas section
- Added to [[requirements-phase]] Core Ideas section
- Added to [[testing-phase]] Core Ideas section

**Connections reviewed:**
- Already linked to [[optimal multi-agent team size is 3 to 7 specialized agents]], [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], [[spec-centric architecture is the most reliable pattern for agents building systems]], [[phased rollout prevents coordination chaos when building multi-agent systems]]
- Coverage is comprehensive; all four existing connections are strong and well-articulated

**Articulation test:** PASS

**Discovery trace:**
- Phase overviews read: [[requirements-phase]], [[development-phase]], [[testing-phase]]
- Sibling claims reviewed: this note is already well-connected; the four existing links cover the key dependencies without creating noise

## /refine

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[crewai-agent-to-agent-handoff-and-interaction-api]] — added link: sequential mode task chain for minimal viable set (requirements → code → test → review)
- [[workflows-are-preferable-to-agents-for-deterministic-sdlc-phases]] — added backward link: the four-agent set covers judgment-intensive phases; surrounding mechanical tasks are workflow territory

**Gap check:**
- crewai-handoff mentioned the 4-agent set without linking; gap closed
- workflows-preferable described the build loop agents without linking minimal-viable-set; gap closed

**Sibling cross-check:**
- Connections are comprehensive via reflect phase

## /validate
(to be filled by /validate phase)
