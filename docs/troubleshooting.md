# Troubleshooting

Each setup guide has a "Common errors" table for its tool. This page covers the agent itself.

| What you see | Cause | Fix |
|---|---|---|
| A step stops with "needs approval" | The research brief or topics are not approved, or changed since approval | Run `/aeo-agent:aeo <domain> review` |
| The report says "Needs your review" every week | A proposal from a scheduled refresh, or an action whose check failed | Run `review` |
| A list ends at exactly 100 (or 250, 500) rows | The tool's row cap for your plan | Expected. The agent pages through or marks the list incomplete |
| "insufficient plan" or "missing add-on" | The report needs a higher plan or an add-on | Expected. The agent uses the next source and labels it. Upgrade only if you need that data |
| No competitors found | New site with little data in SEO tools | Expected. Competitors come from Google results for the starting keywords |
| Keyword volumes say "inferred" | No SEO data source connected | Connect Ahrefs, Semrush or DataForSEO, or accept demand bands |
| An engine is "Not measured" | No source covers it | See the setup table: an API key, Brand Radar, Nimble or Chrome |
| Mention rate jumps up and down | AI answers vary between runs | The report treats changes under 10 points on fewer than 30 answers as noise. Add questions for steadier numbers |
| A tool shows `error` in setup | The last test call failed | The message is in `config.yaml` → `capabilities.sources.<tool>.last_error`; follow the tool's guide, then run `setup` again |
| `python` not found | Python not installed or not on PATH | Install Python 3.9+; the agent falls back to web fetch for the technical check and skips API engines |
| Scheduled run did nothing | Computer asleep, permission prompt waiting, or a tool not allowed | See [setup/scheduling.md](setup/scheduling.md) → Common errors |
| A crawl is blocked or slow | The site's firewall limits the checker | The checker waits 0.5 s between pages and follows robots.txt. Allow its user agent `AEO-Agent/0.1`, or lower `--max-pages` |
| `check_site.py` reports problems | A file was edited by hand into a different format, or an approved file changed | Fix the columns it names, or re-approve with `review` |

## Reporting a bug

Open an issue at [github.com/strategysoul/aeo-agent/issues](https://github.com/strategysoul/aeo-agent/issues) with the mode you ran, your setup level, the error text, and the output of `python scripts/check_site.py <site folder>`. Remove keys, and your site's private data, first.
