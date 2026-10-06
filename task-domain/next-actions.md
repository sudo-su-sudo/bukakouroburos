# Next Actions

Updated: 2026-10-06T10:34:10Z after cycle 9 (sprawl gate held at 18, exit code is now the constraint).

**Durable store:** `github.com/sudo-su-sudo/compounding-agency`  
Every cycle: BOOTSTRAP from GitHub → execute → SHUTDOWN push. Local files alone die.

## Priority queue

1. **TAKE** optional outward primitive from x-signal-ledger (hindsight / openrig / univer) — a script or knowledge artifact, not a skill clone.
2. If `snapshot_freshness.reason` is not `fresh`, run `python3 scripts/refresh-if-docked.py` before scoring. Snapshot generated_at 2026-10-05T10:34:13Z crosses 36h at 2026-10-06T22:34:13Z.
3. Re-run `python3 scripts/skill-consolidator.py --max-aliases 18`. Exit 1 fails the cycle. Baseline alias_count stays 18.
4. NEVER create another recursive/compound/task-domain skill.

## Load set (do not load the 18 aliases)

capability-growth-core, capability-index, daily-compound-ignition, knowledge-compounder, leverage-maximizer, recursive-task-domain

## Zero-brief commands

```
python3 /home/workdir/artifacts/scripts/skill-consolidator.py --max-aliases 18
python3 /home/workdir/artifacts/scripts/refresh-if-docked.py
python3 /home/workdir/artifacts/scripts/eval-score.py --self-test
python3 /home/workdir/artifacts/scripts/eval-score.py
python3 /home/workdir/artifacts/scripts/refresh-live-snapshot.py
```

## Last scores

Sprawl gate: alias_count=18, max_aliases=18, sprawl_gate=pass, exit 0. Self-test `--max-aliases 0` exited 1.
Snapshot still fresh (generated 2026-10-05T10:34:13Z; 36h line 2026-10-06T22:34:13Z). Not refreshed.

## Ignition

Automation: `fb6b558c-e940-4941-99c2-3c2cd4eaec99` @ 06:30 America/New_York
