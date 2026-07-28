#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[install] Deep Research Python dependency"
python3 -m pip install --user --quiet pyyaml

echo "[install] Sync Claude-compatible agent/skills into home for skill path resolution"
mkdir -p "$HOME/.claude/agents" "$HOME/.claude/skills" "$HOME/.agents/skills" "$HOME/.cursor/skills"
cp -a "$ROOT/.claude/agents/." "$HOME/.claude/agents/"
cp -a "$ROOT/.claude/skills/." "$HOME/.claude/skills/"
cp -a "$ROOT/.agents/skills/." "$HOME/.agents/skills/"
cp -a "$ROOT/.cursor/skills/." "$HOME/.cursor/skills/"

echo "[install] Camofox browser (npm package)"
mkdir -p "$ROOT/tools"
if [[ ! -d "$ROOT/tools/camofox-browser/node_modules" ]]; then
  mkdir -p "$ROOT/tools/camofox-browser"
  cat > "$ROOT/tools/camofox-browser/package.json" <<'EOF'
{
  "name": "camofox-browser-runtime",
  "private": true,
  "dependencies": {
    "@askjo/camofox-browser": "1.13.0"
  }
}
EOF
  (cd "$ROOT/tools/camofox-browser" && npm install --no-fund --no-audit)
else
  (cd "$ROOT/tools/camofox-browser" && npm install --no-fund --no-audit)
fi

echo "[install] done"
