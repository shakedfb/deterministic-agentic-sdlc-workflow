---
claim: "requirements agents must produce a structured spec artifact not just prose notes"
classification: closed
source_task: 2026-03-01-making-system-operational-and-creating-agents
semantic_neighbor: null
---

# Claim 012: requirements agents must produce a structured spec artifact not just prose notes

Source: [[2026-03-01-making-system-operational-and-creating-agents]] (lines 39-41)

## Reduce Notes

Extracted from 2026-03-01-making-system-operational-and-creating-agents. This is a CLOSED claim.

Rationale: The source explicitly states the Requirements Analyst Agent "must produce a structured spec artifact, not just notes" and that "the spec format should be agreed upon before building any downstream agents." This is both an agent design constraint and a sequencing requirement — the spec format is a prerequisite for designing downstream agents. Fits extraction category "agent design patterns" with implications for the requirements-phase agent design.

Semantic neighbor: null — no requirements agent output design note exists.

---

## Create

Created: `agents/requirements-agents-must-produce-a-structured-spec-artifact-not-just-prose-notes.md`

Note title: requirements agents must produce a structured spec artifact not just prose notes
Path: agents/requirements-agents-must-produce-a-structured-spec-artifact-not-just-prose-notes.md
Word count: ~370 words (body)
Status: complete

Key content:
- Explains why prose notes fail as requirements output: they force uncoordinated interpretive decisions on every downstream agent
- Establishes structured spec as a shared contract enabling coherent downstream coordination without direct agent-to-agent coupling
- Grounds the claim in GitHub Spec Kit pattern as the current production-validated approach
- States the sequencing constraint explicitly: spec format must be agreed upon before any downstream agent is designed
- Vault implication: Requirements Analyst Agent profile must specify the output format precisely, not just reference "a specification document"
- Connects to: [[spec-centric architecture is the most reliable pattern for agents building systems]], [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]], [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], [[agent profiles must include escalation conditions as a required design field]]

## /map

Completed: 2026-03-02

**Phase overview MOCs updated:**
- Added to [[design-phase]] and [[requirements-phase]] Core Ideas sections

**New connection added:**
- -> [[can GitHub Spec Kit format be adopted as the canonical spec artifact format for this vault]] — extends: resolves the open question of what format the structured spec takes; the spec format question raised here is now answered by that note

**Existing connections reviewed:**
- [[spec-centric architecture is the most reliable pattern for agents building systems]], [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]], [[orchestrator-first bootstrapping reduces multi-agent coordination failures]], [[agent profiles must include escalation conditions as a required design field]] — all well-articulated

**Articulation test:** PASS

**Discovery trace:**
- Phase overviews read: [[requirements-phase]], [[design-phase]]
- can-github-spec-kit (016) directly resolves the format question this note raises, making it a natural extension connection

## /refine
(to be filled by /refine phase)

## /validate
(to be filled by /validate phase)
