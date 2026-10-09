#!/usr/bin/env python3
"""Zero-brief skill consolidator.

Scans SKILL.md frontmatter, clusters name-colliding autonomy skills,
and writes a canonical map + redundancy report. Does not create skills.
Does not delete skills (sandbox skills are read-only from this loop).

Exit code is the sprawl gate: 1 if alias_count rises above --max-aliases
(default 18, the cycle-4 baseline). A later cycle can fail without
re-reading the queue sentence.

Usage:
  python3 scripts/skill-consolidator.py
  python3 scripts/skill-consolidator.py --root /root/.grok/server-skills
  python3 scripts/skill-consolidator.py --max-aliases 18
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

BANNED_TOKENS = (
    "recursive",
    "compound",
    "task-domain",
    "taskdomain",
    "autonomy",
    "forge",
    "evolver",
    "orchestrator",
    "vanguard",
)

# Authoritative roles. Everything else that matches banned tokens is an alias.
CANONICAL = {
    "capability-growth-core": {
        "role": "objective",
        "load": True,
        "why": "Invariant: maximize rate of new capability, not task completion.",
    },
    "capability-index": {
        "role": "frontier-index",
        "load": True,
        "why": "Single source of truth for what is already possible.",
    },
    "recursive-task-domain": {
        "role": "loop-engine",
        "load": True,
        "why": "Sole Compound Loop implementation. Do not re-implement.",
    },
    "daily-compound-ignition": {
        "role": "starter",
        "load": True,
        "why": "Pull GitHub state, execute one frontier item, push. Not a loop.",
    },
    "knowledge-compounder": {
        "role": "memory-primitive",
        "load": True,
        "why": "Turns ephemeral findings into durable files.",
    },
    "leverage-maximizer": {
        "role": "selection-primitive",
        "load": True,
        "why": "Picks the highest-leverage move before execution.",
    },
    "independent-task-generator": {
        "role": "generation-primitive",
        "load": False,
        "why": "Use only when the queue is empty. Not a second loop.",
    },
    "task-domain": {
        "role": "state-substrate",
        "load": False,
        "why": "File layout for task-domain/. Not an execution engine.",
    },
    "singularity-ethos": {
        "role": "orthogonal-detector",
        "load": False,
        "why": "Not part of the compound loop. Do not alias into it.",
    },
}

FRONTMATTER = re.compile(r"^---\n(.*?)\n---", re.S)


def parse_frontmatter(text: str) -> dict:
    m = FRONTMATTER.search(text)
    meta = {"name": "", "description": ""}
    if not m:
        return meta
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        if k in ("name", "description"):
            meta[k] = v.strip().strip('"')
    return meta


def tokens(name: str) -> set:
    return set(re.split(r"[-_]+", name.lower())) - {"", "the", "a"}


def cluster_of(name: str) -> str:
    t = tokens(name)
    if name in CANONICAL:
        return CANONICAL[name]["role"]
    if "singularity" in t:
        return "orthogonal"
    hits = [b for b in BANNED_TOKENS if b in name.lower() or b in t]
    if hits:
        return "alias-of-loop"
    return "other"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="/root/.grok/server-skills")
    ap.add_argument("--out-dir", default="/home/workdir/artifacts")
    ap.add_argument(
        "--max-aliases",
        type=int,
        default=18,
        help="Fail (exit 1) if alias_count exceeds this. Cycle-4 baseline is 18.",
    )
    ap.add_argument(
        "--prior-map",
        default="",
        help="Optional prior skill-canonical-map.json. Writes a set-diff receipt.",
    )
    args = ap.parse_args()
    root = Path(args.root)
    out = Path(args.out_dir)
    skills = []
    for skill_md in sorted(root.glob("*/SKILL.md")):
        text = skill_md.read_text(errors="replace")
        meta = parse_frontmatter(text)
        name = meta["name"] or skill_md.parent.name
        banned = [b for b in BANNED_TOKENS if b in name.lower() or b in meta["description"].lower()]
        entry = {
            "name": name,
            "dir": skill_md.parent.name,
            "path": str(skill_md),
            "description": meta["description"][:280],
            "bytes": skill_md.stat().st_size,
            "banned_token_hits": banned,
            "cluster": cluster_of(name),
            "canonical": name in CANONICAL,
            "load_by_default": CANONICAL.get(name, {}).get("load", False),
            "alias_of": None,
        }
        if entry["cluster"] == "alias-of-loop":
            entry["alias_of"] = "recursive-task-domain"
            entry["disposition"] = "DO_NOT_LOAD"
        elif name in CANONICAL:
            entry["disposition"] = "KEEP"
            entry["why"] = CANONICAL[name]["why"]
        else:
            entry["disposition"] = "KEEP_UNRELATED"
        skills.append(entry)

    aliases = [s for s in skills if s["disposition"] == "DO_NOT_LOAD"]
    keep = [s for s in skills if s["disposition"] == "KEEP"]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    gate_pass = len(aliases) <= args.max_aliases
    report = {
        "generated_at": now,
        "root": str(root),
        "skill_count": len(skills),
        "canonical_keep": [s["name"] for s in keep],
        "alias_count": len(aliases),
        "max_aliases": args.max_aliases,
        "sprawl_gate": "pass" if gate_pass else "fail",
        "sprawl_ratio": round(len(aliases) / max(len(skills), 1), 3),
        "load_set": [s["name"] for s in skills if s["load_by_default"]],
        "rule": "Future cycles load only load_set. Aliases are name-collisions of the Compound Loop and must not be extended. Exit 1 if alias_count > max_aliases.",
        "skills": skills,
    }
    (out / "task-domain").mkdir(parents=True, exist_ok=True)
    (out / "knowledge").mkdir(parents=True, exist_ok=True)
    (out / "task-domain" / "skill-canonical-map.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    lines = [
        "# Skill redundancy report",
        "",
        f"Generated: {now}",
        f"Scanned: `{root}`",
        f"Skills: {len(skills)} | aliases (do not load): {len(aliases)} | max_aliases: {args.max_aliases} | sprawl_gate: {report['sprawl_gate']} | sprawl_ratio: {report['sprawl_ratio']}",
        "",
        "## Load set (only these for a Compound Loop cycle)",
        "",
    ]
    for s in skills:
        if s["load_by_default"]:
            lines.append(f"- `{s['name']}` — {CANONICAL[s['name']]['role']}: {CANONICAL[s['name']]['why']}")
    lines += ["", "## Canonical keep (not always loaded)", ""]
    for s in keep:
        if not s["load_by_default"]:
            lines.append(f"- `{s['name']}` — {CANONICAL.get(s['name'], {}).get('role', s['cluster'])}")
    lines += [
        "",
        "## Aliases — do not load, do not extend, do not clone",
        "",
        "These descriptions restate the same loop (create task domain, recursive compounding, daily autonomy). Loading them dilutes the objective.",
        "",
    ]
    for s in aliases:
        lines.append(f"- `{s['name']}` → alias of `recursive-task-domain` (hits: {', '.join(s['banned_token_hits'][:4])})")
    lines += [
        "",
        "## Consolidation rule",
        "",
        "1. Do not create a skill whose name or description contains recursive, compound, task-domain, autonomy, forge, evolver, orchestrator, or vanguard.",
        "2. New capability goes in `scripts/` or `knowledge/`, not a new skill.",
        "3. Re-run this script each cycle. Exit code is the gate: 1 if alias_count > --max-aliases (default 18).",
        "",
    ]
    (out / "knowledge" / "skill-redundancy-report.md").write_text("\n".join(lines) + "\n")
    gate_lines = [
        "# Sprawl gate",
        "",
        f"Generated: {now}",
        f"alias_count: {len(aliases)}",
        f"max_aliases: {args.max_aliases}",
        f"sprawl_gate: {report['sprawl_gate']}",
        f"sprawl_ratio: {report['sprawl_ratio']}",
        f"skill_count: {len(skills)}",
        "",
        "Command: `python3 scripts/skill-consolidator.py --max-aliases 18`",
        "Exit 0 means the alias pile did not grow past the cycle-4 baseline.",
        "Exit 1 means the cycle failed the sprawl constraint. Do not push a pass.",
        "",
    ]
    (out / "knowledge" / "sprawl-gate.md").write_text("\n".join(gate_lines) + "\n")

    prior_path = Path(args.prior_map) if args.prior_map else None
    delta = {
        "generated_at": now,
        "prior_map": str(prior_path) if prior_path else None,
        "alias_count": len(aliases),
        "added": [],
        "removed": [],
        "unchanged": True,
    }
    if prior_path and prior_path.exists():
        prior = json.loads(prior_path.read_text())
        prior_aliases = {
            s["name"] for s in prior.get("skills", []) if s.get("disposition") == "DO_NOT_LOAD"
        }
        now_aliases = {s["name"] for s in aliases}
        delta["prior_generated_at"] = prior.get("generated_at")
        delta["added"] = sorted(now_aliases - prior_aliases)
        delta["removed"] = sorted(prior_aliases - now_aliases)
        delta["unchanged"] = not delta["added"] and not delta["removed"]
        delta["prior_alias_count"] = prior.get("alias_count")
    (out / "knowledge" / "sprawl-delta.json").write_text(json.dumps(delta, indent=2) + "\n")

    print(json.dumps({
        "skill_count": len(skills),
        "alias_count": len(aliases),
        "max_aliases": args.max_aliases,
        "sprawl_gate": report["sprawl_gate"],
        "load_set": report["load_set"],
        "sprawl_ratio": report["sprawl_ratio"],
        "delta_added": delta["added"],
        "delta_removed": delta["removed"],
        "delta_unchanged": delta["unchanged"],
    }, indent=2))
    return 0 if gate_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
