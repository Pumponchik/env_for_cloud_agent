# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **Cloud Agent environment**, not a standalone application. It ships two things (see `README.md`):

1. **Deep Research skills** — markdown SOPs under `.claude/skills`, `.agents/skills`, `.cursor/skills` (invoked by the agent; the only runtime dependency is `pyyaml` for `.agents/skills/research/validate_json.py`).
2. **Camofox Browser** — a stealth browser HTTP API runtime installed as the npm package `@askjo/camofox-browser` under `tools/camofox-browser/`.

### Setup / dependencies
- Bootstrap is `./scripts/cloud-agent-install.sh` (also the `install` step in `.cursor/environment.json`, and the configured Cloud update script). It is idempotent: installs `pyyaml`, syncs skills into `$HOME`, and `npm install`s the Camofox runtime.
- `tools/` and `node_modules/` are git-ignored runtime installs (see `.gitignore`); they are recreated by the install script, so a clean checkout will not contain them.

### Running the Camofox service (the only long-running service)
- Started automatically by the `camofox` terminal in `.cursor/environment.json`: `cd tools/camofox-browser && npx camofox-browser`. Run that same command to start it manually.
- Listens on **port 9377**. Health check: `curl -sS http://localhost:9377/health` (expect `"ok":true` with `"browserConnected":true`).
- On startup it launches an Xvfb virtual display + a Camoufox (Firefox) browser; the browser binary ships with the npm package, so no extra download step is needed.
- API usage (create tab → snapshot → click/type) is documented in `.agents/skills/camofox-browser/references/AGENTS.md`.

### Lint / test / build
- This repo has **no root `package.json`, `Makefile`, or its own lint/test/build**. Camofox's own test suite lives inside the installed npm package, not in this repo, and is not part of this repo's dev workflow. Do not expect `npm test` at the repo root.
