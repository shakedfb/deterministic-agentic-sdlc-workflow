---
description: Operations and maintenance phase -- agents that monitor and maintain systems
type: moc
phase_purpose: "Monitor production systems, respond to incidents, and maintain reliability"
agents: []
---

# operations phase

## Purpose

Agents in this phase monitor production systems, detect and respond to incidents, and ensure ongoing reliability.

## Agents in This Phase

Research claims relevant to operations-phase agents:

- [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] — operations agents dealing with production incidents are high-stakes; supervision design is required
- [[phased rollout prevents coordination chaos when building multi-agent systems]] — monitoring and incident response agents are Phase 4 (after deployment is stable); operations agents close the learning loop from production back to requirements
- [[what metrics distinguish a well-functioning orchestrator from a coordination bottleneck]] — the four signal categories (delegation success rate, specialist utilization balance, coordination overhead ratio, error containment factor) apply to operations-level orchestrator monitoring
- [[what are the specific escalation patterns used in production agentic SDLC systems]] — the escalation taxonomy (confidence threshold, ambiguity detection, irreversibility gate, loop termination) is most densely applicable to operations-phase agents dealing with production state changes

## Gaps

- Operations Monitoring Agent profile not yet designed (intentionally deferred to iteration 2)
- Incident Response Agent profile not yet designed

## Inputs

From [[deployment-phase]]:
- Deployed systems
- Configuration
- Monitoring setup

## Outputs

Back to [[requirements-phase]] (feedback loop):
- Incident reports
- Performance metrics
- Feature requests
- Bug reports

---

Topics:
- [[agent-registry]]
