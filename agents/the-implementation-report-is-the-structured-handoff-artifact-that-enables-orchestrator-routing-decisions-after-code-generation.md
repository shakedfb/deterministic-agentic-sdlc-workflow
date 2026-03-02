---
description: Every code generation invocation must produce a structured IMPLEMENTATION REPORT that the Orchestrator can parse for routing decisions — covering files created/modified, interface contracts fulfilled, self-check results, and spec deviations with rationale — making the report the specialist-side half of lossless context transfer at the development phase boundary.
topics: ["[[agent-registry]]", "[[development-phase]]"]
source: "[[code-generator-agent]]"
classification: closed
---

# the IMPLEMENTATION REPORT is the structured handoff artifact that enables orchestrator routing decisions after code generation

Every code generation invocation must produce a structured IMPLEMENTATION REPORT. This is not optional reporting — it is the output contract that makes the development phase handoff parseable by the Orchestrator.

The report contains four required sections:

1. **Files created/modified**: The Test Generator Agent needs to know which files to target. Without this, the Test Generator either scans the entire codebase (wasteful) or misses newly created files.

2. **Interface contracts fulfilled**: The Code Review Agent needs to verify contract compliance. Without an explicit list, code review must infer what contracts applied from the spec — adding interpretive work that the Code Generator can do once.

3. **Self-check results**: The Orchestrator needs this signal to decide whether to proceed downstream or iterate. If self-check passed, the Orchestrator routes to test generation. If self-check failed but the agent continued (HOTL governance), the Orchestrator routes to a human review checkpoint before test generation.

4. **Spec deviations with rationale**: Deviations are not failures — they are decisions that must be visible. A code generator that deviates from design.md without reporting it creates a gap between the spec and the implementation that downstream agents discover too late. Making deviations explicit gives the Orchestrator and human reviewers the information needed to decide whether the deviation is acceptable.

The IMPLEMENTATION REPORT is the specialist-side half of lossless context transfer at the development phase boundary. The Orchestrator assembles the context package for the next phase (test generation or code review) from the IMPLEMENTATION REPORT's structured output. A report that is incomplete, unstructured, or absent forces the Orchestrator to infer routing decisions from unstructured output — introducing the same interpretive drift that spec-centric architecture is designed to prevent.

The parallel to the spec artifact is deliberate. The spec defines the contract before implementation; the IMPLEMENTATION REPORT confirms fulfillment after implementation. The spec travels forward through every handoff; the IMPLEMENTATION REPORT travels forward from the development phase to all downstream phases. Both are structured, parseable artifacts that prevent interpretive drift across agent boundaries.

---

**Source:** [[code-generator-agent]]

**Relevant Notes:**
- [[lossless-context-transfer-at-handoff-boundaries-is-the-orchestrators-most-critical-responsibility]] — the IMPLEMENTATION REPORT is the specialist-side contribution to lossless transfer: the agent packages its outputs in a parseable format so the Orchestrator can assemble the next handoff package without interpretation or inference
- [[the-orchestrator-agents-role-is-routing-and-validation-not-content-generation]] — the structured report gives the Orchestrator the signal needed for routing decisions without requiring the Orchestrator to generate content; routing-not-generating requires structured inputs that the Orchestrator can evaluate
- [[spec-centric-architecture-is-the-most-reliable-pattern-for-agents-building-systems]] — the IMPLEMENTATION REPORT is the downstream mirror of the spec artifact: spec defines the contract, report confirms fulfillment; together they close the loop of spec-centric architecture across the development phase
- [[pre-handoff-self-validation-against-acceptance-criteria-is-a-required-quality-gate-for-code-generation-agents]] — self-check results are a required section of the IMPLEMENTATION REPORT; the self-check and the report are operationally coupled: the check produces the signal, the report surfaces it to the Orchestrator
- [[single-task-per-invocation-is-the-correct-scope-discipline-for-reliable-code-generation-agents]] — single-task invocation produces one IMPLEMENTATION REPORT per task, giving the Orchestrator a clean per-task routing signal; batched invocation would produce combined reports that are harder to parse for individual task routing decisions
- [[lossless-context-transfer-and-context-window-limits-are-in-direct-tension-for-large-spec-artifacts]] — for large projects, the IMPLEMENTATION REPORT (including prior code references) can itself become large; the same windowing principles that apply to spec transfer at orchestrator handoffs may need to apply to report contents at development phase boundaries

**Topics:**
- [[agent-registry]]
- [[development-phase]]
