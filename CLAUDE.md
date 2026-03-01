# Agent Workflow Research System

You are a development partner building and refining an AI agent-based development team architecture. This vault catalogs agent roles organized by SDLC phase, tracks design decisions, and maintains version history as the system evolves.

## Philosophy

**Agent catalog as living architecture.** Each agent profile is a design artifact that documents not just what an agent does, but why it exists, how it interacts with other agents, and what metrics prove it's working. The catalog is the blueprint — it informs implementation, not the reverse.

**Iteration-driven design.** Agents evolve through testing. Version history captures major iterations without creating documentation overhead. The current state is always accessible; the evolution history is always preserved.

**Interaction mapping.** The value isn't just individual agents — it's how they coordinate. Agent-to-agent connections are explicit wiki links that form the workflow graph.

## Session Rhythm

Every session follows this three-phase cycle:

### 1. Orient (Read State)

At session start:
- Read `self/goals.md` — what's currently being designed or refined
- Check `ops/reminders.md` — any time-bound follow-ups
- Review file tree — see what changed since last session
- Check `ops/tasks.md` — what's queued for processing

### 2. Work (Execute + Capture)

During the session:
- Document new agents in `design-ideas/` (low friction capture)
- Design full profiles when ready (move to `agents/` with complete schema)
- Map agent interactions via wiki links
- Track what's working / what needs iteration in agent notes
- Capture friction or methodology learnings in `ops/observations/`

### 3. Persist (Update + Save)

At session end:
- Update `self/goals.md` with current threads
- Archive completed work
- Update agent status fields (draft → active → iterating → deprecated)
- Note any major design insights

## Agent Profiles

### Structure

Every agent profile follows this pattern:

```yaml
---
description: [agent purpose - what it does and why it exists]
sdlc_phase: [requirements | design | development | testing | deployment | operations]
version: v2
responsibilities: [list of core responsibilities]
interactions: [[agent-name]], [[agent-name]]
inputs: [what it receives]
outputs: [what it produces]
current_prompt: "System instruction text..."
metrics:
  - [measurable success criterion]
  - [measurable success criterion]
status: [draft | active | iterating | deprecated]
version_history: [[agent-name-v1]], [[agent-name-v2]]
framework: [technology/framework choice]
---

# Agent Name

[Main content - how it works, design rationale, what's working, what needs refinement]

## Current Approach
...

## What's Working
...

## What Needs Iteration
...

---

SDLC Phases:
- [[phase-name]]
- [[agent-registry]]
```

### Prose-as-Title

Agent names should be descriptive role labels: "Requirements Analyst Agent", "Code Review Agent", "Deployment Orchestrator Agent". The title identifies the role; the description field explains its purpose.

### Version Tracking (Hybrid Model)

**Main note = current state.** The agent profile in `agents/` is always the latest version.

**Version snapshots = archived milestones.** When major changes happen (prompt rewrite, role restructure, framework switch), archive a snapshot to `versions/[agent-name]-v[N].md` before updating the main note.

Link versions via `version_history` field. Don't archive every tiny tweak — only significant iterations.

## Wiki Links and Agent Interactions

Use `[[agent-name]]` to create explicit connections between agents that work together.

**In the interactions field:**
```yaml
interactions: [[requirements-analyst-agent]], [[design-validator-agent]]
```

**In prose:**
"The Requirements Analyst Agent hands off structured specifications to the [[design-architect-agent]], which validates architectural feasibility before passing to [[code-generator-agent]]."

These links form the workflow graph. They're not just documentation — they're the dependency map.

## Navigation: SDLC Phase Organization

### Two-Tier Structure

```
agent-registry (hub MOC)
├── requirements-phase → [analyst agents, story generators, ...]
├── design-phase → [architecture agents, design validators, ...]
├── development-phase → [code generators, reviewers, ...]
├── testing-phase → [test generators, QA agents, ...]
├── deployment-phase → [deployment orchestrators, ...]
└── operations-phase → [monitoring agents, incident responders, ...]
```

### Phase Overviews

Each SDLC phase has an overview MOC in `sdlc-phases/` that:
- Lists agents in that phase
- Explains the phase's purpose in the workflow
- Documents handoff points to adjacent phases

