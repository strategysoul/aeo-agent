# Actions: northpine-running.example

MADE-UP EXAMPLE.

Last updated: 2026-10-13 · run 2026-10-13-actions-7e8f
Open: 7 · Done, waiting for check: 1 · Confirmed: 1 · Dismissed: 1

## Open

| ID | Action | Group | Topic | Effect | Effort | Priority |
|---|---|---|---|---|---|---|
| A001 | Allow Claude-SearchBot in robots.txt | technical | site-wide | high | S | high |
| A004 | Write a page: alternatives to Ridgeline for wide feet | page | Alternatives to Ridgeline | high | M | high |
| A005 | Rewrite the wide trail shoes collection page | page | Wide trail running shoes | medium | M | medium |
| A006 | Rewrite the bunions guide so AI answers can cite it | page | Trail shoes for bunions | medium | M | medium |
| A007 | Put the width guide's text in the HTML | technical | Choosing shoe width | medium | M | medium |
| A008 | Ask to be included in Run Review's wide trail shoes list | offsite | Wide trail running shoes | medium | S | medium |
| A009 | Answer wide-feet threads on TrailTalk as the brand | offsite | Wide trail running shoes | medium | M | medium |

### A001 · Allow Claude-SearchBot in robots.txt
- Group: technical · Topic: site-wide · Status: open
- Why: robots.txt has a `User-agent: Claude-SearchBot` group with `Disallow: /`. Anthropic says blocking Claude-SearchBot reduces how often a site appears in Claude's search results. Source: technical/latest.md, 2026-10-13; technical/issues.csv `search_bot_blocked|site`.
- Do: In robots.txt, delete the `User-agent: Claude-SearchBot` / `Disallow: /` group. Leave the GPTBot group if you still want to keep content out of OpenAI training; it does not affect ChatGPT search.
- Expected effect: high — makes the site eligible for Claude's search answers. Not measurable here yet: Claude is not one of the engines checked (no Anthropic key).
- Effort: S (under 2 hours)
- Check: robots.txt allows Claude-SearchBot to fetch `/`.
- Created: 2026-10-06 · Last checked: 2026-10-13 (still blocked)

### A004 · Write a page: alternatives to Ridgeline for wide feet
- Group: page · Topic: Alternatives to Ridgeline · Status: open
- Why: No page for this topic (gaps.csv). Asked "what are good alternatives to Ridgeline for wide feet" (p006) and "Ridgeline or Trailkind for wide feet" (p007), neither engine named Northpine in 4 answers; they cited runreview.example, gearlab-test.example and hikeboard.example. Source: visibility/2026-10-13.csv.
- Do: Write the page from briefs/alternatives-to-ridgeline.md.
- Expected effect: high — the topic scores 13.8 and has no page; 4 keywords (350 searches a month) plus AI questions where only competitors appear.
- Effort: M (2–8 hours)
- Check: a live, indexable page whose H1 contains "alternatives to Ridgeline", in the sitemap, linked from the wide trail shoes collection page.
- Created: 2026-10-06 · Last checked: 2026-10-13 (not found)

### A005 · Rewrite the wide trail shoes collection page
- Group: page · Topic: Wide trail running shoes · Status: open
- Why: Best Search Console position across the topic's 5 keywords is 11.5; the primary keyword averages 14.3 (gaps.csv, reports/rankings.csv). Mentioned in 3 of 8 AI answers for the topic, cited in 2 (Perplexity only). Source: visibility/2026-10-13.csv.
- Do: Rewrite the page from briefs/wide-trail-running-shoes.md: add the direct answer, a width comparison table and the questions section above the product grid.
- Expected effect: medium — the topic with the most demand (6,670 searches a month) ranks 11–20.
- Effort: M (2–8 hours)
- Check: the collection page's first paragraph answers "what are wide trail running shoes" and the page has an H2 for "2E or 4E".
- Created: 2026-10-06 · Last checked: 2026-10-13 (not changed)

### A006 · Rewrite the bunions guide so AI answers can cite it
- Group: page · Topic: Trail shoes for bunions · Status: open
- Why: The guide ranks 6.4 on average (Search Console) but is cited in 0 of 4 AI answers; podiatry-notes.example is cited in all 4. Source: gaps.csv, visibility/2026-10-13.csv.
- Do: Rewrite from briefs/trail-shoes-for-bunions.md. Follow the health-claim rules in the brief: describe fit and toe-box shape, not pain relief.
- Expected effect: medium — the page already ranks; the gap is being cited.
- Effort: M (2–8 hours)
- Check: the guide starts with a direct answer of under 60 words and has question-style H2s for the 3 questions in the brief.
- Created: 2026-10-06 · Last checked: 2026-10-13 (not changed)

