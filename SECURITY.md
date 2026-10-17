# Security

## Reporting a problem

Please report security problems privately through [GitHub's private vulnerability reporting](https://github.com/strategysoul/aeo-agent/security/advisories/new), not in a public issue. Include what you found, how to reproduce it, and what it affects. You should get a reply within a week.

## How the agent handles keys and data

- **Keys** are read from environment variables (`OPENAI_API_KEY`, `DATAFORSEO_PASSWORD` and so on) or from your client's connector settings. The agent checks whether a key is set without printing it, and never writes keys into site folders, logs or reports. `.env` files are in `.gitignore`; `.env.example` holds names only.
- **Site folders** stay on your computer under `AEO_ROOT`. Nothing is uploaded except the calls made to the tools you connected.
- **What goes to each tool:** the questions in `prompts.csv` go to the AI engines you enabled; keywords and domains go to your SEO tool; page fetches go to your own site and to pages being researched. Do not put private information in questions or keywords.
- **The crawler** (`scripts/crawl_check.py`) fetches only the given domain, follows robots.txt for itself, waits between requests, and never logs in or submits forms.
- **Claude in Chrome** uses your logged-in browser. The agent opens new chats, does not log in, does not change settings in AI tools, and stops at login pages and CAPTCHAs.
- **No changes to your site.** The agent never edits your site, CMS, DNS, CDN or tool settings, and does not post or contact anyone.

## Checks in CI

Every push runs `scripts/scan_repo.py`, which fails the build on anything that looks like an API key, a committed `.env` file, a personal email address, or a non-`.example` domain inside the example site.

## Scheduled runs

Unattended runs (`run-aeo.sh`, `run-aeo.cmd`, desktop or Cowork tasks) can use only the tools you allow. Keep the allowed list short, and do not put keys in crontab lines or scheduled-task prompts.
