# Connected Tool Router

- generated_at: 2026-09-29T10:34:00Z
- how_to_use_later: During GENERATE/EXECUTE, pick a row and call `search_connected_tools` then `call_connected_tool`. Do not rediscover schemas from scratch.

## Services present this cycle

| service | remote_name | zero-brief use |
|---------|-------------|----------------|
| Automations | Automations | Daily ignition already exists (`daily-compound-ignition`, taskId `fb6b558c-e940-4941-99c2-3c2cd4eaec99`, 06:30 America/New_York, APP_ONLY). List before creating. Do not spawn duplicates. |
| GitHub | GitHub | Search repos/code, file trees, issues/PRs. Outward: persist harvest notes under `artifacts/knowledge/`. |
| Google Drive | Google Drive | Search/read files when a cycle needs external docs. |
| Vercel | Vercel | Deploy/inspect projects if an outward artifact needs hosting. |
| Voice | Voice | TTS of a brief when a cycle wants a spoken artifact. |

## Call pattern

1. `search_connected_tools` with the action phrase.
2. Read `json_schema` from the returned tool.
3. `call_connected_tool(tool_name, arguments)`.
4. Write a durable note under `/home/workdir/artifacts/knowledge/` so the next cycle does not re-probe.

## Anti-patterns

- Creating another daily-compound-ignition automation (three already exist; only one schedule is enabled).
- Calling connected tools without writing an artifact.
- Assuming Gmail/Slack/Linear exist; they did not appear in the connected set this cycle.
