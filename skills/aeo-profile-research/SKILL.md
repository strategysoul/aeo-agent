---
name: aeo-profile-research
description: Step 1 of the AEO agent. Writes a site profile from the live website, checks which of seven research questions the user's existing research already answers, researches only the missing or outdated parts (Google results, competitors, forums, reviews, communities), and writes a sourced research brief for approval. Use for /aeo-agent:aeo <domain> research, or when a later step finds the brief missing or older than 90 days.
---

# AEO profile and research

Follow `${CLAUDE_PLUGIN_ROOT}/skills/aeo/references/rules.md` throughout. Work inside the site folder `<root>/<domain>/`. Setup must have run (`config.yaml` has `capabilities.checked_at`).

Start a run: create `run_id` (`<today>-research-<4 hex>`) and the folder `research/raw/<today>/`. Save every raw response or fetched page summary there as you go, named `<n>-<source>-<slug>.md` or `.json`. Never edit or delete older dated folders.

## 1. Write or refresh `profile.md`

Skip if `profile.md` is less than 90 days old and the homepage title and main navigation have not changed.

1. Fetch the homepage, `sitemap.xml` (or the sitemap named in `robots.txt`), and up to 10 key pages: product or service pages, pricing, about, the main category pages. Fall back to Claude in Chrome for pages that show no content without JavaScript; note that the page needs JavaScript (a technical finding).
2. Write `profile.md` with these sections, every line sourced to the page URL it came from:
   - **What the business sells** — products or services, as the site names them
   - **Price** — prices or price model, or "not shown on site"
   - **Who it says it is for** — audiences named on the site
   - **Where it operates** — countries, languages, shipping or service areas
   - **Brand names** — every spelling used
   - **Claims and limits** — regulated topics (health, finance, legal, children, etc.) and any disclaimers
   - **Site structure** — main sections and roughly how many pages each has, from the sitemap
3. If `brand_names` or `countries` in `config.yaml` disagree with what the site shows, and `decisions.md` does not already settle it, ask once; do not change `config.yaml` without asking. Record the answer in `decisions.md`.

## 2. Check coverage of the seven questions

Follow `references/coverage.md`. Read every file under `research.paths` in `config.yaml`, plus the existing `research/brief.md` if there is one. For each of the seven questions decide `answered`, `partial`, `stale` or `missing`, with evidence. Write `research/coverage.json`.

Then decide what to research:

| Coverage | Action |
|---|---|
| All seven `answered` | Skip to step 5. Build the brief from existing research. |
| Some `partial`, `stale` or `missing` | Research only those questions. |
| No research paths and no brief | Research all seven. |

Tell the user in one short list which questions will be researched and why, then continue. Do not wait for a reply unless they asked to review the plan first.

## 3. Map the search results

Needed for questions 3 (competitors) and 4 (who ranks and gets cited). Skip if both are `answered`.

1. **Starting keywords.** From `profile.md`, write 10–20 searches a customer would type: the product category, the problem it solves, "best <category>", "<category> for <audience>", "<brand> alternatives", and the main local variant if the site serves one country. Write them in the site's language. Save to `research/raw/<today>/seed-keywords.csv` with `method: inferred`.
2. **Google results for each.** Use the first available source: Ahrefs SERP overview → Semrush → DataForSEO → web search. Check the budget first (rules.md). Record for each keyword: the top 10 URLs and domains, whether an AI Overview appears, and the "People also ask" questions if the source returns them.
   - **Sponsored results.** Also record the ads on each results page: advertiser domain, headline, position (top or bottom). Ahrefs and web search do not return ads; if the source used does not, get them from the next one that does, within budget: Semrush (the keyword's paid search report, `phrase_adwords` in the Semrush API; read it with `get_report_schema` first) → DataForSEO (items of type `paid` in the Google organic results you already have) → Chrome (read the Google results page in the main country; labelled "Sponsored"; at most 20 searches). Never click an ad. If Google shows a CAPTCHA, stop and tell the user. Ads change from one search to the next, so one page is a snapshot: `method: measured`, with the date. None of these available: write "sponsored results not checked" and continue.
3. **Count competitor domains.** Count how many starting keywords each domain ranks top 10 for, and separately how many it shows a sponsored result for. A domain that only advertises is still a competitor: open its landing page to set its `type`. Drop the site itself and generic sites (Wikipedia, YouTube, Reddit, Amazon, major news) from the competitor count, but keep them in a separate "places the audience reads" list for question 6.
4. Write `research/competitors.csv` (format in `references/coverage.md`). If an SEO source reports organic competitors for the domain, merge those in with their own `source`. For a new site where the SEO source returns none, the Google results count is the competitor list.
5. **Competitor ads.** For the top 3–5 direct competitors (by `keywords_in_top10` + `ads_on_seed_keywords`), read their current ads in the Google Ads Transparency Center with `${CLAUDE_PLUGIN_ROOT}/skills/aeo-keywords/references/ads-transparency.md`, and save them to `research/raw/<today>/ads-transparency.csv`. Give the Market agent the offers and claims found, as already known.

## 4. Research the gaps

Split the open questions across research agents, following `references/research-agents.md`. If the client can run subagents, start them at the same time; otherwise run the briefs one after another. Each agent:

- gets only its questions, the profile, the competitor list, and the countries and languages
- uses web search and fetch first, then Firecrawl, then Nimble, if those are `available`
- returns findings in the fixed format in `references/research-agents.md`, each with a URL and the date it was read

Save each agent's raw output to `research/raw/<today>/agent-<question-numbers>.md`.

## 5. Write the brief

One writer (you, not the agents) combines everything into `research/brief.md` using `references/brief-template.md`.

- **Add to the earlier brief instead of overwriting it.** Keep findings that are still within 90 days. Replace a finding only when newer evidence contradicts it, and record the change in `research/change_log.md`: date, question, old finding, new finding, both sources.
- Every claim has a source URL and a date. Gaps say "not found". Guesses say "inferred".
- Update `research/coverage.json` so every researched question shows its new status.

## 6. Ask for approval

Compute the SHA-256 of `brief.md` (any shell tool, e.g. `sha256sum` or `Get-FileHash`).

- **Interactive run:** show a short summary — the top five competitors, the main audiences and their words, the five most common questions, any rules that limit what the business can say, and the questions still `missing`. Ask the user to approve, or to correct something. Apply corrections as edits to `brief.md` with the source "user, <date>", then ask again.
- On approval, set `state.json` → `approvals.research_brief` to `{approved: true, approved_at: <today>, brief_hash: <hash>}`.
- **Scheduled run:** do not approve and do not touch an approved `brief.md`. If a brief was already approved, write the result to `research/brief.proposed.md` instead (same format) and end with "Refreshed research brief waiting for review: /aeo-agent:aeo <domain> review". Later steps keep using the approved brief. If no brief was ever approved, write `brief.md` and end with "Research brief needs approval before keywords can run."

## 7. Log the run

Append to `state.json` → `runs`: `run_id`, `step: "research"`, units spent per source, start and finish times. Set `last_run.research` to today.

## Output to the user

Keep it short: what was reused, what was researched, where the files are, units spent, and the approval question.
