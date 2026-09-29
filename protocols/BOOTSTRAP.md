# BOOTSTRAP PROTOCOL — MANDATORY FIRST ACTION

On every ignition (automation or human), before any other work:

1. Load capability-growth-core.
2. Pull durable state from GitHub repo `sudo-su-sudo/compounding-agency` (branch `main`):
   - `task-domain/state.json`
   - `task-domain/next-actions.md`
   - `task-domain/instance-history.md`
   - `task-domain/capability-frontier.md`
   - `task-domain/log.md`
   - `state/ledger.md`
   - `protocols/BOOTSTRAP.md` and `protocols/SHUTDOWN.md`
3. Write those files into `/home/workdir/artifacts/task-domain/` (and keep ledger under a local copy if useful).
4. If `state.json` is missing or `cycle_count` is absent, treat as cold start — but still use this repo as the write target.
5. Announce one line: cycle_count, last_cycle, top priority_queue item.
6. Only then GENERATE / EXECUTE.

The sandbox is ephemeral. **This repository is the only memory.**
Never assume prior knowledge from chat alone.
