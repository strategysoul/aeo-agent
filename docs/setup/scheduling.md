# Schedule the AEO agent

Last checked: 2026-10-17, against [Desktop scheduled tasks](https://code.claude.com/docs/en/desktop-scheduled-tasks), [Cowork scheduled tasks](https://support.claude.com/en/articles/13854387-schedule-recurring-tasks-in-claude-cowork), [routines](https://code.claude.com/docs/en/routines) and [running Claude Code non-interactively](https://code.claude.com/docs/en/headless).

## What runs when

Two schedules cover everything. Each loops over every site folder under your AEO root.

| Schedule | Command | What it does |
|---|---|---|
| Daily | `/aeo-agent:aeo --all daily --scheduled` | Quick technical check: robots.txt, AI crawler access, sitemaps, the 20 most important pages |
| Weekly | `/aeo-agent:aeo --all weekly --scheduled` | Full technical check, AI answers, actions and the weekly report. Also refreshes keywords when they are more than 30 days old, research when it is more than 90 days old, and re-tests your tools every 30 days. |

The desktop and Cowork schedulers offer hourly, daily, weekday and weekly runs, so the weekly run starts the monthly and quarterly work itself.

Scheduled runs never approve anything. Refreshed research and topics are saved as proposals, and the weekly report lists them under "Needs your review". Run `/aeo-agent:aeo <domain> review` to approve them. Until then the agent keeps using what you approved before.

## Which option to use

| You use | Option | Runs when your computer is off | Reads the site folders on your computer |
|---|---|---|---|
| Claude desktop (Code tab) | Desktop scheduled task | no | yes |
| Cowork | Cowork scheduled task, with the AEO root folder chosen | no (tasks tied to a local folder run locally) | yes |
| Claude Code in a terminal | Your operating system's scheduler running `claude -p` | no | yes |
| Any | Cloud routine | yes | no — see the last section |

All local options need the computer awake at the scheduled time. Claude desktop can keep the computer from idle-sleeping (**Settings → This computer → System → Keep computer awake**); a closed laptop lid still sleeps. Desktop runs one catch-up run for the most recent missed time when the computer wakes.

`/aeo-agent:aeo <domain> setup` offers to create the schedules for you. The steps below are what it does, if you prefer to do it yourself.

## Claude desktop (Code tab)

1. Open **Routines** in the sidebar → **New routine** → **Local**.
2. Name: `aeo-daily`. Instructions: `/aeo-agent:aeo --all daily --scheduled`. Folder: your AEO root (default `Documents/AEO`). Schedule: **Daily**, at a time a few minutes past the hour, e.g. 06:07.
3. Repeat for `aeo-weekly` with `/aeo-agent:aeo --all weekly --scheduled`, **Weekly**, e.g. Monday 07:07.
4. Click **Run now** on each. When a permission prompt appears, choose **always allow**. Later runs reuse those approvals; a run in Manual mode otherwise stops at the first prompt until you answer it.

You can also ask Claude in any desktop session: "create a weekly local scheduled task in my AEO folder that runs /aeo-agent:aeo --all weekly --scheduled".

## Cowork

1. Open **Scheduled** in the sidebar → **New task**.
2. Use the same two instructions and schedules as above. Choose your AEO root as the folder, so the task can read and write the site folders.
3. Run each once by hand and allow the tools it asks for.

Cowork scheduled tasks have your connectors, skills and installed plugins.

## Claude Code in a terminal

`setup` writes a small script into your AEO root, `run-aeo.sh` (macOS, Linux) or `run-aeo.cmd` (Windows), from the plugin's `templates/`. It runs:

```bash
claude -p "/aeo-agent:aeo --all <daily|weekly> --scheduled" --permission-mode acceptEdits --allowedTools "<list>"
```

- `--permission-mode acceptEdits` lets it write the site files; `--allowedTools` lists the commands and connectors it may use without asking (Python scripts, `curl` for balance checks, web search and fetch, your SEO and Search Console connectors). In a `claude -p` run nobody can answer a prompt, so anything else is denied and the run carries on. On Claude Code v2.1.259 or later you can add `--permission-prompts none`, which also tells Claude not to retry denied calls.
- Output goes to `<root>/logs/`.
- Claude Code must be signed in (`claude` then `/login`) on this machine. Your MCP servers from `claude mcp add --scope user` are available.

**macOS or Linux (cron):** run `crontab -e` and add:

```bash
7 6 * * * "$HOME/Documents/AEO/run-aeo.sh" daily
7 7 * * 1 "$HOME/Documents/AEO/run-aeo.sh" weekly
```

cron starts with a minimal environment: if `claude` or `python3` is not found, put the full path to `claude` in the script, and set your API keys in the script's environment or a file it sources (not in the crontab, which is easy to share by accident).

**Windows (Task Scheduler):**

```powershell
schtasks /Create /SC DAILY /ST 06:07 /TN "AEO daily" /TR "`"$env:USERPROFILE\Documents\AEO\run-aeo.cmd`" daily"
schtasks /Create /SC WEEKLY /D MON /ST 07:07 /TN "AEO weekly" /TR "`"$env:USERPROFILE\Documents\AEO\run-aeo.cmd`" weekly"
```

Tasks created this way run only while you are logged in. Environment variables set with `setx` are available to them.

## Check it works

Trigger each schedule once by hand (**Run now**, or run the script with `daily` / `weekly`). Then check:

- `<site>/technical/latest.md` has today's date (daily and weekly)
- `<site>/reports/latest.md` has today's date (weekly)
- the log or the run's session shows no permission denials. If something was denied, add it to the allow list (desktop: always allow; terminal: `ALLOWED` in the script)

## Cloud routines (advanced, not tested with this plugin)

Routines run on Anthropic's cloud even when your computer is off, but each run starts from a fresh clone of a GitHub repository and cannot read files on your computer. To use one you would need to keep your AEO root in a private GitHub repository, make the plugin available in that repository, add your SEO tools as claude.ai connectors (MCP servers added with `claude mcp add` are not available), and store API keys as environment secrets. Claude in Chrome is not available. Each run writes to a `claude/` branch, which you then merge. Routines run at most hourly and are created with `/schedule` or at [claude.ai/code/routines](https://claude.ai/code/routines).

## Common errors

| What you see | Cause | Fix |
|---|---|---|
| Run skipped | computer asleep or app closed at the scheduled time | Keep the computer awake, or rely on the one catch-up run on wake. |
| Run stuck waiting | a permission prompt in a desktop task | Open the run, approve with "always allow". |
| `permission_denied` in the log | a tool not in `ALLOWED` | Add it to the script's `ALLOWED` list. |
| `claude: command not found` in cron | cron's short `PATH` | Use the full path to `claude` in `run-aeo.sh`. |
| Report says "Needs your review" every week | a proposal is waiting | Run `/aeo-agent:aeo <domain> review`. |
