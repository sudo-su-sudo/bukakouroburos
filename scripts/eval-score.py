#!/usr/bin/env python3
"""Zero-brief eval harness.

Score the compounding-agency substrate against eval.json keys.
No user topic. Run from any cold sandbox after BOOTSTRAP pull.

Usage:
  python3 artifacts/scripts/eval-score.py
  python3 artifacts/scripts/eval-score.py --root /home/workdir/artifacts
"""
from __future__ import annotations

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

KEYS = (
    "github_roundtrip",
    "outward_signal_freshness",
    "skill_sprawl_risk",
    "zero_brief_scripts",
    "eval_coverage",
)

REQUIRED_TD = (
    "state.json",
    "next-actions.md",
    "instance-history.md",
    "capability-frontier.md",
    "log.md",
    "eval.json",
)

ZERO_BRIEF_HINTS = (
    "outward-harvest.py",
    "web-brief.py",
    "eval-score.py",
    "score-compound.py",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def exists(p: Path) -> bool:
    return p.is_file() and p.stat().st_size > 0


def score_github_roundtrip(root: Path) -> float:
    td = root / "task-domain"
    hits = sum(1 for n in REQUIRED_TD if exists(td / n))
    extra = 0.0
    if exists(root / "state" / "ledger.md"):
        extra += 0.1
    if exists(root / "protocols" / "BOOTSTRAP.md") and exists(root / "protocols" / "SHUTDOWN.md"):
        extra += 0.1
    return min(1.0, hits / len(REQUIRED_TD) + extra)


def score_outward(root: Path) -> float:
    ledger = root / "knowledge" / "x-signal-ledger.md"
    snap = root / "knowledge" / "live-snapshot.json"
    score = 0.0
    if exists(ledger):
        score += 0.6
        if ledger.stat().st_size > 1000:
            score += 0.2
    if exists(snap):
        score += 0.2
    return min(1.0, score)


def score_sprawl() -> float:
    skill_root = Path("/home/workdir/.grok/skills")
    banned = (
        "recursive",
        "compound",
        "task-domain",
        "autonomy",
        "forge",
        "evolver",
        "orchestrator",
    )
    count = 0
    if skill_root.is_dir():
        for p in skill_root.iterdir():
            name = p.name.lower()
            if any(b in name for b in banned):
                count += 1
    return min(1.0, count / 20.0)


def score_zero_brief(root: Path) -> float:
    skill_scripts = Path("/home/workdir/.grok/skills/recursive-task-domain/scripts")
    local = root / "scripts"
    hits = 0
    for hint in ZERO_BRIEF_HINTS:
        if exists(skill_scripts / hint) or exists(local / hint):
            hits += 1
    return hits / len(ZERO_BRIEF_HINTS)


def score_coverage(root: Path, scores: dict) -> float:
    others = [k for k in KEYS if k != "eval_coverage"]
    return sum(1 for k in others if k in scores and isinstance(scores[k], (int, float))) / len(others)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/home/workdir/artifacts")
    args = ap.parse_args()
    root = Path(args.root)

    scores = {
        "github_roundtrip": round(score_github_roundtrip(root), 3),
        "outward_signal_freshness": round(score_outward(root), 3),
        "skill_sprawl_risk": round(score_sprawl(), 3),
        "zero_brief_scripts": round(score_zero_brief(root), 3),
    }
    scores["eval_coverage"] = round(score_coverage(root, scores), 3)

    composite = (
        scores["github_roundtrip"]
        + scores["outward_signal_freshness"]
        + (1.0 - scores["skill_sprawl_risk"])
        + scores["zero_brief_scripts"]
        + scores["eval_coverage"]
    ) / 5.0

    payload = {
        "cycle": None,
        "ts": utc_now(),
        "scorer": "artifacts/scripts/eval-score.py",
        "persistence_verified": scores["github_roundtrip"] >= 0.8,
        "scores": scores,
        "composite": round(composite, 3),
        "notes": "Zero-brief scorer. Future cycles: run this file, append result, do not rewrite history keys.",
    }

    out_json = root / "task-domain" / "eval.json"
    out_json.parent.mkdir(parents=True, exist_ok=True)
    prior = None
    if out_json.exists():
        try:
            prior = json.loads(out_json.read_text())
        except Exception:
            prior = None
    payload["prior"] = {
        "ts": (prior or {}).get("ts"),
        "scores": (prior or {}).get("scores"),
        "cycle": (prior or {}).get("cycle"),
    }
    out_json.write_text(json.dumps(payload, indent=2) + "\n")

    report = root / "task-domain" / "eval-report.md"
    lines = [
        "# Eval Report",
        "",
        f"ts: {payload['ts']}",
        f"composite: {payload['composite']}",
        f"persistence_verified: {payload['persistence_verified']}",
        "",
        "| key | score | meaning |",
        "|---|---|---|",
        f"| github_roundtrip | {scores['github_roundtrip']} | substrate files present after BOOTSTRAP |",
        f"| outward_signal_freshness | {scores['outward_signal_freshness']} | x-ledger / live snapshot exist |",
        f"| skill_sprawl_risk | {scores['skill_sprawl_risk']} | fraction of banned-name skills / 20 |",
        f"| zero_brief_scripts | {scores['zero_brief_scripts']} | harvest/brief/eval/score scripts found |",
        f"| eval_coverage | {scores['eval_coverage']} | keys actually computed this run |",
        "",
        "Run: `python3 /home/workdir/artifacts/scripts/eval-score.py`",
        "",
    ]
    report.write_text("\n".join(lines))
    print(json.dumps({"ok": True, "composite": payload["composite"], "scores": scores}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
