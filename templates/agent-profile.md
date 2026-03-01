---
_schema:
  entity_type: "agent-profile"
  applies_to: "agents/*.md"
  required:
    - description
    - sdlc_phase
    - version
    - responsibilities
    - interactions
    - inputs
    - outputs
    - current_prompt
    - metrics
    - status
  optional:
    - version_history
    - framework
    - dependencies
    - constraints
    - examples
  enums:
    sdlc_phase:
      - requirements
      - design
      - development
      - testing
      - deployment
      - operations
    status:
      - draft
      - active
      - iterating
      - deprecated
  constraints:
    description:
      max_length: 200
      format: "Purpose - what the agent does and why it exists"
    sdlc_phases:
      format: "Array of wiki links to phase overview MOCs"
    interactions:
      format: "Array of wiki links to other agent profiles"
    version:
      format: "v1, v2, v3, etc."

# Template fields with defaults
description: ""
sdlc_phase:
version: v1
responsibilities: []
interactions: []
inputs: ""
outputs: ""
current_prompt: ""
metrics: []
status: draft
version_history: []
framework: ""
dependencies: []
constraints: []
examples: []
---

# [Agent Role Name]

[Main content - how this agent works, design rationale, what's working, what needs refinement]

## Current Approach

[Describe the agent's current implementation and how it operates]

## What's Working

[Document successes, validated metrics, effective patterns]

## What Needs Iteration

[Note friction points, areas for improvement, open questions]

---

SDLC Phases:
- [[phase-name]]
- [[agent-registry]]
