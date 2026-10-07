# Outward primitive — retain / recall / reflect

Generated: 2026-10-07T10:34:30Z
Source shortlist: cycle-2 x-signal-ledger (hindsight / openrig / univer).
TAKE: vectorize-io/hindsight. Not installed. The op split is the primitive.

## Local map

- retain: append to ledger, log, instance-history. Never rewrite prior entries.
- recall: `python3 scripts/pull-outward-primitive.py --recall <tokens>` — ranked file hits, no LLM.
- reflect: a cycle decision over those hits. Do not call a lookup a reflection.

## Cards

### TAKE — vectorize-io/hindsight
- why: Memory ops split lookup from synthesis. Maps onto append-only files without a new skill.
- stars: 46514  branch: main  license: MIT  source: github_connected_tool
- updated: 2026-10-07T10:29:17Z
- Hindsight: Agent Memory That Learns
- public_api: HTTP Error 403: rate limit exceeded (used stamped observation)

### DEFER — mvschwarz/openrig
- why: A rig wraps harnesses. Needs tmux, Node 22, and provider CLIs this sandbox does not have.
- stars: 5614  branch: main  license: Apache-2.0  source: github_connected_tool
- updated: 2026-10-07T10:32:27Z
- Build your own network of agents from Claude Code, Codex and Pi: persistent teams with roles, shared context and owned work.
- public_api: HTTP Error 403: rate limit exceeded (used stamped observation)

### DEFER — dream-num/univer
- why: Office runtime. Local docx/pptx/xlsx/pdf skills already cover the composition point.
- stars: 22431  branch: dev  license: None  source: github_connected_tool
- updated: 2026-10-07T10:11:36Z
- The Office Harness for AI Agents — Spreadsheets, Docs, Slides, Canvas, Relational Tables, and PDF in one runtime.
- public_api: HTTP Error 403: rate limit exceeded (used stamped observation)

Rejected this cycle: installing hindsight, cloning openrig, wrapping univer. Those are products. The op split is the capability.