### A007 · Put the width guide's text in the HTML
- Group: technical · Topic: Choosing shoe width · Status: open
- Why: /guides/choosing-width has 310 characters of text before JavaScript runs and 7 scripts; some AI crawlers do not run JavaScript. Not confirmed with a rendered page (Chrome not connected): method inferred. Source: technical/issues.csv.
- Do: Render the guide's text on the server (or as static HTML), keeping the interactive size tool as an addition.
- Expected effect: medium — the page is already cited once (Perplexity, p009); more of its text would be readable.
- Effort: M (2–8 hours)
- Check: crawl_check.py reports more than 1,500 characters of text for the page.
- Created: 2026-10-06 · Last checked: 2026-10-13 (still 310)

### A008 · Ask to be included in Run Review's wide trail shoes list
- Group: offsite · Topic: Wide trail running shoes · Status: open
- Why: runreview.example is the domain cited most in AI answers (13 of 24), across 4 topics; its list "Best wide trail running shoes 2026" does not include Northpine. Source: visibility/cited_domains.csv, https://runreview.example/wide-trail-shoes-2026.
- Do: Use the "Suggest a shoe" form linked at the end of the article, or the editor contact on runreview.example/about. Offer a review pair; disclose that it is free.
- Expected effect: medium — a listing on the most-cited domain.
- Effort: S (under 2 hours)
- Check: the article mentions Northpine.
- Created: 2026-10-06 · Last checked: 2026-10-13 (not mentioned)

### A009 · Answer wide-feet threads on TrailTalk as the brand
- Group: offsite · Topic: Wide trail running shoes · Status: open
- Why: trailtalk-forum.example is cited in 9 of 24 answers, across 4 topics. Its "Wide feet" board has open threads asking for 4E trail shoes. Source: visibility/cited_domains.csv, research/brief.md (question 6).
- Do: From an account clearly named as Northpine staff, answer existing questions where a Northpine model fits, following the forum's rules on brand accounts. No posting from personal accounts, no reviews of your own products.
- Expected effect: medium
- Effort: M (2–8 hours over a month)
- Check: at least 3 replies from a Northpine-labelled account on the Wide feet board.
- Created: 2026-10-06 · Last checked: 2026-10-13 (none found)

## Done, waiting for check

### A003 · Remove "We ship worldwide (coming 2025)" from the shipping page
- Group: page · Topic: brand · Status: done
- Why: Asked "what is Northpine Running" (p011), ChatGPT said Northpine "ships worldwide" and cited /pages/shipping, which still has the line "We ship worldwide (coming 2025)". The site ships to the US and Canada only (profile). Accuracy 0. Source: visibility/2026-10-13.csv.
- Do: Delete the line, or replace it with "We ship to the US and Canada."
- Expected effect: high — corrects a wrong claim at its likely source.
- Effort: S (under 2 hours)
- Check: /pages/shipping does not contain "worldwide".
- Created: 2026-10-06 · Marked done by the user: 2026-10-09 · Last checked: 2026-10-13 (**check failed**: the page still contains "We ship worldwide (coming 2025)". It may be cached, or the change was made on a draft.)

## Confirmed

### A002 · Add canonical tags to 6 product pages
- Group: technical · Topic: Wide trail running shoes · Status: confirmed
- Why: 6 product pages had no canonical tag. Source: technical/issues.csv, 2026-10-06.
- Do: Add a self-referencing canonical tag to each.
- Expected effect: low
- Effort: S (under 2 hours)
- Check: crawl_check.py reports no `missing_canonical` on /products/*.
- Created: 2026-10-06 · Last checked: 2026-10-13 (found done on 2026-10-13)

## Dismissed

### A010 · Add an llms.txt file
- Group: technical · Topic: site-wide · Status: dismissed
- Why: No /llms.txt. It is a proposed format with unproven effect; Google says no AI-specific files are needed. Source: technical/latest.md.
- Do: Publish /llms.txt listing the collection, product and guide pages.
- Expected effect: low
- Effort: S (under 2 hours)
- Check: /llms.txt returns 200.
- Created: 2026-10-06 · Dismissed by the user: 2026-10-09 ("not a priority")
