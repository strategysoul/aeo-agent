---
name: aeo-visibility
description: Steps 4 and 5 of the AEO agent. Writes natural questions people ask AI tools for each approved topic, runs them through the best available source per engine (Ahrefs Brand Radar, Nimble, the engines' APIs via ask_engines.py, the user's logged-in AI tools in Chrome, or web search as a weak stand-in), and scores every answer on brand mention, position, citation, accuracy and sentiment. Records which competitors and domains AI answers cite. Use for /aeo-agent:aeo <domain> visibility, or as the first part of the weekly run.
---

# AEO visibility

Follow `${CLAUDE_PLUGIN_ROOT}/skills/aeo/references/rules.md` throughout. Work in `<root>/<domain>/`.

## 0. Check before starting

- `state.json` → `approvals.priority_topics.approved` must be `true` and `topics_hash` must match `keywords/topics.md`. If not: interactive run → offer to review topics now; scheduled run → stop with "Priority topics need approval before visibility checks can run."
- Create `run_id` (`<today>-visibility-<4 hex>`) and `visibility/raw/<today>/`.

## 1. Write or update the questions (`prompts.csv`)

Columns:

```
prompt_id,prompt,topic,type,language,country,active,created,run_id
```

- For every approved topic, write **2–5 questions** the way a person types or says them to an AI tool. Use the audience's own words from the brief (question 2) and the real questions in it (question 5). 30–100 questions per site in total.
- Cover these types across the set: `best` ("what's the best … for …"), `vs` ("… or …, which is better for …"), `alternatives` ("alternatives to <competitor>"), `how_to` ("how do I …"), `recommend` ("can you recommend …"). Add 2–3 `brand` questions about the brand itself ("what is <brand>", "is <brand> any good for …") to check accuracy.
- Do not put the brand name in any question except `brand` ones. Write in the site's language; set `country` to the market the question is for.
- **Keep existing questions unchanged** so weeks stay comparable. Add questions only for newly approved topics; set `active = no` (never delete) for topics no longer approved. `prompt_id` is `p001`, `p002`, … and never reused.
- First run, interactive: show the questions grouped by topic and let the user edit them before anything is asked. Scheduled runs use `prompts.csv` as it is.

## 2. Choose a source for each engine

Follow `references/sources.md`: for each engine, the first `available` source that covers it. Show a short table (engine → source → questions → estimated cost) before spending anything. Engines with no source go under "Not measured".

Budget, from `config.yaml`:

- Ahrefs (Brand Radar) units: as in rules.md.
- Engine API calls: `budget.engine_calls_per_run` in total (default 100).
- Chrome: `budget.chrome_prompts_per_engine` per engine (default 20), interactive runs only unless the user has allowed it for scheduled runs (`budget.chrome_in_scheduled_runs: true`).

If the budget does not cover every active question, ask the highest-scoring topics' questions first, and say how many were left out.

## 3. Collect the answers

Run each source as `references/sources.md` describes. Save every raw answer under `visibility/raw/<today>/` before scoring. Ask each question once per engine per run.

## 4. Score the answers

Score every answer with `references/rubric.md`. Write `visibility/<today>.csv`, one row per question × engine × source:

```
prompt_id,topic,type,engine,source,model_used,mentioned,position,cited,cited_urls,accuracy,accuracy_notes,sentiment,competitors_mentioned,cited_domains,answer_file,method,record_date,run_id
```

Lists are separated by `|`. Brand Radar's aggregate numbers go into the summary rows of `history.csv` (below), not into per-question rows.

## 5. Summarise and keep history

1. Append one row per engine × source to `visibility/history.csv`:

   ```
   record_date,engine,source,answers,mention_rate,citation_rate,avg_position,share_of_voice,accuracy_issues,negative,run_id
   ```

2. Count cited domains across all answers and append to `visibility/cited_domains.csv`:

   ```
   record_date,domain,answers_citing,engines,topics,is_own_site,is_competitor,run_id
   ```

   Domains that are neither the site nor a direct competitor (review sites, directories, forums, publishers) are the **off-site targets** the actions step will use.

3. Compare with the previous run using the rules at the end of `references/rubric.md`.

## 6. Log the run

Update `units_left` for any paid source used, append the run to `state.json` → `runs` with units or calls spent per source, and set `last_run.visibility`.

## Output to the user

Keep it short:

- Engines measured and the source for each; engines not measured and why.
- Per engine: mention rate, citation rate, share of voice, and the change since last run (or "first run").
- Topics where the brand is never mentioned, and who is mentioned instead.
- Every accuracy issue with accuracy 0, quoted.
- The ten domains cited most often that are not the site.
- Calls and units spent against the budget.
