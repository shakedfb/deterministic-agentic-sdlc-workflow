---
description: Code implementation phase -- agents that generate, review, and refactor code
type: moc
phase_purpose: "Implement designs as working code following best practices"
agents: []
---

# development phase

## Purpose

Agents in this phase generate code, conduct code reviews, and ensure implementation quality.

## Agents in This Phase

Research claims relevant to development-phase agents:

- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — establishes code generation and code review as core development-phase agents in the minimal viable set
- [[workflows are preferable to agents for deterministic SDLC phases]] — the design gate for development tooling: linting, formatting, and dependency scanning are workflow territory; code generation and review require agent judgment

## Gaps

- Code Generation Agent profile not yet designed (awaiting spec format confirmation — now resolved)
- Code Review Agent profile not yet designed

## Inputs

From [[design-phase]]:
- System architecture
- Component designs
- Coding standards

## Outputs

To [[testing-phase]]:
- Implemented features
- Code documentation
- Build artifacts

---

Topics:
- [[agent-registry]]
