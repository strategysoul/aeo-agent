# Recipe: Semrush (MCP connector)

Checked 2026-10-17 against [Semrush MCP](https://developer.semrush.com/api/basics/semrush-mcp/) and [API unit balance](https://developer.semrush.com/api/basics/api-units-balance/).

Semrush MCP exposes discovery tools (`keyword_research`, `organic_research`, `competitors_research`, `domain_overview`, `site_audit`, `projects`, and others) plus `get_report_schema` and `execute_report`. Call `get_report_schema` for a report before running it with `execute_report`, so parameters come from the schema rather than memory.

## Cost

- Most reports charge per line returned. Semrush documents 10 units per line for Domain Organic Search Keywords (50 for historical data). Other reports have their own rates, listed on each method's page in the Semrush API docs.
- Before a batch, look up the rate for each report on its developer.semrush.com page. If you cannot confirm it, estimate 50 units per line and say the estimate is conservative.
- Always set the number of lines (`display_limit` or the schema's equivalent).
- Balance:
  - If `SEMRUSH_API_KEY` is set, the free call `https://www.semrush.com/users/countapiunits.html?key=$SEMRUSH_API_KEY` returns the units left as a number. Run it from a shell so the key is read from the environment and never written out. Call it before and after the run.
  - Otherwise there is no balance tool in MCP. Use `units_left` from `config.yaml` (the user reads it from **Subscription info → Summary**) and `budget.hard_cap_units`. If both are empty, stop before spending and ask the user for one of them.

## Calls by need

| Need | Tool | What to ask for |
|---|---|---|
| Site authority | `domain_overview` | Authority Score of the site, main country database |
| Seed expansion | `keyword_research` | related keywords and broad-match keywords for each seed |
| Questions | `keyword_research` | question keywords for each seed |
| Volume, difficulty, intent | `keyword_research` | keyword overview (batch) and keyword difficulty |
| Competitor keywords | `organic_research` | organic keywords for each competitor domain, positions 1–20 |
| Organic competitors | `competitors_research` | organic competitors of the site |
| Google results | `organic_research` | organic results for a keyword (top 10), with SERP features |

Use the country database matching `countries[0]` (for example `us`, `uk`, `de`).

## Mapping to `raw.csv`

| Semrush field | Column |
|---|---|
| Search Volume | `volume` (`method: estimated`) |
| Keyword Difficulty | `difficulty` |
| Intent | `intent` |
| SERP features containing AI Overview | `ai_overview: yes` |
| Authority Score | `config.yaml` → `capabilities.sources.semrush.site_authority` |

`source: semrush`.
