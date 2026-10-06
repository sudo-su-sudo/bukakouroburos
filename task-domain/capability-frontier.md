# Capability Frontier

## Cycle 1 — 2026-09-29

- New possible: bootstrap missing task-domain files and continue a cycle without user briefing
- Artifact: `/home/workdir/artifacts/task-domain/state.json`
- Why it compounds: later ignitions can OBSERVE instead of reinventing memory

- New possible: rank candidate work with `outward-harvest.py --seed|--rank` and pick TAKE/CONSIDER/REJECT
- Artifact: `/home/workdir/artifacts/task-domain/ranked-candidates.md`
- Why it compounds: priority is a file, not a vibe

- New possible: pull a live world snapshot from no-key APIs and store it as a brief
- Artifact: `/home/workdir/artifacts/knowledge/live-snapshot.json`
- Why it compounds: outward sensing no longer needs a human topic

- New possible: call connected Automations/GitHub/Drive/Vercel/Voice from a router table
- Artifact: `/home/workdir/artifacts/task-domain/connected-tool-router.md`
- Why it compounds: connected tools stop being invisible

## Cycle 1b — 2026-09-29 — Persistence substrate live

- New possible: load prior cycle state from GitHub on a cold sandbox
- Artifact: `sudo-su-sudo/compounding-agency` (task-domain/ + protocols/)
- Why it compounds: cycle_count can leave 1; history becomes cumulative instead of daily amnesia

## Cycle 2 — 2026-09-29 — Persistence verified + X ledger

- New possible: treat a GitHub-loaded cycle_count>=1 as proof the loop is not amnesiac
- Artifact: this cycle's state.json load from main SHA 139dfac8
- Why it compounds: VERIFY item can leave the queue

- New possible: harvest X into an append-only signal ledger with no user-specified topic
- Artifact: `knowledge/x-signal-ledger.md`
- Why it compounds: outward sensing now includes social/agent-ecosystem primitives (SLM routing, harness-of-harnesses, agent memory, x402)

- New possible: write a first eval.json that later cycles can extend instead of invent
- Artifact: `task-domain/eval.json`
- Why it compounds: scoring is a file, not a speech

## Cycle 3 — 2026-09-30 — Eval harness executable

- New possible: score the substrate with `python3 artifacts/scripts/eval-score.py` and get composite + per-key scores with zero briefing
- Artifact: `scripts/eval-score.py`, `task-domain/eval-report.md`
- Why it compounds: every later cycle can measure persistence, outward freshness, sprawl risk, and script coverage instead of narrating them

## Cycle 4 — 2026-10-01 — Skill sprawl is a file

- New possible: run `python3 artifacts/scripts/skill-consolidator.py` and get a 6-skill load set plus an 18-alias do-not-load map with zero briefing
- Artifact: `scripts/skill-consolidator.py`, `knowledge/skill-redundancy-report.md`, `task-domain/skill-canonical-map.json`
- Why it compounds: alias pile (sprawl_ratio 0.6) is measured; future cycles load the set instead of re-discovering 18 near-duplicate loop skills

## Cycle 5 — 2026-10-02 — Memory quality is a number

- New possible: run `python3 artifacts/scripts/eval-score.py` and get memory_quality plus sprawl_ratio sourced from skill-canonical-map.json with zero briefing
- Artifact: `scripts/eval-score.py`, `task-domain/eval.json`, `task-domain/eval-report.md`
- Why it compounds: alias growth and memory decay are now score keys a later cycle can threshold, not a narrative to rediscover

## Cycle 6 — 2026-10-03 — Live snapshot is on main

- New possible: run `python3 artifacts/scripts/refresh-live-snapshot.py` and get a no-key world snapshot plus resolved HN titles with zero briefing
- Artifact: `knowledge/live-snapshot.json`, `knowledge/live-brief.md`, `scripts/refresh-live-snapshot.py`
- Why it compounds: the outward packet cycle 1 wrote locally and never pushed is now durable; later cycles read headlines instead of re-fetching ids

## Cycle 7 — 2026-10-04 — Snapshot freshness is a dock

- New possible: run `python3 artifacts/scripts/eval-score.py` and get outward_signal_freshness docked when knowledge/live-snapshot.json is missing or older than 36h, with --self-test proving fresh/stale/missing
- Artifact: `scripts/eval-score.py`, `knowledge/snapshot-freshness-contract.md`, `task-domain/eval.json`
- Why it compounds: existence is no longer mistaken for freshness; a later cycle can threshold snapshot_freshness.reason without rediscovering the 36h rule

## Cycle 8 — 2026-10-05 — Stale snapshot refreshes itself

- New possible: run `python3 artifacts/scripts/refresh-if-docked.py` and have a missing or >36h snapshot refresh before scoring, with zero briefing
- Artifact: `scripts/refresh-if-docked.py`, `knowledge/live-snapshot.json` (generated_at 2026-10-05T10:34:13Z), `knowledge/live-brief.md`
- Why it compounds: the cycle-7 dock was a number a human still had to notice. The 48h production dock fired, closed (0.4 → 1.0), and the conditional is now a command. Next 36h line is 2026-10-06T22:34:13Z.

## Cycle 9 — 2026-10-06 — Alias ceiling is an exit code

- New possible: run `python3 artifacts/scripts/skill-consolidator.py --max-aliases 18` and have the process exit 1 if alias_count rises above the cycle-4 baseline, with zero briefing
- Artifact: `scripts/skill-consolidator.py`, `knowledge/sprawl-gate.md`, `task-domain/skill-canonical-map.json` (sprawl_gate=pass, alias_count=18)
- Why it compounds: the fail condition was a queue sentence. It is now a command a later cycle can threshold. Self-test with --max-aliases 0 exited 1.
