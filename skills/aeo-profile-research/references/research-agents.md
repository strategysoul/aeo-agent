# Research agents

## How to split the work

Group the open questions so each agent has a clear job. Use as many agents as there are groups with open questions, at most four.

| Agent | Questions | Where it looks |
|---|---|---|
| Market | 1, 3 | competitor sites (pricing, features, positioning pages), comparison and "best of" articles, marketplace listings |
| Audience | 2, 6 | forums, Reddit, Quora, review sites, community groups, social posts, YouTube comments, Q&A sites |
| Questions | 5 | "People also ask" from step 3, autocomplete via web search, forums, review questions, Search Console queries if connected |
| Rules | 7 | regulator sites, laws and official guidance for the site's countries, platform ad and content policies, industry codes |

Question 4 is covered by step 3 of the skill (search results). The Market agent adds the AI-citation side: for three of the main starting keywords, search the web for recent articles and note which domains appear as sources. Label this `method: inferred` — measured AI citations come in the visibility step.

## Brief for each agent

Give each agent this, filled in:

```
You are researching <questions> for <domain>, a business that <one-line summary from profile.md>.
Countries: <countries>. Languages: <languages>. Write findings in English; keep quotes in the original language.
Known competitors: <top 10 domains from competitors.csv>.
Already known, do not repeat: <findings already in the brief for these questions>.

Tools, in this order: web search and fetch; then <firecrawl if available>; then <nimble if available>.
Do not log in anywhere, fill in forms, or post anything.
Spend at most <N> searches and <M> page fetches.

Return only findings in the format below. Every finding needs a URL you actually opened and today's date.
If you looked and found nothing, say "not found" and where you looked.
```

Default limits: 15 searches and 25 fetches per agent. Halve them for a re-run that fills `partial` questions only.

## Finding format

Each agent returns Markdown in exactly this shape:

```
## Q<number>: <question name>

- <finding, one sentence>
  - source: <URL>
  - read: <YYYY-MM-DD>
  - method: measured | inferred
  - quote: "<short quote, under 25 words, only for audience phrases and questions>"

### Not found
- <what was looked for> — looked in: <places>
```

`measured` means the page states it directly. `inferred` means the agent concluded it from what it read.

## Checks before writing the brief

- Drop findings without a URL or a date.
- Open a sample of at least three URLs per agent to check they say what the finding claims. Drop findings that fail.
- Merge duplicates and keep the most recent source.
- Audience phrases must be quotes from real people (forums, reviews, queries), not marketing copy.
