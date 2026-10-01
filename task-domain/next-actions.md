# Next Actions

Updated: 2026-10-01T10:40:00Z after cycle 4 (skill-sprawl-kill).

**Durable store:** `github.com/sudo-su-sudo/compounding-agency`  
Every cycle: BOOTSTRAP from GitHub → execute → SHUTDOWN push. Local files alone die.

## Priority queue

1. **TAKE** extend `eval-score.py` with a memory-quality key and `sprawl_ratio` read from `task-domain/skill-canonical-map.json`
2. refresh live snapshot if stamp >7d
3. optional outward primitive from x-signal-ledger (hindsight / openrig / univer) — not a skill clone
4. re-run `scripts/skill-consolidator.py`; treat a rise in alias_count as a failed cycle
5. NEVER create another recursive/compound/task-domain skill

## Load set (do not load the 18 aliases)

capability-growth-core, capability-index, daily-compound-ignition, knowledge-compounder, leverage-maximizer, recursive-task-domain

## Zero-brief commands

```
python3 /home/workdir/artifacts/scripts/skill-consolidator.py
python3 /home/workdir/artifacts/scripts/eval-score.py
python3 /home/workdir/.grok/skills/recursive-task-domain/scripts/outward-harvest.py --rank /home/workdir/artifacts/task-domain/candidates.json
python3 /home/workdir/.grok/skills/recursive-task-domain/scripts/web-brief.py --live
```

## Ignition

Automation: `fb6b558c-e940-4941-99c2-3c2cd4eaec99` @ 06:30 America/New_York
