# Actions: northpine-running.example

MADE-UP EXAMPLE.

Last updated: 2026-10-13 · run 2026-10-13-actions-7e8f
Open: 7 · Done, waiting for check: 1 · Confirmed: 1 · Dismissed: 1

## Start here
The quickest changes with the biggest effect. When one is done, change its Status to `done`; the next run checks it.

1. **A003 · Remove the "ships worldwide" line from the shipping page** — 5 minutes · high effect · marked done, but the line is still live
2. **A001 · Allow Claude-SearchBot in robots.txt** — 10 minutes · high effect
3. **A008 · Ask Run Review to include Northpine in its list** — 15 minutes · medium effect

## Open

| ID | Action | Effect | Effort | Who | Priority |
|---|---|---|---|---|---|
| A001 | Allow Claude-SearchBot in robots.txt | high | S · 10 min | owner (Shopify admin) | high |
| A004 | Publish a page: alternatives to Ridgeline for wide feet | high | M · half a day | owner (Shopify admin) | high |
| A008 | Ask Run Review to include Northpine in its list | medium | S · 15 min | owner | medium |
| A005 | Rewrite the wide trail shoes collection text | medium | M · 2–3 hours | owner (Shopify admin) | medium |
| A006 | Rewrite the bunions guide | medium | M · 2–3 hours | owner (Shopify admin) | medium |
| A007 | Put the width guide's text in the page HTML | medium | M · half a day | owner or theme developer | medium |
| A009 | Answer wide-feet threads on TrailTalk as the brand | medium | M · 1 hour a week | owner | medium |

### A001 · Allow Claude-SearchBot in robots.txt
- Group: technical · Topic: site-wide · Status: open · Who: owner (Shopify admin)
- Why: robots.txt blocks Claude-SearchBot; Anthropic says this reduces how often a site appears in Claude's search results. Source: technical/latest.md, 2026-10-13.
- Where: Shopify admin → Online Store → Themes → ⋯ (current theme) → Edit code → Templates → `robots.txt.liquid`
- Steps:
  1. Open `robots.txt.liquid`.
  2. Delete these two lines:
     ```
     User-agent: Claude-SearchBot
     Disallow: /
     ```
  3. Keep the GPTBot lines if you still want to stay out of OpenAI training data; they do not affect ChatGPT search.
  4. Click Save.
- Expected effect: high — makes the site eligible for Claude's search answers. Not measured here yet: no Anthropic key is connected.
- Effort: S · about 10 minutes
- Check: robots.txt allows Claude-SearchBot to fetch `/`.
- Created: 2026-10-06 · Last checked: 2026-10-13 (still blocked)

### A004 · Publish a page: alternatives to Ridgeline for wide feet
- Group: page · Topic: Alternatives to Ridgeline · Status: open · Who: owner (Shopify admin)
- Why: No page for this topic. Asked "what are good alternatives to Ridgeline for wide feet" (p006) and "Ridgeline or Trailkind for wide feet" (p007), neither engine named Northpine in 4 answers. Source: gaps.csv, visibility/2026-10-13.csv.
- Where: Shopify admin → Online Store → Pages → Add page
- Steps:
  1. Open briefs/alternatives-to-ridgeline.md → "Ready-to-use draft".
  2. Paste the title, body and meta description into the new page; fill the two `[check: …]` items.
  3. Set the URL handle to `ridgeline-alternatives-wide-feet` and click Save, then make it visible.
  4. On the wide trail shoes collection, add the link given in the draft.
- Expected effect: high — the topic scores 13.8 and has no page; 4 keywords (350 searches a month) plus AI questions where only competitors appear.
- Effort: M · about half a day, mostly checking the competitor table
- Check: a live, indexable page whose H1 contains "alternatives to Ridgeline", in the sitemap, linked from the collection page.
- Created: 2026-10-06 · Last checked: 2026-10-13 (not found)

### A008 · Ask Run Review to include Northpine in its list
- Group: offsite · Topic: Wide trail running shoes · Status: open · Who: owner
- Why: runreview.example is the domain AI answers cite most (13 of 24, across 4 topics); its "Best wide trail running shoes 2026" list does not include Northpine. Source: visibility/cited_domains.csv.
- Where: the "Suggest a shoe" form at the end of https://runreview.example/wide-trail-shoes-2026
- Steps:
  1. Open the form and paste:
     ```
     Hello, we make wide and extra-wide (2E and 4E) trail running shoes: the Ridgeback Wide, Talus XW and Fernline Wide ($129–$169). Your wide trail shoes list is one our customers read, and we'd like you to consider testing a pair. We're happy to send a free review pair, with no conditions on what you write. Sizes and specs: https://northpine-running.example/collections/wide-trail-shoes
     ```
  2. Send. If they reply yes, ship the pair and note the date here.
- Expected effect: medium — a listing on the most-cited domain.
- Effort: S · about 15 minutes
- Check: the article mentions Northpine.
- Created: 2026-10-06 · Last checked: 2026-10-13 (not mentioned)

### A005 · Rewrite the wide trail shoes collection text
- Group: page · Topic: Wide trail running shoes · Status: open · Who: owner (Shopify admin)
- Why: Best position across the topic's 5 keywords is 11.5; the main keyword averages 14.3. Mentioned in 3 of 8 AI answers for the topic. Source: gaps.csv, reports/rankings.csv.
- Where: Shopify admin → Products → Collections → Wide Trail Shoes → Description
- Steps:
  1. Open briefs/wide-trail-running-shoes.md → "Ready-to-use draft".
  2. Replace the collection description with the draft's first paragraph.
  3. Add the three question sections from the draft below the product grid (theme editor → collection template → add a "Rich text" block for each).
  4. Paste the new title tag and meta description under "Search engine listing".
