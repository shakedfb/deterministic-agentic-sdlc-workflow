---
description: Requirements gathering and specification phase -- agents that capture and structure user needs
type: moc
phase_purpose: "Transform user needs and stakeholder input into structured, actionable requirements"
agents: []
---

# requirements phase

## Purpose

The requirements phase transforms raw user needs into structured specifications that downstream phases can work with. Agents in this phase handle requirement elicitation, validation, prioritization, and documentation.

## Agents in This Phase

- [[requirements-analyst-agent]] — translates raw user intent into a three-file structured spec (requirements.md, design.md, tasks.md); first specialist in the build loop

Research claims that define this phase's design constraints:

- [[requirements agents must produce a structured spec artifact not just prose notes]] — the output contract for requirements agents: prose is insufficient; a structured spec with defined sections is the minimum valid output
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — the architectural rationale; the spec is the shared contract enabling coherent downstream coordination
- [[can GitHub Spec Kit format be adopted as the canonical spec artifact format for this vault]] — the spec format decision: Spec Kit section taxonomy for requirements.md, with EARS syntax and vault-specific interface contracts as extensions
- [[what does a minimum viable Requirements Analyst Agent prompt look like and how does it produce a structured spec]] — the answer: three-file artifact, explicit escalation conditions, constraint enforcement, and SPEC COMPLETE handoff protocol

## Inputs

- User needs
- Stakeholder interviews
- Business objectives
- Product vision

## Outputs

To [[design-phase]]:
- Structured requirements documents
- User stories
- Acceptance criteria
- Prioritized feature backlog

## Success Criteria

- Requirements are complete, unambiguous, and testable
- Stakeholder alignment on priorities
- Clear handoff to design phase

---

## Tensions

- [[requirements agents must produce a structured spec artifact not just prose notes]] establishes that the spec format must be agreed upon before downstream agents are designed — this creates a hard dependency that blocks parallel design of requirements + code generation agents

## Gaps

- Code Generation Agent profile not yet designed (its input format is the spec artifact; spec format is now resolved)
- Test Generation Agent profile not yet designed

Topics:
- [[agent-registry]]

Agent Notes:
- 2026-03-02: The requirements phase's foundational questions are now answered. Spec format is resolved (claim-016: Spec Kit section taxonomy + EARS + interface contracts). MVP prompt is documented (claim-013: Requirements Analyst Agent). The phase is ready for downstream agent design.
