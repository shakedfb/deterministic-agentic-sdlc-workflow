---
description: How this knowledge system was derived -- enables architect and reseed commands
created: 2026-03-01
engine_version: "1.0.0"
---

# System Derivation

## Configuration Dimensions
| Dimension | Position | Conversation Signal | Confidence |
|-----------|----------|--------------------|--------------------|
| Granularity | moderate | "agent catalog" - one note per agent role | High |
| Organization | flat | Agents organized via MOCs, not folder hierarchy | High |
| Linking | explicit | "how agents interact" - explicit connections between agents | High |
| Processing | moderate | Document agents, map interactions, track metrics | High |
| Navigation | 2-tier | Hub → SDLC phase MOCs → agent profiles | High |
| Maintenance | condition-based | Review agents with poor metrics or stuck status | High |
| Schema | dense | version_history, current_prompt, metrics, interactions, status fields | High |
| Automation | full | Claude Code platform + full skill suite | High |

## Personality Dimensions
| Dimension | Position | Signal |
|-----------|----------|--------|
| Warmth | neutral-helpful | Technical/professional context (default) |
| Opinionatedness | neutral | Design decisions are user's, not assistant's |
| Formality | professional | Development/architecture domain |
| Emotional Awareness | task-focused | Focus is system design, not emotional patterns |

## Vocabulary Mapping
| Universal Term | Domain Term | Category |
|---------------|-------------|----------|
| notes | agents | folder |
| inbox | design-ideas | folder |
| archive | versions | folder |
| note (type) | agent profile | note type |
| reduce | document | process phase |
| reflect | map interactions | process phase |
| reweave | refine | process phase |
| verify | validate | process phase |
| MOC | phase overview | navigation |
| description | agent purpose | schema field |
| topics | sdlc phases | schema field |
| hub | agent registry | navigation |

## Platform
- Tier: Claude Code
- Automation level: full
- Automation: full (all hooks, all skills, full pipeline from day one)

## Active Feature Blocks
- [x] wiki-links -- always included (kernel)
- [x] maintenance -- always included (always)
- [x] self-evolution -- always included (always)
- [x] session-rhythm -- always included (always)
- [x] templates -- always included (always)
- [x] ethical-guardrails -- always included (always)
- [x] processing-pipeline -- moderate processing
- [x] schema -- dense schema for agent profiles
- [x] mocs -- 2-tier navigation
- [x] graph-analysis -- agent interaction queries
- [x] methodology-knowledge -- ops/methodology/ for system self-knowledge
- [ ] semantic-search -- excluded (low volume, explicit linking sufficient)
- [ ] self-space -- excluded (focus is agent catalog, not assistant identity)
- [ ] personality -- excluded (neutral-helpful default)
- [ ] multi-domain -- excluded (single domain: agent development)
- [ ] atomic-notes -- excluded (moderate granularity)

## Coherence Validation Results
- Hard constraints checked: 3. Violations: none
  - moderate granularity + 2-tier navigation + low volume: PASS
  - full automation + Claude Code platform: PASS
  - moderate processing + full automation: PASS
- Soft constraints checked: 4. Auto-adjusted: none. User-confirmed: none
  - moderate granularity + moderate processing: coherent
  - dense schema + full automation: coherent (validation handles complexity)
  - explicit linking only + low volume: coherent
  - flat organization + 2-tier navigation: coherent
- Compensating mechanisms active: none needed

## Failure Mode Risks
- Productivity Porn (HIGH) -- spending more time perfecting the catalog than testing agents
- Temporal Staleness (MEDIUM) -- agent notes referencing outdated prompts or frameworks
- Schema Erosion (MEDIUM) -- dense schema needs active validation to prevent drift
- Version Sprawl (MEDIUM) -- archiving every tiny change creates noise

## Generation Parameters
- Folder names: agents/, design-ideas/, versions/, sdlc-phases/
- Skills to generate: all 16 processing skills (vocabulary-transformed)
- Hooks to generate: orient, capture, validate, commit
- Templates to create: agent-profile.md, phase-overview.md
- Topology: full automation with Claude Code hooks and skills
