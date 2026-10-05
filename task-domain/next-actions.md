# Next Actions

Updated: 2026-10-05T10:34:46Z after cycle 8 (refresh-if-docked fired at 48.01h).

**Durable store:** `github.com/sudo-su-sudo/compounding-agency`  
Every cycle: BOOTSTRAP from GitHub → execute → SHUTDOWN push. Local files alone die.

## Priority queue

1. **TAKE** re-run `scripts/skill-consolidator.py`. Fail the cycle if alias_count rises above 18.
2. If `snapshot_freshness.reason` is not `fresh`, run `python3 scripts/refresh-if-docked.py` before scoring. Snapshot generated_at 2026-10-05T10:34:13Z crosses 36h at 2026-10-06T22:34:13Z.
3. optional outward primitive from x-signal-ledger (hindsight / openrig / univer) — not a skill clone
4. NEVER create another recursive/compound/task-domain skill

## Load set (do not load the 18 aliases)

capability-growth-core, capability-index, daily-compound-ignition, knowledge-compounder, leverage-maximizer, recursive-task-domain

## Zero-brief commands

```
python3 /home/workdir/artifacts/scripts/refresh-if-docked.py
python3 /home/workdir/artifacts/scripts/eval-score.py --self-test
python3 /home/workdir/artifacts/scripts/eval-score.py
python3 /home/workdir/artifacts/scripts/refresh-live-snapshot.py
python3 /home/workdir/artifacts/scripts/skill-consolidator.py
```

## Last scores

Pre-refresh: age 48.01h, dock=0.4, outward=0.4, composite=0.8.
Post-refresh: age 0.01h, dock=0.0, outward=1.0, composite=0.9.

## Ignition

Automation: `fb6b558c-e940-4941-99c2-3c2cd4eaec99` @ 06:30 America/New_York
