---
claim: "spec-centric architecture is the most reliable pattern for agents building systems"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 004: spec-centric architecture is the most reliable pattern for agents building systems

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 37-41)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim.

Rationale: GitHub Spec Kit (2025) evidence grounds this claim in industry practice. The source argues a specification at the center of the process is more reliable because agents work toward a defined endpoint rather than improvising. This is an agent design pattern with direct implications for how the Requirements Analyst Agent is designed — it must produce a structured spec artifact. Fits extraction category "agent design patterns."

Semantic neighbor: null — no existing note on spec-driven agent workflows.

---

## Create

Created: `agents/spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems.md`

Note title: spec-centric architecture is the most reliable pattern for agents building systems
Path: agents/spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems.md
Status: complete (recovered from misplaced file in agents/ directory)

## /map

Completed: 2026-03-02

**Phase overview MOC updated:**
- Added to [[design-phase]] and [[requirements-phase]] Core Ideas sections (note's topics include these phases)

**Connections reviewed:**
- Already linked to [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]], [[requirements agents must produce a structured spec artifact not just prose notes]], [[orchestrator-first bootstrapping reduces multi-agent coordination failures]]
- Existing connections are comprehensive

**Articulation test:** PASS

**Discovery trace:**
- Phase overviews read: [[design-phase]], [[requirements-phase]]
- Sibling claims reviewed: core connections already present; note well-integrated into the spec-centric cluster

## /refine

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[requirements-analyst-agent]] — added inline link to spec-centric principle in intro paragraph
- [[spec-centric-architecture]] note body updated to reference [[can GitHub Spec Kit format be adopted as the canonical spec artifact format for this vault]] (which operationalizes spec-centric)

**Gap check:**
- requirements-analyst-agent mentioned spec-centric as foundational without wiki-linking; gap closed
- spec-centric body mentioned Spec Kit without linking the adoption decision note; gap closed

**Sibling cross-check:**
- when-langgraph: spec as shared state for LangGraph nodes is a genuine gap; not added (too indirect)

## /validate

**Verified:** 2026-03-02T12:35:07Z

Recite:
- Prediction: 3/5 — description adds mechanism/context beyond title
- Retrieval: deferred (semantic search disabled in config)
- Description: kept (passes minimum threshold, length exceeds 200-char guideline)

Validate:
- Required fields: PASS (description and topics present)
- Description constraints: WARN (290 chars, exceeds 200-char guideline; trailing period; adds mechanism)
- Topics: PASS

Review:
- Frontmatter: PASS
- Phase overview connection: PASS (note appears in assigned topic map)
- Wiki links: 10 outgoing — PASS
- Link resolution: PASS (all links resolve after fixes applied)

Overall: PASS (2 warnings)

Actions taken:
- Fixed dangling wiki links where title-form links used question titles instead of file slugs
- Added topics field to requirements-analyst-agent.md
- Removed misplaced numbered duplicates from agents/ directory (2026-03-01-*-004/007/016/017.md)

Recommended actions:
- Trim descriptions to under 200 chars in a future editing pass (WARN-level, not urgent)
- Design code-generation-agent profile to resolve forward reference in requirements-analyst-agent.md

