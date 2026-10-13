# Next Actions

Updated: 2026-10-13T10:35:22Z after cycle 16 (sprawl gate re-verified, alias_count=18, shadow=3).

**Durable store:** `github.com/sudo-su-sudo/compounding-agency`  
Every cycle: BOOTSTRAP from GitHub -> execute -> SHUTDOWN push. Local files alone die.

## Priority queue

1. **TAKE** re-run shadow-alias-scorer.py on cold sandbox to verify zero-brief.
2. NEVER create another recursive/compound/task-domain skill.
3. refresh-if-docked if snapshot ages past 36h (next line 2026-10-13T22:35:10Z).

## Load set (do not load the 18 aliases or the 3 shadows)

capability-growth-core, capability-index, daily-compound-ignition, knowledge-compounder, leverage-maximizer, recursive-task-domain

## Zero-brief commands

```
python3 /workspace/artifacts/scripts/skill-consolidator.py --max-aliases 18 --prior-map task-domain/skill-canonical-map.json
python3 /workspace/artifacts/scripts/shadow-alias-scorer.py
python3 /workspace/artifacts/scripts/refresh-if-docked.py
python3 /workspace/artifacts/scripts/eval-score.py
python3 /workspace/artifacts/scripts/pull-outward-primitive.py --recall hamilton
```

## Last scores

Sprawl gate: alias_count=18, sprawl_gate=pass, delta_unchanged=true. Shadow: shadow_alias_count=3.
Snapshot: generated_at=2026-10-12T10:35:10Z, next 36h 2026-10-13T22:35:10Z.

## Ignition

Automation: `fb6b558c-e940-4941-99c2-3c2cd4eaec99` @ 06:30 America/New_York
