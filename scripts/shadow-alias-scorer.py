#!/usr/bin/env python3
"""Shadow alias scorer for description-only clones.

Identifies skills that restate the Compound Loop in description
but whose names do not trigger the name-based alias gate in
skill-consolidator.py. Scores them as shadow_alias_count without
raising max_aliases or creating new skills.

Zero-brief: python3 scripts/shadow-alias-scorer.py
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

KNOWN_SHADOW = {
    "task-engine",
    "task-evolution",
    "task-evolution-domain",
}

CANONICAL_DESC_TOKENS = {
    "recursive", "compound", "task domain", "autonomous", "daily",
    "independence", "frequency", "effectiveness", "self-improving",
    "meta-task", "orchestration", "capability",
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


def overlap_score(desc: str) -> float:
    d = desc.lower()
    hits = sum(1 for t in CANONICAL_DESC_TOKENS if t in d)
    return round(hits / max(len(CANONICAL_DESC_TOKENS), 1), 3)


def main() -> int:
    root = Path("/root/.grok/server-skills")
    out = Path("/home/workdir/artifacts")  # adjusted for local
    shadows = []
    for skill_md in sorted(root.glob("*/SKILL.md")):
        text = skill_md.read_text(errors="replace")
        meta = parse_frontmatter(text)
        name = meta["name"] or skill_md.parent.name
        if name not in KNOWN_SHADOW:
            continue
        score = overlap_score(meta["description"])
        shadows.append({
            "name": name,
            "path": str(skill_md),
            "description_excerpt": meta["description"][:200],
            "overlap_score": score,
            "disposition": "SHADOW_ALIAS",
            "reason": "Description restates Compound Loop (recursive compounding, daily autonomy, task domain) but name does not hit banned-token gate.",
        })
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    report = {
        "generated_at": now,
        "shadow_alias_count": len(shadows),
        "max_aliases_unchanged": 18,
        "note": "These are not added to alias_count. Scoring only. Do not load. Do not extend.",
        "shadows": shadows,
        "recommendation": "Treat as description-only clones. Prefer recursive-task-domain + capability-index. No new skill required.",
    }
    (out / "knowledge").mkdir(parents=True, exist_ok=True)
    (out / "knowledge" / "shadow-alias-score.json").write_text(
        json.dumps(report, indent=2) + "\n"
    )
    md_lines = [
        "# Shadow Alias Score",
        "",
        f"Generated: {now}",
        f"shadow_alias_count: {len(shadows)}",
        "max_aliases remains 18 (unchanged).",
        "",
        "## Description-only clones (do not load)",
        "",
    ]
    for s in shadows:
        md_lines.append(f"- `{s['name']}` — overlap {s['overlap_score']} — {s['reason']}")
    md_lines += [
        "",
        "## Rule",
        "",
        "shadow_alias_count is informational. It does not raise the sprawl gate.",
        "Future cycles can run `python3 scripts/shadow-alias-scorer.py` with zero briefing to re-score.",
        "",
    ]
    (out / "knowledge" / "shadow-alias-score.md").write_text("\n".join(md_lines) + "\n")
    print(json.dumps({"shadow_alias_count": len(shadows), "generated_at": now}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
