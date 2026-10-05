# Eval Report

ts: 2026-10-05T10:34:21Z
composite: 0.9
persistence_verified: True

| key | score | meaning |
|---|---|---|
| github_roundtrip | 1.0 | substrate files present after BOOTSTRAP |
| outward_signal_freshness | 1.0 | ledger plus snapshot; docked if snapshot missing or >36h |
| skill_sprawl_risk | 1.0 | legacy: banned-name skills / 20 (not in composite) |
| zero_brief_scripts | 1.0 | harvest/brief/eval/consolidator scripts found |
| memory_quality | 1.0 | state, history depth, ledger, prior eval |
| sprawl_ratio | 0.6 | alias_count/skill_count from skill-canonical-map.json |
| eval_coverage | 1.0 | keys actually computed this run |

snapshot: present=True reason=fresh age_hours=0.0 dock=0.0 generated_at=2026-10-05T10:34:13Z
sprawl source: task-domain/skill-canonical-map.json alias_count=18 load_set=6
memory parts: {"completed_artifacts": 1.0, "state_ok": 1.0, "history_depth": 1.0, "log_depth": 1.0, "frontier_depth": 1.0, "ledger_depth": 1.0, "prior_eval": 1.0}

Run: `python3 /home/workdir/artifacts/scripts/eval-score.py`
