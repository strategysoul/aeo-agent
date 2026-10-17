# Scoring and grouping

## Score per keyword

`score = 3 × fit + intent + demand + ease + bonus` (range 0–20). A keyword with `fit = 0` is dropped, whatever its other scores.

### Fit (0–3), judged against `profile.md` and the brief

| Score | Meaning |
|---|---|
| 3 | Describes what the site sells, for an audience it serves |
| 2 | A problem or task the product solves, or a close neighbour of it |
| 1 | Related to the audience's world, but the site could only answer it with general content |
| 0 | Not relevant, a different product, a job search, a competitor's login or support page, or a place the business does not serve |

Write a short reason for every fit score in `fit_reason`. The reason must point at something in the profile or brief, not at general knowledge.

### Intent (0–3)

| Score | Intent |
|---|---|
| 3 | Transactional (buy, price, signup, near me) or commercial comparison (best, vs, alternatives, review) |
| 2 | Informational, where the answer naturally leads to the product (how to <task the product does>) |
| 1 | Informational, general |
| 0 | Navigational to another brand |

Use the source's intent label if it has one; otherwise judge from the wording.

### Demand (0–3)

| Score | Measured or estimated monthly volume | Fallback band |
|---|---|---|
| 0 | 0 or unknown | `none` |
| 1 | 1–100 | `low` |
| 2 | 101–1,000 | `medium` |
| 3 | more than 1,000 | `high` |

Search Console impressions (90 days ÷ 3) count as monthly demand when no volume is available.

### Ease (0–3): difficulty compared with the site's authority

Authority is the site's Ahrefs Domain Rating or Semrush Authority Score (both 0–100) from `config.yaml`. Difficulty is the source's 0–100 score.

| Score | `difficulty − authority` |
|---|---|
| 3 | −10 or lower |
| 2 | −9 to 10 |
| 1 | 11 to 30, or either value unknown |
| 0 | more than 30 |

If the site already ranks in the top 20 for the keyword (Search Console), ease is at least 2.

### Bonus (0–2)

- +1 if an AI Overview shows for the keyword
- +1 if it is a question, or written the way people talk to an AI tool ("what is the best … for …")

Questions with zero or unknown volume are kept. They score low on demand but stay in the list, because people ask them in AI tools.

## Grouping into topics

One topic is one page to write or improve. Each topic has 3–15 keywords.

1. **Comparison and brand topics are separate.** Keywords with "vs", "alternative(s)", "compared", "review", or a competitor's name go into comparison topics (one per competitor or per comparison). Keywords with the site's own brand go into brand topics.
2. **Group the rest by search results when you have them.** Two keywords belong to the same topic if at least 3 of their top-10 URLs are the same. Get top 10s only for the 50–100 highest-scoring keywords, within budget, and attach the rest by meaning.
3. **Without search results, group by meaning:** the same need, answered by the same page.
4. A group with more than 15 keywords is split by sub-need. Fewer than 3 keywords: merge into the closest topic, or keep it as a single-question topic if it is a question with fit 3.

For each topic record:

| Field | Meaning |
|---|---|
| `topic` | short descriptive name |
| `primary_keyword` | the keyword with the highest demand, ties broken by score |
| `keywords` | all keywords in it |
| `type` | `product`, `category`, `guide`, `comparison`, `brand`, `faq` |
| `demand` | sum of volumes (or band counts in fallback) |
| `score` | mean of its top 5 keyword scores |
| `existing_url` | the site's page that already ranks for it (Search Console) or best matches it (sitemap), or empty |
| `approved` | `yes` / `no` |
