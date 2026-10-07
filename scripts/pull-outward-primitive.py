#!/usr/bin/env python3
"""Pull one outward primitive from the cycle-2 X-ledger shortlist.

Zero-brief. No new skills. Public GitHub metadata only.

  python3 scripts/pull-outward-primitive.py
  python3 scripts/pull-outward-primitive.py --recall sprawl

TAKE is vectorize-io/hindsight: retain / recall / reflect.
openrig and univer are recorded as deferred primitives, not cloned.
Local recall is a file search. Reflect stays a cycle decision, not this script.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
TARGETS = [
    {
        "id": "hindsight",
        "repo": "vectorize-io/hindsight",
        "ops": ["retain", "recall", "reflect"],
        "why": "Memory ops split lookup from synthesis. Maps onto append-only files without a new skill.",
        "decision": "TAKE",
    },
    {
        "id": "openrig",
        "repo": "mvschwarz/openrig",
        "ops": ["rig", "seat", "review"],
        "why": "A rig wraps harnesses. Needs tmux, Node 22, and provider CLIs this sandbox does not have.",
        "decision": "DEFER",
    },
    {
        "id": "univer",
        "repo": "dream-num/univer",
        "ops": ["facade", "plugin", "headless"],
        "why": "Office runtime. Local docx/pptx/xlsx/pdf skills already cover the composition point.",
        "decision": "DEFER",
    },
]
# Stamped from authenticated github___search_repositories on 2026-10-07 when
# api.github.com returned 403. Used only if the public fetch fails.
OBSERVED = {
    "vectorize-io/hindsight": {
        "full_name": "vectorize-io/hindsight",
        "description": "Hindsight: Agent Memory That Learns",
        "stars": 46514,
        "default_branch": "main",
        "updated_at": "2026-10-07T10:29:17Z",
        "license": "MIT",
        "html_url": "https://github.com/vectorize-io/hindsight",
        "source": "github_connected_tool",
    },
    "mvschwarz/openrig": {
        "full_name": "mvschwarz/openrig",
        "description": "Build your own network of agents from Claude Code, Codex and Pi: persistent teams with roles, shared context and owned work.",
        "stars": 5614,
        "default_branch": "main",
        "updated_at": "2026-10-07T10:32:27Z",
        "license": "Apache-2.0",
        "html_url": "https://github.com/mvschwarz/openrig",
        "source": "github_connected_tool",
    },
    "dream-num/univer": {
        "full_name": "dream-num/univer",
        "description": "The Office Harness for AI Agents — Spreadsheets, Docs, Slides, Canvas, Relational Tables, and PDF in one runtime.",
        "stars": 22431,
        "default_branch": "dev",
        "updated_at": "2026-10-07T10:11:36Z",
        "license": None,
        "html_url": "https://github.com/dream-num/univer",
        "source": "github_connected_tool",
    },
}

SEARCH_DIRS = [KNOWLEDGE, ROOT / "task-domain", ROOT / "state", ROOT / "protocols"]


def fetch_repo(full: str) -> dict:
    url = f"https://api.github.com/repos/{full}"
    req = urllib.request.Request(url, headers={"User-Agent": "compounding-agency-cycle", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read().decode())
    return {
        "full_name": data.get("full_name"),
        "description": data.get("description"),
        "stars": data.get("stargazers_count"),
        "default_branch": data.get("default_branch"),
        "updated_at": data.get("updated_at"),
        "license": (data.get("license") or {}).get("spdx_id"),
        "html_url": data.get("html_url"),
        "pushed_at": data.get("pushed_at"),
    }


def recall(query: str, limit: int = 12) -> list:
    tokens = [t for t in re.split(r"\W+", query.lower()) if len(t) > 2]
    if not tokens:
        return []
    hits = []
    for folder in SEARCH_DIRS:
        if not folder.exists():
            continue
        for path in folder.rglob("*"):
            if not path.is_file() or path.suffix not in {".md", ".json", ".txt"}:
                continue
            try:
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
            except OSError:
                continue
            for i, line in enumerate(lines, 1):
                low = line.lower()
                score = sum(1 for t in tokens if t in low)
                if score:
                    hits.append({
                        "score": score,
                        "path": str(path.relative_to(ROOT)),
                        "line": i,
                        "text": line.strip()[:220],
                    })
    hits.sort(key=lambda h: (-h["score"], h["path"], h["line"]))
    return hits[:limit]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--recall", help="local recall: ranked file hits, no LLM")
    parser.add_argument("--limit", type=int, default=12)
    args = parser.parse_args()

    if args.recall:
        hits = recall(args.recall, args.limit)
        print(json.dumps({"op": "recall", "query": args.recall, "hits": hits}, indent=2))
        return 0 if hits else 2

    cards = []
    errors = []
    for spec in TARGETS:
        card = dict(spec)
        try:
            card["live"] = fetch_repo(spec["repo"])
            card["live"]["source"] = "api.github.com"
        except Exception as exc:  # noqa: BLE001 — outward fetch must not kill the card
            card["live"] = OBSERVED.get(spec["repo"])
            card["fetch_error"] = str(exc)
            errors.append(spec["repo"])
        cards.append(card)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    take = next(c for c in cards if c["decision"] == "TAKE")
    payload = {
        "generated_at": now,
        "source": "cycle-2 x-signal-ledger S2 shortlist",
        "take": take["id"],
        "primitive": "retain_recall_reflect",
        "local_map": {
            "retain": "append-only write to state/ledger.md, task-domain/log.md, instance-history.md",
            "recall": "python3 scripts/pull-outward-primitive.py --recall <tokens>",
            "reflect": "cycle decision over recalled hits; not this script",
        },
        "cards": cards,
        "fetch_errors": errors,
    }
    KNOWLEDGE.mkdir(parents=True, exist_ok=True)
    (KNOWLEDGE / "outward-primitive.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Outward primitive — retain / recall / reflect",
        "",
        f"Generated: {now}",
        "Source shortlist: cycle-2 x-signal-ledger (hindsight / openrig / univer).",
        "TAKE: vectorize-io/hindsight. Not installed. The op split is the primitive.",
        "",
        "## Local map",
        "",
        "- retain: append to ledger, log, instance-history. Never rewrite prior entries.",
        "- recall: `python3 scripts/pull-outward-primitive.py --recall <tokens>` — ranked file hits, no LLM.",
        "- reflect: a cycle decision over those hits. Do not call a lookup a reflection.",
        "",
        "## Cards",
        "",
    ]
    for card in cards:
        live = card.get("live") or {}
        lines.append(f"### {card['decision']} — {card['repo']}")
        lines.append(f"- why: {card['why']}")
        if live:
            lines.append(f"- stars: {live.get('stars')}  branch: {live.get('default_branch')}  license: {live.get('license')}  source: {live.get('source')}")
            lines.append(f"- updated: {live.get('updated_at')}")
            lines.append(f"- {live.get('description')}")
            if card.get("fetch_error"):
                lines.append(f"- public_api: {card['fetch_error']} (used stamped observation)")
        lines.append("")
    lines.append("Rejected this cycle: installing hindsight, cloning openrig, wrapping univer. Those are products. The op split is the capability.")
    lines.append("")
    (KNOWLEDGE / "outward-primitive.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"take": take["id"], "errors": errors, "wrote": ["knowledge/outward-primitive.json", "knowledge/outward-primitive.md"]}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
