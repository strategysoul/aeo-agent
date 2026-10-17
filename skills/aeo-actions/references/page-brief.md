# Page brief template

One brief per page action, at `briefs/<topic-slug>.md`. A brief is a plan for a writer, not the page itself. Do not write the page.

```markdown
# Brief: <working title>

Topic: <topic> · Type: <product | category | guide | comparison | faq> · Action: <A007>
Page: <new, suggested URL /…> or <rewrite of URL>
Language: <…> · Market: <country>

## Who it is for and what they need
<audience from the brief, with their words in quotes and the source>

## Keywords
| Keyword | Volume | Role |
|---|---|---|
Primary: <…>. Use the primary keyword in the title, H1 and first paragraph.

## Questions the page must answer
- <question> — from <prompts.csv p0xx | People also ask | forum URL>
Use the most important ones as question-style H2 or H3 headings.

## Direct answer at the top
Write a 40–60 word answer to <primary question> as the first paragraph under the H1: plain, specific, no lead-in.
Suggested facts to include: <facts from profile.md and brief.md, each with its source>

## Outline
1. H1: <…>
2. Direct answer
3. H2: <question> — <what to cover, which facts>
…
For comparison pages: a table with the same rows for each option (price, who it is for, key differences), sourced and dated.

## What the cited pages do that this site does not
<for the 2–3 pages AI answers cite most for this topic: what they cover, their structure, what facts they give — summarised, not copied>

## Facts to use, with sources
| Fact | Source | Date |

## Rules to follow
<limits from research brief question 7: claims that need evidence, required disclaimers, words to avoid. "None found" if none.>

## Schema
<types that match the visible content, e.g. Product with offers; Article with author and date. Only types that describe what is on the page.>

## Internal links
- Link to this page from: <URLs>
- Link from this page to: <URLs>

## Done when
- Live at <URL>, indexable (no noindex), in the sitemap, linked from <URL>
- The questions above are answered on the page
```

Rules:

- Every fact in the brief has a source. Facts about the business come from `profile.md`; facts about the market from `research/brief.md`.
- Do not copy text from competitor pages. Describe what they cover.
- Do not tell the writer to add claims the site cannot back (reviews, awards, prices) or anything the industry rules forbid.
