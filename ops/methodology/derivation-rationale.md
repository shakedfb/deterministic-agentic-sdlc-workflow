---
description: Why each configuration dimension was chosen — the reasoning behind initial system setup
category: derivation-rationale
created: 2026-03-01
status: active
---
# derivation rationale for agent workflow architecture

This system was designed for cataloging AI agent roles in an SDLC-based development team — tracking agent designs, versioning iterations, mapping interactions, and measuring success.

## Domain Context

The user is designing (not implementing) an AI agent-based development team where each SDLC phase (requirements, design, development, testing, deployment, operations) contains specialized agents that coordinate to complete software projects. The catalog documents agent roles, their responsibilities, how they interact, and their evolution through testing.

## Configuration Decisions

**Granularity: Moderate**
Signal: "agent catalog" — one note per agent role
Rationale: Each agent profile is a self-contained design document. Atomic decomposition (separate notes for prompts, metrics, interactions) would fragment the design. Coarse granularity (one big document for all agents) would prevent versioning individual agents. Moderate = one note per agent = the natural unit.

**Organization: Flat**
Signal: "how agents interact" + cross-phase coordination
Rationale: Folder-per-SDLC-phase would create silos that prevent cross-phase interaction tracking. Flat organization with phase MOCs allows agents to connect across phases naturally while maintaining phase-based browsing.

**Linking: Explicit**
Signal: "how agents interact with other agents"
Rationale: Agent-to-agent interactions are the workflow graph. These connections must be explicit wiki links, not inferred. At expected volume (5-20 agents initially), semantic search is unnecessary overhead.

**Processing: Moderate**
Signal: "iterate to see what works better" + "design decisions and rationale"
Rationale: Not light (just capture) — requires documenting design rationale, mapping interactions, tracking metrics. Not heavy (full extraction pipeline) — content is generated, not mined from sources. Moderate = structured documentation with interaction mapping and version tracking.

**Navigation: 2-Tier**
Signal: Low volume (handful of agents) + SDLC phase organization
Rationale: Hub MOC → SDLC phase MOCs → agent profiles. At 5-20 agents, deeper hierarchy adds overhead without value. As volume grows past 50 agents, 3-tier could be reconsidered.

**Maintenance: Condition-Based**
Signal: "iterate" + metrics tracking + version history
Rationale: Review when stuck agents (status: iterating for 7+ days), orphan agents (no interactions), or stale metrics accumulate. Condition-based maintenance surfaces agents that need attention without manual scheduling.

**Schema: Dense**
Signal: "versioning history" + "prompts and metrics" + "inputs and outputs"
Rationale: Agent profiles have natural structure: version, current_prompt, metrics, interactions, inputs, outputs, status, framework. Dense schema enables queryability (find all agents in testing phase, find agents with poor metrics) without imposing arbitrary fields.

**Automation: Full**
Platform: Claude Code detected
Rationale: Full skill suite + hooks from day one. Processing pipelines, validation hooks, session capture all available. User can opt down via config.yaml if automation creates friction.

## Active Feature Blocks

- Processing pipeline (moderate): document → design → map interactions → track metrics → version snapshot
- Dense schema: extensive YAML fields for agent profiles
- 2-tier MOC navigation: hub → phase overviews → agents
- Graph analysis: queries for orphan detection, interaction mapping, status distribution
- Methodology folder: system self-knowledge for meta-skills
- Version tracking: hybrid model (main note = current, versions/ = snapshots)

## Coherence Validation

All constraints passed:
- Moderate granularity + 2-tier navigation + low volume: coherent
- Dense schema + full automation: validation handles complexity
- Moderate processing + full automation: pipeline supports structured documentation
- Flat organization + phase MOCs: browsing works without folders

## Failure Mode Mitigation

**Productivity Porn (HIGH risk)**
Prevention: Time-box documentation, test agents before elaborating profiles, catalog serves implementation

**Temporal Staleness (MEDIUM risk)**
Prevention: Active use of status field, version snapshots before major changes, deprecation marking

**Schema Erosion (MEDIUM risk)**
Prevention: Validation hooks, required field enforcement, template as single source of truth

**Version Sprawl (MEDIUM risk)**
Prevention: Only snapshot major iterations, not minor tweaks

## Evolution Triggers

Reconsider configuration when:
- Agent count grows past 50 (may need 3-tier navigation)
- Cross-vocabulary needs emerge (may need semantic search)
- Manual validation becomes overhead (already have automation, but could tighten)
- Phase organization feels constraining (could add domain/product dimensions)

---

Topics:
- [[methodology]]