- Expected effect: medium — the topic with the most demand (6,670 searches a month) ranks 11–20.
- Effort: M · 2–3 hours
- Check: the collection page's first paragraph answers "what are wide trail running shoes" and the page has an H2 for "2E or 4E".
- Created: 2026-10-06 · Last checked: 2026-10-13 (not changed)

### A006 · Rewrite the bunions guide
- Group: page · Topic: Trail shoes for bunions · Status: open · Who: owner (Shopify admin)
- Why: The guide ranks 6.4 on average but is cited in 0 of 4 AI answers; podiatry-notes.example is cited in all 4. Source: gaps.csv.
- Where: Shopify admin → Online Store → Blog posts (or Pages) → "Trail shoes for bunions"
- Steps:
  1. Open briefs/trail-shoes-for-bunions.md → "Ready-to-use draft".
  2. Replace the opening paragraph and add the three question headings with their text.
  3. Keep the wording about fit and comfort; do not add pain-relief claims (rules in the brief).
- Expected effect: medium — the page already ranks; the gap is being cited.
- Effort: M · 2–3 hours
- Check: the guide starts with a direct answer of under 60 words and has question-style H2s for the 3 questions in the brief.
- Created: 2026-10-06 · Last checked: 2026-10-13 (not changed)

### A007 · Put the width guide's text in the page HTML
- Group: technical · Topic: Choosing shoe width · Status: open · Who: owner or theme developer
- Why: /guides/choosing-width has 310 characters of text before JavaScript runs; some AI crawlers do not run JavaScript. Not confirmed with a rendered page (Chrome not connected). Source: technical/issues.csv.
- Where: the page's content in Shopify admin → Online Store → Pages → "Choosing your width"
- Steps:
  1. Check whether the width explanation is typed into the page content or only shown by the size-finder app.
  2. If only the app shows it: copy the explanation into the page content above the app block, so it is plain text.
  3. If you use a developer, send them: "Please make the text on /guides/choosing-width part of the page HTML, not loaded by JavaScript. Keep the size finder below it."
- Expected effect: medium — the page is already cited once (Perplexity, p009); more of its text becomes readable.
- Effort: M · about half a day
- Check: crawl_check.py reports more than 1,500 characters of text for the page.
- Created: 2026-10-06 · Last checked: 2026-10-13 (still 310)

### A009 · Answer wide-feet threads on TrailTalk as the brand
- Group: offsite · Topic: Wide trail running shoes · Status: open · Who: owner
- Why: trailtalk-forum.example is cited in 9 of 24 answers, across 4 topics; its "Wide feet" board has open threads asking for 4E trail shoes. Source: visibility/cited_domains.csv.
- Where: https://trailtalk-forum.example/c/wide-feet
- Steps:
  1. Create or use an account named clearly as Northpine (for example "Northpine_team"), as the forum's brand-account rules require.
  2. Once a week, answer 1–2 threads where a 2E or 4E shoe fits. Start replies with "I work at Northpine." Answer the question first; mention a model only if it fits.
  3. No reviews of your own products and no posting from personal accounts.
- Expected effect: medium
- Effort: M · about 1 hour a week for a month
- Check: at least 3 replies from a Northpine-labelled account on the Wide feet board.
- Created: 2026-10-06 · Last checked: 2026-10-13 (none found)

## Done, waiting for check

### A003 · Remove the "ships worldwide" line from the shipping page
- Group: page · Topic: brand · Status: done · Who: owner (Shopify admin)
- Why: Asked "what is Northpine Running" (p011), ChatGPT said Northpine "ships worldwide" and cited /pages/shipping, which still has "We ship worldwide (coming 2025)". Northpine ships to the US and Canada only. Accuracy 0. Source: visibility/2026-10-13.csv, decisions.md.
- Where: Shopify admin → Online Store → Pages → Shipping
- Steps:
  1. Find the line `We ship worldwide (coming 2025).`
  2. Replace it with:
     ```
     We ship to the US and Canada.
     ```
  3. Click Save, then open https://northpine-running.example/pages/shipping in a private window to confirm the live page changed.
- Expected effect: high — corrects a wrong claim at its likely source.
- Effort: S · about 5 minutes
- Check: /pages/shipping does not contain "worldwide".
- Created: 2026-10-06 · Marked done by the owner: 2026-10-09 · Last checked: 2026-10-13 (**check failed**: the live page still contains the line. It may have been changed in a draft or another language version.)

## Confirmed

### A002 · Add canonical tags to 6 product pages
- Group: technical · Topic: Wide trail running shoes · Status: confirmed · Who: owner
- Why: 6 product pages had no canonical tag. Source: technical/issues.csv, 2026-10-06.
- Steps: done by the owner.
- Expected effect: low · Effort: S
- Check: crawl_check.py reports no `missing_canonical` on /products/*.
- Created: 2026-10-06 · Last checked: 2026-10-13 (found done on 2026-10-13)

## Dismissed

### A010 · Add an llms.txt file
- Group: technical · Topic: site-wide · Status: dismissed
- Why: No /llms.txt. It is a proposed format with unproven effect; Google says no AI-specific files are needed. Source: technical/latest.md.
- Expected effect: low · Effort: S
- Created: 2026-10-06 · Dismissed by the owner: 2026-10-09 ("not a priority"; recorded in decisions.md → Not interested)
