---
description: Language-agnostic code generation prompts trade specialization quality for reusability across projects — a v2 resolution introduces a project_config input (language, framework, linting rules, test framework) that the prompt reads at runtime, enabling stack-specific behavior without requiring prompt rewrites per project.
topics: ["[[agent-registry]]", "[[development-phase]]"]
source: "[[code-generator-agent]]"
classification: open
---

# language-agnostic code generation prompts require a project_config parameter to specialize for framework and toolchain without prompt rewrites

The v1 Code Generator prompt is deliberately language-agnostic. It describes implementation steps, self-validation protocol, and output format without specifying a language, framework, linting standard, or test framework. This makes the prompt reusable across projects but at a cost: code generation quality varies significantly by language and framework, and a generic prompt cannot provide the idiomatic guidance that produces high-quality output for any specific stack.

A TypeScript React component requires different structural conventions than a Python FastAPI endpoint, which requires different conventions than a Go gRPC service. Without stack-specific guidance, the code generator falls back to training data patterns — which may be correct but may also reflect outdated conventions, style preferences that differ from the project's linting configuration, or patterns that are idiomatic in isolation but inconsistent with the existing codebase.

The v2 resolution is a `project_config` input that the prompt reads at runtime. Rather than maintaining separate prompts per stack, a single generic prompt becomes a stack-specialized generator through runtime configuration. The config specifies:
- **Language**: the programming language and version
- **Framework**: the primary framework and its conventions
- **Linting rules**: the project's style configuration (ESLint config, Ruff settings, etc.)
- **Test framework**: the testing library (Jest, pytest, JUnit) and conventions for testable code structure

The prompt reads this config in its "Understand the Project Context" step (before planning or implementing) and applies the specified conventions throughout. This pattern is common in production code generation systems — the base model provides the coding capability, the project config provides the guardrails.

This is an open hypothesis because it assumes the quality gap between generic and configured prompts is large enough to warrant the added input complexity. The hypothesis is falsifiable: if testing shows that the base model already produces idiomatic, linting-compliant code for common stacks without explicit configuration, the v2 change is unnecessary overhead. The empirical test is first-attempt pass rate (the fraction of tasks where generated code passes the test suite on the first attempt) segmented by language/framework — if pass rates are high and consistent across stacks without project_config, the generic prompt is sufficient.

The `project_config` also serves as the natural injection point for testing conventions, addressing the test-awareness gap documented in [[code-generation-agents-without-test-awareness-produce-output-that-increases-iteration-cycles-with-downstream-test-generation-agents]]. Rather than a separate `testing_conventions` input, testing framework conventions can be a section of the project_config, collocating all stack-specific context in one parameter.

---

**Source:** [[code-generator-agent]]

**Relevant Notes:**
- [[base-model-quality-matters-more-than-framework-choice-for-agent-capability]] — project_config provides guardrails for the base model's coding capability; this note contextualizes the relationship between model-level quality and prompt-level specialization, suggesting project_config supplements rather than compensates for base model gaps
- [[crewai-aligns-best-with-catalog-driven-sdlc-agent-architectures]] — CrewAI's task description or context parameter is the natural injection point for project_config at runtime; the framework choice determines the specific mechanism for passing configuration into the code generator's context
- [[code-generation-agents-without-test-awareness-produce-output-that-increases-iteration-cycles-with-downstream-test-generation-agents]] — the test-awareness gap is naturally resolved by adding testing conventions to project_config; the two v2 improvements share the same solution shape

**Topics:**
- [[agent-registry]]
- [[development-phase]]
