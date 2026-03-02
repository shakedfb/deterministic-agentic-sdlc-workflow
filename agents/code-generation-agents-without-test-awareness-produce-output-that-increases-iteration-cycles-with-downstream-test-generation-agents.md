---
description: V1 code generation agents produce code without knowledge of how the test generation agent will test it, creating an implicit coupling assumption that code structure is inherently testable — a hypothesis requiring validation, with a proposed v2 resolution of including test patterns and framework conventions in the code generator's input.
topics: ["[[agent-registry]]", "[[development-phase]]", "[[testing-phase]]"]
source: "[[code-generator-agent]]"
classification: open
---

# code generation agents without test-awareness produce output that increases iteration cycles with downstream test generation agents

The v1 Code Generator produces implementation code without any knowledge of the test patterns, testing framework conventions, or testability requirements that the downstream Test Generator Agent will apply. This creates an implicit coupling assumption: that code generated from a spec without testability guidance will naturally be structured for testability.

This assumption may not hold. Code that is not structured for testability — tightly coupled components, business logic mixed with I/O operations, missing dependency injection, side effects in functions that should be pure — forces the Test Generator to work around implementation details rather than testing behavior. In cases where the Test Generator cannot test the generated code directly, it either writes incomplete tests, generates fixture-heavy workarounds, or returns the code to the Code Generator for structural revision. Each of these outcomes adds iteration cycles to the build loop.

The gap is an interface contract that is currently implicit. The spec defines what the code should do (acceptance criteria, interface contracts). It does not define how the code should be structured for testability. In language ecosystems where testability conventions are strong (e.g., dependency injection frameworks in Java/Spring, pytest fixtures in Python), this gap may be small because the code generator's training data encodes testable patterns. In ecosystems where testability conventions are weaker or more varied, the gap may be significant.

The proposed v2 resolution is to include test patterns and testing framework conventions in the Code Generator's input — either as part of the `project_config` parameter proposed for language/framework specialization, or as a separate `testing_conventions` input. The goal is not for the Code Generator to write tests, but for it to produce code that the Test Generator can test without structural revision.

This is an open hypothesis. Validating it requires comparing iteration cycle counts (code-to-test revisions) between:
- A baseline code generator without test-awareness
- A v2 code generator with testing framework conventions in its input

The hypothesis is falsified if iteration cycles do not decrease when test-awareness is added, suggesting that the Code Generator's base model already produces testable code for common patterns without explicit guidance.

---

**Source:** [[code-generator-agent]]

**Relevant Notes:**
- [[the-minimal-viable-agent-set-for-software-building-is-requirements-code-generation-test-generation-and-code-review]] — the minimal set assumes agents are sequentially compatible; the test-awareness gap is a coupling assumption between two of the four agents that may not hold without explicit interface contract design
- [[spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems]] — spec-centric architecture ensures behavioral alignment via acceptance criteria; test-awareness extends that alignment to structural testability conventions, which the spec does not currently define
- [[language-agnostic-code-generation-prompts-require-a-project-config-parameter-to-specialize-for-framework-and-toolchain-without-prompt-rewrites]] — the project_config parameter proposed for language/framework specialization is the natural injection point for testing conventions; both problems share the same solution shape
- [[hard-iteration-limits-per-task-are-required-to-prevent-runaway-loops-in-multi-agent-pipelines]] — test-awareness gap is a source of unnecessary iteration cycles; reducing structural revision loops between code generator and test generator is the practical motivation for addressing this gap, as unnecessary iterations consume the iteration budget reserved for substantive failures

**Topics:**
- [[agent-registry]]
- [[development-phase]]
- [[testing-phase]]
