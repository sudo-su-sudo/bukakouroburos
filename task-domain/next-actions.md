# Next Actions

Updated: 2026-10-15T10:35:19Z after cycle 18 (refresh-if-docked closed stale dock).

**Durable store:** `github.com/sudo-su-sudo/compounding-agency`  
Every cycle: BOOTSTRAP from GitHub -> execute -> SHUTDOWN push. Local files alone die.

## Priority queue

1. **TAKE** skill-consolidator --max-aliases 18 --prior-map.
2. NEVER create another recursive/compound/task-domain skill.
3. re-score shadow aliases after any skill change.

## Load set (do not load the 18 aliases or the 3 shadows)

capability-growth-core, capability-index, daily-compound-ignition, knowledge-compounder, leverage-maximizer, recursive-task-domain

## Zero-brief commands

```
python3 /home/workdir/artifacts/scripts/skill-consolidator.py --max-aliases 18 --prior-map task-domain/skill-canonical-map.json
python3 /home/workdir/artifacts/scripts/shadow-alias-scorer.py
python3 /home/workdir/artifacts/scripts/refresh-if-docked.py
python3 /home/workdir/artifacts/scripts/eval-score.py
python3 /home/workdir/artifacts/scripts/pull-outward-primitive.py --recall hamilton
```

## Last scores

Sprawl gate: alias_count=18, sprawl_gate=pass. Shadow: shadow_alias_count=3.
Snapshot: generated_at≈2026-10-15T10:35Z, fresh, next 36h ~2026-10-16T22:35Z.

## Ignition

Automation: `fb6b558c-e940-4941-99c2-3c2cd4eaec99` @ 06:30 America/New_York
