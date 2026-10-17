# How it works

The agent is a set of Claude skills plus three small Python scripts. Claude does the research, scoring and writing; the scripts do the parts that need exact, repeatable output.

| Piece | What it is |
|---|---|
| `skills/aeo` | Entry point: finds the site folder, picks the mode, enforces approvals, runs the weekly sequence |
| `skills/aeo-setup` | Tests every data source, writes the setup table, offers scheduling |
| `skills/aeo-profile-research` | Step 1: profile, coverage check, research, brief |
| `skills/aeo-keywords` | Steps 2–3: discovery, scoring, topics |
| `skills/aeo-visibility` | Steps 4–5: AI questions, answers, scoring |
| `skills/aeo-technical` | Technical and AI-crawler check |
| `skills/aeo-actions` | Steps 6–7: gaps, actions, page briefs |
| `scripts/ask_engines.py` | Asks OpenAI, Perplexity, Gemini and Anthropic with web search on; saves answers and citations |
| `scripts/crawl_check.py` | Polite crawl of the site: robots.txt per bot, sitemaps, page checks |
| `scripts/check_site.py` | Checks a site folder is complete and consistent |

## The site folder

Everything for one site lives in `<AEO_ROOT>/<domain>/` (default `~/Documents/AEO`). Nothing is stored anywhere else.

```
config.yaml      countries, languages, budgets, which tools are connected
state.json       approvals, last run per step, every run's spending
decisions.md     everything you told the agent, so it never asks twice
profile.md       what the site says about itself
research/        coverage.json, brief.md, competitors.csv, change_log.md, raw/<date>/
keywords/        raw.csv, scored.csv, topics.md
prompts.csv      the AI questions, stable week to week
visibility/      <date>.csv, history.csv, cited_domains.csv, raw/<date>/
technical/       latest.md, issues.csv, history.csv, raw/<date>/
gaps.csv         per-topic gap table
actions.md       open, done, confirmed, dismissed actions
briefs/          one brief per page action
reports/         <date>.md, latest.md, rankings.csv
```

Raw data goes into dated folders and is never overwritten, so runs can be compared. History files are append-only. A full example: [examples/example-site](../examples/example-site/README.md).

## Rules every step follows

- **It finds out what is available.** Setup makes the cheapest possible call to every source and records plan, units left and limits. Each step uses the best available source and falls back to the next if a call fails. See [data-sources.md](data-sources.md).
- **Every data point says where it came from:** `source`, `method` (measured, estimated, inferred), `record_date`, `run_id`. Reports say when a weaker source was used.
- **Ask once.** Every answer you give goes into `decisions.md` and is reused; the agent asks again only if you say something changed or new evidence contradicts it. Specific requests ("add a topic on X") touch only that part.
- **Actions you can do without thinking.** `actions.md` starts with the 3 quickest high-value changes. Each action says who does it, where (the exact page, CMS screen or file), numbered steps, the text or code to paste, and how the agent will check it. Page actions come with a ready-to-paste draft.
- **Research only what is missing.** Existing research is reused if it answers the seven questions; only missing or stale (over 90 days) parts are researched.
- **Two approvals.** You approve the research brief and the priority topics. Scheduled runs never approve; refreshed versions wait as proposals until you run `review`.
- **A budget per run,** by default 10% of a tool's remaining units per site, and 100 AI-engine questions. Spending is logged.
- **It recommends; it does not change anything.** No edits to the site, CMS, DNS, CDN or tool settings. No posting, signing up or contacting anyone.
- **Nothing private in files.** Keys stay in environment variables or connector settings.
- **No carry-over between sites.** Nothing from one site's folder is used for another.

## The weekly cycle

`/aeo-agent:aeo --all weekly --scheduled`:

1. Re-test tools if the last test is over 30 days old.
2. Refresh keywords if over 30 days old, research if over 90 (as proposals).
3. Technical check.
4. Ask the AI questions and score the answers.
5. Re-check existing actions on the live site; turn new gaps into actions.
6. Write the report.

A daily quick technical check runs on the other days. Scheduling: [setup/scheduling.md](setup/scheduling.md).
