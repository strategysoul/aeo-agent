# Recipe: no SEO data source

Used when none of `ahrefs`, `semrush`, `dataforseo` is `available`. Everything here is `method: inferred` unless it comes from Search Console.

## Discovery

- Seeds and questions from `research/brief.md` (questions 2 and 5) and `research/raw/*/seed-keywords.csv`.
- Search Console queries, if `gsc` is available (free and measured — always use it).
- Google autocomplete, if `chrome` is available: type each seed into the main country's Google domain and read the suggestions without running the search. At most 20 seeds per run. If Google shows a CAPTCHA, stop and tell the user; never try to solve it.
- "People also ask" and "Related searches" from Google results pages, read through Chrome or web search.

## Demand without volumes

Do not invent search volumes. Put a band in `demand_band` and leave `volume` empty:

| Band | Evidence |
|---|---|
| `high` | Search Console impressions ≥ 1,000 in 90 days, or the term appears in autocomplete for the bare seed and in "Related searches" |
| `medium` | impressions 100–999, or it appears in autocomplete or "People also ask" |
| `low` | impressions 1–99, or only forum or review mentions |
| `none` | no signal found (keep it if it is a question; people ask AI tools things they never type into Google) |

## Difficulty without a tool

Leave `difficulty` empty. In the Google results for the keyword, count how many top-10 results are from domains in `competitors.csv` with type `publisher` or big marketplaces. Put that count in `notes` (`strong_domains_in_top10: <n>`). Scoring treats difficulty as unknown.

## AI Overview flag

From the Google results page if read through Chrome: `ai_overview: yes` if an AI Overview shows, `no` if not. From web search only: `unknown`.

`source`: `gsc`, `chrome:google`, or `web_search`.
