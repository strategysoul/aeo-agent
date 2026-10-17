# Capability tests

One test per source, cheapest call first. "Tool names" are matched loosely: connector tool names differ by client (for example `mcp__ahrefs__…` in Claude Code, or a UUID-prefixed name in Claude desktop). Look at your available tools, including deferred ones, for a name or description that matches.

For environment variables, check only whether they are set. Example (bash): `[ -n "${OPENAI_API_KEY:-}" ] && echo set || echo missing`. Never print a value.

## Free sources

### `web` — web search and fetch
- Detect: built in to Claude.
- Test: fetch `https://<domain>/robots.txt`.
- Record: `status: available`. If the fetch fails because the site blocks it, still `available`, and note the error; the site's own crawl settings are a technical finding for later.

### `gsc` — Google Search Console
- Detect: a connected tool that lists Search Console sites or properties, or queries search analytics.
- Test: list properties. Find the one matching the domain: `sc-domain:<domain>`, `https://<domain>/` or `https://www.<domain>/`.
- Record: `status: available`, `property: <exact property string>`. Property list works but no match: `status: error`, `last_error: "no property for this domain"`.
- No tool: `status: missing`. The Chrome fallback (reading Search Console in the user's browser) counts only for manual checks, not as `available`.

### `chrome` — Claude in Chrome
- Detect: `claude-in-chrome` tools (`tabs_context_mcp`, `navigate`, `get_page_text`).
- Test: `tabs_context_mcp`. Do not open any AI site during setup.
- Record: `status: available`. Tools present but the call says the extension is not connected: `status: error`, with the message.
- Which AI tools the user is logged into is checked in the visibility step, not here.

## SEO data sources

### `ahrefs`
- Detect: Ahrefs MCP tools.
- Test: the subscription-info / limits-and-usage tool. Ahrefs documents it as reporting plan limits and current usage.
- Record: `plan`, `units_left`, `units_reset`, `row_limit`, and `addons` (look for Brand Radar in the response). If the response does not include a field, leave it out rather than guessing.
- Plan row limits published by Ahrefs (help center, checked 2026-10-17): Lite 100, Standard 250, Advanced 500, Enterprise unlimited. Use the live response first; this list is only for display if the response lacks it.
- 401 error: see `docs/setup/ahrefs.md` → Common errors.

### `semrush`
- Detect: Semrush MCP tools (`keyword_research`, `get_report_schema`, `execute_report`, …).
- Test: `get_report_schema` for one keyword report. It returns parameters, not data.
- Balance: if `SEMRUSH_API_KEY` is set, run the free call `curl -s "https://www.semrush.com/users/countapiunits.html?key=$SEMRUSH_API_KEY"` from a shell. It returns the units left as a number. Never echo the key.
- Record: `status: available, via: mcp, unit: units`, and `units_left` if the balance call worked. Without it, keep any `units_left` the user entered and note "balance not readable; set SEMRUSH_API_KEY or units_left".
- Only `SEMRUSH_API_KEY` set, no MCP tools: `status: missing` with the note "API key set, connector not connected". The keywords step uses Semrush through MCP only.

### `dataforseo`
- Detect: DataForSEO MCP tools (`api_request`, `docs_search`, or older per-endpoint tools), or both `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` set.
- Test: `GET /v3/appendix/user_data` (free) through `api_request`, or through `curl -s -u "$DATAFORSEO_LOGIN:$DATAFORSEO_PASSWORD" https://api.dataforseo.com/v3/appendix/user_data` if there is no MCP.
- Record: `status: available, via: mcp | api, unit: usd, units_left: <money.balance>`.
- 401: `status: error`, `last_error: "authentication failed"`; see `docs/setup/dataforseo.md`.

## AI-visibility sources

### `brand_radar`
- Not a separate connector: it is an Ahrefs add-on. Take it from the `ahrefs` test (`addons`). Present: `status: available, via: ahrefs`. Ahrefs test passed but no add-on listed: `status: missing`. No Ahrefs: `status: missing`.

### `nimble`
- Detect: Nimble MCP tools (`nimble_*`).
- Test: none; setup spends no pages. Record `untested` if the tools are present, `missing` if not. The visibility or research step sets `available` after its first successful call, or `error` with the message.
- `NIMBLE_API_KEY` set but no tools: `missing`, note "API key set, connector not connected".

## AI-engine API keys

Used by `scripts/ask_engines.py`. Test all four in one go with free calls (listing models), from a shell:

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/ask_engines.py" --check
```

It prints JSON with a `status` per engine: `available`, `missing`, `untested` (Perplexity: key set, no free check exists) or `error` with `last_error`. Copy each into `capabilities.sources.<engine>` with `via: env`. If Python is not available, record a set key as `untested` and note "python not found".

| Source | Variable |
|---|---|
| `openai` | `OPENAI_API_KEY` |
| `perplexity` | `PERPLEXITY_API_KEY` |
| `gemini` | `GEMINI_API_KEY` |
| `anthropic` | `ANTHROPIC_API_KEY` |

## Research helpers

| Source | Detect |
|---|---|
| `firecrawl` | Firecrawl MCP tools or `FIRECRAWL_API_KEY` |

Record `untested` if detected, `missing` if not. Setup spends no credits on it: the research step sets `status: available` after its first successful call, or `error` with the message if that call fails.