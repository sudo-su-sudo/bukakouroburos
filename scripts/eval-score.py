#!/usr/bin/env python3
"""Zero-brief eval harness.

Score the compounding-agency substrate against eval.json keys.
No user topic. Run from any cold sandbox after BOOTSTRAP pull.

Cycle 5: memory_quality + sprawl_ratio from skill-canonical-map.json.
Cycle 7: outward_signal_freshness docks when knowledge/live-snapshot.json
is missing or generated_at is older than 36h. Existence alone is not freshness.

Usage:
  python3 artifacts/scripts/eval-score.py
  python3 artifacts/scripts/eval-score.py --root /home/workdir/artifacts
  python3 artifacts/scripts/eval-score.py --self-test
"""
from __future__ import annotations

import argparse
import json
import re
import tempfile
from datetime import datetime, timedelta, timezone
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
SNAPSHOT_MAX_AGE_H = 36.0
STALE_DOCK = 0.4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_now_str() -> str:
    return utc_now().strftime("%Y-%m-%dT%H:%M:%SZ")


def exists(p: Path) -> bool:
    return p.is_file() and p.stat().st_size > 0


def parse_ts(value: str) -> datetime | None:
    if not value or not isinstance(value, str):
        return None
    text = value.strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def score_github_roundtrip(root: Path) -> float:
    td = root / "task-domain"
    hits = sum(1 for n in REQUIRED_TD if exists(td / n))
    extra = 0.0
    if exists(root / "state" / "ledger.md"):
        extra += 0.1
    if exists(root / "protocols" / "BOOTSTRAP.md") and exists(root / "protocols" / "SHUTDOWN.md"):
        extra += 0.1
    return min(1.0, hits / len(REQUIRED_TD) + extra)


def inspect_snapshot(root: Path, now: datetime | None = None) -> dict:
    """Age of knowledge/live-snapshot.json. Missing or >36h must dock freshness."""
    now = now or utc_now()
    snap = root / "knowledge" / "live-snapshot.json"
    detail = {
        "path": "knowledge/live-snapshot.json",
        "present": False,
        "generated_at": None,
        "age_hours": None,
        "max_age_hours": SNAPSHOT_MAX_AGE_H,
        "stale": True,
        "dock": STALE_DOCK,
        "reason": "missing",
    }
    if not exists(snap):
        return detail
    detail["present"] = True
    generated = None
    source = None
    try:
        blob = json.loads(snap.read_text())
        generated = parse_ts(blob.get("generated_at") or "") or parse_ts(blob.get("enriched_at") or "")
        if generated:
            source = "generated_at" if blob.get("generated_at") else "enriched_at"
    except Exception:
        generated = None
    if generated is None:
        generated = datetime.fromtimestamp(snap.stat().st_mtime, timezone.utc)
        source = "mtime"
    age_h = (now - generated).total_seconds() / 3600.0
    stale = age_h > SNAPSHOT_MAX_AGE_H
    detail.update({
        "generated_at": generated.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "age_hours": round(age_h, 2),
        "source": source,
        "stale": stale,
        "dock": STALE_DOCK if stale else 0.0,
        "reason": "stale" if stale else "fresh",
    })
    return detail


def score_outward(root: Path, now: datetime | None = None) -> tuple[float, dict]:
    ledger = root / "knowledge" / "x-signal-ledger.md"
    snap_detail = inspect_snapshot(root, now=now)
    score = 0.0
    if exists(ledger):
        score += 0.6
        if ledger.stat().st_size > 1000:
            score += 0.2
    if snap_detail["present"] and not snap_detail["stale"]:
        score += 0.2
    # Dock: missing or older than 36h. Existence is not freshness.
    score = max(0.0, score - float(snap_detail["dock"]))
    snap_detail["score"] = round(score, 3)
    return min(1.0, score), snap_detail


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
    td = root / "task-domain"
    parts: dict[str, float] = {}
    cycle_count = 0
    state_ok = 0.0
    hist = logn = front = 0
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


