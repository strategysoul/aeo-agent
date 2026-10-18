---
name: aeo-keywords
description: Steps 2 and 3 of the AEO agent. Finds keywords and questions for a website from seed expansion, competitor keywords, competitor ads in the Google Ads Transparency Center, "People also ask" and Search Console, scores each on audience fit, intent, demand, difficulty and AI-answer potential, groups them into page-sized topics, and asks for approval of the priority topics. Spends paid units only within the site's budget. Use for /aeo-agent:aeo <domain> keywords, or the monthly keyword refresh.
---

# AEO keywords

Follow `${CLAUDE_PLUGIN_ROOT}/skills/aeo/references/rules.md` throughout. Work in `<root>/<domain>/`.

## 0. Check before starting

- `state.json` → `approvals.research_brief.approved` must be `true`, and its `brief_hash` must match the current `research/brief.md`. If not: in an interactive run, offer to run research approval now; in a scheduled run, stop with "Research brief needs approval before keywords can run."
- Pick the SEO data source: the first `available` of `ahrefs` → `semrush` → `dataforseo`. Read its recipe in `references/recipe-<source>.md`. None available: use `references/recipe-fallback.md` and say in the output that volumes are inferred.
- Search Console (`gsc`) is used whenever it is available, alongside any source. It is free.
- Competitor ads from the Google Ads Transparency Center are read with `references/ads-transparency.md`, alongside any source. They are free through Chrome.
- Create `run_id` (`<today>-keywords-<4 hex>`) and `keywords/raw/<today>/` for raw responses.

## 1. Set the budget

1. Read the balance live where the recipe says how (Ahrefs `subscription-info`, Semrush `countapiunits`, DataForSEO `user_data`). Otherwise use `units_left` from `config.yaml`.
2. Budget for this run = `budget.share_of_remaining` × balance, capped by `budget.hard_cap_units` if set. For DataForSEO both are in US dollars.
3. No balance and no hard cap: interactive run → ask the user for a cap once and save it as `budget.hard_cap_units` in `config.yaml`; scheduled run → do only the free parts (Search Console, existing research) and say why.

## 2. Plan the calls, cheapest and most useful first

Write the plan as a short table (call, rows, estimated cost) before spending anything. Fill it in this order and stop adding calls when the next one would go past the budget:

| Order | Call | Default size |
|---|---|---|
| 1 | Search Console queries, last 90 days, main country | up to 1,000 rows (free) |
| 2 | Site authority | 1 call |
| 3 | Seed expansion: related terms, suggestions and questions for each seed from the brief | 10–20 seeds × 50 rows |
| 4 | Competitor keywords: top 3–5 direct competitors from `research/competitors.csv`, positions 1–20 | 100–200 rows each |
| 5 | Competitor ads: the same competitors in the Google Ads Transparency Center, last 30 days (`references/ads-transparency.md`) | up to 30 ads each (free through Chrome) |
| 6 | Volume, difficulty and intent for the merged list (whatever 3–5 did not already return) | the whole list, batched |
| 7 | Google top 10 for the highest-scoring keywords, for grouping and the AI Overview flag | 50–100 keywords |

Estimate cost from the recipe's cost section. If the plan had to be cut, say which rows were dropped. Reuse raw responses from earlier runs that are less than 30 days old instead of calling again.

During the run, if a response comes back with exactly the plan's row limit, treat it as cut off (rules.md). If a call fails with a plan or add-on error, record it in `config.yaml`, then use the next source for that need only.

## 3. Discover

Run the planned calls. Save each response to `keywords/raw/<today>/`. Merge everything into `keywords/raw.csv`:

```
keyword,origin,volume,demand_band,difficulty,intent,ai_overview,paa,gsc_impressions,gsc_position,gsc_url,notes,source,method,record_date,run_id
```

- `origin`: `seed:<seed>`, `competitor:<domain>`, `ads:<domain>`, `paa`, `gsc`, `brief`. A keyword found several ways keeps all origins, separated by `|`.
- Add the phrases taken from competitor ads, following `references/ads-transparency.md`.
- Also add the questions from the brief (question 5) and the "People also ask" questions saved in `research/raw/`.
- Normalise before merging: lower-case, trim, collapse spaces. Keep plural and word-order variants as separate rows, but group them later.
- Drop keywords in a language or for a country the site does not serve.
- New runs append; keep earlier rows.

## 4. Score

Score every keyword with `references/scoring.md`. Write `keywords/scored.csv`: the `raw.csv` columns for this run plus `fit,fit_reason,intent_score,demand,ease,bonus,score`. Sort by score.

Judge fit from `profile.md` and the brief only. Do not reuse fit reasons from another site.

## 5. Group into topics

Group with the rules in `references/scoring.md`. Write `keywords/topics.md`:

```markdown
# Topics: <domain>

Run <run_id> · <date> · Data: <source> (<method>) · Search Console: <yes/no>

## Summary
<n> keywords scored, <n> dropped for fit 0, <n> topics.

## Topics

| # | Topic | Type | Primary keyword | Keywords | Demand | Score | Existing page | Approved |
|---|---|---|---|---|---|---|---|---|

### 1. <topic>
- Keywords: <keyword (volume)>, …
- Why it matters: <one line from fit reasons and demand>
- Existing page: <url or "none">
```

Keep `approved` from the earlier `topics.md` for topics that still exist with the same primary keyword.

## 6. Ask for approval of the priority topics

Compute the SHA-256 of `topics.md`.

- **Interactive run:** propose the 10–20 highest-scoring topics as priorities (fewer if fewer exist), and show them as a short table. Ask the user to approve, remove or add topics. Set `Approved` to `yes` or `no` in `topics.md`, recompute the hash, and save `approvals.priority_topics = {approved: true, approved_at, topics_hash}` in `state.json`.
- **Scheduled run:** do not approve and do not touch an approved `topics.md`. If topics were already approved, write the result to `keywords/topics.proposed.md` instead and end with "Refreshed topics waiting for review: /aeo-agent:aeo <domain> review". Visibility and actions keep using the approved topics. If topics were never approved, write `topics.md` and end with "Topics need approval before visibility checks can run."

## 7. Measure the spend and log the run

Read the balance again where possible. Units spent = before − after; otherwise use the estimate and say so. Update `units_left` in `config.yaml`. Append the run to `state.json` → `runs`, and set `last_run.keywords`.

## Output to the user

Source used (and any fallback), keywords found by origin (say if competitor ads were not checked and why), topics, units spent against the budget, what was cut for budget, and the approval question.
