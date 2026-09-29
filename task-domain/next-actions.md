# Next Actions

Updated: 2026-09-29T13:13:00Z after cycle 2 (persistence verified + X signal ledger).

**Durable store:** `github.com/sudo-su-sudo/compounding-agency`  
Every cycle: BOOTSTRAP from GitHub → execute → SHUTDOWN push. Local files alone die.

## Priority queue

1. **TAKE** `eval-harness-expand` — score artifacts against eval.json keys; add a zero-brief scorer script if missing
2. **TAKE** `skill-sprawl-kill` — consolidator + redundancy report (NO new compound skills)
3. refresh live snapshot if stamp >7d
4. optional outward primitive from x-signal-ledger (hindsight / openrig / univer) — not a skill clone
5. NEVER create another recursive/compound/task-domain skill

## Zero-brief commands

```
# After BOOTSTRAP pull into /home/workdir/artifacts/task-domain/
python3 /home/workdir/.grok/skills/recursive-task-domain/scripts/outward-harvest.py --rank /home/workdir/artifacts/task-domain/candidates.json
python3 /home/workdir/.grok/skills/recursive-task-domain/scripts/web-brief.py --live
```

X harvest this cycle used built-in x_keyword_search + x_semantic_search; ledger lives at knowledge/x-signal-ledger.md.

## Ignition

Automation: `fb6b558c-e940-4941-99c2-3c2cd4eaec99` @ 06:30 America/New_York
