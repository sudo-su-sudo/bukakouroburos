#!/usr/bin/env python3
"""refresh-if-docked.py — zero-brief execution of the cycle-7 queue conditional.

The queue used to say: if snapshot_freshness.reason != fresh, refresh before scoring.
That sentence is now a command. Future cycles do not re-derive the 36h rule.

  python3 /home/workdir/artifacts/scripts/refresh-if-docked.py
  python3 /home/workdir/artifacts/scripts/refresh-if-docked.py --dry-run
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path("/home/workdir/artifacts")
REFRESH = ROOT / "scripts" / "refresh-live-snapshot.py"
SCORE = ROOT / "scripts" / "eval-score.py"

spec = importlib.util.spec_from_file_location("eval_score", SCORE)
eval_score = importlib.util.module_from_spec(spec)
spec.loader.exec_module(eval_score)


def main() -> int:
    dry = "--dry-run" in sys.argv
    before = eval_score.inspect_snapshot(ROOT)
    refreshed = False
    if before["reason"] != "fresh" and not dry:
        subprocess.check_call([sys.executable, str(REFRESH)])
        refreshed = True
    after = eval_score.inspect_snapshot(ROOT)
    score_out = None
    if not dry:
        proc = subprocess.run(
            [sys.executable, str(SCORE)], check=True, capture_output=True, text=True
        )
        score_out = json.loads(proc.stdout)
    payload = {
        "before_reason": before["reason"],
        "before_age_hours": before["age_hours"],
        "after_reason": after["reason"],
        "after_age_hours": after["age_hours"],
        "refreshed": refreshed,
        "dry_run": dry,
        "composite": None if not score_out else score_out.get("composite"),
        "outward_signal_freshness": None
        if not score_out
        else score_out["scores"]["outward_signal_freshness"],
        "next": "skill-consolidator" if after["reason"] == "fresh" else "refresh-if-docked",
    }
    print(json.dumps(payload, indent=2))
    return 0 if after["reason"] == "fresh" or dry else 1


if __name__ == "__main__":
    raise SystemExit(main())
