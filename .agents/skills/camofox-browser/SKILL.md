---
name: camofox-browser
description: >-
  Use the Camofox anti-detection browser API for web browsing, scraping,
  login flows, and sites that block Playwright/Chrome. Prefer this over
  plain WebFetch when pages need JS rendering, Cloudflare bypass, or
  interactive click/type flows. Server default: http://localhost:9377.
---

# Camofox Browser

Stealth headless browser for AI agents (Camoufox / Firefox). Talk to the local
REST API with `curl` or any HTTP client — do not assume OpenClaw plugin tools
are available in Cursor.

## When to use

- Page needs a real browser (JS-rendered content, SPAs)
- Bot detection / Cloudflare / captcha blocks ordinary fetch
- Need click, type, scroll, screenshot, or search macros
- Authenticated browsing with cookies / storage state

## Prerequisites

1. Camofox server should already be running (see environment `terminals`).
2. Health check:

```bash
curl -sS http://localhost:9377/health
```

If it is down, start it from `tools/camofox-browser` (created by install):

```bash
cd tools/camofox-browser && npm start
```

Default base URL: `http://localhost:9377`. Use a stable `userId` per agent run
(e.g. `cursor-cloud`) so sessions stay isolated.

## Core workflow

1. **Create tab** → get `tabId`
2. **Navigate** (URL or search macro)
3. **Snapshot** → accessibility tree with refs `e1`, `e2`, …
4. **Interact** (click/type/scroll) using refs
5. Re-snapshot after navigation (refs reset)

## Essential API (curl)

### Create tab

```bash
curl -sS -X POST http://localhost:9377/tabs \
  -H 'Content-Type: application/json' \
  -d '{"userId":"cursor-cloud","sessionKey":"task1","url":"https://example.com"}'
```

### Navigate / search macro

```bash
curl -sS -X POST "http://localhost:9377/tabs/$TAB_ID/navigate" \
  -H 'Content-Type: application/json' \
  -d '{"userId":"cursor-cloud","url":"https://example.com"}'

curl -sS -X POST "http://localhost:9377/tabs/$TAB_ID/navigate" \
  -H 'Content-Type: application/json' \
  -d '{"userId":"cursor-cloud","macro":"@google_search","query":"weather today"}'
```

### Snapshot

```bash
curl -sS "http://localhost:9377/tabs/$TAB_ID/snapshot?userId=cursor-cloud"
```

### Click / type / scroll

```bash
curl -sS -X POST "http://localhost:9377/tabs/$TAB_ID/click" \
  -H 'Content-Type: application/json' \
  -d '{"userId":"cursor-cloud","ref":"e1"}'

curl -sS -X POST "http://localhost:9377/tabs/$TAB_ID/type" \
  -H 'Content-Type: application/json' \
  -d '{"userId":"cursor-cloud","ref":"e2","text":"hello","pressEnter":true}'

curl -sS -X POST "http://localhost:9377/tabs/$TAB_ID/scroll" \
  -H 'Content-Type: application/json' \
  -d '{"userId":"cursor-cloud","direction":"down","amount":500}'
```

### Close tab

```bash
curl -sS -X DELETE "http://localhost:9377/tabs/$TAB_ID?userId=cursor-cloud"
```

## Search macros

`@google_search`, `@youtube_search`, `@amazon_search`, `@reddit_search`,
`@wikipedia_search`, `@twitter_search`, `@yelp_search`, `@linkedin_search`

## Auth notes

- If `CAMOFOX_ACCESS_KEY` is set, send `Authorization: Bearer <key>` on every request except `/health`.
- Cookie import requires `CAMOFOX_API_KEY` (disabled when unset).
- Interactive login: see VNC plugin docs in references (needs `ENABLE_VNC=1`).

## Full reference

Read [`references/AGENTS.md`](references/AGENTS.md) for the complete agent API,
session model, plugins, Docker, and OpenAPI notes (`/docs`, `/openapi.json`).
