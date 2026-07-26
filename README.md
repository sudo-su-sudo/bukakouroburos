# Compounding Agency

**Single source of truth for the recursive task domain.**

This repository is the only durable memory. Every scheduled task must load from it at initialization and commit back to it before termination.

## Mandatory Protocols

- `protocols/BOOTSTRAP.md` — first action of every run
- `protocols/SHUTDOWN.md` — last action of every run
- `state/ledger.md` — append-only history
- `state/capability-map.md` — current strengths, gaps, leverage points
- `state/daily-compound.md` — forced measurable improvement log

If a run ends without a commit, the cycle is considered failed.
