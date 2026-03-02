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

### Agent Profiles
- [[code-generator-agent]] — implementation engine of the build loop; consumes spec artifact (requirements.md, design.md, tasks.md), implements one task per invocation, self-validates, produces IMPLEMENTATION REPORT

### Research Claims Relevant to Development-Phase Agents
- [[the minimal viable agent set for software-building is requirements, code generation, test generation, and code review]] — establishes code generation and code review as core development-phase agents in the minimal viable set
- [[workflows are preferable to agents for deterministic SDLC phases]] — the design gate for development tooling: linting, formatting, and dependency scanning are workflow territory; code generation and review require agent judgment
- [[single-task-per-invocation-is-the-correct-scope-discipline-for-reliable-code-generation-agents]] — core design principle for the Code Generator: one task per invocation for diagnosable failures and enforceable iteration limits
- [[pre-handoff-self-validation-against-acceptance-criteria-is-a-required-quality-gate-for-code-generation-agents]] — required quality gate before handoff: self-check against acceptance criteria reduces iteration cost in the build loop
- [[the-implementation-report-is-the-structured-handoff-artifact-that-enables-orchestrator-routing-decisions-after-code-generation]] — the Code Generator's output contract: structured report enabling Orchestrator routing without interpretation
- [[code-generation-agents-without-test-awareness-produce-output-that-increases-iteration-cycles-with-downstream-test-generation-agents]] — open v2 hypothesis: test-awareness input reduces structural revision loops with Test Generator
- [[language-agnostic-code-generation-prompts-require-a-project-config-parameter-to-specialize-for-framework-and-toolchain-without-prompt-rewrites]] — open v2 hypothesis: project_config for stack-specific specialization without prompt rewrites

## Gaps

- Code Review Agent profile not yet designed
- Test Generator Agent profile not yet designed

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
