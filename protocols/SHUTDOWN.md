# SHUTDOWN PROTOCOL — MANDATORY LAST ACTION

Before the run is allowed to end:

1. Update local `/home/workdir/artifacts/task-domain/`:
   - increment `cycle_count`, set `last_cycle` to now
   - append-only: `log.md`, `instance-history.md`, `capability-frontier.md`
   - refresh `next-actions.md`
2. Append a dated entry to `state/ledger.md` (outcome + capability delta).
3. Push **all** changed files to `sudo-su-sudo/compounding-agency` on `main` via `github___push_files` (or create_or_update_file per path).
   Commit message format: `cycle N — YYYY-MM-DD — <one-line delta>`
4. If push fails, retry. A run that ends without a successful commit is a **failed cycle**.

Do not rely on local artifacts surviving. Only the GitHub commit compounds.
