---
name: aeo-setup
description: Sets up the AEO agent for one website. Creates the site folder, tests which data sources are connected (SEO suites, Google Search Console, Claude in Chrome, AI-engine API keys) with the cheapest possible call, records plan, units and limits in config.yaml, and shows a setup table with links to setup guides for anything missing. Use for /aeo-agent:aeo <domain> setup, for the monthly capability re-check, or when a data source starts failing.
---

# AEO setup

Follow `${CLAUDE_PLUGIN_ROOT}/skills/aeo/references/rules.md` throughout.

## 1. Create or open the site folder

Root and domain rules are in the `aeo` skill. If `<root>/<domain>/` does not exist:

1. Create it with these subfolders: `research/raw/`, `keywords/`, `visibility/`, `technical/`, `briefs/`, `reports/`.
2. Copy `${CLAUDE_PLUGIN_ROOT}/templates/config.yaml` and `${CLAUDE_PLUGIN_ROOT}/templates/state.json` into it. Set `domain` in both.
3. Create an empty `actions.md` with the headings `## Open`, `## Done, waiting for check`, `## Confirmed`, `## Dismissed`.

## 2. Fill in the site basics

If `countries`, `languages` or `brand_names` still hold template values:

1. Fetch the homepage. Read `<html lang>`, `hreflang` links, currency and phone formats, the site name in `<title>` and `og:site_name`.
2. Propose values and ask the user to confirm or correct them in one question.
3. Ask whether they already have research (documents, folders, notes) and record the paths in `research.paths`. "None" is a fine answer.

In a non-interactive run, keep what is there and note the open questions in the setup output.

## 3. Test every data source

Run the tests in `references/capability-tests.md`, in the order listed. Each test uses the cheapest call the source offers. Run the free tests first; they cost nothing.

Record each result under `capabilities.sources.<name>` in `config.yaml`, using the fields shown in the template. Set `capabilities.checked_at` to today. Do not overwrite fields the test could not read: leave them as they were and set `status: untested` if nothing was confirmed.

## 4. Work out the setup level

| Level | Needs |
|---|---|
| Free | web search and fetch work (Search Console and Chrome add to it) |
| Recommended | Free + one of `ahrefs`, `semrush`, `dataforseo` available + at least one AI-engine key present |
| Full | Recommended + an AI-visibility source (`ahrefs` with the Brand Radar add-on, or `nimble`) + keys for OpenAI, Perplexity, Gemini and Anthropic |

## 5. Show the setup table

Show one table, then the level reached, then what to do next. Example layout:

| Source | Status | What it adds | Cost | Setup guide |
|---|---|---|---|---|
| Web search and fetch | available | research, competitor pages, fallback rank checks | free | built in |
| Google Search Console | missing | your own queries, clicks and rankings, measured | free | `docs/setup/google-search-console.md` |
| Claude in Chrome | available | reads AI answers from your logged-in ChatGPT, Perplexity, Gemini | included in Pro/Max/Team/Enterprise | `docs/setup/claude-in-chrome.md` |
| Ahrefs | available (Lite, 180,000 units left, 100 rows) | measured keyword volume, difficulty, competitors, site audit | from Lite plan | `docs/setup/ahrefs.md` |

Rules for the table:

- Every row with status `missing` or `error` has a guide link. Link to the file under `${CLAUDE_PLUGIN_ROOT}/docs/setup/`. If the guide file does not exist yet, write "guide coming" instead of a link.
- For `error`, show the error in a short phrase and the fix from the guide's "Common errors" section.
- Give the cost as the plan the source needs, not a price. Prices change; the guide links to the provider's pricing page.
- Below the table, name the one change that would add the most, e.g. "Connecting Search Console gives measured rankings for free."

## 6. Re-test after the user connects something

When the user says they connected a source, run only that source's test again, update `config.yaml`, and show its row.

## 7. Log the run

Append a run entry to `state.json` → `runs` with `step: "setup"` and the units spent (normally 0). Set `last_run.setup` to today.

## 8. Offer to schedule (interactive, once)

Schedules cover every site, so they are recorded once for the root, in `<root>/schedule.json`. Skip this step in scheduled runs, and when that file exists. Otherwise ask once whether to set up the two schedules in `${CLAUDE_PLUGIN_ROOT}/docs/setup/scheduling.md` (daily and weekly, all sites). Creating a schedule is a lasting change, so only go ahead on a clear yes.

Pick the method from the client you are running in:

- **Claude desktop or Cowork** (a scheduled-tasks tool such as `create_scheduled_task` is available): create two local tasks with the AEO root as the folder: `aeo-daily` running `/aeo-agent:aeo --all daily --scheduled` daily at 06:07, and `aeo-weekly` running `/aeo-agent:aeo --all weekly --scheduled` weekly on Monday at 07:07 (the user may pick other times; keep them a few minutes past the hour). Then tell the user to click **Run now** on each once and choose "always allow" at each permission prompt, so later runs do not stop.
- **Claude Code in a terminal:** copy `${CLAUDE_PLUGIN_ROOT}/templates/run-aeo.sh` (macOS, Linux; make it executable) or `run-aeo.cmd` (Windows) to the AEO root. Replace `__ALLOWED_TOOLS__` with a comma-separated list: `Bash(python *),Bash(python3 *),Bash(curl *),WebFetch,WebSearch`, plus `mcp__<server>` for each MCP server that setup found `available` (for example `mcp__ahrefs`). Show the user the cron lines or `schtasks` commands from the guide and offer to add them; add them only on a yes.
- **Neither:** show the guide link and stop.

Record what was created in `<root>/schedule.json`: `{method, tasks: [{name, command, when}], created_at}`. If the user says no, write `{method: "none", declined_at}` so setup does not ask again; they can run the steps in the guide later.

## Monthly re-check

The `aeo` skill reruns setup when `checked_at` is older than 30 days; the weekly scheduled run does this automatically. A re-check in a scheduled run only re-tests sources and updates the table in `config.yaml`.
