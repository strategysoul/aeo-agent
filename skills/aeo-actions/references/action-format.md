# Action format

Every action must be something the owner can do **without working anything out**: where to go, what to click or paste, and how to know it worked. If a step needs a decision only the owner can make, ask it once (rules.md → Ask once) instead of leaving it in the action.

## `actions.md`

~~~~markdown
# Actions: <domain>

Last updated: <date> · run <run_id>
Open: <n> · Done, waiting for check: <n> · Confirmed: <n> · Dismissed: <n>

## Start here
The quickest changes with the biggest effect. When one is done, change its Status to `done`; the next run checks it.

1. **A003 · Remove the "ships worldwide" line** — 5 minutes · high effect
2. **A001 · Allow Claude-SearchBot in robots.txt** — 10 minutes · high effect
3. **A008 · Ask Run Review to include you** — 15 minutes · medium effect

## Open

| ID | Action | Effect | Effort | Who | Priority |
|---|---|---|---|---|---|

### A001 · Allow Claude-SearchBot in robots.txt
- Group: technical · Topic: site-wide · Status: open · Who: site owner (Shopify admin)
- Why: robots.txt blocks Claude-SearchBot; Anthropic says this reduces how often a site appears in Claude's search results. Source: technical/latest.md, 2026-10-13.
- Where: Shopify admin → Online Store → Themes → … → Edit code → `robots.txt.liquid`
- Steps:
  1. Open the file above.
  2. Delete these two lines:
     ```
     User-agent: Claude-SearchBot
     Disallow: /
     ```
  3. Save.
- Expected effect: high — makes the site eligible for Claude's search answers.
- Effort: S · about 10 minutes
- Check: robots.txt allows Claude-SearchBot to fetch `/`.
- Created: 2026-10-06 · Last checked: 2026-10-13 (still blocked)

## Done, waiting for check
## Confirmed
## Dismissed
~~~~

People may edit `Status` by hand: `open`, `done` (they did it), or `dismissed` (they will not do it, with a reason). The agent sets `confirmed` and reopens actions. Keep every action; never delete one. When an action is dismissed, add the reason to `decisions.md` → `## Not interested` if it applies to similar actions too.

## Fields

| Field | Rule |
|---|---|
| ID | `A001`, `A002`, … in creation order; never reused |
| Group | `page`, `technical`, `offsite` |
| Who | Who does it, from `decisions.md` → `Who can change what` (e.g. "site owner (Shopify admin)", "your developer", "your agency"). If unknown, "whoever edits the site". |
| Why | Evidence with the file and date it came from. No claim without a source. One or two sentences. |
| Where | The exact place: page URL and section; the CMS screen or file (use the CMS from `decisions.md` or `technical/raw/<date>/crawl.json` → `site.cms`); the listing or form URL. If the CMS is unknown, say what to look for ("the file that serves /robots.txt"). |
| Steps | Numbered, one action per step. Include everything to copy as a code block: exact replacement text, robots.txt lines, title and meta description text, JSON-LD, redirect rules, the message to send. For page actions, point to the draft in the brief. |
| Expected effect | `high` / `medium` / `low`, plus the metric it should move and how much demand it touches. No invented percentages or traffic forecasts. |
| Effort | `S` / `M` / `L` plus a plain estimate ("about 10 minutes", "half a day"), for one person who knows the site. S is under 2 hours, M 2–8 hours, L more than a day. |
| Priority | high if effect high and effort S or M; low if effect low or effort L with effect medium; otherwise medium |
| Check | One test the agent can run on the live site or in its own data to confirm the action is done |

## Order

- **Open table:** sort by priority, then by effort (smallest first), then by effect.
- **`## Start here`:** the quick wins. Take open actions, plus `done` actions whose check failed, whose `Who` is the owner or someone they named. List effort `S` first (high effect before medium, then fewest minutes), and fill up to 3 with `M` actions only if there are fewer than 3 `S`. Show the minutes estimate for each.
- Never list an action the owner said they cannot do (`decisions.md`): either rewrite it for the person who can ("send this to your agency:" + the text), or leave it out.

## Effect guide

| Effect | When |
|---|---|
| high | Unblocks a search bot or fixes an indexing error on an approved-topic page; a new page for a topic with high score and no page; correcting an accuracy-0 claim at its source |
| medium | Rewriting an existing page that ranks 11–30 or is never cited; a listing on a domain cited in 3 or more answers |
| low | Hygiene fixes on non-topic pages; llms.txt; schema not tied to a rich result |

## Matching across runs

Before adding an action, look for an existing one with the same group and target (topic for `page`, `issue_key` for `technical`, domain for `offsite`). If one exists in any status, update its Why and Last checked instead of adding a new one. A `dismissed` action is never re-proposed unless its evidence has changed a lot (for example, a domain cited three times as often), and then as a note on the old action. Nothing matching `decisions.md` → `## Not interested` is proposed.
