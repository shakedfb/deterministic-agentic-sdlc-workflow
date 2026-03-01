---
description: Process research on making the agent system operational into concrete agent designs
source: design-ideas/2026-03-01-making-system-operational-and-creating-agents.md
queued: 2026-03-01
status: pending
priority: high
---

# Seed: Making the System Operational

## Source Summary

Research synthesis on bootstrapping a multi-agent SDLC team. 10 sources analyzed covering architecture patterns, framework choices, and phased rollout strategies.

## Extractable Artifacts

### Agent Profiles to Create (ordered by priority)

1. **Orchestrator Agent** — coordination anchor; maintains project context, routes work, escalates to humans
   - Phase: operations (cross-cutting)
   - Priority: FIRST — all other agents depend on this

2. **Requirements Analyst Agent** — translates user intent into structured spec artifacts
   - Phase: requirements
   - Key design constraint: must output a formal spec (GitHub Spec Kit pattern), not just notes

3. **Code Generator Agent** — generates implementation from specs
   - Phase: development
   - Key design constraint: works from spec artifact, not freeform prompts

4. **Test Generator Agent** — creates unit/integration tests from specs and code
   - Phase: testing
   - Key design constraint: generates tests aligned with spec acceptance criteria

5. **Code Review Agent** — validates generated code before commit
   - Phase: development
   - Key design constraint: iteration 2 (manual review in phase 1)

### Design Decisions to Capture

- Spec-centric architecture: spec artifact is the central coordination document
- CrewAI as recommended orchestration framework (role-based, fits vault philosophy)
- Agent profiles should include escalation conditions (when to stop and ask a human)
- `framework` field should capture orchestration framework AND target base model
- Use workflows (not agents) for deterministic tasks (linting, formatting, CI triggers)

### Phased Rollout Plan

- Phase 1: Requirements Analyst + Code Generator + Test Generator (manual code review)
- Phase 2: Add Code Review Agent, close the inner loop
- Phase 3: Add Deployment Orchestrator, connect to CI/CD
- Phase 4: Add Operations/Monitoring agents, enable closed-loop learning

## Processing Actions

- [ ] Design Orchestrator Agent profile → `agents/orchestrator-agent.md`
- [ ] Design Requirements Analyst Agent profile → `agents/requirements-analyst-agent.md`
- [ ] Design Code Generator Agent profile → `agents/code-generator-agent.md`
- [ ] Design Test Generator Agent profile → `agents/test-generator-agent.md`
- [ ] Update phase MOCs with new agents
- [ ] Update agent-registry with quick stats
- [ ] Define spec artifact format (prerequisite for Requirements Analyst)
