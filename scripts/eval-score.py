#!/usr/bin/env python3
"""Zero-brief eval harness.

Score the compounding-agency substrate against eval.json keys.
No user topic. Run from any cold sandbox after BOOTSTRAP pull.

Cycle 5 adds:
  memory_quality  — append-only memory is present, parseable, and deep enough
  sprawl_ratio    — read from task-domain/skill-canonical-map.json (not a recount)

Usage:
  python3 artifacts/scripts/eval-score.py
  python3 artifacts/scripts/eval-score.py --root /home/workdir/artifacts
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

KEYS = (
    "github_roundtrip",
    "outward_signal_freshness",
    "skill_sprawl_risk",
    "zero_brief_scripts",
    "memory_quality",
    "sprawl_ratio",
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
    "skill-consolidator.py",
)

CYCLE_HEADING = re.compile(r"^## Cycle \d+", re.M)


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


def score_sprawl_name() -> float:
    """Legacy name-collision heuristic. Kept so old eval keys stay comparable."""
    skill_root = Path("/root/.grok/server-skills")
    if not skill_root.is_dir():
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
    skill_scripts = Path("/root/.grok/server-skills/recursive-task-domain/scripts")
    if not skill_scripts.is_dir():
        skill_scripts = Path("/home/workdir/.grok/skills/recursive-task-domain/scripts")
    local = root / "scripts"
    hits = 0
    for hint in ZERO_BRIEF_HINTS:
        if exists(skill_scripts / hint) or exists(local / hint):
            hits += 1
    return hits / len(ZERO_BRIEF_HINTS)


def load_map(root: Path) -> dict | None:
    path = root / "task-domain" / "skill-canonical-map.json"
    if not exists(path):
        return None
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def score_sprawl_ratio(root: Path) -> tuple[float, dict]:
    """Read sprawl_ratio from the canonical map. Missing map is worst (1.0)."""
    data = load_map(root)
    detail = {"source": "missing", "alias_count": None, "skill_count": None, "load_set": 0}
    if not data:
        return 1.0, detail
    alias = data.get("alias_count")
    total = data.get("skill_count") or 0
    ratio = data.get("sprawl_ratio")
    if not isinstance(ratio, (int, float)):
        ratio = (alias / total) if isinstance(alias, int) and total else 1.0
    detail = {
        "source": "task-domain/skill-canonical-map.json",
        "alias_count": alias,
        "skill_count": total,
        "load_set": len(data.get("load_set") or []),
        "generated_at": data.get("generated_at"),
    }
    return float(min(1.0, max(0.0, ratio))), detail


def score_memory_quality(root: Path) -> tuple[float, dict]:
    """How usable is durable memory without a human briefing.

    Components (equal weight):
      state_ok          cycle_count>=1 and last_cycle present
      history_depth     instance-history cycle headings >= cycle_count
      log_depth         log.md cycle headings >= cycle_count
      frontier_depth    capability-frontier cycle sections >= 1
      ledger_depth      state/ledger.md has a dated task line
      prior_eval        eval.json already has scores (scorer can diff)
      artifacts_listed  completed_artifacts non-empty
    """
    td = root / "task-domain"
    parts: dict[str, float] = {}
    cycle_count = 0
    state_ok = 0.0
    state_path = td / "state.json"
    if exists(state_path):
        try:
            state = json.loads(state_path.read_text())
            cycle_count = int(state.get("cycle_count") or 0)
            if cycle_count >= 1 and state.get("last_cycle"):
                state_ok = 1.0
            elif cycle_count >= 1:
                state_ok = 0.5
            parts["completed_artifacts"] = 1.0 if state.get("completed_artifacts") else 0.0
        except Exception:
            parts["completed_artifacts"] = 0.0
    else:
        parts["completed_artifacts"] = 0.0
    parts["state_ok"] = state_ok

    def headings(path: Path) -> int:
        if not exists(path):
            return 0
        return len(CYCLE_HEADING.findall(path.read_text(errors="replace")))

    need = max(cycle_count, 1)
    hist = headings(td / "instance-history.md")
    logn = headings(td / "log.md")
    front = headings(td / "capability-frontier.md")
    parts["history_depth"] = min(1.0, hist / need)
    parts["log_depth"] = min(1.0, logn / need)
    parts["frontier_depth"] = 1.0 if front >= 1 else 0.0

    ledger = root / "state" / "ledger.md"
    if exists(ledger) and re.search(r"TASK:", ledger.read_text(errors="replace")):
        parts["ledger_depth"] = 1.0
    else:
        parts["ledger_depth"] = 0.0

    prior_ok = 0.0
    ev = td / "eval.json"
    if exists(ev):
        try:
            blob = json.loads(ev.read_text())
            if isinstance(blob.get("scores"), dict) and blob["scores"]:
                prior_ok = 1.0
        except Exception:
            prior_ok = 0.0
    parts["prior_eval"] = prior_ok

    score = sum(parts.values()) / len(parts)
    detail = {
        "parts": {k: round(v, 3) for k, v in parts.items()},
        "cycle_count_seen": cycle_count,
        "history_headings": hist,
        "log_headings": logn,
        "frontier_headings": front,
    }
    return score, detail


def score_coverage(scores: dict) -> float:
    others = [k for k in KEYS if k != "eval_coverage"]
    return sum(1 for k in others if k in scores and isinstance(scores[k], (int, float))) / len(others)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/home/workdir/artifacts")
    args = ap.parse_args()
    root = Path(args.root)

    mem, mem_detail = score_memory_quality(root)
    ratio, ratio_detail = score_sprawl_ratio(root)
    scores = {
        "github_roundtrip": round(score_github_roundtrip(root), 3),
        "outward_signal_freshness": round(score_outward(root), 3),
        "skill_sprawl_risk": round(score_sprawl_name(), 3),
        "zero_brief_scripts": round(score_zero_brief(root), 3),
        "memory_quality": round(mem, 3),
        "sprawl_ratio": round(ratio, 3),
    }
    scores["eval_coverage"] = round(score_coverage(scores), 3)

    # sprawl_ratio (map) replaces the name heuristic in the composite so the
    # measured alias pile is what the loop optimizes. skill_sprawl_risk stays
    # emitted for continuity with cycles 3-4.
    composite = (
        scores["github_roundtrip"]
        + scores["outward_signal_freshness"]
        + (1.0 - scores["sprawl_ratio"])
        + scores["zero_brief_scripts"]
        + scores["memory_quality"]
        + scores["eval_coverage"]
    ) / 6.0

    payload = {
        "cycle": None,
        "ts": utc_now(),
        "scorer": "artifacts/scripts/eval-score.py",
        "persistence_verified": scores["github_roundtrip"] >= 0.8,
        "scores": scores,
        "composite": round(composite, 3),
        "memory_quality_detail": mem_detail,
        "sprawl_ratio_detail": ratio_detail,
        "notes": (
            "Zero-brief scorer. memory_quality and sprawl_ratio added cycle 5. "
            "sprawl_ratio is read from skill-canonical-map.json. "
            "Composite uses (1 - sprawl_ratio), not the legacy name heuristic."
        ),
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
        f"| skill_sprawl_risk | {scores['skill_sprawl_risk']} | legacy: banned-name skills / 20 (not in composite) |",
        f"| zero_brief_scripts | {scores['zero_brief_scripts']} | harvest/brief/eval/consolidator scripts found |",
        f"| memory_quality | {scores['memory_quality']} | state, history depth, ledger, prior eval |",
        f"| sprawl_ratio | {scores['sprawl_ratio']} | alias_count/skill_count from skill-canonical-map.json |",
        f"| eval_coverage | {scores['eval_coverage']} | keys actually computed this run |",
        "",
        f"sprawl source: {ratio_detail.get('source')} alias_count={ratio_detail.get('alias_count')} load_set={ratio_detail.get('load_set')}",
        f"memory parts: {json.dumps(mem_detail.get('parts'))}",
        "",
        "Run: `python3 /home/workdir/artifacts/scripts/eval-score.py`",
        "",
    ]
    report.write_text("\n".join(lines))
    print(json.dumps({"ok": True, "composite": payload["composite"], "scores": scores, "sprawl": ratio_detail, "memory": mem_detail}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