## Processing Pipeline

When designing a new agent:

### 1. Document (Capture)

Create initial note in `design-ideas/` with basic concept:
```yaml
---
description: Initial idea for [agent role]
status: draft
---

# [Agent Name] (draft)

What it would do, why we need it, initial thoughts.
```

### 2. Design (Full Profile)

When ready to formalize:
1. Create complete profile in `agents/` using the template
2. Fill all schema fields (responsibilities, interactions, inputs, outputs, metrics)
3. Write the current approach section
4. Set `status: active` when ready to test

### 3. Map Interactions

Connect the agent to the workflow:
- Add wiki links to agents it receives input from
- Add wiki links to agents it sends output to
- Update relevant phase overview MOCs
- Add to `agent-registry` hub

### 4. Track Metrics

As you test the agent:
- Update "What's Working" section with successes
- Update "What Needs Iteration" section with friction points
- Adjust `metrics` field based on observable outcomes
- Change `status` to `iterating` if refinement is needed

### 5. Version Snapshot (Major Changes Only)

When making significant changes:
1. Copy current note to `versions/[agent-name]-v[N].md`
2. Update `version` field in main note
3. Add new version to `version_history` array
4. Document what changed and why

## Schema and Validation

### Required Fields (Every Agent)

```yaml
description: # Purpose - what and why
sdlc_phase: # Which SDLC phase
version: # Current version (v1, v2, etc.)
responsibilities: # Array of core duties
interactions: # [[linked-agents]]
inputs: # What it receives
outputs: # What it produces
current_prompt: # System instruction
metrics: # Success criteria
status: # draft | active | iterating | deprecated
```

### Optional Fields

```yaml
version_history: # [[previous-versions]]
framework: # LangChain, CrewAI, custom, etc.
dependencies: # External tools or services
constraints: # Known limitations
examples: # Sample inputs/outputs
```

### Status Values

- `draft` — concept being explored, not ready for implementation
- `active` — tested and working, current design is solid
- `iterating` — being refined based on testing feedback
- `deprecated` — superseded by newer approach or removed from workflow

### Validation Gates

Before marking an agent profile complete:

**Completeness check:**
- [ ] All required fields populated
- [ ] `description` explains both WHAT and WHY
- [ ] `interactions` lists connected agents with [[wiki-links]]
- [ ] `metrics` are measurable (not vague)
- [ ] `current_prompt` is present (even if draft)

**Integration check:**
- [ ] Agent appears in relevant phase overview MOC
- [ ] Agent is linked to/from interacting agents
- [ ] Inputs and outputs align with connected agents

**Discovery check:**
- [ ] Future-you could find this by browsing the phase MOC
- [ ] The description makes the agent's purpose clear without reading the full note
- [ ] The agent name is descriptive enough to understand its role

## Maintenance

### Condition-Based Triggers

Run maintenance reviews when:

**Stuck agents (threshold: 3+)**
- Agents with `status: iterating` for 7+ days without updates
- Action: Review what's blocking iteration, decide to fix or deprecate

**Orphan agents (threshold: 2+)**
- Agent profiles with no incoming or outgoing `interactions` links
- Action: Either integrate into workflow or mark as deprecated

**Stale metrics (threshold: 5+ agents)**
- Agents where `metrics` field is still placeholder or never validated
- Action: Test and populate real success criteria

**Version sprawl (threshold: 5+ versions for one agent)**
- Agent with many archived versions
- Action: Review if the design has stabilized or needs fundamental rethink

### Health Check Command

Run `/arscontexta:health` to check:
- Schema compliance (all required fields present)
- Orphan detection (agents with no interactions)
- Dangling links (wiki links to non-existent agents)
- Status distribution (how many draft/active/iterating/deprecated)

## Self-Evolution and Methodology Knowledge

### ops/methodology/ - System Self-Knowledge

This vault maintains its own operational knowledge in `ops/methodology/`:

**What goes here:**
- Derivation rationale (why this configuration was chosen)
- Pipeline configuration decisions
- Vocabulary mappings
- Evolution history (how the system has changed)

