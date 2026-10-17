# Weekly AEO report: northpine-running.example

MADE-UP EXAMPLE.

Week to 2026-10-13 · run 2026-10-13-report-9a0b · Setup level: Recommended

## Summary
Northpine was named in 8 of 24 AI answers this week (ChatGPT 3 of 12, Perplexity 5 of 12), up from 6 of 24, but with 12 answers per engine that change is within normal variation. It is never named for bunions or for alternatives to Ridgeline. ChatGPT says Northpine "ships worldwide", which comes from an old line on the shipping page; that fix is marked done but the line is still live. Claude-SearchBot is still blocked in robots.txt.

## Start here
1. **A003 · Remove the "ships worldwide" line** — 5 minutes, you (Shopify admin). In Online Store → Pages → Shipping, replace "We ship worldwide (coming 2025)." with "We ship to the US and Canada." Your earlier change did not reach the live page.
2. **A001 · Allow Claude-SearchBot** — 10 minutes, you (Shopify admin). In `robots.txt.liquid`, delete the two `Claude-SearchBot` lines.
3. **A008 · Ask Run Review to include Northpine** — 15 minutes, you. The message to paste is in actions.md.

Full steps: [actions.md](../actions.md).

## Needs your review
- A003 is marked done, but /pages/shipping still contains "We ship worldwide (coming 2025)". Check whether the change was published, then run `/aeo-agent:aeo northpine-running.example review`.

## Search rankings
| Topic | Clicks | Change | Impressions | Change | Avg position | Change |
|---|---|---|---|---|---|---|
| Wide trail running shoes | 70 | +6 | 1,860 | +70 | 14.3 | −0.5 (better) |
| Trail shoes for bunions | 83 | −2 | 810 | +20 | 7.8 | −0.1 (better) |
| Choosing shoe width | 59 | +2 | 650 | +10 | 5.5 | −0.1 (better) |
| Alternatives to Ridgeline | 0 | 0 | 0 | 0 | — | — |

Source: Search Console, 2026-10-04 to 2026-10-10 compared with 2026-09-27 to 2026-10-03.

## AI answers
| Engine | Source | Answers | Mentioned | Cited | Share of voice | Change since last week |
|---|---|---|---|---|---|---|
| ChatGPT (OpenAI API, gpt-5.5) | api:openai | 12 | 25% | 17% | 14% | mentioned +8 pts, cited +9 pts |
| Perplexity (Sonar API) | api:perplexity | 12 | 42% | 33% | 20% | mentioned +9 pts, cited +8 pts |

These changes are under 10 points on fewer than 30 answers per engine, so treat them as noise, not a trend. API answers can differ from what people see in the ChatGPT and Perplexity apps.

Topics where the brand is never mentioned:
- Trail shoes for bunions — WideFoot Gear, Ridgeline and Trailkind are named; podiatry-notes.example is cited in all 4 answers
- Alternatives to Ridgeline — WideFoot Gear and Trailkind are named; runreview.example, gearlab-test.example and hikeboard.example are cited

Accuracy problems:
- ChatGPT, p011: "It ships worldwide" → Northpine ships to the US and Canada only (accuracy 0; see A003)
- Perplexity, p012: "Prices start from $99" → current range is $129–$169 (accuracy 1)

## Technical health
Health score: 98.3 (own crawl, 120 pages) · change 0
Search bots blocked: Claude-SearchBot (A001)
New errors: 0 · Fixed: 6 (canonical tags on product pages)

## Actions
Confirmed this week: A002 canonical tags on 6 product pages
New: none (all gaps already have actions)
Open: 7 (2 high priority: A001 Claude-SearchBot, A004 alternatives page) · Waiting for check: 1 (A003)

## Sources and spending
| Step | Source | Method | Units or calls | Budget |
|---|---|---|---|---|
| Technical | own crawl (crawl_check.py) | measured | 120 pages | 200 pages |
| AI answers | OpenAI API with web search | measured | 12 calls | 100 calls, all engines |
| AI answers | Perplexity Sonar API | measured | 12 calls | (same) |
| Rankings | Search Console | measured | free | — |
| Keywords | not run this week (last 2026-10-06; next refresh due 2026-11-05) | — | — | — |

Not measured: Gemini, Claude and Copilot (no API key or AI-visibility source); Google AI Overviews and AI Mode (no AI-visibility source, and Claude in Chrome is not connected). Connecting an Anthropic key would also show whether A001 changes Claude's answers.
