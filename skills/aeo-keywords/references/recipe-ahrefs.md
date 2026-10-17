# Recipe: Ahrefs (MCP connector)

Checked 2026-10-17 against [Ahrefs MCP tool categories](https://docs.ahrefs.com/mcp/docs/tool-categories) and [limits consumption](https://docs.ahrefs.com/api/docs/limits-consumption).

Tool names differ by client. Match tools by their group and description. Read a tool's input schema before the first call; do not guess parameter names.

## Cost

- Each call costs `max(50, per_row_cost × rows)` units. Always set the row limit (`limit` or similar) to what you need.
- Requests served from Ahrefs' cache cost nothing.
- Rows per request are capped by plan (Lite 100, Standard 250, Advanced 500). A response with exactly the cap is cut off.
- Balance: the `subscription-info` tool reports plan limits and usage. Call it before and after the run to measure what the run spent.

## Calls by need

| Need | Tool group | What to ask for |
|---|---|---|
| Site authority | `public` (free domain rating) or `site-explorer` overview | Domain Rating (0–100) of the site |
| Seed expansion | `keywords-explorer` | matching terms, related terms, search suggestions for each seed, in the main country |
| Questions | `keywords-explorer` | matching terms filtered to questions, for each seed |
| Volume, difficulty, intent | `keywords-explorer` overview | volume, KD, intent, SERP features for a batch of keywords |
| Competitor keywords | `site-explorer-reports` | organic keywords for each competitor domain, positions 1–20, sorted by traffic |
| Organic competitors | `site-explorer-reports` | organic competitors of the site |
| Google results | `serp-overview` | top 10 for a keyword; note AI Overview and "People also ask" if returned |

## Mapping to `raw.csv`

| Ahrefs field | Column |
|---|---|
| volume | `volume` (`method: estimated`) |
| keyword difficulty (KD) | `difficulty` |
| intents | `intent` |
| SERP features containing an AI Overview | `ai_overview: yes` |
| Domain Rating | `config.yaml` → `capabilities.sources.ahrefs.site_authority` |

`source: ahrefs`.
