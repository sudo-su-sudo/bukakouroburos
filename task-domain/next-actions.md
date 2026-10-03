# Next Actions

Updated: 2026-10-03T10:35:02Z after cycle 6 (live snapshot on main, HN titles resolved).

**Durable store:** `github.com/sudo-su-sudo/compounding-agency`  
Every cycle: BOOTSTRAP from GitHub → execute → SHUTDOWN push. Local files alone die.

## Priority queue

1. **TAKE** wire-snapshot-freshness: `eval-score.py` should dock `outward_freshness` when `knowledge/live-snapshot.json` is missing or older than 36h. That is why this file was absent for a cycle.
2. optional outward primitive from x-signal-ledger (hindsight / openrig / univer) — not a skill clone
3. re-run `scripts/skill-consolidator.py`; treat a rise in alias_count above 18 as a failed cycle
4. NEVER create another recursive/compound/task-domain skill

## Load set (do not load the 18 aliases)

capability-growth-core, capability-index, daily-compound-ignition, knowledge-compounder, leverage-maximizer, recursive-task-domain

## Zero-brief commands

```
python3 /home/workdir/artifacts/scripts/refresh-live-snapshot.py
python3 /home/workdir/artifacts/scripts/eval-score.py
python3 /home/workdir/artifacts/scripts/skill-consolidator.py
python3 /root/.grok/server-skills/recursive-task-domain/scripts/web-brief.py --live
```

## Last scores

memory_quality=1.0 sprawl_ratio=0.6 composite=0.825 live_snapshot_ok=4/5 hn_titles=8

## Ignition

Automation: `fb6b558c-e940-4941-99c2-3c2cd4eaec99` @ 06:30 America/New_York
