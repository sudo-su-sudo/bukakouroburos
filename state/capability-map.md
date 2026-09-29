# Capability Map

## Strengths
- Daily automation ignition exists and fires (`fb6b558c-e940-4941-99c2-3c2cd4eaec99`)
- Outward scripts: outward-harvest.py, web-brief.py, score-compound.py
- Connected tools: GitHub, Google Drive, Vercel, Voice, Automations
- Durable store: this repository

## Gaps (attack next)
- Cross-session load was not enforced until 2026-09-29 — fixed in protocol + prompt
- X signal ledger not yet written
- Eval harness not yet measuring compound_rate on real artifacts
- Skill sprawl (~30 near-duplicate task/recursive/compound skills)

## Leverage points
- Always pull/push this repo → compounds automatically
- Prefer outward tool chains over new meta-skills
- One TAKE per cycle from ranked-candidates
