# Action format

## `actions.md`

```markdown
# Actions: <domain>

Last updated: <date> · run <run_id>
Open: <n> · Done, waiting for check: <n> · Confirmed: <n> · Dismissed: <n>

## Open

| ID | Action | Group | Topic | Effect | Effort | Priority |
|---|---|---|---|---|---|---|

### A007 · Write a comparison page: Example Trail Pro vs Sample Ridge
- Group: page · Topic: comparison: sample ridge · Status: open
- Why: Asked "Example Trail Pro or Sample Ridge for wide feet?" (p014), ChatGPT and Perplexity named Sample Ridge first and cited reviews.example.org; the site has no comparison page. Source: visibility/2026-10-17.csv, keywords/topics.md.
- Do: Write the page from briefs/comparison-sample-ridge.md.
- Expected effect: medium — a page now exists for 8 keywords (1,900 searches a month) and 3 AI questions where the brand is not mentioned.
- Effort: M (4–8 hours)
- Check: a live page whose H1 contains "vs Sample Ridge", indexable, linked from the product page.
- Created: 2026-10-17 · Last checked: 2026-10-17 (not found)

## Done, waiting for check
## Confirmed
## Dismissed
```

People may edit `Status` by hand: `open`, `done` (they did it), or `dismissed` (they will not do it, with a reason). The agent sets `confirmed` and reopens actions. Keep every action; never delete one.

## Fields

| Field | Rule |
|---|---|
| ID | `A001`, `A002`, … in creation order; never reused |
| Group | `page`, `technical`, `offsite` |
| Why | Evidence with the file and date it came from. No claim without a source. |
| Do | Specific enough to do without asking: which URL, which file, which section, which listing. |
| Expected effect | `high` / `medium` / `low`, plus the metric it should move and how much demand it touches. No invented percentages or traffic forecasts. |
| Effort | `S` (under 2 hours), `M` (2–8 hours), `L` (more than a day), for one person who knows the site |
| Priority | high if effect high and effort S or M; low if effect low or effort L with effect medium; otherwise medium |
| Check | One test the agent can run on the live site or in its own data to confirm the action is done |

## Effect guide

| Effect | When |
|---|---|
| high | Unblocks a search bot or fixes an indexing error on an approved-topic page; a new page for a topic with high score and no page; correcting an accuracy-0 claim at its source |
| medium | Rewriting an existing page that ranks 11–30 or is never cited; a listing on a domain cited in 3 or more answers |
| low | Hygiene fixes on non-topic pages; llms.txt; schema not tied to a rich result |

## Matching across runs

Before adding an action, look for an existing one with the same group and target (topic for `page`, `issue_key` for `technical`, domain for `offsite`). If one exists in any status, update its Why and Last checked instead of adding a new one. A `dismissed` action is never re-proposed unless its evidence has changed a lot (for example, a domain cited three times as often), and then as a note on the old action.
