---
_schema:
  entity_type: "phase-overview"
  applies_to: "sdlc-phases/*.md"
  required:
    - description
    - phase_purpose
    - agents
  optional:
    - inputs_from
    - outputs_to
    - success_criteria
  constraints:
    description:
      max_length: 200
      format: "What this SDLC phase accomplishes"
    agents:
      format: "Array of wiki links to agent profiles in this phase"

# Template fields with defaults
description: ""
phase_purpose: ""
agents: []
inputs_from: []
outputs_to: []
success_criteria: []
type: moc
---

# [SDLC Phase Name]

[Overview of this phase's role in the development workflow]

## Purpose

[What this phase accomplishes in the overall SDLC]

## Agents in This Phase

[List and describe the agents operating in this phase]

- [[agent-name]] -- [brief description of role]
- [[agent-name]] -- [brief description of role]

## Inputs

[What this phase receives from previous phases]

From [[previous-phase]]:
- [input type]

## Outputs

[What this phase produces for next phases]

To [[next-phase]]:
- [output type]

## Success Criteria

[How to measure if this phase is working well]

- [criterion 1]
- [criterion 2]

---

Topics:
- [[agent-registry]]
