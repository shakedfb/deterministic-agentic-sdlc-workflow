---
description: Full context at every handoff prevents specialist failures from interpretive drift, but large spec artifacts may physically exceed context window limits, making lossless transfer impossible — the correct v2 resolution is intelligent windowing, but this tension cannot be dissolved in v1 and represents a deliberate design constraint.
topics: ["[[agent-registry]]", "[[design-phase]]"]
source: "[[orchestrator-agent]]"
classification: closed
---

# lossless context transfer and context window limits are in direct tension for large spec artifacts

Two principles that individually are correct come into direct conflict at scale. The first: lossless context transfer at handoff boundaries is the orchestrator's most critical responsibility, because incomplete context causes specialist failures that are more expensive than the transfer overhead (see [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]]). The second: context windows are finite, and for large spec artifacts — detailed multi-module systems, comprehensive API specifications, extensive requirement sets — the full document may exceed what fits in a single context window.

When both principles are in force simultaneously, one must yield. The question is which one, under what conditions, and with what mitigation.

The tension is not symmetric. Yielding on lossless transfer has a known cost: specialist failures from interpretive drift, retry cycles, and compounding misalignment. Yielding on context window limits is not an option — it is a physical constraint, not a design choice. The resolution must therefore be a technique that preserves as much of the lossless transfer principle as possible while respecting the physical limit.

Intelligent windowing — full spec for the first task, then deltas and relevant sections for subsequent tasks — is the designed mitigation. But intelligent windowing has its own failure mode: if the relevance selection is incorrect (the orchestrator identifies the wrong sections as relevant), the specialist receives a context window that appears complete but is missing critical constraints. This failure mode is harder to detect than an obvious context truncation because the specialist's output looks plausible.

The tension is documented here as a design fact rather than a problem to solve in v1. For typical v1 specs that fit within context windows, the tension is dormant. The tension becomes active when spec size first exceeds the window — that is the correct trigger for implementing intelligent windowing, not earlier. Implementing windowing before the tension is active adds complexity without benefit; implementing it after the tension has caused failures gives you failure data that informs the windowing design.

---

**Source:** [[orchestrator-agent]]

**Relevant Notes:**
- [[lossless context transfer at handoff boundaries is the orchestrators most critical responsibility]] — the principle that context window limits threaten; this tension is the constraint that makes lossless transfer harder to honor at scale
- [[intelligent context windowing is needed when spec artifacts exceed the context window]] — the v2 mitigation strategy for this tension; this note describes the tension that windowing must resolve
- [[spec-centric architecture is the most reliable pattern for agents building systems]] — spec-centric architecture is what makes the spec artifact large; it is the upstream cause of the context window tension; the architectural choice creates the infrastructure requirement
- [[token cost of lossless context transfer is justified by the failure cost of context stripping]] — the economic argument that makes intelligent windowing preferable to arbitrary stripping; even when full transfer is infeasible, the windowing approach must be structured, not arbitrary

**Topics:**
- [[agent-registry]]
- [[design-phase]]
