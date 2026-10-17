# Technical check: northpine-running.example

MADE-UP EXAMPLE.

2026-10-13 · full · Sources: no audit tool (Ahrefs and Semrush not connected), own crawl (120 pages)

## AI and search crawler access

| Crawler | Kind | Allowed in robots.txt | Home page fetch (indicative) |
|---|---|---|---|
| Googlebot | search | yes | 200 |
| Bingbot | search | yes | 200 |
| OAI-SearchBot | search | yes | 200 |
| PerplexityBot | search | yes | 200 |
| **Claude-SearchBot** | search | **no** | 200 |
| ChatGPT-User | user | yes | 200 |
| Perplexity-User | user | yes | 200 |
| Claude-User | user | yes | 200 |
| GPTBot | training | no | — |
| ClaudeBot | training | yes | — |
| Google-Extended | training | yes | — |

Claude-SearchBot is blocked, so the site appears less often in Claude's search results. GPTBot is blocked too; that only controls OpenAI model training, not ChatGPT search, and is a business decision.

## Changes since the last check
- New: none
- Fixed: missing canonical tags on 6 product pages (first seen 2026-10-06)

## Errors on important pages
| Page | Issue | Detail | Since |
|---|---|---|---|
| robots.txt (site-wide) | search bot blocked | Claude-SearchBot | 2026-10-06 |

## Other issues
- possibly_js_only (1): /guides/choosing-width — 310 characters of text before JavaScript runs. Not confirmed, because Claude in Chrome is not connected.
- http_error (2): /blog/spring-sale-2024, /blog/old-size-chart — both 404 and still in the sitemap.
- duplicate_title (2): /blog/trail-tips, /blog/trail-tips-2
- missing_description (14): mostly blog posts

## Structured data found
| Page | JSON-LD types |
|---|---|
| /collections/wide-trail-shoes | BreadcrumbList, CollectionPage |
| /products/* (38) | Product, BreadcrumbList |
| /guides/choosing-width | none |

## llms.txt
Not present. It is a proposed format, not a standard, and Google says no AI-specific files are needed for AI Overviews or AI Mode. Low priority.
