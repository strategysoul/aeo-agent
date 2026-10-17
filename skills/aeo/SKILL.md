---
name: aeo
description: Main entry for the AEO agent. Measures whether a website shows up in Google and in AI answers (ChatGPT, Perplexity, Gemini, Claude, Google AI Overviews) and recommends what to change. Use when the user runs /aeo-agent:aeo <domain> [mode], or asks to check a site's SEO, AEO, GEO or AI visibility, to set up the AEO agent for a site, or to see its weekly report.
argument-hint: <domain|--all> [setup|research|keywords|visibility|technical|actions|report|review|daily|weekly] [--scheduled]
---

# AEO agent

Usage: `/aeo-agent:aeo <domain> [mode]` or `/aeo-agent:aeo --all <mode>` (loops over every site folder). Add `--scheduled` for unattended runs.

Before anything else, read `${CLAUDE_PLUGIN_ROOT}/skills/aeo/references/rules.md`. Every mode follows it.

## 1. Find the site folder

- Root: the `AEO_ROOT` environment variable if set, otherwise `~/Documents/AEO`. Check with a shell command that prints only whether it is set, never other variables.
- Site folder: `<root>/<domain>/`. Normalise the domain first: lower-case, no scheme, no `www.`, no path, no trailing slash.
- `--all`: every folder under the root that contains a `config.yaml`. Run the mode for each site in turn, and finish one site before starting the next. A failure on one site is noted and the loop moves on.

If the site folder does not exist: interactive → run setup first; `--scheduled` → skip the site and say so.

## 2. Interactive or scheduled

A run is **scheduled** when `--scheduled` is given or nobody can answer questions. Scheduled runs:

- never ask questions, never approve anything, and never pass an approval gate that is not approved;
- write refreshed research and topics as proposals (`research/brief.proposed.md`, `keywords/topics.proposed.md`) and leave the approved files alone, so the weekly run keeps working on what was approved;
- use Claude in Chrome only if `budget.chrome_in_scheduled_runs` is `true`;
- end every site with a short status: what ran, what was skipped and why, what needs review.

## 3. Check whether setup is current

Read `config.yaml`. Run setup before the requested mode when `capabilities.checked_at` is empty or more than 30 days old, or the mode needs a source whose status is `error`. In scheduled runs, setup only re-tests sources; it does not ask about site basics.

## 4. Run the mode

| Mode | What it does |
|---|---|
| `setup` | Capability test, setup table, guide links, scheduling. Follow the `aeo-setup` skill. |
| `research` | Profile and market research (step 1). Follow the `aeo-profile-research` skill. |
| `keywords` | Keyword discovery, scoring and topics (steps 2–3). Follow the `aeo-keywords` skill. |
| `visibility` | AI questions and AI-answer checks (steps 4–5). Follow the `aeo-visibility` skill. |
| `technical` | Technical health and AI crawler access. Follow the `aeo-technical` skill. `technical quick` for the short check. |
| `actions` | Gap analysis and recommendations (steps 6–7). Follow the `aeo-actions` skill. |
| `report` | Weekly report (step 8). Follow `references/report.md`. |
| `review` | Interactive only. Show anything waiting for approval (see §5) and approve or correct it. |
| `daily` | `technical quick`. |
| `weekly` | The due refreshes (below), then `technical` → `visibility` → `actions` → `report`. |

**Due refreshes in `weekly`**, checked from `state.json` → `last_run` before the weekly steps:

| Refresh | Due when | Runs |
|---|---|---|
| Monthly | `last_run.keywords` more than 30 days ago | `keywords` |
| Quarterly | `last_run.research` more than 90 days ago | `research` |

Setup's own 30-day re-check (§3) covers the monthly capability test. Schedulers in Claude desktop and Cowork offer hourly, daily, weekday and weekly runs only, so monthly and quarterly work is started by the weekly run instead of a schedule of its own.

**Order and gates.** A step whose gate is not approved is skipped, not failed, and the next step still runs on the last approved data. `technical` needs no research or approval. If `research/brief.md` does not exist at all, every mode except `setup` and `technical` runs `research` first (interactive) or skips (scheduled).

**Something specific or new.** When the user asks for one thing ("add a topic on X", "also check Canada", "Y is a new competitor", "redo the questions for topic Z"), do only that part: reuse every stored file, update just what the request touches, and record the change in `decisions.md`. Do not rerun research or other steps that are still current.

No mode given: run `setup` if the site is new; otherwise show the site's status (last run per step, approvals, anything waiting for review, units used this month) and the modes above.

## 5. Approvals and proposals

Two points need a person's approval: the research brief and the priority topics. They are stored in `state.json` → `approvals` with a hash of the approved file.

`review` (or running `research` or `keywords` interactively when a proposal exists):

1. If `research/brief.proposed.md` exists: show what changed compared with `research/brief.md` (new, changed and removed findings, with sources). On approval, replace `brief.md` with it, delete the proposal, and store the new hash. On rejection, delete the proposal and note it in `research/change_log.md`.
2. If `keywords/topics.proposed.md` exists: show topics added, removed and re-scored compared with `topics.md`, keeping `Approved` values for topics that still exist. Let the user change which topics are approved. On approval, replace `topics.md` and store the hash.
3. Actions marked `done` whose check failed: show them and ask whether to keep, reopen or dismiss each.
