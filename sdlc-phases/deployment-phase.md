---
description: Deployment and release phase -- agents that orchestrate releases
type: moc
phase_purpose: "Package and deploy validated builds to production environments"
agents: []
---

# deployment phase

## Purpose

Agents in this phase handle build packaging, deployment orchestration, and release management.

## Agents in This Phase

Research claims relevant to deployment-phase agents:

- [[agentic SDLC systems require explicit human supervision at high-stakes handoff points]] — deployment to production is a canonical irreversibility gate; the deployment agent must escalate before any production state change
- [[phased rollout prevents coordination chaos when building multi-agent systems]] — deployment orchestration agents are Phase 3 (after core loop and review agents are stable); building a deployment agent before the build loop is validated is out of sequence
- [[workflows are preferable to agents for deterministic SDLC phases]] — CI/CD pipeline triggers and artifact packaging are workflow territory; deployment orchestration is the agent concern

## Gaps

- Deployment Orchestrator Agent profile not yet designed (intentionally deferred to iteration 2)

## Inputs

From [[testing-phase]]:
- Validated builds
- Test results
- Release notes

## Outputs

To [[operations-phase]]:
- Deployed systems
- Deployment logs
- Configuration

---

Topics:
- [[agent-registry]]
