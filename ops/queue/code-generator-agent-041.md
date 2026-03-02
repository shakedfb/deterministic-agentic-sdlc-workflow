---
id: claim-041
type: claim
batch: code-generator-agent
target: "language-agnostic code generation prompts require a project_config parameter to specialize for framework and toolchain without prompt rewrites"
classification: open
file: code-generator-agent-041.md
created: 2026-03-02T00:00:00Z
current_phase: create
completed_phases: []
---

# Claim 041: language-agnostic code generation prompts require a project_config parameter to specialize for framework and toolchain without prompt rewrites

## Source
ops/queue/archive/2026-03-02-code-generator-agent/code-generator-agent.md

## Claim
The v1 Code Generator prompt is language-agnostic, which trades specialization quality for reusability. In practice, code generation quality varies significantly by language and framework — a TypeScript React component requires different patterns than a Python FastAPI endpoint. Rather than maintaining separate prompts per stack, v2 should introduce a `project_config` input that specifies language, framework, linting rules, and test framework. The prompt then reads this config and applies stack-specific conventions without requiring a prompt rewrite per project. This pattern allows one generic prompt to behave as a specialized generator based on runtime configuration.

## Classification
OPEN — v2 design hypothesis; pattern is common in production code generation systems but not yet validated for this agent

## Connections
- [[crewai-aligns-best-with-catalog-driven-sdlc-agent-architectures]] (implements in: CrewAI context parameter or task description is the natural injection point for project_config)
- [[base-model-quality-matters-more-than-framework-choice-for-agent-capability]] (context: language-agnostic prompts may already leverage base model's language-specific training; project_config provides guardrails rather than compensating for base model gaps)

## Create
(filled by create phase)

## Reflect
(filled by reflect phase)

## Reweave
(filled by reweave phase)

## Verify
(filled by verify phase)
