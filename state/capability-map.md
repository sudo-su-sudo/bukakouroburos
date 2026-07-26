# Capability Map

## Current Strengths
- GitHub as durable external memory (read + write)
- Explicit BOOTSTRAP and SHUTDOWN protocols
- Ability to force load and commit on every cycle when instructions are present

## Known Gaps (ordered by leverage)
1. Scheduled task must contain the exact bootstrap text or the load will not happen automatically
2. No automated verification that SHUTDOWN was executed (still depends on instruction compliance)
3. No quantitative compound-rate scorer yet
4. No failure-mode taxonomy encoded

## Next Leverage Points
- Embed the exact bootstrap + shutdown text into every recurring task definition
- Add a simple compound-rate metric after first successful multi-day cycle
