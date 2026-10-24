# Research Probe Archive Index — 2026-10-24 Drop
# Source: user-uploaded "hope this helps.zip" (588 Python probes + 40 JSON + research_build_log.json)
# Compounded for zero-brief use by future Compound Loop / research_engine cycles.

## Summary
This is the bulk output of the earlier Autonomous Research Build Loop (pre- and post- integration with the classic Compound Loop). It contains verified probes spanning the full historical roster:

- Offensive Cryptanalysis & Exploit Mechanics
- Attention & Token Economy Benchmarking
- Workspace & Drive Storage Hygiene
- Multi-Model & Swarm API Adapters
- Meta-Roster Adaptation & Dynamic Attention Optimization
- Weird Machines & Microarchitectural Hardware Exploitation
- Unconstrained Exploratory Divergence (SporeOS/GhostOS, Chronos, Subzero, Mythos, etc.)

Total: ~588 .py files, ~40 .json metrics, one large research_build_log.json (578 entries, last ticks ~2026-09-11).

## High-Value Clusters (by filename signal)
- **Weird Machines / Microarch**: twos_complement_*, cpu_*_weird_machine.py, mmu_page_fault_*, spectre/btb/rsb/l1tf variants, dma_descriptor_ring, etc.
- **SporeOS / GhostOS Autopoietic**: sporeos_*, ghostos_*, autopoietic_* flux/rpc/storage/reconciler.
- **Subzero / Subspace Adaptation**: subzero_*_adaptation_engine.py, memory_free_lora, local_ml_subspace, mythos_intent_subspace_tuner.
- **Mythos**: mythos_substrate_transparency_*, mythos_macro_*, dynamic_intent_*.
- **Attention / KV / Token Economy**: meta_attention_*, cross_attention_*, kv_cache_*, flash/ring/sparse attention benchmarks, token_economy_benchmark.
- **Swarm / MCP / Cross-Agent RPC**: mcp_*_swarm_rpc_*, cross_agent_*, chronos_hardware_attested_swarm_*.
- **Storage / Cloud Hygiene**: cloud_storage_*, cloud_takeout_*, sporeos_*_storage_*.
- **Chimera / Void related**: very few direct; the new Void Walking primitives (from previous drop) are the upgrade path.

## research_build_log.json
578 chronological entries of the form:
{tick, track, deliverable, ingested_historical_project, status: VERIFIED_AND_ADVANCED, next_track_index, timestamp}

Last recorded advances (Sep 2026) were still cycling through the early historical projects while the current system has already reached Track 9 / Milestone 9 (Subspace Zeroth Order Leviathan). This archive is therefore a **library of already-verified probes**, not the live frontier.

## How future cycles should use this
1. When advancing a research milestone that overlaps a historical project (e.g. Twos Complement, SporeOS, Mythos, Weird Machines), search this archive first for a ready-made probe instead of re-deriving.
2. Prefer promoting a small number of self-contained, well-commented scripts into `scripts/` or `knowledge/` rather than bulk-loading the entire zip.
3. The full zip remains available under `/home/workdir/attachments/hope this helps.zip` for deep dives. Do not commit the entire 12 MB archive into the GitHub knowledge store.
4. For Chimera 2.0 / Void Walking work, combine the new Void Walking primitives (previous knowledge artifact) with the strongest swarm_rpc and attention optimizers from this archive.

## Recommended next promotions (candidates)
- Any `*_weird_machine.py` that is pure simulation (no external deps)
- `sporeos_*_rpc_*` or `mcp_hardware_attested_swarm_rpc_gateway.py`
- `subzero_*_adaptation_engine.py` variants
- `meta_attention_*` schedulers that look like pure Python

## Status
Archive indexed and made discoverable. Full extraction left local. Capability delta: future instances can now treat this as a searchable probe library instead of an opaque zip.