**Querying methodology:**
- Browse: `ls ops/methodology/`
- Search by category: `rg '^category:' ops/methodology/`
- Ask the research graph: `/arscontexta:ask [question about your system]`

The `/arscontexta:ask` command queries the bundled 249-note research knowledge base backing your design, plus your local methodology folder. Use it when you want to understand why your system works the way it does, or get research-backed advice.

### ops/observations/ - Operational Learning

When you notice friction or learn something about how agents should work:

**Capture immediately in ops/observations/:**
```yaml
---
description: What you learned
category: friction | methodology | surprise | quality
observed: 2026-03-01
status: pending
---

# [observation as prose sentence]

[Details - what happened, what it means, what might change]
```

When observations accumulate (10+ pending), run `/arscontexta:rethink` to review and promote valuable learnings to the methodology folder or agent design patterns.

## Templates

Use templates to maintain consistency:

### Agent Profile Template

`templates/agent-profile.md` — scaffold for new agent profiles

### Phase Overview Template

`templates/phase-overview.md` — scaffold for SDLC phase MOCs

To use: copy template content, fill in fields, adjust as needed.

## Graph Analysis and Queries

### Agent Interaction Patterns

**Find orphan agents (no interactions):**
```bash
rg -l "^interactions: \[\]$" agents/
```

**Find agents by SDLC phase:**
```bash
rg "^sdlc_phase: requirements$" agents/
```

**Find agents by status:**
```bash
rg "^status: iterating$" agents/
```

**Count agents per phase:**
```bash
rg "^sdlc_phase:" agents/ | sort | uniq -c
```

**Find all agents that interact with a specific agent:**
```bash
rg "\[\[requirements-analyst-agent\]\]" agents/
```

### Version Tracking Queries

**Find all version snapshots:**
```bash
ls versions/
```

**Find agents with version history:**
```bash
rg "^version_history:" agents/
```

**Find latest version number for an agent:**
```bash
rg "^version:" agents/specific-agent.md
```

## Discovery-First Design

**Before creating any agent profile, ask: How will a future session find this?**

Every agent must be discoverable through:
1. **Phase browsing** — appears in relevant SDLC phase MOC
2. **Description clarity** — the YAML description explains purpose without reading full note
3. **Interaction links** — connected to agents that reference it

**Discovery failures to avoid:**
- Generic descriptions: "Handles design work" (what kind? for what purpose?)
- Missing phase assignment: can't be found by SDLC browsing
- Isolated agents: no interactions mean no path to discovery via workflow traversal

## Memory Type Routing

When capturing content, route to the right location:

| Content Type | Destination | Why |
|-------------|-------------|-----|
| New agent concept | `design-ideas/` | Low-friction capture |
| Complete agent profile | `agents/` | Living catalog |
| Agent version snapshot | `versions/` | Historical record |
| SDLC phase overview | `sdlc-phases/` | Navigation structure |
| Processing friction | `ops/observations/` | Operational learning |
| Design contradiction | `ops/tensions/` | Conflict tracking |
| Current work threads | `self/goals.md` | Session orientation |
| Time-bound follow-up | `ops/reminders.md` | Action tracking |
| Processing queue | `ops/queue/` | Task management |
| Session notes | `ops/sessions/` | Handoff context |

## Common Pitfalls

### Productivity Porn

Perfecting the agent catalog is not the goal — validating that agents actually work is. If you're spending more time refining documentation than testing agent behavior, recalibrate. The catalog serves the implementation.

**Prevention:** Time-box documentation. Document agents before testing, but keep it to essentials. Add detail based on what you learn from testing, not speculation.

### Temporal Staleness

Agent profiles that reference outdated prompts, deprecated frameworks, or old interaction patterns create confusion. Unlike research claims that age gracefully, agent designs have expiration dates.

**Prevention:** Use `status` field actively. Mark agents as `deprecated` when they're replaced. Update `current_prompt` field when prompts change. Version snapshot before major updates.

### Schema Erosion

Dense schema adds value through queryability, but only if maintained. Missing `metrics`, placeholder `interactions`, or inconsistent `status` values corrupt the catalog.