def build_payload(root: Path, now: datetime | None = None) -> dict:
    mem, mem_detail = score_memory_quality(root)
    ratio, ratio_detail = score_sprawl_ratio(root)
    outward, snap_detail = score_outward(root, now=now)
    scores = {
        "github_roundtrip": round(score_github_roundtrip(root), 3),
        "outward_signal_freshness": round(outward, 3),
        "skill_sprawl_risk": round(score_sprawl_name(), 3),
        "zero_brief_scripts": round(score_zero_brief(root), 3),
        "memory_quality": round(mem, 3),
        "sprawl_ratio": round(ratio, 3),
    }
    scores["eval_coverage"] = round(score_coverage(scores), 3)
    composite = (
        scores["github_roundtrip"]
        + scores["outward_signal_freshness"]
        + (1.0 - scores["sprawl_ratio"])
        + scores["zero_brief_scripts"]
        + scores["memory_quality"]
        + scores["eval_coverage"]
    ) / 6.0
    return {
        "cycle": None,
        "ts": utc_now_str(),
        "scorer": "artifacts/scripts/eval-score.py",
        "persistence_verified": scores["github_roundtrip"] >= 0.8,
        "scores": scores,
        "composite": round(composite, 3),
        "memory_quality_detail": mem_detail,
        "sprawl_ratio_detail": ratio_detail,
        "snapshot_freshness": snap_detail,
        "notes": (
            "Zero-brief scorer. Cycle 7 docks outward_signal_freshness by 0.4 "
            "when knowledge/live-snapshot.json is missing or generated_at is older than 36h. "
            "sprawl_ratio is read from skill-canonical-map.json. "
            "Composite uses (1 - sprawl_ratio), not the legacy name heuristic."
        ),
    }


def write_outputs(root: Path, payload: dict) -> None:
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
    scores = payload["scores"]
    snap = payload["snapshot_freshness"]
    ratio_detail = payload["sprawl_ratio_detail"]
    mem_detail = payload["memory_quality_detail"]
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
        f"| outward_signal_freshness | {scores['outward_signal_freshness']} | ledger plus snapshot; docked if snapshot missing or >36h |",
        f"| skill_sprawl_risk | {scores['skill_sprawl_risk']} | legacy: banned-name skills / 20 (not in composite) |",
        f"| zero_brief_scripts | {scores['zero_brief_scripts']} | harvest/brief/eval/consolidator scripts found |",
        f"| memory_quality | {scores['memory_quality']} | state, history depth, ledger, prior eval |",
        f"| sprawl_ratio | {scores['sprawl_ratio']} | alias_count/skill_count from skill-canonical-map.json |",
        f"| eval_coverage | {scores['eval_coverage']} | keys actually computed this run |",
        "",
        f"snapshot: present={snap.get('present')} reason={snap.get('reason')} age_hours={snap.get('age_hours')} dock={snap.get('dock')} generated_at={snap.get('generated_at')}",
        f"sprawl source: {ratio_detail.get('source')} alias_count={ratio_detail.get('alias_count')} load_set={ratio_detail.get('load_set')}",
        f"memory parts: {json.dumps(mem_detail.get('parts'))}",
        "",
        "Run: `python3 /home/workdir/artifacts/scripts/eval-score.py`",
        "",
    ]
    report.write_text("\n".join(lines))


def self_test() -> int:
    now = datetime(2026, 10, 4, 10, 33, tzinfo=timezone.utc)
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "knowledge").mkdir()
        (root / "task-domain").mkdir()
        (root / "knowledge" / "x-signal-ledger.md").write_text("x" * 1200)
        fresh = {"generated_at": "2026-10-04T00:00:00Z"}
        stale = {"generated_at": "2026-10-01T00:00:00Z"}
        snap = root / "knowledge" / "live-snapshot.json"
        snap.write_text(json.dumps(fresh))
        fresh_score, fresh_detail = score_outward(root, now=now)
        snap.write_text(json.dumps(stale))
        stale_score, stale_detail = score_outward(root, now=now)
        snap.unlink()
        missing_score, missing_detail = score_outward(root, now=now)
    ok = (
        fresh_detail["reason"] == "fresh"
        and fresh_detail["dock"] == 0.0
        and abs(fresh_score - 1.0) < 1e-9
        and stale_detail["reason"] == "stale"
        and stale_detail["dock"] == STALE_DOCK
        and abs(stale_score - 0.4) < 1e-9
        and missing_detail["reason"] == "missing"
        and abs(missing_score - 0.4) < 1e-9
    )
    print(json.dumps({
        "ok": ok,
        "fresh": fresh_score,
        "stale": stale_score,
        "missing": missing_score,
        "fresh_detail": fresh_detail,
        "stale_detail": stale_detail,
        "missing_detail": missing_detail,
    }, indent=2))
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/home/workdir/artifacts")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()
    root = Path(args.root)
    payload = build_payload(root)
    write_outputs(root, payload)
    print(json.dumps({
        "ok": True,
        "composite": payload["composite"],
        "scores": payload["scores"],
        "snapshot": payload["snapshot_freshness"],
        "sprawl": payload["sprawl_ratio_detail"],
        "memory": payload["memory_quality_detail"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
