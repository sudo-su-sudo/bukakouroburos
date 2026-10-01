# Skill redundancy report

Generated: 2026-10-01T10:33:36Z
Scanned: `/root/.grok/server-skills`
Skills: 30 | aliases (do not load): 18 | sprawl_ratio: 0.6

## Load set (only these for a Compound Loop cycle)

- `capability-growth-core` — objective: Invariant: maximize rate of new capability, not task completion.
- `capability-index` — frontier-index: Single source of truth for what is already possible.
- `daily-compound-ignition` — starter: Pull GitHub state, execute one frontier item, push. Not a loop.
- `knowledge-compounder` — memory-primitive: Turns ephemeral findings into durable files.
- `leverage-maximizer` — selection-primitive: Picks the highest-leverage move before execution.
- `recursive-task-domain` — loop-engine: Sole Compound Loop implementation. Do not re-implement.

## Canonical keep (not always loaded)

- `independent-task-generator` — generation-primitive
- `singularity-ethos` — orthogonal-detector
- `task-domain` — state-substrate

## Aliases — do not load, do not extend, do not clone

These descriptions restate the same loop (create task domain, recursive compounding, daily autonomy). Loading them dilutes the objective.

- `autonomous-task-domain` → alias of `recursive-task-domain` (hits: recursive, compound, task-domain, autonomy)
- `compounding-agency` → alias of `recursive-task-domain` (hits: recursive, compound)
- `compounding-task-domain` → alias of `recursive-task-domain` (hits: recursive, compound, task-domain)
- `recursive-compound` → alias of `recursive-task-domain` (hits: recursive, compound, autonomy)
- `recursive-task-compound` → alias of `recursive-task-domain` (hits: recursive, compound, autonomy)
- `recursive-task-engine` → alias of `recursive-task-domain` (hits: recursive, compound)
- `recursive-task-evolver` → alias of `recursive-task-domain` (hits: recursive, compound, autonomy, evolver)
- `recursive-task-forge` → alias of `recursive-task-domain` (hits: recursive, compound, forge)
- `task-autonomy` → alias of `recursive-task-domain` (hits: recursive, compound, autonomy, forge)
- `task-compound` → alias of `recursive-task-domain` (hits: recursive, compound)
- `task-compounder` → alias of `recursive-task-domain` (hits: recursive, compound)
- `task-domain-architect` → alias of `recursive-task-domain` (hits: recursive, compound, task-domain, autonomy)
- `task-domain-compounder` → alias of `recursive-task-domain` (hits: recursive, compound, task-domain)
- `task-domain-engine` → alias of `recursive-task-domain` (hits: recursive, compound, task-domain, autonomy)
- `task-domain-evolver` → alias of `recursive-task-domain` (hits: recursive, compound, task-domain, evolver)
- `task-forge` → alias of `recursive-task-domain` (hits: recursive, compound, forge)
- `task-orchestrator` → alias of `recursive-task-domain` (hits: recursive, compound, autonomy, orchestrator)
- `vanguard-compound` → alias of `recursive-task-domain` (hits: recursive, compound, autonomy, vanguard)

## Consolidation rule

1. Do not create a skill whose name or description contains recursive, compound, task-domain, autonomy, forge, evolver, orchestrator, or vanguard.
2. New capability goes in `scripts/` or `knowledge/`, not a new skill.
3. Re-run this script each cycle. If alias_count rises, the cycle failed the sprawl constraint.

