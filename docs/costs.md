# Costs

The plugin is free (MIT). You pay the providers of the tools you connect, at their prices. Figures below were checked on 2026-10-17; each setup guide links to the provider's current pricing page.

| Tool | Pricing model | Notes | Guide |
|---|---|---|---|
| Claude | your Claude plan | Every run uses your plan's usage like any other session | — |
| Google Search Console | free | — | [guide](setup/google-search-console.md) |
| Claude in Chrome | included in Pro, Max, Team, Enterprise | — | [guide](setup/claude-in-chrome.md) |
| Ahrefs | subscription, Lite and up for MCP | API units per month (Lite 200,000); each call at least 50 units | [guide](setup/ahrefs.md) |
| Ahrefs Brand Radar | add-on | from $199 a month for one AI platform, $699 for all | [guide](setup/brand-radar.md) |
| Semrush | subscription with API units | 50,000 units on Pro and Guru plans; most reports charged per line | [guide](setup/semrush.md) |
| DataForSEO | pay as you go, $50 minimum top-up | Labs about $0.012 per task + $0.00012 per item | [guide](setup/dataforseo.md) |
| OpenAI, Perplexity, Gemini, Anthropic | per call, plus tokens | e.g. Perplexity Sonar $5–12 per 1,000 requests; Anthropic web search $10 per 1,000 searches; Gemini 5,000 free searches a month | [guide](setup/ai-engine-api-keys.md) |
| Nimble | per page | $1 per 1,000 pages, 5,000 free | [guide](setup/nimble.md) |

## How the agent keeps to a budget

Set in each site's `config.yaml`:

| Setting | Default | Applies to |
|---|---|---|
| `budget.share_of_remaining` | 0.10 | Share of a tool's remaining units (or dollars for DataForSEO) per site per run |
| `budget.hard_cap_units` | none | Absolute cap per run |
| `budget.engine_calls_per_run` | 100 | AI-engine API questions per site per run, all engines together |
| `budget.chrome_prompts_per_engine` | 20 | Questions per engine through Chrome |

Before spending, each step shows its planned calls and estimated cost, and cuts the lowest-value calls if the plan goes over budget. After the run it reads the balance again where the tool allows and logs the actual spend in `state.json`. The weekly report has a "Sources and spending" table.

## Rough monthly cost per site

With weekly runs, 50 AI questions and two engines (OpenAI and Perplexity): about 400 API calls a month. With DataForSEO as the SEO source, a monthly keyword refresh is usually a few dollars. Your numbers depend on question count, engines, answer length and plan; check the spending table after the first few runs.
