#!/usr/bin/env python3
"""Zero-brief capability index query.

Scans local knowledge/ and task-domain/ for frontier items and ranks them by recency and type.
Future cycles can run this with zero briefing to get a snapshot of current independent capabilities.

Usage: python3 scripts/capability-index-query.py
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOW = ROOT / "knowledge"
TD = ROOT / "task-domain"

def main() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    files = []
    for folder in [KNOW, TD]:
        if folder.exists():
            for p in sorted(folder.rglob("*")):
                if p.is_file() and p.suffix in {".md", ".json"}:
                    stat = p.stat()
                    files.append({
                        "path": str(p.relative_to(ROOT)),
                        "size": stat.st_size,
                        "mtime": datetime.fromtimestamp(stat.st_mtime, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                    })
    files.sort(key=lambda x: x["mtime"], reverse=True)
    report = {
        "generated_at": now,
        "file_count": len(files),
        "top_recent": files[:10],
        "note": "Zero-brief query of durable capability artifacts. Use to identify next expansion without re-scanning GitHub.",
    }
    print(json.dumps(report, indent=2))
    # Optionally write a small artifact
    out = KNOW / f"capability-index-query-{now[:10]}.json"
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Wrote {out.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
