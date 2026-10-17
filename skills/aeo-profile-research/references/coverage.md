# Coverage check

## The seven questions

| # | Question | Answered when the research has |
|---|---|---|
| 1 | Product and price | what is sold, the price or price model, and how it compares with alternatives |
| 2 | Audiences, their goals and the words they use | at least two named audiences, each with goals and real phrases they use (quoted from forums, reviews or search queries, not invented) |
| 3 | Competitors and alternatives | at least five direct competitors and the non-product alternatives (doing it yourself, a spreadsheet, an agency, doing nothing) |
| 4 | Who ranks and gets cited | the domains that rank for the main searches, and which sources AI answers cite for them |
| 5 | Questions people ask | at least 20 real questions, from "People also ask", forums, reviews, or Search Console |
| 6 | Where audiences read and talk | named communities, forums, review sites, publications, newsletters, creators |
| 7 | Rules that limit what the business can say | the regulations, platform rules or industry codes that apply in its countries, or a sourced "none found" |

## How to decide the status

For each question, look through every file under `research.paths` and the existing `research/brief.md`.

- `answered` — meets the "answered when" test above, every finding has a source, and the newest supporting evidence is no more than `research.max_age_days` (default 90) old.
- `partial` — some of the test is met. Say exactly what is missing, e.g. "only one audience", "no quoted phrases", "competitors named but no alternatives".
- `stale` — would be `answered`, but the evidence is older than the limit.
- `missing` — nothing relevant found.

Dating evidence: use a date written in the document or next to the finding. If there is none, use the file's modified date and note `date_basis: file_modified`. Unsourced claims in the user's research count as `inferred`: they can support `partial`, never `answered`.

## `research/coverage.json`

```json
{
  "checked_at": "2026-10-17",
  "run_id": "2026-10-17-research-a1b2",
  "max_age_days": 90,
  "questions": {
    "1": {
      "status": "partial",
      "missing": "no price comparison with alternatives",
      "evidence": [
        {"file": "research/brief.md", "where": "## Product and price", "date": "2026-08-02", "date_basis": "in_document"}
      ],
      "action": "research"
    },
    "2": {"status": "missing", "missing": "everything", "evidence": [], "action": "research"}
  }
}
```

`action` is `research` or `reuse`. After the brief is written, update `status` for researched questions and add the new evidence.

## `research/competitors.csv`

```
domain,name,type,keywords_in_top10,seed_keywords_checked,evidence_url,source,method,record_date,run_id
```

- `type`: `direct` (sells the same thing), `alternative` (a different way to solve the same problem), `publisher` (ranks with content but does not sell).
- `keywords_in_top10` out of `seed_keywords_checked`.
- New runs add rows. Keep earlier rows; the `record_date` tells them apart.
