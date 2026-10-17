# Scoring AI answers

Score every answer with the same rubric, every week, so weeks can be compared. Judge only from the answer text, its citations, `profile.md` and the brief.

## Per answer

| Field | Values | How to decide |
|---|---|---|
| `mentioned` | `yes` / `no` | The answer names the brand (any spelling in `brand_names`) or the domain. A mention only inside a citation title does not count; that is `cited`. |
| `position` | 1, 2, 3 … or empty | Order of the brand's first mention among all brands and products the answer names. Empty if not mentioned. |
| `cited` | `yes` / `no` | Any citation URL is on the site's domain or a subdomain. |
| `cited_urls` | list | The site's URLs that were cited. |
| `accuracy` | `2` / `1` / `0` / empty | 2 = everything said about the brand matches `profile.md`; 1 = minor errors (an old price, a missing feature); 0 = a wrong claim that could cost a customer (wrong product, wrong country, says it does something it doesn't, confuses it with another company). Empty if not mentioned. |
| `accuracy_notes` | text | Each wrong claim, the correct fact, and the profile line that shows it. |
| `sentiment` | `positive` / `neutral` / `negative` / empty | How the answer presents the brand: recommended or praised; listed without judgement; warned against or criticised. Empty if not mentioned. |
| `competitors_mentioned` | list | Brands from `research/competitors.csv` that the answer names, plus any other product names it recommends. |
| `cited_domains` | list | Every domain cited, normalised (lower-case, no `www.`). |

Write facts, not impressions, in `accuracy_notes`. Quote the answer's words (under 25 words) when flagging an error.

## Per engine and source, per run

| Metric | Formula |
|---|---|
| `mention_rate` | answers with `mentioned = yes` ÷ scored answers |
| `citation_rate` | answers with `cited = yes` ÷ scored answers |
| `avg_position` | mean `position` where mentioned |
| `share_of_voice` | brand mentions ÷ (brand mentions + mentions of every competitor in `competitors.csv`) |
| `accuracy_issues` | answers with `accuracy` 0 or 1 |
| `negative` | answers with `sentiment = negative` |

Brand Radar reports its own share of voice and mention counts. Record them as reported, with `source: brand_radar`, and do not mix them into the formulas above.

## Comparing with earlier weeks

- Compare only the same `prompt_id`, engine and source. A change of source (for example API one week, Chrome the next) breaks the comparison: show it as a new series, not a change.
- AI answers vary from one run to the next. Treat a change in `mention_rate` of less than 10 points, on fewer than 30 answers, as noise. Say so in the report instead of calling it a trend.
- New prompts join the trend from the week they are added.
