# Weekly report (step 8)

Runs last in `weekly`, or alone as `report`. Reads what the other steps wrote; spends no paid units except free Search Console calls.

## 1. Rankings

- **Search Console available:** for the keywords of approved topics, get clicks, impressions and average position for the last 7 complete days and the 7 days before (Search Console data lags about two days). Per topic: sum clicks and impressions, impression-weighted average position.
- **Otherwise:** use the positions recorded by the latest keywords run (SEO source, or rank checks), and say their date.
- Append to `reports/rankings.csv`:

  ```
  record_date,period_start,period_end,topic,clicks,impressions,avg_position,source,run_id
  ```

## 2. Write `reports/<today>.md` and copy it to `reports/latest.md`

```markdown
# Weekly AEO report: <domain>

Week to <date> · run <run_id> · Setup level: <Free | Recommended | Full>

## Summary
<3–5 sentences: the biggest change, the biggest gap, the most important action. Plain facts with numbers.>

## Start here
<copy the 3 items from actions.md → Start here: ID, title, minutes, who, and the first step. Link to actions.md for the full steps.>

## Needs your review
<only if something is waiting: a proposed research brief, proposed topics, actions marked done that failed their check, an engine source in error. Say what to run, e.g. "/aeo-agent:aeo <domain> review". Omit the section if nothing waits.>

## Search rankings
| Topic | Clicks | Change | Impressions | Change | Avg position | Change |
Source: <Search Console, last 7 days vs previous 7 | other, dated>

## AI answers
| Engine | Source | Answers | Mentioned | Cited | Share of voice | Change since last week |
<noise note from rubric.md where it applies>

Topics where the brand is never mentioned: <topic — who is mentioned instead>
Accuracy problems: <quoted claim → correct fact>

## Technical health
Health score: <score> (<source>) · change <+/-n>
Search bots blocked: <none | list>
New errors: <n> · Fixed: <n>

## Actions
Confirmed this week: <list>
New: <list, highest priority first>
Open: <n> (<n> high priority) · Waiting for check: <n>

## Sources and spending
| Step | Source | Method | Units or calls | Budget |
<every source used this week, and every weaker fallback, with the reason>
Not measured: <engines or data with no source>
```

## 3. Across sites (`--all` only)

After every site, write `<root>/summary-<today>.md`: one row per site with setup level, AI mention rate change, health score change, open high-priority actions, and anything in "Needs your review".

## 4. Log the run

Append the run to `state.json` → `runs` and set `last_run.report`.

## Rules

- Only report numbers that are in the site's files. If a step did not run this week, say "not run this week" and show its last date.
- Changes compare with the previous report's numbers from the same source. If the source changed, write "new source" instead of a change.
- No text from another site's folder.
