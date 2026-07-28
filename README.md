# Cloud Agent environment

Environment repo for Cursor Cloud Agents with:

1. **[Deep Research skills](https://github.com/Weizhena/Deep-Research-skills)** — structured research workflow (`research`, `research-deep`, `research-report`, …)
2. **[Camofox Browser](https://github.com/jo-inc/camofox-browser)** — stealth browser API skill + runtime on port `9377`

## Layout

| Path | Purpose |
|------|---------|
| `.cursor/skills/` | Cursor project skills (picked up by Cloud Agents) |
| `.agents/skills/` | Same skills for Agents discovery |
| `.claude/skills/` + `.claude/agents/` | Claude-compatible research skills + `web-search-agent` |
| `.cursor/environment.json` | Cloud Agent install + Camofox terminal |
| `scripts/cloud-agent-install.sh` | Idempotent bootstrap (`pyyaml`, skill sync, Camofox npm install) |

## Cloud Agent usage

1. Point your Cloud Agent environment at this repository (or use it as the agent workspace).
2. On start, `install` syncs skills and installs Camofox; the `camofox` terminal starts the browser server.
3. Invoke research with `/research <topic>` (and related skills).
4. For hard-to-fetch pages, use the `camofox-browser` skill against `http://localhost:9377`.

## Local check

```bash
./scripts/cloud-agent-install.sh
cd tools/camofox-browser && npx camofox-browser
# health: curl -sS http://localhost:9377/health
```

## Upstream sources

- Deep Research: English skills from `skills/research-en` + `agents/web-search-agent.md`
- Camofox: packaged as a Cursor skill from upstream `AGENTS.md` + npm `@askjo/camofox-browser@1.13.0`