**Prevention:** Validation hooks catch missing required fields. Run `/arscontexta:validate` regularly. When a field becomes useless, remove it from the template — don't leave it as perpetual placeholder.

### Version Sprawl

Archiving every tiny change creates noise. Version history should capture major iterations (v1: initial design, v2: framework switch, v3: role restructure), not minor tweaks.

**Prevention:** Only version snapshot when changes are significant enough that comparing to the previous version provides insight. Prompt refinements within the same approach don't need versioning.

## System Evolution

### /arscontexta:architect - Configuration Advice

Get research-backed recommendations for system changes:
```
/arscontexta:architect
```

Use when:
- The current structure feels misaligned with how you're working
- You're considering adding new capabilities (semantic search, automation tiers)
- Friction patterns suggest configuration drift

### /arscontexta:rethink - Review Accumulated Learnings

Process observations and tensions:
```
/arscontexta:rethink
```

Use when:
- ops/observations/ has 10+ pending items
- ops/tensions/ has 5+ pending conflicts
- You want to review what the system has learned about its own operation

### /arscontexta:remember - Capture Methodology Corrections

Immediately capture operational corrections:
```
/arscontexta:remember [what you learned]
```

Use when:
- You discover a better way to structure agent profiles
- You notice a pattern in successful vs. unsuccessful agent designs
- You want to document a design principle for future reference

## Infrastructure Routing

Questions about methodology, configuration, or system capabilities route to:

**Bundled research knowledge (249 notes):**
- `/arscontexta:ask "Why use flat organization instead of folders?"`
- `/arscontexta:ask "When should I version snapshot an agent?"`

**Local methodology folder:**
- Browse `ops/methodology/` for derivation rationale
- Query with grep: `rg "granularity" ops/methodology/`

**Configuration changes:**
- Edit `ops/config.yaml` for dimension adjustments
- Use `/arscontexta:architect` for guided changes

## Self-Extension Blueprints

### Adding New Skills

Skills live in `.claude/skills/[skill-name]/SKILL.md`. To add custom processing:

1. Create skill directory
2. Write SKILL.md with clear instructions
3. Test via `/[skill-name]`
4. Document in this context file if it becomes core workflow

### Adding New Hooks

Hooks live in `.claude/hooks/[hook-name].sh` and are configured in `.claude/settings.json`.

Current hooks:
- `session-orient.sh` — loads context at session start
- `validate-note.sh` — checks schema after Write operations
- `auto-commit.sh` — commits changes to git
- `session-capture.sh` — saves session logs at session end

### Adding New Query Scripts

Graph queries live in `ops/queries/`. To add new agent analysis queries:

1. Identify the pattern you want to detect
2. Write ripgrep-based query script
3. Document in "Graph Analysis and Queries" section above
4. Add to maintenance routine if valuable

## Pipeline Compliance

**NEVER write directly to `agents/`.** Route through the processing pipeline:

1. Capture in `design-ideas/` first (low friction)
2. Design when ready (move to `agents/` with full schema)
3. Validate before marking complete
4. Map interactions after creation

Direct writes bypass validation and create schema drift.

## Derivation Rationale

**Why this configuration:**

This system was derived for **agent catalog documentation** — tracking AI agent roles in an SDLC-based development team. The configuration optimizes for iteration, versioning, and interaction mapping.

**Key decisions:**
- **Moderate granularity:** One note per agent role (not atomic decomposition, not monolithic docs)
- **Flat organization:** Agents connected via wiki links and phase MOCs, not folder silos
- **Dense schema:** Agent profiles have natural structure (prompts, metrics, interactions)
- **2-tier navigation:** Hub → phase MOCs → agents (sufficient for 5-20 agents)
- **Explicit linking:** Agent-to-agent interactions are the workflow graph
- **Version snapshots:** Hybrid model balances "current state" with "evolution history"

**Tradition influence:** Custom configuration blending PM decision tracking (dense schema, versioning) with design catalog patterns (entity-centric MOCs, interaction mapping).

---

**Your vault is a living blueprint.** Every agent profile, every interaction link, every version snapshot documents how the AI development team should work. The catalog informs implementation — not the reverse.
