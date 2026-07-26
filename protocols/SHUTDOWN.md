# SHUTDOWN PROTOCOL — MANDATORY LAST ACTION

Before the task is allowed to end:

1. Append every new task, outcome, and delta to `state/ledger.md`.
2. Update `state/capability-map.md` with any new strengths, closed gaps, or newly discovered leverage points.
3. Write today’s entry in `state/daily-compound.md` (one measurable improvement minimum).
4. Push the updated files to the `main` branch with a clear commit message that includes the date and a one-line summary of the compound delta.

If the push fails, retry. Do not terminate the run until the state is committed.
A run that ends without a successful commit is a failed cycle.
