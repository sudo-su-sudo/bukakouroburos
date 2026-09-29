# Next Actions

Updated: 2026-09-29T12:55:00Z after persistence fix (cycle 1b).

**Durable store:** `github.com/sudo-su-sudo/compounding-agency`  
Every cycle: BOOTSTRAP from GitHub → execute → SHUTDOWN push. Local files alone die.

## Priority queue

1. **VERIFY** next automated run loads `cycle_count >= 1` from GitHub (no empty-artifacts re-bootstrap)
2. **TAKE** `x-signal-ledger` — X harvest → append-only signal under task-domain/ or knowledge/
3. **TAKE** `eval-harness` — write `task-domain/eval.json`, push
4. skill-sprawl-kill (30 overlapping skills)
5. refresh live snapshot if >7d stale
6. NEVER create another recursive/compound/task-domain skill

## Zero-brief commands

```
# After BOOTSTRAP pull into /home/workdir/artifacts/task-domain/
python3 /home/workdir/.grok/skills/recursive-task-domain/scripts/outward-harvest.py --rank /home/workdir/artifacts/task-domain/candidates.json
python3 /home/workdir/.grok/skills/recursive-task-domain/scripts/web-brief.py --live
```

## Ignition

Automation: `fb6b558c-e940-4941-99c2-3c2cd4eaec99` @ 06:30 America/New_York
