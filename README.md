# AEO Agent

A Claude plugin that checks whether a website shows up in Google **and** in AI answers (ChatGPT, Perplexity, Gemini, Claude, Google AI Overviews), works out which keywords and questions matter to the business, and tells you what to change. It re-checks every week and tracks the results.

Site health tools show whether a site can be crawled. This agent answers the next questions: which searches and questions matter for this business, does the site appear for them in Google and in AI answers, who appears instead, and what would change that.

It works with whatever tools you have — from nothing paid to full SEO suites — and tells you what each missing tool would add and how to connect it.

## What it does

1. **Profile and research.** Reads your site and writes a profile. Checks seven research questions (product and price; audiences and the words they use; competitors; who ranks and gets cited; questions people ask; where audiences talk; rules that limit what you can say) against any research you already have, and researches only what is missing or older than 90 days. You approve the brief.
2. **Keywords.** Finds keywords and questions from your seed terms, competitors, "People also ask" and Search Console. Scores them on audience fit, intent, demand, difficulty and AI-answer potential, and groups them into page-sized topics. You approve the priority topics.
3. **AI visibility.** Writes 30–100 natural questions for the approved topics, asks them through the best source you have, and scores each answer: is the brand mentioned, in what position, is the site cited, is what it says accurate, is it positive. Records which sites AI answers cite instead.
4. **Technical check.** robots.txt access for AI and search crawlers (OAI-SearchBot, PerplexityBot, Claude-SearchBot, GPTBot, ClaudeBot, Google-Extended and more), indexability, titles, canonicals, structured data, pages that need JavaScript to show their content.
5. **Actions.** For each topic: is there a page, does it rank, is it cited, who is cited instead. Turns the gaps into specific actions — pages to write or rewrite (with a brief), technical fixes, other sites to get listed on — each with its evidence, expected effect, effort and a check. Confirms done actions on the live site.
6. **Weekly report.** Rankings, AI visibility trend, technical health, actions done and open, sources used and units spent.

It **recommends; it never changes your site**, CMS, DNS or tool settings. See [docs/how-it-works.md](docs/how-it-works.md).

## Setup levels

| Level | Tools | What you get |
|---|---|---|
| **Free** | Claude's web search and fetch, [Google Search Console](docs/setup/google-search-console.md), [Claude in Chrome](docs/setup/claude-in-chrome.md) | Research, your own rankings and clicks, and AI answers read from your logged-in AI tools in Chrome. Keyword volumes are estimates labelled "inferred". |
| **Recommended** | Free + one SEO data source ([Ahrefs](docs/setup/ahrefs.md), [Semrush](docs/setup/semrush.md) or [DataForSEO](docs/setup/dataforseo.md)) + at least one [AI-engine API key](docs/setup/ai-engine-api-keys.md) | Measured keyword volume and difficulty, competitor keywords, site audit, and repeatable AI-answer checks |
| **Full** | Recommended + an AI-visibility source ([Ahrefs Brand Radar](docs/setup/brand-radar.md) or [Nimble](docs/setup/nimble.md)) + keys for all four engines | AI answers with search-volume context and citation share across more engines |

`/aeo-agent:aeo <domain> setup` tests what you have connected and shows this table for your setup, with links to the guide for each missing tool.

## Install

**Claude Code:**

```bash
claude plugin marketplace add strategysoul/aeo-agent
```

```bash
claude plugin install aeo-agent@aeo-agent
```

Or inside a session: `/plugin marketplace add strategysoul/aeo-agent`, then `/plugin install aeo-agent@aeo-agent`.

**Claude desktop and Cowork:** download `aeo-agent.plugin` from the [latest release](https://github.com/strategysoul/aeo-agent/releases/latest) and add it in the app's plugin settings.

The scripts need Python 3.9 or later and no extra packages.

## Quick start

```text
/aeo-agent:aeo example.com setup
```

Setup creates a folder for the site (default `~/Documents/AEO/<domain>/`; set `AEO_ROOT` to change it), tests your tools, asks you to confirm the site's countries and languages, and offers to schedule the weekly run. Then:

```text
/aeo-agent:aeo example.com research
/aeo-agent:aeo example.com keywords
/aeo-agent:aeo example.com weekly
```

Approve the research brief and the topics when asked. After that, the [scheduled runs](docs/setup/scheduling.md) keep everything up to date, and `/aeo-agent:aeo example.com review` shows anything waiting for you.

All modes: `setup`, `research`, `keywords`, `visibility`, `technical`, `actions`, `report`, `review`, `daily`, `weekly`. Use `--all` instead of a domain to run every site.

See a full example on a made-up site: [examples/example-site](examples/example-site/README.md).

## Costs

The plugin is free. The tools it uses cost what their providers charge; the agent only uses what you have connected and keeps to a budget you set (by default at most 10% of a tool's remaining monthly units per site per run, and 100 AI-engine questions per run). Details per tool: [docs/costs.md](docs/costs.md).

## Limits

- **AI answers vary.** The same question can get a different answer tomorrow. The agent asks the same questions every week and calls small changes noise.
- **API answers are not app answers.** Answers from the engines' APIs can differ from what people see in the ChatGPT, Perplexity, Gemini or Claude apps. Answers read in Chrome reflect your own account.
- **Estimates are labelled.** Search volumes are provider estimates; without an SEO tool they are inferred from signals. Every number in every file says where it came from (`source`, `method`, `record_date`, `run_id`).
- **Some coverage depends on paid tools.** Google AI Overviews, AI Mode and Copilot can only be measured through Brand Radar, Nimble, DataForSEO or your Chrome session.
- **Local schedules need the computer awake.** Cloud routines can't read local folders. See [docs/setup/scheduling.md](docs/setup/scheduling.md).
- **No guarantees.** Recommendations follow current documentation from Google, OpenAI, Perplexity and Anthropic, but no one controls what an AI engine says.

## Privacy and keys

API keys live in environment variables or your client's connector settings, never in files the agent writes. Site folders stay on your computer. Nothing is sent anywhere except to the tools you connected. See [SECURITY.md](SECURITY.md).

## More

- [How it works](docs/how-it-works.md) · [Data sources and fallbacks](docs/data-sources.md) · [Costs](docs/costs.md) · [Troubleshooting](docs/troubleshooting.md)
- Setup guides: [docs/setup/](docs/setup/)
- [Contributing](CONTRIBUTING.md) · [License (MIT)](LICENSE)
