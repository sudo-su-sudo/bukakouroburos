#!/usr/bin/env python3
"""refresh-live-snapshot.py — zero-brief outward snapshot.

Runs the no-key web-brief harvest, then resolves Hacker News ids into titles
so later cycles can read headlines without a second fetch.

  python3 artifacts/scripts/refresh-live-snapshot.py
"""
from __future__ import annotations

import json
import os
import runpy
import sys
import urllib.request
from datetime import datetime, timezone

ART = "/home/workdir/artifacts"
LIVE = os.path.join(ART, "knowledge", "live-snapshot.json")
BRIEF = os.path.join(ART, "knowledge", "live-brief.md")
WEB_BRIEF = "/root/.grok/server-skills/recursive-task-domain/scripts/web-brief.py"


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_json(url: str, timeout: int = 12):
    req = urllib.request.Request(url, headers={"User-Agent": "compound-loop-refresh/1"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8", errors="replace"))


def resolve_hn(snap: dict) -> int:
    n = 0
    for entry in snap.get("endpoints", []):
        if entry.get("name") != "hn_top" or not entry.get("ok"):
            continue
        ids = (entry.get("summary") or {}).get("top_ids_sample") or []
        stories = []
        for i in ids:
            try:
                item = fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{i}.json")
                stories.append({
                    "id": i,
                    "title": item.get("title"),
                    "url": item.get("url"),
                    "score": item.get("score"),
                    "by": item.get("by"),
                })
                n += 1
            except Exception as e:
                stories.append({"id": i, "error": str(e)})
        entry["stories"] = stories
    snap["enriched_at"] = utc_now()
    snap["enrichment"] = "hn titles resolved so future cycles read headlines without a second fetch"
    return n


def write_brief(snap: dict) -> None:
    lines = [
        "# Live brief",
        "",
        f"- generated_at: {snap.get('generated_at')}",
        f"- enriched_at: {snap.get('enriched_at')}",
        "- how_to_use_later: load this file during OBSERVE. Do not re-fetch unless generated_at is older than 24h.",
        "",
    ]
    for e in snap.get("endpoints", []):
        lines.append(f"## {e.get('name')} ok={e.get('ok')}")
        if e.get("stories"):
            for s in e["stories"]:
                lines.append(f"- ({s.get('score')}) {s.get('title')} — {s.get('url') or 'https://news.ycombinator.com/item?id='+str(s.get('id'))}")
        else:
            lines.append("```")
            lines.append(json.dumps(e.get("summary") or e.get("error"), indent=2)[:1200])
            lines.append("```")
        lines.append("")
    os.makedirs(os.path.dirname(BRIEF), exist_ok=True)
    with open(BRIEF, "w") as f:
        f.write("\n".join(lines))


def main() -> None:
    sys.argv = [WEB_BRIEF, "--live"]
    runpy.run_path(WEB_BRIEF, run_name="__main__")
    snap = json.load(open(LIVE))
    n = resolve_hn(snap)
    # trim bulky weather payloads before persist
    for e in snap.get("endpoints", []):
        if e.get("name") == "wttr_nyc" and isinstance(e.get("summary"), dict):
            cur = (e["summary"].get("current_condition") or [])[:1]
            e["summary"] = {"current_condition": cur}
    with open(LIVE, "w") as f:
        json.dump(snap, f, indent=2)
        f.write("\n")
    write_brief(snap)
    ok = sum(1 for e in snap["endpoints"] if e.get("ok"))
    print(json.dumps({"live": LIVE, "brief": BRIEF, "ok": ok, "n": len(snap["endpoints"]), "hn_titles": n}))


if __name__ == "__main__":
    main()
