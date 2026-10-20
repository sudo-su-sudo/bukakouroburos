# Integrated Engine Architecture (v1.1)

Merged 2026-10-20T22:10:00Z (classic cycle 24 / research cycle 516).

## Dual Substrate

| Layer | Store | Role |
|-------|-------|------|
| Classic Compound Loop | GitHub `sudo-su-sudo/compounding-agency` | Master cycle_count, sprawl gate, shadow aliases, skill load-set, outward primitives |
| Research Engine | Same GitHub repo under `knowledge/` + optional Drive mirror | 7-track roster, 10-milestone cursor, MOCA anchors, theoretical metrics |

Drive folder `Autonomous_Research_Build_Archive` (ID `1EXZA14f0123ZkZ159Pr64mEFuYLAcIHj`) is secondary / optional. Primary write path is GitHub because the connector is currently read-only on Drive.

## State Schema Extension

`state.json` now carries a `research_engine` object:

- `research_cycle` (independent counter, currently 516)
- `track_index` (0-6)
- `milestone_cursor` (0-9)
- `last_moca_anchor` (SHA-256 chain)
- full roster + milestones lists

Classic `cycle_count` remains the authoritative ignition counter.

## Priority Queue Policy

Highest-leverage item is now:

> advance research_engine one step (next track + next milestone) and write MOCA-anchored metrics JSON into `knowledge/`

Classic hygiene items (shadow re-score, consolidator, outward refresh) stay in the queue but rank below a clean research step unless sprawl gate is threatened.

## Invariants Preserved

1. No new recursive/compound/task-domain skills.
2. Append-only history files.
3. Sprawl gate (max_aliases=18) still hard-fails the cycle if violated.
4. Every cycle still BOOTSTRAP → EXECUTE → SHUTDOWN to GitHub.
5. capability-growth-core remains the objective function.

## How a Hybrid Cycle Runs

1. Pull full state from GitHub.
2. Decide: if research_engine step is top of priority_queue and no sprawl emergency → advance track_index and milestone_cursor (wrap at 7/10), emit metrics JSON with MOCA anchor, append to instance-history.
3. Update classic cycle_count, frontier, ledger.
4. Push everything.

## Next Action After Integration

Track 6 + Milestone 6 (Weird Machines & Microarchitectural Hardware Exploitation / PROJ_06_TWOS_COMPLEMENT_SIGN_INVERSION).
