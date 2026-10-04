# Next Actions

Updated: 2026-10-04T10:35:46Z after cycle 7 (snapshot freshness dock wired).

**Durable store:** `github.com/sudo-su-sudo/compounding-agency`  
Every cycle: BOOTSTRAP from GitHub → execute → SHUTDOWN push. Local files alone die.

## Priority queue

1. **TAKE** if `task-domain/eval.json` snapshot_freshness.reason is not `fresh`, run `scripts/refresh-live-snapshot.py` before scoring. Snapshot generated_at 2026-10-03T10:33:36Z crosses 36h at 2026-10-04T22:33:36Z.
2. re-run `scripts/skill-consolidator.py`; treat a rise in alias_count above 18 as a failed cycle
3. optional outward primitive from x-signal-ledger (hindsight / openrig / univer) — not a skill clone
4. NEVER create another recursive/compound/task-domain skill

## Load set (do not load the 18 aliases)

capability-growth-core, capability-index, daily-compound-ignition, knowledge-compounder, leverage-maximizer, recursive-task-domain

## Zero-brief commands

```
python3 /home/workdir/artifacts/scripts/eval-score.py --self-test
python3 /home/workdir/artifacts/scripts/eval-score.py
python3 /home/workdir/artifacts/scripts/refresh-live-snapshot.py
python3 /home/workdir/artifacts/scripts/skill-consolidator.py
```

## Last scores

See task-domain/eval-report.md after this cycle. Live snapshot age was 24.03h, dock=0.0.

## Ignition

Automation: `fb6b558c-e940-4941-99c2-3c2cd4eaec99` @ 06:30 America/New_York
