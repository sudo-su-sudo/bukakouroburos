#!/usr/bin/env python3
"""
Zero-brief indexer for the large research probe archive ("hope this helps.zip").
Future Compound Loop cycles can run this against the zip or an extracted directory
to get a fresh categorized inventory without re-deriving the taxonomy.

Usage:
  python3 scripts/index_research_probe_archive.py /path/to/hope this helps.zip
  python3 scripts/index_research_probe_archive.py /path/to/extracted/helpful for ai/

Outputs:
  - Prints summary + cluster counts to stdout
  - Writes knowledge/research_probe_archive_index_latest.md
"""

import os
import sys
import zipfile
import json
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timezone

CLUSTERS = {
    "weird_machines": ["weird_machine", "twos_complement", "spectre", "mmu_page", "btb_", "rsb_", "l1tf", "foreshadow", "store_to_load", "dma_descriptor"],
    "sporeos_ghostos": ["sporeos", "ghostos", "autopoietic"],
    "subzero_subspace": ["subzero", "subspace", "lora", "memory_free_lora"],
    "mythos": ["mythos"],
    "attention_kv": ["attention", "kv_cache", "kv_", "flash_attention", "ring_attention", "sparse_attention", "token_economy"],
    "swarm_rpc_mcp": ["mcp_", "swarm_rpc", "cross_agent", "rpc_gateway", "rpc_codec", "rpc_adapter"],
    "chronos_temporal": ["chronos", "temporal_tensor", "tezo_"],
    "storage_cloud": ["cloud_storage", "cloud_takeout", "storage_vfs", "storage_reclaimer"],
    "crypto_offensive": ["diffie_hellman", "montgomery", "coppersmith", "shamir", "x25519", "rns_"],
    "chimera_void": ["chimera", "void_walk", "black_hole"],
}

def categorize(name: str) -> list[str]:
    low = name.lower()
    hits = []
    for cluster, keys in CLUSTERS.items():
        if any(k in low for k in keys):
            hits.append(cluster)
    return hits or ["uncategorized"]

def scan_directory(root: Path):
    py_files = list(root.rglob("*.py"))
    json_files = list(root.rglob("*.json"))
    clusters = defaultdict(list)
    for p in py_files:
        for c in categorize(p.name):
            clusters[c].append(str(p.relative_to(root)))
    return py_files, json_files, clusters

def scan_zip(zip_path: Path):
    py_files = []
    json_files = []
    clusters = defaultdict(list)
    with zipfile.ZipFile(zip_path, "r") as z:
        for info in z.infolist():
            name = info.filename
            if name.endswith(".py"):
                py_files.append(name)
                for c in categorize(Path(name).name):
                    clusters[c].append(name)
            elif name.endswith(".json"):
                json_files.append(name)
    return py_files, json_files, clusters

def main():
    if len(sys.argv) < 2:
        print("Usage: index_research_probe_archive.py <zip_or_dir>")
        sys.exit(1)

    target = Path(sys.argv[1]).expanduser().resolve()
    if not target.exists():
        print(f"Path not found: {target}")
        sys.exit(1)

    if target.is_file() and target.suffix.lower() == ".zip":
        py_files, json_files, clusters = scan_zip(target)
        source = f"zip:{target.name}"
    elif target.is_dir():
        py_files, json_files, clusters = scan_directory(target)
        source = f"dir:{target}"
    else:
        print("Target must be a .zip or a directory")
        sys.exit(1)

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_py = len(py_files)
    total_json = len(json_files)

    print(f"Source: {source}")
    print(f"Python probes: {total_py}")
    print(f"JSON metrics:  {total_json}")
    print("\nCluster counts:")
    for c, files in sorted(clusters.items(), key=lambda x: -len(x[1])):
        print(f"  {c}: {len(files)}")

    out_dir = Path("/home/workdir/artifacts/knowledge")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "research_probe_archive_index_latest.md"

    lines = [
        f"# Research Probe Archive Index (latest)",
        f"# Generated: {now}",
        f"# Source: {source}",
        "",
        f"- Python probes: **{total_py}**",
        f"- JSON files: **{total_json}**",
        "",
        "## Clusters",
        "",
    ]
    for c, files in sorted(clusters.items(), key=lambda x: -len(x[1])):
        lines.append(f"### {c} ({len(files)})")
        for f in sorted(files)[:15]:
            lines.append(f"- `{f}`")
        if len(files) > 15:
            lines.append(f"- ... and {len(files)-15} more")
        lines.append("")

    lines.extend([
        "## Usage notes for Compound Loop",
        "- Prefer promoting 1–3 self-contained probes into `scripts/` when a milestone needs them.",
        "- Do not bulk-commit the entire archive into GitHub knowledge/.",
        "- Combine with `chimera_swarm_4_void_walking_primitives.md` and `fire_wasi_automated_lab_blueprint.md` for Chimera 2.0 work.",
        "",
    ])

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out_path}")

if __name__ == "__main__":
    main()
