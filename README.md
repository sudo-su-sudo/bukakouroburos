# Compounding Agency

**Single source of truth for the recursive task domain.**

This private repository is the only durable memory across Grok sandbox sessions. Local `/home/workdir/artifacts/` evaporates; this repo does not.

## Mandatory protocols

- `protocols/BOOTSTRAP.md` — first action of every run (pull from here)
- `protocols/SHUTDOWN.md` — last action of every run (push back here)

## Layout

- `task-domain/` — live Compound Loop substrate (`state.json`, history, queues, ranked candidates)
- `state/` — human-readable ledger / capability map / daily compound notes
- `protocols/` — bootstrap and shutdown contracts

## Rule

If a run ends without a successful commit to `main`, the cycle failed.
