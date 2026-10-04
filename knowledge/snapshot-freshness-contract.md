# Snapshot freshness contract

Cycle 7. Zero-brief rule for `scripts/eval-score.py`.

## Rule

`outward_signal_freshness` docks when `knowledge/live-snapshot.json` is missing or `generated_at` (else `enriched_at`, else mtime) is older than 36 hours.

- Fresh and present: ledger 0.8 + snapshot 0.2 = 1.0, dock 0.0
- Stale (>36h): no snapshot bonus, dock 0.4 → 0.4 if the X ledger is large
- Missing: same dock path → 0.4 if the X ledger is large

`snapshot_freshness.reason` is `fresh`, `stale`, or `missing`.

## Prove without a stale file

```
python3 /home/workdir/artifacts/scripts/eval-score.py --self-test
```

Expected: fresh=1.0, stale=0.4, missing=0.4, ok=true.

## When the dock fires

Run `python3 /home/workdir/artifacts/scripts/refresh-live-snapshot.py` before the next score. Do not invent a new skill to notice a stale file.
