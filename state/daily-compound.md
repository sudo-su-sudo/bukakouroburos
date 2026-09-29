# Daily Compound Log

## 2026-09-29
- Measurable improvement: durable GitHub persistence path restored and wired into ignition prompt.
- Before: every automation run = Cycle 1 on empty disk.
- After: BOOTSTRAP pulls task-domain state; SHUTDOWN must commit or cycle fails.
