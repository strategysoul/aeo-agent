---
name: aeo-technical
description: Technical health check for the AEO agent. Reads Ahrefs or Semrush Site Audit results if available, and always runs its own polite crawl of robots.txt, sitemaps, llms.txt and key pages to check AI crawler access (OAI-SearchBot, PerplexityBot, Claude-SearchBot, GPTBot, ClaudeBot, Google-Extended and others), indexability, titles, canonicals, structured data and pages whose content needs JavaScript. Use for /aeo-agent:aeo <domain> technical, or the daily quick check.
argument-hint: <domain> technical [quick]
---

# AEO technical

Follow `${CLAUDE_PLUGIN_ROOT}/skills/aeo/references/rules.md` throughout. Work in `<root>/<domain>/`. Interpret results with `references/checks.md`.

Two modes:

- **full** (default; weekly or on request): audit source + crawl of up to 200 pages.
- **quick** (daily schedule): robots.txt, llms.txt, sitemaps and the 20 most important pages only, no audit-tool units spent. Report only what changed since the last run.

Create `run_id` (`<today>-technical-<4 hex>`) and `technical/raw/<today>/`.

## 1. Pick the important pages

Write `technical/raw/<today>/priority-urls.txt`, one URL per line, in this order: the home page; `existing_url` of every approved topic in `keywords/topics.md`; pages with the most Search Console clicks (if `gsc` is available); site URLs cited in `visibility/` answers. Quick mode stops at 20.

## 2. Audit tool (full mode only)

First `available` of:

- **Ahrefs Site Audit** (`site-audit` tools) for the project in `audit.ahrefs_project_id`. If the id is empty, list the user's projects and match the domain; if one matches, save its id in `config.yaml`. Read the health score and the issues list with affected URLs. Do not start a new crawl or change project settings.
- **Semrush Site Audit** (`site_audit`, read-only) for `audit.semrush_project_id`, same way.

No audit tool, or no project for this domain: say so and rely on the own crawl. Budget the calls as in rules.md. Save raw responses.

## 3. Own crawl (both modes)

```bash
python "${CLAUDE_PLUGIN_ROOT}/scripts/crawl_check.py" --domain <domain> \
  --urls "<site>/technical/raw/<today>/priority-urls.txt" \
  --max-pages <200 full | 20 quick> --bot-check \
  --out "<site>/technical/raw/<today>/crawl.json"
```

It also guesses the CMS from the home page (`site.cms`, e.g. `shopify`, `wordpress`); if `decisions.md` has no CMS yet, suggest this guess the next time the user is asked anything, and record the answer. The script fetches only the site's own pages, waits 0.5 seconds between requests, follows robots.txt for itself, and never logs in or submits forms. If Python is not available, do the robots.txt, llms.txt, sitemap and home-page checks with web fetch and say the crawl was limited.

## 4. Confirm JavaScript-only pages

For pages flagged `possibly_js_only` that are in approved topics (at most 5 per run): if `chrome` is available, open the page and read its visible text. If the rendered page has the content the raw HTML lacks, the issue is confirmed (`method: measured`). Without Chrome, keep it as `inferred`.

## 5. Write the results

**`technical/issues.csv`** — one row per issue and URL, kept across runs:

```
issue_key,type,severity,url,detail,in_topic,source,first_seen,last_seen,status,run_id
```

- `issue_key` = `<type>|<url>` (or `<type>|site` for site-wide issues such as a blocked bot). Update `last_seen` for issues still present; set `status: fixed` for open issues not seen this run in a page that was checked again; add new ones with `status: open`.
- Site-wide rows for every blocked bot from `robots.bots`, a robots.txt that does not answer, and missing or broken sitemaps.

**`technical/history.csv`** — append one row per source:

```
record_date,source,mode,health_score,errors,warnings,notices,pages_checked,search_bots_blocked,run_id
```

**`technical/latest.md`**:

```markdown
# Technical check: <domain>

<date> · <mode> · Sources: <audit tool or "none">, own crawl (<n> pages)

## AI and search crawler access
| Crawler | Kind | Allowed in robots.txt | Home page fetch (indicative) |

## Changes since the last check
- New: …  · Fixed: …

## Errors on important pages
| Page | Issue | Detail | Since |

## Other issues
<counts by type, with up to 5 example URLs each>

## Structured data found
| Page | JSON-LD types |

## llms.txt
<present / not present, with what checks.md says about it>
```

## 6. Log the run

Append the run to `state.json` → `runs` (units spent on audit tools, pages crawled) and set `last_run.technical`.

## Output to the user

Search bots blocked (if any) first, then new errors on important pages, then what was fixed since last time. In quick mode, say "No changes" if nothing changed.
