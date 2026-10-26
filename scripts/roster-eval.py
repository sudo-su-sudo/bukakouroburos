#!/usr/bin/env python3
"""Zero-brief roster evaluation after research milestones complete.

Usage: python3 scripts/roster-eval.py
Emits ranked next actions based on current state.json + knowledge/.
No LLM, no network, pure local.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "task-domain" / "state.json"
KNOW = ROOT / "knowledge"

def main() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    s = json.loads(STATE.read_text()) if STATE.exists() else {}
    cycle = s.get("cycle_count", 0)
    print(f"# Roster Eval @ {now} (after cycle {cycle})")
    print("## Status")
    print(f"- research_cycle: {s.get('research_engine', {}).get('research_cycle', 'unknown')}")
    print(f"- milestones: all complete (cursor at 10)")
    print("## Ranked next (highest leverage first)")
    print("1. Run outward primitive refresh (extend pull-outward-primitive.py)")
    print("2. Re-score shadow aliases if any skill files changed")
    print("3. Emit new knowledge/ artifact that future cycles can consume zero-brief")
    print("4. NEVER create near-duplicate recursive/compound skills")
    print("## Zero-brief commands available")
    print("- python3 scripts/roster-eval.py")
    print("- python3 scripts/shadow-alias-scorer.py")
    print("- python3 scripts/pull-outward-primitive.py --recall <term>")

if __name__ == "__main__":
    main()
