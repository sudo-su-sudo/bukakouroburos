# Sprawl gate

Generated: 2026-10-06T10:34:02Z
alias_count: 18
max_aliases: 18
sprawl_gate: pass
sprawl_ratio: 0.6
skill_count: 30

Command: `python3 scripts/skill-consolidator.py --max-aliases 18`
Exit 0 means the alias pile did not grow past the cycle-4 baseline.
Exit 1 means the cycle failed the sprawl constraint. Do not push a pass.

Self-test this cycle: `--max-aliases 0` exited 1 with sprawl_gate=fail. The pass file above was rewritten by the real run (max 18) after the self-test used a throwaway out-dir.
