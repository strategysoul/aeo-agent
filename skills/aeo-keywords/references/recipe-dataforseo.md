# Recipe: DataForSEO (MCP connector or API login)

Checked 2026-10-17 against the [DataForSEO MCP server](https://github.com/dataforseo/mcp-server-typescript), [DataForSEO Labs docs](https://docs.dataforseo.com/v3/dataforseo_labs/google/overview/), [user_data](https://docs.dataforseo.com/v3/appendix/user_data/) and [pricing](https://dataforseo.com/pricing).

The current DataForSEO MCP server exposes documentation tools (`docs_index`, `docs_list_sections`, `docs_search`) and one call tool, `api_request`, which calls any API endpoint with the user's credentials. Older versions exposed one tool per endpoint; if those are what you see, use them with the same endpoints below.

Before calling an endpoint for the first time in a run, read its request fields with `docs_search` (or the docs page). Do not guess field names.

## Cost

- DataForSEO is pay-as-you-go in US dollars. Record `unit: usd` in `config.yaml`.
- `GET /v3/appendix/user_data` is free. It returns the balance (`money.balance`) and a `price` table per endpoint. Call it before the run, estimate each batch from the `price` table, and call it again after the run to measure the spend.
- Labs endpoints cost a fee per task plus a fee per item returned (the pricing page listed $0.012 per task + $0.00012 per item on 2026-10-17). Always set `limit`.
- Prefer one task with many keywords, up to the endpoint's keyword limit given in its docs, over many single-keyword tasks.

Without the MCP server, if `DATAFORSEO_LOGIN` and `DATAFORSEO_PASSWORD` are set, call the same endpoints at `https://api.dataforseo.com` with HTTP Basic auth from a shell, e.g. `curl -s -u "$DATAFORSEO_LOGIN:$DATAFORSEO_PASSWORD" …`. Never write the credentials out.

## Calls by need

All Labs paths start with `/v3/dataforseo_labs/google/` and end with `/live`.

| Need | Endpoint | Notes |
|---|---|---|
| Site authority | not in Labs | Leave `site_authority` empty; scoring treats it as unknown |
| Seed expansion | `keyword_suggestions`, `related_keywords`, `keyword_ideas` | one task per seed, `limit` 50–100 |
| Questions | `keyword_suggestions` filtered to keywords starting with question words in the site's language | |
| Volume, difficulty, intent | `keyword_overview` (volume, intent), `bulk_keyword_difficulty`, `search_intent` | batch the whole list |
| Competitor keywords | `ranked_keywords` | per competitor, filter rank ≤ 20 |
| Organic competitors | `competitors_domain` | for the site |
| Google results | `/v3/serp/google/organic/live/advanced` | top 10; the response lists item types, including `ai_overview` and `people_also_ask` |

Set `location_name` (or `location_code`) and `language_code` from `countries[0]` and `languages[0]`.

## Mapping to `raw.csv`

| DataForSEO field | Column |
|---|---|
| `keyword_info.search_volume` | `volume` (`method: estimated`) |
| `keyword_difficulty` | `difficulty` |
| `search_intent_info.main_intent` | `intent` |
| SERP item type `ai_overview` | `ai_overview: yes` |

`source: dataforseo`.
