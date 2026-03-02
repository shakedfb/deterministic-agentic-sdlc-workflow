---
claim: "what does a minimum viable Requirements Analyst Agent prompt look like and how does it produce a structured spec"
classification: open
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 013: what does a minimum viable Requirements Analyst Agent prompt look like and how does it produce a structured spec

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (line 93)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is an OPEN claim (open question / research direction).

Rationale: This is an explicitly flagged research direction from the source. It is actionable and domain-specific — a future session needs this question retrievable to know what to investigate next when designing the Requirements Analyst Agent. Open questions guide future work. Fits extraction category "agent design patterns" (open question variant).

Semantic neighbor: null — connects to claims 004 (spec-centric architecture) and 012 (requirements agents must produce structured spec).

---

## Create

Created: `agents/requirements-analyst-agent.md`

Note title: Requirements Analyst Agent
Path: agents/requirements-analyst-agent.md
Word count: ~950 words (body + prompt)
Status: complete

Key content:
- Answers the open question: defines a minimum viable prompt structure with three components — output format contract, explicit escalation conditions, and constraint enforcement
- Defines the three-file spec artifact (requirements.md, design.md, tasks.md) grounded in AWS Kiro and GitHub Spec Kit convergence
- Provides the complete system prompt text including EARS format requirements, section templates, four escalation conditions, three hard constraints, and SPEC COMPLETE handoff protocol
- Establishes measurable metrics: acceptance criteria testability rate, downstream first-pass test success (target >70%), escalation rate (target <20%), task atomicity target (15-45 min per task)
- Status: draft (v1 based on research synthesis, not yet production-tested)
- Connects to: [[requirements-phase]], [[agent-registry]], [[orchestrator-first-bootstrapping-reduces-multi-agent-coordination-failures]], [[the-minimal-viable-agent-set-for-software-building-is-requirements-code-generation-test-generation-and-code-review]]

## /map

Completed: 2026-03-02

**Phase overview MOC updated:**
- [[requirements-analyst-agent]] is the created note; it was already added to [[requirements-phase]] by the create phase

**Connections reviewed:**
- The created note (requirements-analyst-agent.md) uses hyphenated wiki links in the interactions field that may need verification
- Note is connected to [[requirements-phase]] and [[agent-registry]]

**Articulation test:** PASS — the Requirements Analyst Agent profile is the concrete answer to the open question

**Discovery trace:**
- Phase overview read: [[requirements-phase]]
- The agent profile is the resolution of the open question; it documents the MVP prompt with three components: output format contract, escalation conditions, constraint enforcement
- Note references [[can GitHub Spec Kit format be adopted as the canonical spec artifact format for this vault]] via the three-file structure grounded in Kiro/GitHub Spec Kit convergence

## /refine

Completed: 2026-03-02

**Backward pass (OLDER notes updated to reference THIS note):**
- [[agent-profiles-must-include-escalation-conditions-as-a-required-design-field]] — added backward link: Requirements Analyst Agent is the first concrete implementation of escalation conditions schema requirement
- [[specific-escalation-patterns-in-production-agentic-sdlc-systems]] — added backward link: RAA's four escalation conditions map to ambiguity detection + irreversibility gate categories

**Gap check:**
- escalation-conditions schema note didn't reference its first implemented example; gap closed
- specific-escalation-patterns didn't reference the RAA as its first concrete application; gap closed

**Sibling cross-check:**
- can-github-spec-kit links requirements-analyst-agent as the implementing profile

## /validate

**Verified:** 2026-03-02T12:35:07Z

Recite:
- Prediction: 4/5 — description adds mechanism/context beyond title
- Retrieval: deferred (semantic search disabled in config)
- Description: kept (passes minimum threshold, length exceeds 200-char guideline)

Validate:
- Required fields: PASS (description and topics present)
- Description constraints: WARN (230 chars, exceeds 200-char guideline; trailing period; adds mechanism)
- Topics: PASS

Review:
- Frontmatter: PASS
- Phase overview connection: PASS (note appears in assigned topic map)
- Wiki links: 8 outgoing — PASS
- Link resolution: PASS (all links resolve after fixes applied)

Overall: PASS (3 warnings)

Actions taken:
- Fixed dangling wiki links where title-form links used question titles instead of file slugs
- Added topics field to requirements-analyst-agent.md
- Removed misplaced numbered duplicates from agents/ directory (2026-03-01-*-004/007/016/017.md)

Recommended actions:
- Trim descriptions to under 200 chars in a future editing pass (WARN-level, not urgent)
- Design code-generation-agent profile to resolve forward reference in requirements-analyst-agent.md

