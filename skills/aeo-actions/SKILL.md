---
name: aeo-actions
description: Steps 6 and 7 of the AEO agent. For each approved topic, checks whether the site has a page, ranks, and is cited in AI answers, and who is cited instead. Turns the gaps into specific, sourced actions in three groups (pages to write or rewrite with a brief for each, technical fixes, other websites to get listed on), each with expected effect, effort and a check. Keeps action status between runs and confirms done actions on the live site. Recommends only; never changes the site. Use for /aeo-agent:aeo <domain> actions, or as part of the weekly run.
---

# AEO actions

Follow `${CLAUDE_PLUGIN_ROOT}/skills/aeo/references/rules.md` throughout. Work in `<root>/<domain>/`. Action format and rules: `references/action-format.md`. Page briefs: `references/page-brief.md`.

## 0. Check before starting

Needs approved priority topics (same check as the visibility step). Uses the latest of each, and says which are missing or older than 14 days:

- `keywords/topics.md` and `keywords/scored.csv`
- `visibility/<latest>.csv` and `visibility/cited_domains.csv`
- `technical/issues.csv`
- Search Console data, if `gsc` is available (positions and pages per query)

Create `run_id` (`<today>-actions-<4 hex>`). Missing visibility or technical data does not stop the run; the related checks are marked "no data".

## 1. Check existing actions first

Read `actions.md`. For every action that is `open`, `done` or `confirmed`, run its **Check**:

| Status now | Check passes | Check fails |
|---|---|---|
| `open` | → `confirmed`, note "found done on <date>" | stays `open` |
| `done` | → `confirmed` | stays `done`, note what is still missing |
| `confirmed` | stays `confirmed` | → `open`, note "reverted on <date>" |

Checks use the live site (web fetch, or `technical/raw/<today>/crawl.json` if the technical step ran today) and the agent's own data (for example, a domain listing found by fetching the listing URL). Update `Last checked` with the result. `dismissed` actions are not checked.

## 2. Gap analysis per approved topic

Write `gaps.csv` (new rows each run; keep earlier rows):

```
topic,primary_keyword,demand,page_url,page_ok,best_position,position_source,ai_answers,mentioned,cited,cited_instead,ranks_instead,gap,record_date,run_id
```

| Column | How |
|---|---|
| `page_url` | `existing_url` from topics.md; else the Search Console page with most impressions for the topic's keywords; else a sitemap URL whose title or H1 clearly matches; else empty |
| `page_ok` | page returns 200, is indexable, and has no error in `technical/issues.csv` |
| `best_position` | best Search Console average position across the topic's keywords (or the SEO source's ranking data); empty if unknown |
| `ai_answers`, `mentioned`, `cited` | from the latest visibility file, for the topic's prompts: number of scored answers, how many mention the brand, how many cite the site |
| `cited_instead` | the 3 domains cited most in those answers that are not the site |
| `ranks_instead` | the top 3 domains in Google results for the primary keyword (from keywords or research raw data) |
| `gap` | `no_page`, `page_broken`, `not_ranking` (no position in top 30), `ranks_low` (best position 11–30), `ranks_not_cited` (top 10 but cited in no answer), `cited_not_mentioned`, `inaccurate` (any accuracy 0 answer), or `ok` |

## 3. Turn gaps into actions

Write new actions only where no matching action exists (matching rules in `action-format.md`). At most **10 new actions per run**, highest priority first; mention how many more were held back.

**Pages** (one action per topic):

- `no_page` → write a new page. `not_ranking`, `ranks_low`, `ranks_not_cited`, `cited_not_mentioned` → rewrite the existing page.
- Write a brief for each in `briefs/<topic-slug>.md` from `references/page-brief.md`. Before writing it, fetch the 2–3 pages AI answers cite most for the topic, and summarise what they cover.
- `inaccurate` → find where the wrong claim may come from (the site's own outdated page, a cited third-party page, an old listing) and recommend correcting it there. Quote the wrong claim and the correct fact from `profile.md`.

**Technical** (from `technical/issues.csv`, open issues only):

- One action per site-wide issue (a blocked search bot, robots.txt not answering, broken sitemap).
- One action per issue type on approved-topic pages, listing the URLs.
- Group hygiene issues on other pages into one low-priority action per type.
- Follow `${CLAUDE_PLUGIN_ROOT}/skills/aeo-technical/references/checks.md` for how to frame each one. Training-bot blocks are not actions unless the user asked.

**Off-site** (from `visibility/cited_domains.csv`):

- Domains cited in answers for approved topics that are not the site or a direct competitor: review sites, directories, comparison lists, forums, publishers.
- For each of the top 5 by answers cited, fetch the cited page and work out the realistic route: claim or update a profile, request inclusion in a list (name the article and its author or contact page if shown), answer existing questions on a forum as the brand (following that community's rules), or offer data or an expert quote to a publisher.
- Never suggest fake reviews, undisclosed paid posts, or posting as someone other than the brand. The agent does not post, sign up or contact anyone.

Every action gets Who, Why (with sources), Where, Steps (with everything to copy), Expected effect, Effort, Priority and Check, as in `action-format.md`. Read `decisions.md` first: write the steps for the CMS and the person it names, and skip anything under `Not interested`. For technical actions, put the exact text to paste in the steps (robots.txt lines, replacement copy, title and meta text, redirect rules). For off-site actions, include the message to send, ready to copy.

## 4. Write `actions.md`

Rewrite the file in the format in `action-format.md`: the counts, then `## Start here` with the 3 quickest high-value actions, then every action in its status section, with the open table sorted as `action-format.md` → Order says.

## 5. Log the run

Append the run to `state.json` → `runs` and set `last_run.actions`.

## Output to the user

- **Start here:** the 3 actions from `## Start here`, each with its minutes estimate and its first step.
- Actions confirmed or reverted since last run.
- The new actions, in the same order, one line each.
- The 3 topics with the biggest gaps and what is cited instead.
- What data was missing or old.
